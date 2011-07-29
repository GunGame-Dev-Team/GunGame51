# ../core/cfg/__init__.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
from path import path

# EventScripts Imports
#   ES
import es
#   Cfglib
from cfglib import AddonCFG
#   Gamethread
from gamethread import delayed

# GunGame Imports
#   Addons
from gungame51.core.addons import get_valid_addons
from gungame51.core.addons import AddonManager
from gungame51.core.addons import load
from gungame51.core.addons import unload
from gungame51.core.addons import dependencies
from gungame51.core.addons import conflicts
#   Messaging
from gungame51.core.messaging.shortcuts import langstring
#   Base
from gungame51.core import get_game_dir

# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
base_config_path = path(
    path(__file__).parent.rsplit('addons', 1)[0]).joinpath('cfg/gungame51')


# =============================================================================
# >> CONFIG MANAGER CLASS
# =============================================================================
class ConfigManager(object):
    '''
    Class designed to handle the loading, unloading, and executing of python
    configs coded using cfglib.AddonCFG().
    '''
    def __new__(cls, *p, **k):
        if not '_the_instance' in cls.__dict__:
            cls._the_instance = object.__new__(cls)
            # Initialize the class instance variables
            cls._the_instance.__loaded__ = {}
            cls._the_instance.__cvardefaults__ = {}
            cls._the_instance._config_files = {}
        return cls._the_instance

    def load_configs(self):
        '''Loads all "main", "included", and "custom" addon config files'''

        es.addons.registerForEvent(self, 'server_cvar', self.server_cvar)

        self.cfg_executing = False

        es.dbgmsg(0, langstring('Load_Configs'))

        for cfgfile in _config_types['main']:

            self.load(cfgfile, 'main')

        for cfgfile in _config_types['included']:

            self.load(cfgfile, 'included')

        es.dbgmsg(0, langstring('Load_CustomConfigs'))

        for cfgfile in _config_types['custom']:

            self.load(cfgfile, 'custom')

    def load(self, cfgfile, cfg_type):
        config = self._import_config(cfgfile.namebase, cfg_type)

        if 'load' in config.__dict__:
            config.load()

        cfg = None

        basepath = path(config.__dict__['__file__']).namebase

        if cfg_type != 'main':

            basepath = basepath[:~6]

        if basepath in self._config_files:

            cfg = self._config_files[basepath]

        else:

            for item in config.__dict__:

                if not isinstance(config.__dict__[item], AddonCFG):
                    continue

                cfg = config.__dict__[item]

                self._config_files[basepath] = cfg

                break

        if cfg is None:
            return

        revisit = []

        for cvar, value, description in cfg.getCvars().values():

            self.__cvardefaults__[cvar] = value

            if bool(str(value)) and False in [
              x == '0' for x in str(value).split('.')]:

                revisit.append(cvar)

        self.cfg_executing = True

        delayed(0.01, self._reset_config_execution)

        delayed(0, cfg.execute)

        revisist = [x for x in revisit if x in get_valid_addons()]

        for cvar in revisit:

            es.forcevalue(cvar, 0)

            delayed(0, es.server.queuecmd,
                ('%s %s' % (cvar, self.__cvardefaults__[cvar])))

    def _import_config(self, name, cfg_type):
        if name in self.__loaded__:
            return self.__loaded__[name]

        if cfg_type == 'main':

            self.__loaded__[name] = __import__('gungame51.core.cfg.files.%s'
                % name, globals(), locals(), [''])

        else:

            addon = name.replace('_config', '')

            self.__loaded__[name] = __import__('gungame51.scripts.%s.%s.%s'
                % (cfg_type, addon, name), globals(), locals(), [''])

        reload(self.__loaded__[name])

        return self.__loaded__[name]

    def _reset_config_execution(self):
        self.cfg_executing = False

    def unload_configs(self):
        for cfg in self._config_files.values():

            for cvar, value, description in cfg.getCvars().values():

                es.ServerVar(cvar).set(value)

                if cvar in self.__cvardefaults__:

                    del self.__cvardefaults__[cvar]

                es.ServerVar(cvar).removeFlag('notify')

        for name in self.__loaded__.keys():

            reload(self.__loaded__[name])

            if 'unload' in self.__loaded__[name].__dict__:

                self.__loaded__[name].unload()

            del self.__loaded__[name]

        es.addons.unregisterForEvent(self, 'server_cvar')

    def server_cvar(self, event_var):
        '''
        Handles CVARs that are loaded via GunGame's ConfigManager.
        '''
        cvarName = event_var['cvarname']
        cvarValue = event_var['cvarvalue']

        if cvarName not in get_valid_addons():
            return

        # Load addons if the value is not 0, '', or a float equal to 0
        if bool(str(cvarValue)) and False in \
        [x == '0' for x in str(cvarValue).split('.')]:

            # Make sure the addon is not already loaded
            if cvarName in AddonManager().__loaded__:
                return

            # Check to see if the user has tried to disable the addon, or if it
            # was executed by a config
            if self.cfg_executing and cvarName in conflicts.keys():
                if str(ConfigManager().__cvardefaults__[cvarName]) == \
                  str(cvarValue):
                    return

            delayed(0, load, (cvarName))

        # Unload addons with the value of 0 (including floats) or ''
        else:
            # Make sure that the addon is loaded
            if cvarName not in AddonManager().__loaded__:
                return

            # Check to see if the user has tried to disable the addon, or if it
            # was executed by a config
            if self.cfg_executing and cvarName in dependencies.keys():
                if str(ConfigManager().__cvardefaults__[cvarName]) == \
                  str(cvarValue):
                    return

            delayed(0, unload, (cvarName))


