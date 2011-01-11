# ../core/addons/__init__.py

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

# Eventscripts Imports
import es
import gamethread

# GunGame Imports
from gungame51.core import get_game_dir
from gungame51.core import get_file_list
from gungame51.core.events.shortcuts import EventManager
from gungame51.core.messaging import MessageManager

# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
ggVersion = None
_gg_info_quiet = True
_gg_info = None


# =============================================================================
# >> CLASSES
# =============================================================================
class AddonInfo(dict):
    '''
    This will hold the sub-addon info similar to es.AddonInfo().
    It will be initialized in sub-addons that wish to use it.
    '''
    # =========================================================================
    # >> AddonInfo() CLASS INITIALIZATION
    # =========================================================================
    def __init__(self):
        '''
        Initialize the dictionary and populate it with mandatory
        information.

        NOTE:
            This class is intended for internal use only.

        USAGE:
            from gungame.core.addons import AddonInfo

            info = AddonInfo()

            # The addon's name, as if you were unsing es_load
            info.name = 'example_addon'

            # The title of the addon, as it would be displayed in a menu
            info.title = 'Example Addon'

            # The author's name
            info.author = 'yournamehere'

            # The version number
            info.version = '1.0'
                * This number will be overrided if you have the SVN keyword
                  Rev in the doc string

            # GunGame scripts that are required for your addon to run properly
            # This MUST be a list
            info.requires = ['gg_addon1', 'gg_addon2']

            # GunGame scripts that will conflict with your addon if loaded
            # This MUST be a list
            info.conflicts= ['gg_addon3', 'gg_addon4']
        '''
        self.name = ''
        self.title = ''
        self.author = ''
        self.requires = []
        self.conflicts = []
        self.translations = []

    # =========================================================================
    # >> AddonInfo() CLASS ATTRIBUTE METHODS
    # =========================================================================
    def __setattr__(self, name, value):
        '''
        Setting an attribute is equivalent to setting an item
        '''
        self[name] = value

    def __getattr__(self, name):
        '''
        Getting an attribute is equivalent to getting an item
        '''
        if name == 'version':
            if name not in self._getKeyList():
                return '0.0'
        return self[name]

    def __setitem__(self, name, value):
        if name not in self._getKeyList():
            raise KeyError('AddonInfo instance has no key: "%s". \
                            Use only "%s".'
                                % (name, '", "'.join(self._getKeyList())))

        dict.__setitem__(self, name, value)

    def __getitem__(self, name):
        if name not in self._getKeyList():
            raise KeyError('AddonInfo instance has no key: "%s". \
                            Use only "%s".'
                                % (name, '", "'.join(self._getKeyList())))

        return dict.__getitem__(self, name)

    # =========================================================================
    # AddonInfo() STATIC CLASS METHODS
    # =========================================================================
    @staticmethod
    def _getKeyList():
        '''
        Return a list of valid attributes.
        '''
        return ['name', 'title', 'author', 'version', 'requires', 'conflicts',
                'translations']


class AddonLoadedByDependency(dict):
    '''
    This class is designed to store subaddons that were loaded as a result of
    being a dependency to another subaddon.
    '''
    def __new__(cls, *p, **k):
        if not '_the_instance' in cls.__dict__:
            cls._the_instance = dict.__new__(cls)
        return cls._the_instance

    # =========================================================================
    # >> AddonLoadedByDependency() CUSTOM CLASS METHODS
    # =========================================================================
    def add(self, dependency, addon_name):
        '''
        We will only add dependencies (subaddons) that were not loaded via
        configs or that were previously determined as being loaded due to
        being a dependency.
        '''
        # Create a new dependency list
        if dependency not in self:
            self[dependency] = []

        # Add the addon to the dependency list
        self[dependency].append(addon_name)

    def remove(self, addon_name):
        '''
        We will remove the addons from the list of dependencies that were
        loaded. If the dependency no longer has any addons that rely on it,
        we will unload the dependency.
        '''
        for dependency in list(self):
            # Ensure that the subaddon is listed in the dictionary
            if not addon_name in self[dependency]:
                return

            # Remove the subaddon from the list
            self[dependency].remove(addon_name)

            # If no more addons are listed under the dependency, unload it
            if not self[dependency]:
                es.set(dependency, 0)
                unload(dependency)
                del self[dependency]


class DependencyError(Exception):
    """
    We want a nice, descriptive error for dependency problems
    Due to the fact this error is unique it will need to be referenced by
    module.  If we want this error excepted we must except:
    gungame.DependencyError
    """
    pass


