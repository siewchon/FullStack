-- Table definitions for the tournament project.
--
drop view if exists vw_playerStandings
;
drop table if exists matches
;
drop table if exists players
;
drop database if exists tournament
;
create database tournament
;
-- connect to the 'tournament' database
\c tournament
;
create table if not exists players (
    id          Serial      Primary Key,
    name    text
)
;
create table if not exists matches (
    id            Serial      Primary Key,
    winner    Integer    References players(id),
    loser       Integer    References players(id)
)
;
-- combine player's name and the game each played into one view
CREATE OR REPLACE VIEW vw_playerStandings
AS
SELECT id,
       name,
       (SELECT count(*) FROM matches WHERE players.id = matches.winner) AS wins,
       (SELECT count(*) FROM matches WHERE players.id = matches.winner
                                       OR players.id = matches.loser) AS matches
FROM players
;
