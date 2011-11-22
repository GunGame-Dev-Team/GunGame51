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
from os import name as os_name
from path import path

# Eventscripts Imports
import es


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
game_path = path(path(
    __file__).parent.rsplit('addons', 1)[0][:~0].replace('\\', '/'))


# =============================================================================
# >> CLASSES
# =============================================================================
class GunGameError(Exception):
    pass


class GunGameInfo(object):
    def __new__(cls):
        if not '_the_instance' in cls.__dict__:
            cls._the_instance = object.__new__(cls)
        return cls._the_instance

    def __init__(self):
        if not hasattr(self, '_version'):
            self._version = self._get_version()

    def _get_info(self):
        if hasattr(self, '_info'):
            return self._info
        return None

    def _set_info(self, info):
        if isinstance(info, es.AddonInfo):
            self._info = info

    info = property(fget=_get_info, fset=_set_info)

    @property
    def version(self):
        return self._version

    @staticmethod
    def _get_version():
        revision = int(__doc__.split('$Rev: ')[1].split()[0])
        for file_path in get_game_dir(
          'addons/eventscripts/gungame51').walkfiles('*.py'):
            if 'custom' in file_path.splitall():
                continue
            try:
                with file_path.open() as pyfile:
                    version = int(pyfile.read().split('$Rev: ')[1].split()[0])
                if version > revision:
                    revision = version
            except:
                continue
        return '5.1.%s' % revision


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
        return game_path.joinpath(folder)
    return game_path


def get_os():
    return os_name


def in_map():
    '''!Checks to see if the server is currently in a map.

    @retval True The server is in a map.
    @retval False The server is not in a map.'''
    return (str(es.ServerVar('eventscripts_currentmap')) != '')


def remove_return_chars(text):
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

    if info == 'version':
        return GunGameInfo().version

    if info == 'addoninfo':
        GunGameInfo().info = _info
        gungame_info('update')

    elif info == 'update':
        if GunGameInfo().info is None:
            return
        GunGameInfo().info.__setattr__(
            'Included Addons', gungame_info('included'))
        GunGameInfo().info.__setattr__(
            'Custom Addons', gungame_info('custom'))

    if info in ('included', 'custom'):
        if GunGameInfo().info is None:
            return
        # Retrieve the Loaded Addons
        from addons.loaded import LoadedAddons

        # Format our output
        addonlist = ['\t' * 4 + '%s (v%s)\n' % (
            LoadedAddons[addon].info.name,
            LoadedAddons[addon].info.version) for addon in
            LoadedAddons if LoadedAddons[addon].addon_type == info]

        # If no addons, output is None
        if not addonlist:
            return 'None\n'

        # Add a line return to the beginning of our output
        addonlist.insert(0, '\n')

        # Return the list as one string
        return ' '.join(addonlist)
