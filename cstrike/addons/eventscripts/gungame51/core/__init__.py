# ../core/__init__.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
from __future__ import with_statement
from os import name as platform
from path import path

# Eventscripts Imports
import es


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
ggVersion = None
_gg_info_quiet = True
_gg_info = None
gamePath = path(path(__file__).parent.rsplit('addons', 1)[0][:~0])


# =============================================================================
# >> CLASSES
# =============================================================================
class GunGameError(Exception):
    pass


# =============================================================================
# >> FILES, DIRECTORIES, & OS FUNCTIONS
# =============================================================================
def get_game_dir(folder=None):
    '''!Gets an absolute path to a game directory.

    @remark Implicitly replaces \\ with / (linux support)

    @param dir Directory to append to the game directory.

    @return An absolute path to the game directory plus \p dir.'''
    if folder:
        folder = str(folder).replace('\\', '/')
        return gamePath.joinpath(folder)
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

# =============================================================================
# >> OLD FILE REMOVAL
# =============================================================================
# List of old files no longer in use.
old_files = [
    'addons/eventscripts/gungame51/core/events/data/es_gungame_events.res',
    'addons/eventscripts/gungame51/scripts/included/gg_error_logging',
    'addons/eventscripts/gungame51/scripts/included/gg_thanks',
    'cfg/gungame51/included_addon_configs/gg_error_logging.cfg',
    'cfg/gungame51/included_addon_configs/gg_thanks.cfg',
]

# Delete any out of date files
for old_file in old_files:

    # Get the full path to the file
    old_file = get_game_dir(old_file)

    if old_file.isfile():
        old_file.remove()

    # Delete entire directory?
    elif old_file.isdir():
        old_file.rmtree()
    else:
        continue

    # Send console message
    es.server.queuecmd('echo [GunGame] Deleted %s' % str(old_file))


def gungame_info(info, _info=None):
    '''
    Fetches the head revision number from all of gungame's files
    '''
    global ggVersion
    global _gg_info_quiet
    global _gg_info

    if info == 'version':
        # Stop here if we already have done this, and return the version.
        if ggVersion:
            return ggVersion

        # This files revision is our starting point
        rev = int(__doc__.split('$Rev: ')[1].split()[0])

        # Our generator which walks through the files
        gen = get_file_list()

        # Loop until an exception is raised
        while True:
            # See if we can get the next file
            try:
                files = gen.next()

            # Exception raised, we are out of files. Return the version.
            except:
                ggVersion = '5.1.%s' % rev
                return ggVersion

            # Folder name
            base_name = files[0]

            # Don't look for the GG version in custom scripts
            if 'gungame51/scripts/custom' in base_name:
                continue

            # Look through all the files in the folder
            for fileName in files[1]:
                # Try to open the file, then grab it's version
                try:
                    with open(base_name + "/" + fileName, 'r') as pyfile:
                        ver = int(pyfile.read().split('$Rev: ')[1].split()[0])

                    # Is this the new high version?
                    if ver > rev:
                        rev = ver

                    continue

                # File could not be read for version, continue..
                except:
                    continue

    '''
    Fetches a list of addons and it's version number in str format for
    es.AddonInfo()
    '''
    if info in ('included', 'custom'):
        # Stop here if this is the initial load
        if _gg_info_quiet:
            return

        # Retrieve the AddonManager
        from addons import AddonManager
        AM = AddonManager()

        # Format our output
        addonlist = ['\t' * 4 + '%s (v%s)\n' % (
            AM.get_addon_info()[addon].name,
            AM.get_addon_info()[addon].version) for addon in
            AM.get_addon_info().keys() if AM.get_addon_type(addon) == info]

        # If no addons, output is None
        if not addonlist:
            return 'None\n'

        # Add a line return to the beginning of our output
        addonlist.insert(0, '\n')

        # Return the list as one string
        return ' '.join(addonlist)

    '''
    Lets gungame51.py pass it's instance of es.AddonInfo into this file
    so we can update it. (stored as _gg_info global)
    '''
    if info == 'addoninfo':
        _gg_info = _info
        _gg_info_quiet = False
        gungame_info('update')

    '''
    Updates es.AddonInfo instance for gungame51
    '''
    if info == 'update':
        # If this is the inital load, or we don't have a es.AddonInfo()
        # instance then stop here.
        if _gg_info_quiet or not _gg_info:
            return

        # Collect included addons w/ versions
        _gg_info.Included_Addons = gungame_info('included')

        # Collect custom addons w/ versions
        _gg_info.Custom_Addons = gungame_info('custom')
