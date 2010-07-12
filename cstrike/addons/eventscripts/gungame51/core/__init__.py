# ../addons/eventscripts/gungame51/core/__init__.py

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
from path import path

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
def get_game_dir(folder=None):
    '''!Gets an absolute path to a game directory.

    @remark Implicitly replaces \\ with / (linux support)

    @param dir Directory to append to the game directory.

    @return An absolute path to the game directory plus \p dir.'''
    if folder:
        folder = str(folder).replace('\\', '/')
        return path('%s/%s' % (gamePath, folder))
    return path(gamePath)

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

def get_file_list(top=get_game_dir('addons/eventscripts')):
    '''
    Generator that returns a list of files from within the gungame51 directory
    recursively.

    returns something like this:
    ['c:/srcds/cstrike/addons/eventscripts/gungame51',
        ['core', 'gungame51.py', 'scripts', '__init__.py']]

    (Excluding svn folders and files.)
    '''
    for name in path(top).walkdirs():
        if not "gungame51" in name:
            continue

        yield [str(name).replace('\\', '/'), 
            [str(x.name) for x in name.files('*.py')]]

# ============================================================================
# >> OLD FILE REMOVAL
# ============================================================================
# List of old files no longer in use.
old_files = [get_game_dir('addons/eventscripts/gungame51/scripts/included' +
                '/gg_error_logging'),
             get_game_dir('addons/eventscripts/gungame51/scripts/included' +
                '/gg_thanks'),
             get_game_dir('cfg/gungame51/included_addon_configs' + 
                '/gg_error_logging.cfg'),
             get_game_dir('cfg/gungame51/included_addon_configs' + 
                '/gg_thanks.cfg')]

# Delete any out of date files
for old_file in old_files:
    
    if old_file.isfile():
        old_file.remove()

    # Delete entire directory?
    elif old_file.isdir():
        old_file.rmtree()
    else:
        continue

    # Send console message
    es.server.queuecmd('echo [GunGame] Deleted %s' % str(old_file))