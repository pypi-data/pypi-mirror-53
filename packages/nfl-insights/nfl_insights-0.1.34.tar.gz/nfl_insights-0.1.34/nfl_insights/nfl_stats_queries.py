import os
import pandas as pd
from datetime import datetime as dt
from pathlib import Path

import gspread

from contendo_utils import ProUtils
from contendo_utils import BigqueryUtils
from contendo_utils import ContendoConfigurationManager

NFL_DOMAIN_NAME = 'Football.NFL'
NFL_DOMAIN_CONFIG_GID = 274419028
NFL_DATA_DATASET = 'NFL_Data'
NFL_PBP_TABLEID = 'all_game_pbp_enriched'

class NFLStatsQueries():
    #
    # read in the configurations
    def __init__(self, project=None):
        #
        # get the initial configurations
        self.ccm = ContendoConfigurationManager()
        self.sourcesConfigDict = self.ccm.get_configuration_dict(NFL_DOMAIN_NAME, NFL_DOMAIN_CONFIG_GID, 'Configname')
        self.statsDict = self.ccm.get_configuration_dict(NFL_DOMAIN_NAME, 530297342, 'StatName')
        self.compStatsDict = self.ccm.get_configuration_dict(NFL_DOMAIN_NAME, 1414140695, 'StatName')
        self.gameDimentionsDict = self.ccm.get_configuration_dict(NFL_DOMAIN_NAME, 1621060823, 'ConditionCode')
        self.playDimentionsDict = self.ccm.get_configuration_dict(NFL_DOMAIN_NAME, 1120955874, 'ConditionCode')
        self.ptmapDict = self.ccm.get_configuration_dict(NFL_DOMAIN_NAME, 582380093, 'Object')
        #
        # initialize BQ
        self.bqu = BigqueryUtils(project)
        #
        # data file name
        self.resourceDir = 'resource'
        self.pbpDataFileName = '{}/pbp_data.csv'.format(self.resourceDir)
        self.pbpDF = None
        self.gamesDF = None

    def _generate_pbp_query(self):
        exceptionList = [
            'description', 'blockingPlayer', 'penalty', 'recoveringTeam',
            'homePlayersOnField', 'awayPlayersOnField', 'penalties', 'subPlays', 'teamReferences',
            'interceptedAtPosition', 'passedFromPosition',
        ]
        pbp_schema = self.bqu.get_table_schema(NFL_DATA_DATASET, NFL_PBP_TABLEID)
        fieldsList = []
        def aggregate_fieldslist(schema, parent=None):
            def calc_fieldname(name, parent):
                if parent:
                    return '{parent}.{field}'.format(field=field['name'], parent=parent)
                else:
                    return name

            for field in schema:
                name = field['name']
                if name in exceptionList or name[0]=='_':
                    continue

                fieldname = calc_fieldname(name, parent)
                if field['type'] == 'RECORD':
                    if field['mode'] == 'REPEATED':
                        print(name)
                        continue
                    else:
                        aggregate_fieldslist(field['fields'], fieldname)
                else:
                    fieldsList.append('{} as {}'.format(fieldname, fieldname.replace('.','_')))

        aggregate_fieldslist(pbp_schema)
        fieldsStr = str(fieldsList).replace('[', '').replace(']', '').replace(',', ',\n').replace("'", '')
        query = 'SELECT {fields} FROM `sportsight-tests.NFL_Data.all_game_pbp_enriched`'.format(fields=fieldsStr)
        if 'CONTENDO_DEV' in os.environ:
            ProUtils.write_string_to_file('{}/queries/pbp_flat_query.sql'.format(str(Path(__file__).parent)), query)
        return query

    def update_pbp_data(self):
        pbpQuery = self._generate_pbp_query()
        _pbpDF = self.bqu.execute_query_to_df(pbpQuery)
        if not os.path.exists(self.resourceDir):
            os.mkdir(self.resourceDir)
        _pbpDF.to_csv(self.pbpDataFileName)

    def _read_pbp_data(self):
        #
        # Read the pbp data from file.
        if not os.path.exists(self.pbpDataFileName):
            self.update_pbp_data()

        if self.pbpDF is None:
            self.pbpDF = pd.read_csv(self.pbpDataFileName)
            self.pbpDF['all']=1
            self.pbpDF['count']=1

    def get_games(self, filter='game.homeTeam!=""'):
        if self.gamesDF == None:
            query = """
                SELECT
                  schedule.id as gameid,
                  schedule.homeTeam.abbreviation as homeTeam,
                  schedule.awayTeam.abbreviation as awayTeam,
                  schedule.startTime,
                  score.homeScoreTotal,
                  score.awayScoreTotal,
                  schedule.playedStatus,
                  Season  
                FROM
                  `sportsight-tests.NFL_Data.seasonal_games`
                LEFT JOIN
                  UNNEST (Seasondata.games)
                where schedule.playedStatus = 'COMPLETED'
                order by startTime desc            
            """
            self.gamesDF = self.bqu.execute_query_to_df(query)
        game = self.gamesDF
        return eval('game[({})]'.format(filter))


    def _get_gamedimention_condition(self, gameDimention):
        gamedimDef = self.gameDimentionsDict[gameDimention]
        condition = gamedimDef['Condition']
        if condition and condition!='True':
            return '{}'.format(condition)
        else:
            return 'True'

    def _get_playdimention_condition(self, playDimention):
        playdimDef = self.playDimentionsDict[playDimention]
        condition = playdimDef['Condition']
        if condition and condition!='True':
            return '{}'.format(condition)
        else:
            return 'True'

    def _get_stat_condition(self, statDef):
        condition = statDef['Condition']
        _function = statDef['Function']
        if condition:
            if condition=='True':
                pass
            elif _function == 'count':
                return '{}'.format(condition)
            else:
                return '({}) & (df.{}!="")'.format(condition, statDef['AggField'])

        return 'True'

    def _save_trace_df(self, traceDF, initialColumns, spreadId=None, sheetName=None):
        if not spreadId:
            spreadId = '1Q5O3ejSyEDZrlFXX04bOIWOqMxfiHJYimunZKtpFswU'
        if not sheetName:
            sheetName = 'trace'

        finalColumns=['season', 'gameid', 'gamename', 'homeScore', 'awayScore','quarter', 'playType', 'currentDown']

        for col in initialColumns:
            if col in traceDF.columns:
                finalColumns.append(col)

        for col in traceDF.columns:
            if col not in finalColumns:
                finalColumns.append(col)

        if 'CONTENDO_AT_HOME' in os.environ:
            from gspread_pandas import Spread, Client
            import google.auth
            credentials, project = google.auth.default()
            gc = gspread.Client(credentials)
            spread = Spread(spreadId, client=gc)
            spread.df_to_sheet(traceDF[finalColumns], index=False, sheet=sheetName, start='A1', replace=True)
            print('trace can be found in this url:', spread.url)
        else:
            fileName = '{}.csv'.format(sheetName)
            traceDF[finalColumns].to_csv(fileName)
            print ('Trace to file ', fileName)
            try:
                import google.colab
                IN_COLAB = True
                from google.colab import files
                print ('Downloading', fileName)
                files.download(fileName)
            except Exception as e:
                print ('Error getting trace file {}, {}'.format(fileName, e))
                IN_COLAB = False

    def pbp_get_stat(self, statName, object, playDimention='all', gameDimention='game', aggfunc=None, playType=None, filter='True', trace=False):
        assert statName in self.statsDict, "Illegal statName: '{}', must be one of {}".format(statName, self.statsDict.keys())
        assert object in self.ptmapDict, "Illegal object: '{}', must be one of {}".format(object, self.ptmapDict.keys())
        #assert playType in self.statsDict, "Illegal playType: '{}', must be one of {}".format(statName, self.statsDict.keys())
        #assert aggfunc in self.statsDict, "Illegal aggfunc: '{}', must be one of {}".format(statName, self.statsDict.keys())
        assert playDimention in self.playDimentionsDict, "Illegal statName: '{}', must be one of {}".format(playDimention, self.playDimentionsDict.keys())
        assert gameDimention in self.gameDimentionsDict, "Illegal gameDimention: '{}', must be one of {}".format(gameDimention, self.gameDimentionsDict.keys())
        #
        # make sure the pbpDF is loaded
        self._read_pbp_data()
        #
        # build the query conditions
        statDef = self.statsDict[statName]
        queryInst = {
            'statcond': self._get_stat_condition(statDef),
            'gamecond': self._get_gamedimention_condition(gameDimention),
            'playcond': self._get_playdimention_condition(playDimention),
            'filtercond': filter,
            'isInplayCond': "(df.playType=='penalty') | (df.isNoPlay!=True)"
        }
        df = self.pbpDF
        queryeval = 'df[({statcond}) & ({gamecond}) & ({playcond}) & ({filtercond}) & ({isInplayCond})]'.format(**queryInst)
        try:
            filteredDF = eval(queryeval)
            #print(filteredDF.shape, df.shape)
        except Exception as e:
            print("Error evaluating filtering statemet: {}, error: {}".format(queryeval, e))
            raise e

        #
        # return empty if no answers
        if filteredDF.shape[0]==0:
            print ('ZERO results for filter {}, total plays {}', queryeval, df.shape[0])
            return pd.DataFrame()

        objectDef = self.ptmapDict[object]
        statObject = objectDef['StatObject']
        if statObject=='team':
            groupby = "['{object}_id', '{object}_name']"
        else:
            groupby = "['{object}_id', '{object}_firstName', '{object}_lastName', '{object}_position', '{team}_name']"
        groupby = groupby.format(object=object, team=objectDef['TeamType'])

        aggField = statDef['AggField']
        groupingeval = "filteredDF.groupby({groupby}, as_index=False).agg({}'{aggField}': '{aggFunc}', 'count': 'count'{}).sort_values(by='{aggField}', ascending=False)"

        if not aggfunc:
            aggfunc = statDef['Function']
        groupingeval = groupingeval.format('{', '}',groupby=groupby, aggField=aggField, aggFunc=aggfunc)

        try:
            finalDF = eval(groupingeval)
        except Exception as e:
            print("Error evaluating aggregation statemet: {}, error: {}".format(groupingeval, e))
            raise e

        if trace:
            self._save_trace_df(filteredDF, finalDF.columns, sheetName='trace-{}-{}-{}-{}'.format(statName, object, playDimention, gameDimention))
        #
        # add the rank - denserank.
        finalDF['rank'] = finalDF[aggField].rank(method='dense', ascending=False)
        return finalDF

    def pbp_get_composed_stat(self, compstat, object, playDimention='all', gameDimention='game', filter='True'):
        assert compstat in self.compStatsDict, "Illegal statName: '{}', must be one of {}".format(statName, self.compStatsDict.keys())
        compstatDef = self.compStatsDict[compstat]
        numerator = compstatDef['NumeratorStatName']
        numeratorDef = self.statsDict[numerator]
        denominator = compstatDef['DenominatorStatName']
        denominatorDef = self.statsDict[denominator]
        #
        # define the index-key(s) for team/player
        objectDef = self.ptmapDict[object]
        if objectDef['StatObject'] == 'team':
            key = object+'_id'
        else:
            key = [object+'_id', objectDef['TeamType']+'_name']
        #
        # get the numerator data
        numeratorDF = self.pbp_get_stat(numerator, object, playDimention, gameDimention, filter=filter).set_index(key)
        if numeratorDF.shape[0]==0:
            return numeratorDF
        #
        # get the denominator data
        denominatorDF = self.pbp_get_stat(denominator, object, playDimention, gameDimention, filter=filter).set_index(key)
        if denominatorDF.shape[0]==0:
            return denominatorDF

        df = numeratorDF.join(
            denominatorDF,
            rsuffix='_dn',
            on=key,
            how='left'
        )
        #print(df)
        #print(df[['offenseTeam_name',  'count', denominatorDef['AggField']+'_dn']])
        #numeratorDF[denominatorDef['AggField']+'_dn'] = df[denominatorDef['AggField']+'_dn']
        df[compstat] = df[numeratorDef['AggField']]/df[denominatorDef['AggField']+'_dn']*compstatDef['StatRatio']
        df.sort_values(by=compstat, ascending=False, inplace=True)
        df['rank'] = df[compstat].rank(method='dense', ascending=False)
        retCols = list()
        for col in df.columns:
            if col.find('_dn')==-1 or col==denominatorDef['AggField']+'_dn':
                retCols.append(col)
        return df[retCols]


