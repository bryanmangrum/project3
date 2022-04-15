-- All commands used for data cleaning in the SQLITE file

-- Drop tables that won't be used
DROP TABLE News;
DROP TABLE News_Missing;
DROP TABLE Game_Officials;
DROP TABLE Game_Inactive_Players;
DROP TABLE Draft_Combine;
DROP TABLE Player_Bios;
DROP TABLE Team_History;
DROP TABLE Player;

-- Limit NBA games to the 2020-21 season

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

-- Find potential duplicate player names in our player salaries in Draft
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

-- Export desired tables to CSV


-- Create tables in postgresql to import CSV tables

CREATE TABLE draft (
    yearDraft REAL NOT NULL,
    numberPickOverall INT NOT NULL,
    numberRound INT NOT NULL,
    numberRoundPick INT NOT NULL,
    namePlayer VARCHAR(255) NOT NULL,
    slugTeam VARCHAR(255) NOT NULL,
    nameOrganizationFrom VARCHAR(255),
    typeOrganizationFrom VARCHAR(255),
    idPlayer REAL NOT NULL Primary Key,
    idTeam REAL,
    nameTeam VARCHAR(255) NOT NULL,
    cityTeam VARCHAR(255) NOT NULL,
    teamName VARCHAR(255) NOT NULL,
    PLAYER_PROFILE_FLAG INT,
    slugOrganizationTypeFrom VARCHAR(255), 
    locationOrganizationFrom VARCHAR(255)
);

CREATE TABLE Team_Attributes (
    ID INT NOT NULL PRIMARY KEY,
    ABBREVIATION VARCHAR(5)NOT NULL,
    NICKNAME VARCHAR(255)NOT NULL,
    YEARFOUNDED REAL NOT NULL,
    CITY VARCHAR(255) NOT NULL,
    ARENA VARCHAR(255)NOT NULL,
    ARENACAPACITY REAL,
    OWNER VARCHAR(255)NOT NULL,
    GENERALMANAGER VARCHAR(255)NOT NULL,
    HEADCOACH VARCHAR(255)NOT NULL,
    DLEAGUEAFFILIATION VARCHAR(255)NOT NULL,
    FACEBOOK_WEBSITE_LINK VARCHAR(255)NOT NULL,
    INSTAGRAM_WEBSITE_LINK VARCHAR(255)NOT NULL,
    TWITTER_WEBSITE_LINK VARCHAR(255)NOT NULL
);

CREATE TABLE Win_Counts (
    Team VARCHAR(255) NOT NULL PRIMARY KEY,
    Division VARCHAR(255) NOT NULL,
    Conference VARCHAR(255) NOT NULL,
    Win_Count INT NOT NULL
);

CREATE TABLE Player_2020_Salaries (
    Rank INT NOT NULL PRIMARY KEY,
    idPlayer REAL,
    Team VARCHAR(255) NOT NULL,
    Player VARCHAR(255) NOT Null,
    Salary INTEGER NOT NULL,
    FOREIGN KEY(idPlayer) REFERENCES Draft(idPlayer)
);

--Create Table for arena info
CREATE TABLE arenas(
    arena_PK VARCHAR(255) PRIMARY KEY NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    arena VARCHAR(255) NOT NULL,
    team VARCHAR (255) NOT NULL,
    sector VARCHAR(255) NOT NULL,
    subSector VARCHAR(255)
);

-- Create Table for NBA colors
CREATE TABLE colors(
    team VARCHAR(255) PRIMARY KEY NOT NULL,
    color1 VARCHAR(6),
    color2 VARCHAR(6),
    color3 VARCHAR(6),
    color4 VARCHAR(6),
    color5 VARCHAR(6)
);