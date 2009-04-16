# ============================================================================
# >> IMPORTS
# ============================================================================
# Python Imports
from os import name as platform

# Eventscripts Imports
import es

# ============================================================================
# >> GLOBALS
# ============================================================================
gamePath = str(es.ServerVar('eventscripts_gamedir')).replace('\\', '/')

# ============================================================================
# >> CLASSES
# ============================================================================
class GunGameError(Exception):
    pass

# ============================================================================
# >> FUNCTIONS
# ============================================================================
def getGameDir(dir):
    '''!Gets an absolute path to a game directory.
    
    @remark Implicitly replaces \\ with / (linux support)
    
    @param dir Directory to append to the game directory.
    
    @return An absolute path to the game directory plus \p dir.'''
    # Linux path seperators
    dir = dir.replace('\\', '/')
    
    # Return
    return '%s/%s' % (gamePath, dir)
    
def isDead(userid):
    '''!Checks to see if \p userid is dead.
    
    @retval 1 The player is dead.
    @retval 0 The player is alive.'''
    return es.getplayerprop(userid, 'CBasePlayer.pl.deadflag')
    
def inMap():
    '''!Checks to see if the server is currently in a map.
    
    @retval True The server is in a map.
    @retval False The server is not in a map.'''
    return (str(es.ServerVar('eventscripts_currentmap')) != '')

def isSpectator(userid):
    '''!Checks to see if \p userid is a spectator.
    
    @retval True The player is a spectator, currently connecting or not on the server.
    @retval False The player is on an active team.'''
    return es.getplayerteam(userid) <= 1
    
def getOS():
    return platform