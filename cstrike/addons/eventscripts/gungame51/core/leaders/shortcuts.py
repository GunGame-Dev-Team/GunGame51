# ../cstrike/addons/eventscripts/gungame51/core/leaders/shortcuts.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
# EventScripts Imports
import es

# GunGame Imports
from gungame51.core import removeReturnChars
from gungame51.core.leaders import leaders

# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
def isLeader(userid):
    userid = int(userid)
    return (userid in leaders.current)
    
def resetLeaders():
    leaders.reset()
    
def getLeaderCount():
    '''
    Returns the amount of leaders.
    '''
    return len(leaders.current)
    
def getOldLeaderList():
    '''
    Returns the userids of the old/previous leader(s).
    '''
    # Remove disconnected userids from the previous leaders and return the list
    return leaders.cleanup('previous')
    
def getLeaderList():
    '''
    Returns the userids of the current leader(s).
    '''
    # Remove disconnected userids from the current leaders and return the list
    return leaders.cleanup('current')
    
def getLeaderNames():
    '''Returns the names of the current leader(s).'''
    return [removeReturnChars(es.getplayername(x)) for x in getLeaderList()]
    
def getLeaderLevel():
    '''Returns the current leader level.'''
    return leaders.leaderlevel