# =============================================================================
# >> LIST MANAGEMENT CLASSES
# =============================================================================
class ListManagement(list):
    header = ''
    first = ''
    indent = 0

    def __init__(self, config):
        self.config = config

    def print_to_text(self):
        if not len(self):
            return
        if self.header:
            self.config.text(self.header)
        for section in self:
            if isinstance(section, str):
                self.config.text(self.first + section)
            elif isinstance(section, list):
                self.config.text(self.first + section[0])
                for line in section[1:]:
                    self.config.text(' ' * self.indent + line)


class ListDescription(ListManagement):
    header = 'Description:'
    first = ' ' * 3
    indent = 6


class ListInstructions(ListManagement):
    header = 'Instructions:'
    first = '   * '
    indent = 7


class ListNotes(ListManagement):
    header = 'Notes:'
    first = '   * '
    indent = 6
    requires = list()
    conflict = list()

    def print_to_text(self):
        if not (len(self) or self.conflict or self.requires):
            return
        self.config.text(self.header)
        for addon in self.requires:
            self.config.text(
                self.first + '"' + addon + '" will automatically be enabled.')
            self.config.text(self.first +
                'Will not load if "' + addon + '" can not be enabled.')
        for addon in self.conflict:
            self.config.text(
                self.first + 'Will not load with "' + addon + '" enabled.')
        for section in self:
            if isinstance(section, str):
                self.config.text(self.first + section)
            elif isinstance(section, list):
                self.config.text(self.first + section[0])
                for line in section[1:]:
                    self.config.text(' ' * self.indent + line)


class ListExamples(ListManagement):
    header = 'Examples:'
    first = '   * '
    indent = 9


class ListOptions(ListManagement):
    header = 'Options:'
    first = ' ' * 3
    indent = 9


