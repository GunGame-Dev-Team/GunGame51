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
def getWinnersList(n=10):
    '''
    Returns an ordered list dicts of (n) player names in order from highest
    to lowest win count.
    '''
    if not str(n).isdigit():
        raise ValueError('Expected digit, and got a str() (%s)' % n)
    n = int(n)
    if n > 50:
        n = 50
    ggDB = Database()
    return ggDB.select('gg_wins', ('name', 'wins'),
                            'ORDER BY wins DESC', True, n)

def pruneWinnersDB(days=None):
    '''
    Prunes the database within n amount of days, defaults to gg_prune_database
    '''
    if not days:
        if not int(gg_prune_database):
            return
        days = int(gg_prune_database)

    ggDB = Database()
    ggDB.query("DELETE FROM gg_wins WHERE " +
                "timestamp < strftime('%s','now', '-%s days')" % ('%s', days))
    ggDB.commit()