class AddonCompatibility(dict):
    '''
    This class holds sub-addons that are depended on or will conflict with
    a sub-addon being loaded. The loaded sub-addon will be stored under each
    dependency or conflict so we know what addons rely or conflict with other
    addons.
    '''
    # =========================================================================
    # >> AddonCompatibility() CUSTOM CLASS METHODS
    # =========================================================================
    def add(self, addon_name, namelist):
        '''
        Adds a list of dependencies or conflicts, storing the
        addon name under each entry so we know which addons depend on
        or conflict with other addons.
        '''
        for name in namelist:
            self[name] = self.get(name, []) + [addon_name]

    def remove(self, addon_name):
        '''
        Removes every dependency or conflict for a sub-addon
        '''
        for sub_addon in list(self):
            if addon_name in self[sub_addon]:
                self[sub_addon].remove(addon_name)
                if not self[sub_addon]:
                    del self[sub_addon]


dependencies = AddonCompatibility()
conflicts = AddonCompatibility()


class PriorityAddon(list):
    '''
    Class designed to handle the PreventLevel player attribute. This class is a
    list type, which allows us to potentially catch errors such as duplicate
    entries of addons in the PriorityAddon list, as well as preventing errors
    when scripters attempt to remove an entry that does not exist.
    '''

    _the_instance = None

    def __new__(cls, *elems):
        if cls._the_instance is None:
            cls._the_instance = t = list.__new__(cls)
        return cls._the_instance

    def __init__(self, *elems):
        self.extend(elems)

    # =========================================================================
    # >> PriorityAddon() CUSTOM CLASS METHODS
    # =========================================================================
    def append(self, name):
        if name not in self:
            list.append(self, name)

    def extend(self, names):
        for name in names:
            if name in self:
                continue

            list.append(self, name)

    def remove(self, name):
        if name in self:
            list.remove(self, name)

    def clear(self):
        del self[:]


