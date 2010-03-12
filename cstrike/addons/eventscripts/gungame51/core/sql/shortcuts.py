# ../addons/eventscripts/gungame/core/sql/shortcuts.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
# Eventscripts Imports
from es import ServerVar

# GunGame Imports
from gungame51.core.sql import Database

# ============================================================================
# >> GLOBALS
# ============================================================================
gg_prune_database = ServerVar('gg_prune_database')

# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
def insert_winner(name, uniqueid, wins, timestamp='strftime("%s","now")'):
    '''
    Inserts a new entry into the database.
    '''
    # Send to be queried
    ggDB = Database()
    ggDB._query("INSERT INTO gg_wins (name, uniqueid, wins, timestamp) VALUES" +
                "(?, ?, ?, ?)", values=(name, uniqueid, wins, timestamp))
    ggDB.commit()

def update_winner(columnTuple, valueTuple, name=None, uniqueid=None, wins=None,
            timestamp=None):
    '''
    Updates the database for the columns in columnTuple with the values in
    valueTuple of the same index. 
    '''
    # Valid columnTuple entries
    validEntries = ("name", "wins", "timestamp")

    # If there are no columns to update, stop here
    if not columnTuple:
        return

    # Make sure that we are working with tuples
    if not isinstance(columnTuple, tuple):
        columnTuple = (columnTuple,)
    if not isinstance(valueTuple, tuple):
        valueTuple = (valueTuple,)

    # If the columnTuple and valueTuple aren't equal in length, raise a
    # valueError
    if len(columnTuple) != len(valueTuple):
        raise ValueError("columnTuple and valueTuple must be the same length")
    
    # Check columnTuple for valid entries
    for column in columnTuple:
        if column in validEntries:
            continue

        raise NameError("Valid columnTuple entries are %s, %s, and %s" %
                validEntries)
    
    conditionParams = {'name':name, 'uniqueid':uniqueid, 'wins':wins,
                        'timestamp':timestamp}
    
    conditions = ""
    conditionValues = []
    # Create the WHERE conditions
    for condition in conditionParams:
        # If the condition was a parameter
        if conditionParams[condition]:
            # If this is the first conditions, add WHERE, otherwise add AND
            if not len(conditions):
                conditions = "WHERE"
            else:
                conditions += " AND"
            
            # Add the condition
            conditions += " %s=?" % condition
            
            conditionValues.append(conditionParams[condition])
    
    updateString = ""
    # Create the SET statement
    for column in columnTuple:
        if len(updateString):
            updateString += ", "

        updateString += "%s=?" % column
    
    # Add the updateString and conditions to queryString
    queryString = "UPDATE gg_wins SET %s %s" % (updateString, conditions)
    
    # Include the values for the conditions in the valueTuple
    valueTuple += tuple(conditionValues)
    
    # Send to be queried
    ggDB = Database()
    ggDB._query(queryString, values=valueTuple)
    ggDB.commit()

def get_rank(uniqueid):
    ggDB = Database()
    # Get the current number of wins for the uniqueid
    currentWins = ggDB.select('gg_wins', 'wins', 'where uniqueid = "%s"' % \
                                                                    uniqueid)

    # Return -1 if the player has no wins
    if currentWins == None:
        return -1

    # Return the count + 1 of players who have more wins than the uniqueid
    return ggDB.select("gg_wins", ("COUNT(*)"), "WHERE ABS(wins) > %s" % \
                                                            currentWins) + 1

def get_winner_count():
    return Database().select("gg_wins", ("COUNT(*)"))

def get_winners_list(n=10):
    '''
    Returns an ordered list dicts of (n) player names in order from highest
    to lowest win count.
    '''
    if not str(n).isdigit():
        raise ValueError('Expected digit, and got a str() (%s)' % n)
    n = int(n)
    ggDB = Database()
    winner_list = ggDB.select('gg_wins', ('name', 'uniqueid', 'wins'),
                                            'ORDER BY ABS(wins) DESC', True, n)
    if winner_list:
        return winner_list
    return []

def prune_winners_db(days=None):
    '''
    Prunes the database within n amount of days, defaults to gg_prune_database
    '''
    if not days:
        if not int(gg_prune_database):
            return
        days = int(gg_prune_database)

    ggDB = Database()
    ggDB._query('DELETE FROM gg_wins WHERE ' +
                'timestamp < strftime("%s","now", "-%s days")' % ('%s', days))
    ggDB.commit()