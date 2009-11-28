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
        folder = cleanString(folder).replace('\\', '/')
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

def cleanString(text, exceptions=[]):
    '''
    Removes escape characters from a string and replaces them with their
    original text.
    
    i.e. c:\addons becomes 'c:\x07ddons' and this function turns it back into
    c:\\addons
    '''
    bad_chars = (('\x07', '\\a'), ('\x08', '\\b'), ('\x0c', '\\f'),
        ('\n', '\\n'), ('\\N', '\\N'), ('\r', '\\r'), ('\t', '\\t'),
        ('\x0b', '\\v'))
    for escape_char in bad_chars:
        if escape_char[0] in exceptions or escape_char[0] not in text:
            continue
        text = text.replace(escape_char[0], escape_char[1])
    return text

def get_file_list(top=get_game_dir('addons/eventscripts/gungame51')):
    '''
    Generator that returns a list of files from within the gungame51 directory
    recursively.

    returns something like this:
    ['c:/srcds/cstrike/addons/eventscripts/gungame51',
        ['core', 'gungame51.py', 'scripts', '__init__.py']]

    (Excluding svn folders and files.)
    '''
    names = [n for n in listdir(top) if n != '.svn']
    yield [top, names]
    for name in names:
        if name == '.svn':
            continue
        try:
            st = lstat(path.join(top, name))
        except:
            continue
        if not S_ISDIR(st.st_mode):
            continue
        for (newtop, children) in get_file_list('%s/%s' % (top, name)):
            yield [newtop, [c for c in children if c != '.svn']]