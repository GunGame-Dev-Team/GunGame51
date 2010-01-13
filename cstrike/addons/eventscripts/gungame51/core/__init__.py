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
from os import listdir
from os import path
from os import lstat
import path
from stat import S_ISDIR

# Eventscripts Imports
from es import ServerVar

# ============================================================================
# >> GLOBALS
# ============================================================================
gamePath = str(ServerVar('eventscripts_gamedir')).replace('\\', '/')

# ============================================================================
# >> CLASSES
# ============================================================================
class GunGameError(Exception):
    pass

# ============================================================================
# >> FILES, DIRECTORIES, & OS FUNCTIONS
# ============================================================================
def get_game_dir(folder=None):
    '''!Gets an absolute path to a game directory.

    @remark Implicitly replaces \\ with / (linux support)

    @param dir Directory to append to the game directory.

    @return An absolute path to the game directory plus \p dir.'''
    if folder:
        folder = str(folder).replace('\\', '/')
        return '%s/%s' % (gamePath, folder)
    return gamePath

def getOS():
    return platform

def inMap():
    '''!Checks to see if the server is currently in a map.

    @retval True The server is in a map.
    @retval False The server is not in a map.'''
    return (str(ServerVar('eventscripts_currentmap')) != '')
    
def removeReturnChars(text):
    text = text.replace('\\r', '')
    return text.replace('\\n', '')

def get_file_list(top=get_game_dir('addons/eventscripts')):
    '''
    Generator that returns a list of files from within the gungame51 directory
    recursively.

    returns something like this:
    ['c:/srcds/cstrike/addons/eventscripts/gungame51',
        ['core', 'gungame51.py', 'scripts', '__init__.py']]

    (Excluding svn folders and files.)
    '''
    for name in path.path(top).walkdirs():
        if not "gungame51" in name:
            continue

        yield [str(name).replace('\\', '/'), [str(x.name) for x in name.files('*.py')]]