def test_all_stats(generator, startTime=dt.now()):
    counter=dict()
    results=[]
    for statName, statDef in generator.statsDict.items():
        if statDef['Condition']=='' or statDef['Doit'] != 'y':
            continue
        for gameCondCode, gameCondDef in generator.gameDimentionsDict.items():
            for playCondCode, playCondDef in generator.playDimentionsDict.items():
                for object, objectDef in generator.ptmapDict.items():
                    #
                    # only do if defined as 1
                    if statDef[object] != 'y':
                        continue

                    if gameCondDef['Condition']=='' or playCondDef['Condition']=='':
                        #print ('skipping', statDef, gameCondDef, playCondDef)
                        #return
                        continue
                    if statDef['playType'] != 'all' and playCondDef['playType'].find(statDef['playType'])==-1:
                        continue

                    df = generator.pbp_get_stat(statName, object, playCondCode, gameCondCode)
                    isResults = (df.shape[0]>0)
                    counter[isResults] = counter.get(isResults, 0)+1
                    print (counter[isResults], isResults, df.shape, statName, object, playCondCode, gameCondCode, dt.now() - startTime)
                    if isResults:
                        results.append(
                            {
                                'StatName': statName,
                                'Object': object,
                                'StatObject': objectDef['StatObject'],
                                'PlayDimention': playCondCode,
                                'GameDimention': gameCondCode,
                                'nResults': df.shape[0],
                            }
                        )

    print(counter)
    keys = results[0].keys()
    resultsDF = pd.DataFrame(results, columns=keys)
    from gspread_pandas import Spread, Client
    spread = Spread(generator.ccm.get_domain_docid('Football.NFL'))
    spread.df_to_sheet(resultsDF, index=False, sheet='PBP Stats results', start='A1', replace=True)

def test():
    startTime=dt.now()
    pd.set_option('display.max_columns', 12)
    pd.set_option('display.width', 200)
    #os.environ['CONTENDO_AT_HOME'] = 'y'
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "{}/sportsight-tests.json".format(os.environ["HOME"])
    os.environ['CONTENDO_DEV']='y'
    os.chdir('{}/tmp/'.format(os.environ["HOME"]))
    generator = NFLStatsQueries()
    #print(generator._generate_pbp_query())
    print('Start updating pbp data', dt.now() - startTime)
    #generator.update_pbp_data()
    print('Start querying data', dt.now() - startTime)
    df = generator.pbp_get_stat('sacks', 'soloTacklingPlayer', 'all', 'game',aggfunc='count', filter="df.season=='2019-regular'", trace=True)
    #df = generator.pbp_get_composed_stat('yardsPerCatch', 'passingPlayer')
    #df = generator.get_games()
    print(df.columns, df.shape,'\n', df)
    #print ('shape: {}\nIndex: {}\nColumns: {}\n'.format(df.shape, df.index, df.columns))
    #test_all_stats(generator)
    print('Done', dt.now() - startTime)

if __name__ == '__main__':
    test()