# =============================================================================
# >> CONTEXT MANAGEMENT CLASSES
# =============================================================================
class ConfigContextManager(object):
    '''Context Management class used to create config files'''

    class CvarContextManager(object):
        '''
        Context Management class used to create variables within config files
        '''

        def __init__(self, cvarname, notify, config):
            '''Called when the class is first initialized'''

            # Create the cvar's attributes as their base values
            self.cvarname = cvarname
            self.name = None
            self.description = ListDescription(config)
            self.instructions = ListInstructions(config)
            self.notes = ListNotes(config)
            self.extra = ListManagement(config)
            self.examples = ListExamples(config)
            self.options = ListOptions(config)
            self.default = None
            self.text = None
            self.notify = notify

        def __enter__(self):
            '''Returns the class instance to use for Context Management'''

            # Return the class
            return self

        def __exit__(self, exc_type, exc_value, _traceback):
            '''Verifies that certain attributes have values on exit'''

            if _traceback:
                es.dbgmsg(0, _traceback)
                return False

            # Does the cvar have a name value?
            if self.name is None:

                # Raise an error
                raise NameError

            # Does the cvar have a default value?
            if self.default is None:

                # Raise an error
                raise NameError

            # Does the cvar have a text value?
            if self.text is None:

                # Raise an error
                raise NameError

            return True

    def __init__(self, filepath):
        '''Called when the class is first initialized'''

        # Split the given file path.
        config_path = path(filepath).splitpath()

        # Get the first part of the path
        config_type = config_path[0]

        # Set the filename of the cfg file
        self.filename = config_path[1] + '.cfg'

        # Is the path from an included or custom addon?
        if config_type in ('included', 'custom'):

            # Get the name of the addon
            self.name = ' '.join(config_path[1].split('_')).capitalize()

            # Set the description to use
            self.description = ('This file defines GunGame '
                + config_type.capitalize() + ' Addon settings.')

            # Set the path within ../cfg/gungame51/ for the .cfg file
            self.cfgpath = config_type + '_addon_configs/' + self.filename

        # Is this from the core of GunGame?
        else:

            # Set name to None to be set later by the _config.py file itself
            self.name = None

            # Set desc to None to be set later by the _config.py file itself
            self.description = None

            # Set the path within ../cfg/gungame51/ for the .cfg file
            self.cfgpath = self.filename

        # Set the path to the .cfg file
        self.filepath = base_config_path.joinpath(self.cfgpath)

    def __enter__(self):
        '''Returns the class instance to use for Context Management'''

        # Get the AddonCFG instance for the .cfg file
        self.config = AddonCFG(self.filepath)

        # Add the AddonCFG instance to config_files
        ConfigManager()._config_files[self.filename[:~3]] = self.config

        # Create the list of sections to add cvars and text to
        self.sections = list()

        # Return the instance
        return self

    def cfg_cvar(self, cvarname):
        '''Used to create cvars and their text for the .cfg file'''

        # Set "notify" to False
        notify = False

        # Is this cvar the name of the file?
        # Used for auto adding the "notify" flag for included/custom addons
        if cvarname == self.filename[:~3]:

            # Set the "notify" flag to True
            notify = True

        # Get the CvarContextManager instance for the current cvar
        section = self.CvarContextManager(cvarname, notify, self.config)

        # Add the CvarContextManager instance to the list of sections
        self.sections.append(section)
        return section

    def cfg_section(self, section_name):
        '''Used to create separated sections within the .cfg file'''

        # Add the new section name to the list of sections
        self.sections.append(section_name.upper())

    def __exit__(self, exc_type, exc_value, _traceback):
        '''Verifies that there is a description and creates the .cfg file'''

        if _traceback:
            es.dbgmsg(0, _traceback)
            return False

        # Does the .cfg file have a description
        if self.description is None:

            # Raise an error
            raise NameError

        # Create the first line of the header
        self.config.text('*' * 76)

        # Is there nothing to add to the filename in the header?
        if self.name is None:

            # Set the topline to be just the filename
            topline = self.filename

        # Is there a name that needs to be added to the filename in the header?
        else:

            # Set the topline to be the filename and the name
            topline = self.filename + ' -- ' + self.name

        # Add the topline to the header
        self.config.text('*' + topline.center(74) + '*')

        # Add a blank line to the header
        self.config.text('*' + ' ' * 74 + '*')

        # Add the description to the header
        self.config.text('*' + self.description.center(74) + '*')

        # Add a blank line to the header
        self.config.text('*' + ' ' * 74 + '*')

        # Add the note lines to the header
        self.config.text('*' +
            'Note: Any alteration of this file requires a'.center(74) + '*')
        self.config.text('*' +
            'server restart or a reload of GunGame.'.center(74) + '*')

        # Add the last line of the header
        self.config.text('*' * 76)

        # Loop through all sections to add to the .cfg file
        for section in self.sections:

            # Add a blank line before each section
            self.config.text('')

            # Is the current section just text?
            if isinstance(section, str):

                # Add a blank line for separation
                self.config.text('')

                # Start the section header
                self.config.text('+' * 76)

                # Add the section header name
                self.config.text('|' + section.center(74) + '|')

                # End the section header
                self.config.text('+' * 76)

                # Add a blank line for separation
                self.config.text('')

            # Is the section for a cvar?
            else:

                # Start the cvar section header
                self.config.text('=' * 76)

                # Add the section name
                self.config.text('>> ' + section.name)

                # End the cvar section header
                self.config.text('=' * 76)

                # Print the description
                section.description.print_to_text()

                # Print the instructions
                section.instructions.print_to_text()

                # Print the notes
                section.notes.print_to_text()

                # Print any extra text
                section.extra.print_to_text()

                # Print the examples
                section.examples.print_to_text()

                # Print the options
                section.options.print_to_text()

                # Is the default value a string?
                if isinstance(section.default, str):

                    # Add "" around the value when printing the default
                    self.config.text('Default Value: "' +
                        str(section.default) + '"')

                # Is the default value not a string?
                else:

                    # Add the default value section
                    self.config.text('Default Value: ' + str(section.default))

                # Create the ServerVar instance for the cvar
                current = self.config.cvar(
                    section.cvarname, section.default, section.text)

                # Is the cvar supposed to be set to notify?
                if section.notify:

                    # Add the notify flag
                    current.addFlag('notify')

        # Print message that the file has been created
        es.dbgmsg(0, '\t' + self.cfgpath)

        # Write the .cfg file
        self.config.write()

        return True


