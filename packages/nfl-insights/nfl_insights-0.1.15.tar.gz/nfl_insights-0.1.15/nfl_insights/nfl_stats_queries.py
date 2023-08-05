import os
import pandas as pd
from datetime import datetime as dt
from pathlib import Path

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
            'gamename', 'description',
            'interceptedAtPosition', 'penalty', 'passedFromPosition',
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
                        continue
                    else:
                        aggregate_fieldslist(field['fields'], fieldname)
                else:
                    fieldsList.append('{} as {}'.format(fieldname, fieldname.replace('.','_')))

        aggregate_fieldslist(pbp_schema)
        fieldsStr = str(fieldsList).replace('[', '').replace(']', '').replace(',', ',\n').replace("'", '')
        query = 'SELECT {fields} FROM `sportsight-tests.NFL_Data.all_game_pbp_enriched`'.format(fields=fieldsStr)
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
        function = statDef['Function']
        if condition:
            if condition=='True':
                pass
            elif function == 'count':
                return '{}'.format(condition)
            else:
                return '({}) & (df.{}!="")'.format(condition, statDef['AggField'])

        return 'True'


    def pbp_get_stat(self, statName, object, playDimention='all', gameDimention='game', aggfunc=None, playType=None, filter='True'):
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
        }
        df = self.pbpDF
        queryeval = 'df[({statcond}) & ({gamecond}) & ({playcond}) & ({filtercond})]'.format(**queryInst)
        try:
            filteredDF = eval(queryeval)
            print(filteredDF.shape, df.shape)
        except Exception as e:
            print("Error evaluating filtering statemet: {}, error: {}".format(queryeval, e))
            raise e

        #
        # return empty if no answers
        if filteredDF.shape[0]==0:
            print ('ZERO results for filter {}, total plays {}', queryeval, df.shape[0])
            return pd.DataFrame()


        if aggfunc:
            function = aggfunc
        else:
            function = statDef['Function']

        objectDef = self.ptmapDict[object]
        statObject = objectDef['StatObject']
        if statObject=='team':
            groupby = "['{object}_id', '{object}_name']"
        else:
            groupby = "['{object}_id', '{object}_firstName', '{object}_lastName', '{object}_position', '{team}_name']"
        groupby = groupby.format(object=object, team=objectDef['TeamType'])

        aggField = statDef['AggField']
        groupingeval = "filteredDF.groupby({groupby}).agg({}'{aggField}': '{aggFunc}', 'count': 'count'{}).sort_values(by='{aggField}', ascending=False)"
        groupingeval = groupingeval.format('{', '}',groupby=groupby, aggField=aggField, aggFunc=function)

        try:
            finalDF = eval(groupingeval)
        except Exception as e:
            print("Error evaluating aggregation statemet: {}, error: {}".format(groupingeval, e))
            raise e

        #
        # return empty if no answers
        if filteredDF.shape[0]==0:
            print ('ZERO results for filter {}, total plays {}', queryeval, df.shape[0])
            return pd.DataFrame()

        finalDF['rank'] = finalDF[aggField].rank(method='dense', ascending=False)
        #print(finalDF, finalDF.shape)
        return finalDF

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
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "{}/sportsight-tests.json".format(os.environ["HOME"])
    os.chdir('{}/tmp/'.format(os.environ["HOME"]))
    generator = NFLStatsQueries()
    #print(generator._generate_pbp_query())
    print('Start updating pbp data', dt.now() - startTime)
    #generator.update_pbp_data()
    #generator.read_pbp_data()
    print('Start querying data', dt.now() - startTime)
    df = generator.pbp_get_stat('yardsRushed', 'offenseTeam', 'all', 'ownTerritory',aggfunc='sum', filter="df.season=='2018-regular'")
    #df = generator.get_games()
    print(df)
    #print ('shape: {}\nIndex: {}\nColumns: {}\n'.format(df.shape, df.index, df.columns))
    #test_all_stats(generator)
    print('Done', dt.now() - startTime)

if __name__ == '__main__':
    test()
