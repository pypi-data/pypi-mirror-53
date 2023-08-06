with players as (
   SELECT
    season,
    id AS playerId,
    currentTeam.id AS teamId,
    firstName,
    lastName,
    age,
    primaryPosition,
    height,
    weight,
    handedness.throws AS handedness,
    birthCountry,
    birthCity,
    birthDate
  FROM
    `NFL_Data.game_boxscore_*`
  LEFT JOIN
    UNNEST (references.playerReferences)
  GROUP BY
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13
  ORDER BY
    season DESC,
    playerid,
    teamid
  )
SELECT
  playerId,
  firstName,
  lastName,
  teamId
FROM
  players
WHERE
  season='2019-regular'
GROUP BY
  1,
  2,
  3,
  4