class ConfigTypeDictionary(dict):
    def __getitem__(self, item):
        if item in self:
            return super(ConfigTypeDictionary, self).__getitem__(item)
        values = self[item] = get_configs_by_type(item)
        return values

_config_types = ConfigTypeDictionary()


# =============================================================================
# >> FUNCTIONS
# =============================================================================
def get_configs_by_type(name):
    cfg_list = []
    if not name in ('main', 'included', 'custom'):
        raise ValueError('"%s" is not a valid config type' % name)
    if name == 'main':
        cfgpaths = path(__file__).parent.joinpath('files')
    else:
        cfgpaths = path(
            path(__file__).parent.rsplit('core')[0]).joinpath('scripts', name)
    for cfgpath in cfgpaths.walkfiles('*_config.py'):
        cfg_list.append(cfgpath)
    return cfg_list


def get_config_list(cfg_type=None):
    if cfg_type is None:
        cfg_list = []
        for each_type in ('main', 'included', 'custom'):
            cfg_list.extend(
                [item.namebase for item in _config_types[each_type]])
        return cfg_list
    if not cfg_type in ('main', 'included', 'custom'):
        raise ValueError('"%s" is not a valid config type' % name)
    return [item.namebase for item in _config_types[cfg_type]]


def generate_header(config):
    '''
    Generates a generic header based off of the addon name.
    '''
    config.text('*' * 76)

    # Retrieve the config path
    cfgPath = config.cfgpath

    # Get the addon name from the config path
    addon = cfgPath.split('/')[len(cfgPath.split('/')) - 1].replace('.cfg', '')

    # Split the name via underscores
    list_title = str(addon).split('_')

    # Format the addon title
    addonTitle = '%s.cfg --' % str(addon)
    for index in range(1, len(list_title)):
        addonTitle += ' %s' % list_title[index].title()
    addonTitle += ' Configuration'

    config.text('*' + addonTitle.center(74) + '*')
    config.text('*' + ' ' * 74 + '*')
    config.text('*' + 'This file defines GunGame Addon settings.'.center(74) +
                '*')
    config.text('*' + ' ' * 74 + '*')
    config.text('*' +
                'Note: Any alteration of this file requires a'.center(74) +
                '*')
    config.text('*' + 'server restart or a reload of GunGame.'.center(74) +
                '*')
    config.text('*' * 76)
    config.text('')
    config.text('')