class AddonManager(object):
    def __new__(cls, *p, **k):
        if not '_the_instance' in cls.__dict__:
            cls._the_instance = object.__new__(cls)
            # Create instance variables
            cls._the_instance.__loaded__ = {}
            cls._the_instance.__events__ = {}
            cls._the_instance.__order__ = []
        return cls._the_instance

    # =========================================================================
    # >> AddonManager() CUSTOM CLASS METHODS
    # =========================================================================
    def load(self, name):
        '''
        Loads a GunGame sub-addon by name
        '''
        # If the addon is loaded we cannot load it again
        if name in self.__loaded__:
            raise NameError('GunGame sub-addon "%s" is already loaded' % name)

        # Retrieve the addon
        addon = self.get_addon_by_name(name)

        # Add dependencies or conflicts of the sub-addon being unloaded
        self.add_dependencies_conflicts(addon, name)

        # Load the translation files
        self.load_translations(addon)

        # Register the events in the addon
        self.register_events(addon, name)

        # Save the module by name so we know it is loaded
        self.__loaded__[name] = addon

        # Add the module to the order of called events
        self.__order__.append(name)

        # Call the load block as is normally done by ES
        # We do this last because if there is a load error we don't want to
        # stop loading the sub-addon
        self.call_block(addon, 'load')

        # Updating es.AddonInfo
        gungame_info('update')

        # Fire the event "gg_addon_loaded"
        EventManager().gg_addon_loaded(name, self.get_addon_type(name))

    def unload(self, name, unloading_gg=False):
        '''
        Unloads a GunGame sub-addon by name
        '''
        # If the addon is not loaded we cannot unload it
        if name not in self.__loaded__:
            raise NameError("GunGame sub-addon '%s' is not loaded" % name)

        # Retrieve the addon
        addon = self.get_addon_by_name(name)

        # Remove dependencies or conflicts of the sub-addon being unloaded
        self.remove_dependencies_conflicts(name)

        # Unload the translation files
        self.unload_translations(addon)

        # Unload any subaddons that were loaded as dependencies
        self.remove_loaded_by_dependency(name)

        # Unregister the events in the addon
        self.unregister_events(addon, name)

        # Remove the module from the loaded module dictionary
        del self.__loaded__[name]

        # Remove the module from the order of called events
        self.__order__.remove(name)

        # Remove custom attribute callbacks associated with this addon
        Player.remove_callbacks_for_addon(name)

        # Call the unload block as is normally done by ES
        # Again, we do this last so it doesn't matter if the block errors
        self.call_block(addon, 'unload')

        # Updating es.AddonInfo
        if not unloading_gg:
            gungame_info('update')

        # Fire the event "gg_addon_unloaded"
        EventManager().gg_addon_unloaded(name, self.get_addon_type(name))

    def register_events(self, addon, name):
        '''
        Register all functions in the module as events to ES
        '''
        # Retrieve the module's dictionary
        addon_globals = addon.__dict__

        # Loop through all items in the module's dictionary
        for item in addon_globals:
            # Ensure that the item is callable as well as a function
            if not callable(addon_globals[item]) or \
                type(addon_globals[item]).__name__ != 'function':
                continue

            # See if this is an event that we have not previously registered
            if item not in self.__events__.keys():
                # Add the event to our __events__ dictionary
                self.__events__[item] = {}

                # We only register the specific event once, and use
                #   self.call_event() to handle ALL events
                es.addons.registerForEvent(self, item, self.call_event)

            # Add the addon to the list of addons to call when the event
            #   triggers
            self.__events__[item][name] = addon_globals[item]

    def unregister_events(self, addon, name):
        '''
        Unregister all functions in the module from being called by ES as
        events
        '''
        # Retrieve the module's dictionary
        addon_globals = addon.__dict__

        # Loop through all items in the addon dictionary
        for item in addon_globals:
            # Ensure that the item is callable, as well as contained within
            #   the __events__ dictionary
            if callable(addon_globals[item]) and item in self.__events__:
                # Delete the addon from the list of addons to call when the
                #   event triggers
                current_event = self.__events__[item]
                if name in current_event:
                    del current_event[name]

                # Unregister the event if no more sub-addons are using it
                if not self.__events__[item]:
                    # Unregister the event with EventScripts
                    es.addons.unregisterForEvent(self, item)

                    # Remove the event from our __events__ dictionary
                    del self.__events__[item]

    def call_event(self, event_var):
        '''
        Calls the events in sub-addons in the order dictated by __order__
        '''
        # Grab the current event's dictionary from our __events__ dictionary
        current_event = self.__events__[str(event_var['es_event'])]

        # Loop through each addon in the __order__ list
        for name in self.__order__:
            # Check to see if there is an addon taking priority
            if PriorityAddon():
                # The addon's event does not fire if it is not a priority addon
                if name not in PriorityAddon():
                    # Always fire these events
                    if not name in current_event or not \
                            current_event[name].__name__ in ["es_map_start",
                                    "player_activate", "es_player_validated",
                                                        "player_disconnect"]:
                        continue

            # If the addon name is in the current event, call the function
            if name in current_event:
                current_event[name](event_var)

    def add_dependencies_conflicts(self, addon, name):
        '''
        Raises an error if there is a dependency or conflict problem or adds
        the addon's dependencies and conflicts to the existing dictionaries
        '''
        # Gather a list of dependencies and conflicts
        addon_depend, addon_conflict = self.get_dependencies_conflicts(name)

        # If an addon is depended on and also conflicts, wth?
        conflicting = set(addon_depend).intersection(addon_conflict)

        if conflicting:
            raise DependencyError('Sub-addon "%s" depends on and also '
                % name + 'conflicts with sub-addon(s) "%s"'
                    % ('", "'.join(conflicting)))

        # Ensure this addon does not conflict with a loaded addon
        if name in conflicts:
            es.set(name, 0)
            raise DependencyError('Loaded sub-addon(s) "%s" conflict with '
                    % ('", "'.join(conflicts[name])) +
                    'sub-addon "%s"' % (name))

        # Ensure loaded addons do not conflict with this addon
        conflicting = set(self.__loaded__).intersection(addon_conflict)

        if conflicting:
            es.set(name, 0)
            raise DependencyError('Sub-addon "%s" conflicts with loaded'
                % name + ' sub-addon(s) "%s"' % ('", "'.join(conflicting)))

        # Ensure addons depended on by this sub-addon are loaded
        conflicting = set(addon_depend).difference(self.__loaded__)

        if conflicting:
            # Loop through all addons that are not loaded and load them
            for subaddon in conflicting:
                # Add the subaddon to the "AddonLoadedByDependency()" dict
                gamethread.delayed(0, self.add_loaded_by_dependency,
                                                            (subaddon, name))

        # Add this sub-addon's dependencies and conflicts
        dependencies.add(name, addon_depend)
        conflicts.add(name, addon_conflict)

    def remove_dependencies_conflicts(self, name):
        '''
        Removes the dependencies or conflicts associated with a sub-addon
        '''
        # Ensure this addon is not depended on by other sub-addons
        if name in dependencies:
            es.set(name, 1)
            raise DependencyError('Loaded sub-addon(s) "%s" depend on '
                % ('", "'.join(dependencies[name])) + 'sub-addon "%s"' % name)

        # Remove the sub-addon's dependencies and conflicts
        dependencies.remove(name)
        conflicts.remove(name)

    def get_dependencies_conflicts(self, addon):
        '''
        Returns the dependencies and conflicts of an addon
        '''
        # Retrieve the addon's module
        mod = self.get_addon_by_name(addon)

        # Grab the addon info
        info = self.get_addon_info(mod.__name__.split('.')[-1])

        # Gather a list of dependencies
        addon_depend = info.requires if 'requires' in info else []

        # Gather a list of conflicts
        addon_conflict = info.conflicts if 'conflicts' in info else []

        return addon_depend, addon_conflict

    def add_loaded_by_dependency(self, dependency, addon_name):
        '''
        Adds dependencies to be unloaded later that were loaded as a result of
        as sub-addon.
        '''
        if dependency in self.__loaded__:
            return

        es.set(dependency, 1)
        load(dependency)
        AddonLoadedByDependency().add(dependency, addon_name)

    def remove_loaded_by_dependency(self, name):
        '''
        Removes and unloads dependencies that were loaded as a result of a
        sub-addon.
        '''
        AddonLoadedByDependency().remove(name)

    def get_addon_by_name(self, name):
        '''
        Returns the module of an addon by name
        '''
        # If the addon is loaded we have stored the module
        if name in self.__loaded__:
            return self.__loaded__[name]

        # If the addon is not loaded we need to import it
        addonType = self.get_addon_type(name)
        modulePath = 'gungame51.scripts.%s.%s.%s' % (addonType, name, name)
        mod = __import__(modulePath, globals(), locals(), [''])

        # We have to reload the module to re-instantiate the globals
        reload(mod)

        return mod

    def load_translations(self, addon):
        for translation in self.get_addon_info(addon).translations:
            MessageManager().load(translation, addon.__name__.split('.')[-1])

    def unload_translations(self, addon):
        for translation in self.get_addon_info(addon).translations:
            MessageManager().unload(translation, addon.__name__.split('.')[-1])

    def get_addon_info(self, addon=None):
        '''
        Returns the AddonInfo instance in the module if present
        '''
        if not addon:
            # Return a dictionary of all addons
            dict_addon = {}
            for name in self.__loaded__:
                addon = self.get_addon_by_name(name)
                addon_globals = addon.__dict__
                for item in addon_globals:
                    if isinstance(addon_globals[item], AddonInfo):
                        dict_addon[name] = addon_globals[item]
                        break

            return dict_addon

        if type(addon).__name__ == 'str':
            addon = self.get_addon_by_name(addon)

        # If the addon info exists we return it
        addon_globals = addon.__dict__

        for name in addon_globals:
            if isinstance(addon_globals[name], AddonInfo):
                return addon_globals[name]

        return None

    # =========================================================================
    # AddonManager() STATIC CLASS METHODS
    # =========================================================================
    @staticmethod
    def get_addon_type(name):
        '''
        Returns a string value of the addon type:
            "custom"
            "included"
        '''
        # Check addon exists
        if not AddonManager().addon_exists(name):
            raise ValueError('Cannot get addon type (%s): doesn\'t exist.'
                % name)

        # Get addon type
        if name in included_addons_cache:
            return 'included'
        elif name in custom_addons_cache:
            return 'custom'

    @staticmethod
    def addon_exists(name):
        '''
        Returns a bool value depending on a GunGame addon's existance.
        '''
        return (name in get_valid_addons())

    @staticmethod
    def call_block(addon, blockname, *a, **kw):
        """ Calls a block in a loaded sub-addon """
        addon_globals = addon.__dict__
        if blockname in addon_globals and callable(addon_globals[blockname]):
            addon_globals[blockname](*a, **kw)


