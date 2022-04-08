-- All commands used for data cleaning

-- Drop tables that won't be used
DROP TABLE News;
DROP TABLE News_Missing;
DROP TABLE Game_Officials;
DROP TABLE Game_Inactive_Players;
DROP TABLE Draft_Combine;
DROP TABLE Player_Bios;
DROP TABLE Team_History;
DROP TABLE Player;

-- Limit NBA games to the 2000-01 season onwards

-- 2020-21 season started on December 22, 2020
DELETE FROM Game
WHERE GAME_DATE < '2020-12-22';

-- Limit players to those who at least finished the 2000-01 season
DELETE FROM Player_Attributes
WHERE TO_YEAR < '2001';

-- Clean up incorrect entries
DELETE FROM Player_Attributes
WHERE DRAFT_YEAR <= 1983;

-- Delete all players from the draft that do not show up
-- from filtered Player_Attributes table
-- NOTE: Players drafted in 2020 do not appear in Player_Attributes
-- but we will need their id when when we display their photos.
DELETE FROM Draft
WHERE yearDraft <= 1983;

-- Get rid of all the players that aren't in the edited Draft table
DELETE FROM Player_Photos
WHERE idPlayer NOT IN (
    SELECT idPlayer
    FROM Draft
);

-- Create table of league division and conference and game wins
CREATE TABLE Win_Counts AS

SELECT Team, Division, Conference, SUM(Win_Count) AS Win_Count
FROM (
         SELECT COUNT(WL_HOME)   AS Win_Count,
                "NBA Division"   AS Division,
                "NBA Conference" AS Conference
             ,
                TEAM_NAME_HOME   AS Team
         FROM Game
                  JOIN Div_Conf ON TEAM_NAME_HOME = "NBA Team"
         WHERE WL_HOME = 'W'
         GROUP BY TEAM_NAME_HOME
         UNION ALL
         SELECT COUNT(WL_AWAY)   AS Win_Count,
                "NBA Division"   AS Division,
                "NBA Conference" AS Conference
             ,
                TEAM_NAME_AWAY   AS Team
         FROM Game
                  JOIN Div_Conf ON TEAM_NAME_HOME = "NBA Team"
         WHERE WL_AWAY = 'W'
         GROUP BY TEAM_NAME_AWAY
     )
GROUP BY Team;

-- After importing web scraped CSV of player salaries from ESPN...

-- Find potential duplicate player names in our player salaries in our draft table
SELECT NAME
FROM player_salaries
WHERE NAME IN (
    SELECT namePlayer
    FROM Draft
    GROUP BY namePlayer
    HAVING COUNT(namePlayer)>1
);

-- Create player salaries table for 2020-21 season with IDs, null if no ID
CREATE TABLE Player_2020_Salaries AS
SELECT player_salaries.RANK AS Rank,
    idPlayer,
    player_salaries.TEAM AS Team,
    player_salaries.NAME AS Player,
    player_salaries.SALARY AS Salary
FROM player_salaries
LEFT JOIN Draft ON Draft.namePlayer=player_salaries.NAME;