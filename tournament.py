#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    try:
        db_conn = connect()
        db_cursor = db_conn.cursor()
        db_cursor.execute("DELETE FROM matches")
        db_conn.commit()
    except psycopg2.DatabaseError as e:
        print "Exception caught! \n Exception Message: %s" % e.pgerror
    finally:
        db_conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    try:
        db_conn = connect()
        db_cursor = db_conn.cursor()
        db_cursor.execute("DELETE FROM players")
        db_conn.commit()
    except psycopg2.DatabaseError as e:
        print "Exception caught: %s " % e.pgerror
    finally:
        db_conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    try:
        db_conn = connect()
        db_cursor = db_conn.cursor()
        db_cursor.execute("select count(*) from players;")
        rows = db_cursor.fetchone()
        count = rows[0]
    except psycopg2.DatabaseError as e:
        print "Exception caught: %s"  % e.pgerror
    finally:
        db_conn.close()

    return count


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    try:
        db_conn = connect()
        db_cursor = db_conn.cursor()
        sql = "INSERT INTO players (name) VALUES (%s);"
        db_cursor.execute(sql, (name,))
        db_conn.commit()
    except psycopg2.DatabaseError as e:
        print "Exception caught: %s" % e.pgerror
    finally:
        db_conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    try:
        db_conn = connect()
        db_cursor = db_conn.cursor()
        sql = "select id, name, wins, matches from vw_playerStandings order by wins desc"
        db_cursor.execute(sql)
        pStandings = db_cursor.fetchall()
    except psycopg2.DatabaseError as e:
        print "Exception caught: %s " % e.pgerror
    finally:
        db_conn.close()

    return pStandings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    try:
        db_conn = connect()
        db_cursor  = db_conn.cursor()
        sql = "INSERT INTO matches (winner, loser) VALUES (%s, %s);"
        db_cursor.execute(sql, (winner, loser,))
        db_conn.commit()
    except psycopg2.DatabaseError as e:
        print "DB Exception caught: %s" % e.pgerror
    finally:
        db_conn.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings()

    # added extra credit:
    # if found odd number of players, skip the last player and give him a "bye"
    if len(standings)%2 == 1:
        # add a dummy player to make the total players even
        addDummyPlayer()
    # end extra credit

    standings = playerStandings()
    extract_idName = []
    next_pair=[]
    for (id,name,win,match) in standings:
        extract_idName.append((id,name))

    for i in range(0,len(extract_idName),2):
        # if one of the player is -999, the other player is automatically win this match:
        if extract_idName[i][0] == -999:
            next_pair.append(extract_idName[i+1]+extract_idName[i])
        else:
            next_pair.append(extract_idName[i]+extract_idName[i+1])

    return next_pair


# functions from here onwards are from extra credit section:
# functions from here onwards are from extra credit section:
# functions from here onwards are from extra credit section:

def foundRematch(id1, id2):
    """Return True if a rematch found between a pair of players.

    Args:
      id1: the first player's unique id
      id2: the second player's unique id

    Return:
      True: a rematch found between two players in this match
      False: a rematch not found between two players in this match
    """
    try:
        db_conn = connect()
        db_cursor = db_conn.cursor()
        sql = "select count(*) from matches where (winner=%s and loser=%s) \
        or (winner=%s and loser=%s);"
        db_cursor.execute(sql, (id1,id2,id2,id1,))
        rematchCount = db_cursor.fetchone()
        if rematchCount[0] >= 1:
            return True
        else:
            return False
    except psycopg2.DatabaseError as e:
        print "DB Exception caught: %s" % e.pgerror
    finally:
        db_conn.close()


def addDummyPlayer():
    """Add a dummy player with id -999 to the players table."""
    try:
        db_conn = connect()
        db_cursor2  = db_conn.cursor()
        # ensure the dummy player not existed before adding one
        db_cursor2.execute("select count(*) from players where id = -999")
        if db_cursor2.fetchone()[0] == 0:
            # create a dummy loser to play against the lucky player
            sqlAddDummy = "INSERT INTO players (id, name) VALUES (%s, %s);"
            db_cursor2.execute(sqlAddDummy, (-999, 'Dummy',))
            db_conn.commit()
    except psycopg2.DatabaseError as e:
        print "DB Exception caught: %s" % e.pgerror
    finally:
        db_conn.close()


def getBye(id):
    """Return number of "bye" count

        Args:
            id: the id of a player
    """
    try:
        db_conn = connect()
        db_cursor = db_conn.cursor()
        sql = "select count(*) from matches where loser = -999 and winner = %s;"
        db_cursor.execute(sql, (id,))
        rows = db_cursor.fetchone()
        count = rows[0]
    except psycopg2.DatabaseError as e:
        print "DB Exception caught: %s" % e.pgerror
    finally:
        db_conn.close()
        
    return count