# =============================================================================
# >> FUNCTIONS
# =============================================================================
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

'''
This wrapper makes it possible to use key addon functions
without interacting with the AddonManager directly
'''


def load(*a, **kw):
    AddonManager().load(*a, **kw)
load.__doc__ = AddonManager.load.__doc__


def unload(*a, **kw):
    AddonManager().unload(*a, **kw)
unload.__doc__ = AddonManager.unload.__doc__

# Variable to cache the results of get_valid_addons() - saves overhead from
# reading the disk each time get_valid_addons() is called
valid_addons_cache = []
# Variable to cache valid included addons (same concept as valid_addons_cache)
included_addons_cache = []
# Variable to cache valid included addons (same concept as valid_addons_cache)
custom_addons_cache = []


def get_valid_addons():
    '''
    Returns a list of valid addon names from the included and custom addons
    directory.
    '''
    # If we have cached a list of valid addons, return the cached list
    if valid_addons_cache:
        return valid_addons_cache

    # Create directory references to loop through
    included = get_game_dir('addons/eventscripts/gungame51/scripts/included')
    custom = get_game_dir('addons/eventscripts/gungame51/scripts/custom')

    # Loop through each path name
    for pathName in [included, custom]:
        # Loop through directories in the given paths
        for item in pathName.dirs():
            # Append basename of the directory (addon name) to the cached list
            if item.parent == included:
                included_addons_cache.append(item.namebase)
            else:
                custom_addons_cache.append(item.namebase)
            valid_addons_cache.append(item.namebase)
    return valid_addons_cache

from gungame51.core.players.shortcuts import Player
