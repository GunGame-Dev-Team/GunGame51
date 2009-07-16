# ../addons/eventscripts/gungame/core/__init__.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

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
# >> FILES, DIRECTORIES, & OS FUNCTIONS
# ============================================================================
def getGameDir(dir=None):
    '''!Gets an absolute path to a game directory.

    @remark Implicitly replaces \\ with / (linux support)

    @param dir Directory to append to the game directory.

    @return An absolute path to the game directory plus \p dir.'''
    if dir:
        # Return
        return '%s/%s' % (gamePath, dir.replace('\\', '/'))
    return gamePath

def getOS():
    return platform

def inMap():
    '''!Checks to see if the server is currently in a map.

    @retval True The server is in a map.
    @retval False The server is not in a map.'''
    return (str(es.ServerVar('eventscripts_currentmap')) != '')
    
def removeReturnChars(text):
    text = text.replace('\\r', '')
    return text.replace('\\n', '')