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

# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Store the base path to the ../cfg/gungame51/ directory
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
        '''Create a new instance of ConfigManager()
            and make sure there is only "one" instance'''

        # Is there already an instance
        if not '_the_instance' in cls.__dict__:

            # Create the instance
            cls._the_instance = object.__new__(cls)

            # Initialize the class instance variables
            cls._the_instance.__loaded__ = {}
            cls._the_instance.__cvardefaults__ = {}
            cls._the_instance._config_files = {}
            cls._the_instance.files_have_been_executed = False

        # Return the class instance
        return cls._the_instance

    def load_configs(self):
        '''Loads all "main", "included", and "custom" addon config files'''

        # Register for the server_cvar event
        es.addons.registerForEvent(self, 'server_cvar', self.server_cvar)

        self.cfg_executing = False

        # Print a message that the base cfg files
        # and the Included Addon cfg files are being loaded
        es.dbgmsg(0, langstring('Load_Configs'))

        # Loop through all base _config.py files
        for cfgfile in _config_types['main']:

            # Load the file
            self.load(cfgfile, 'main')

        # Loop through all Included Addon _config.py files
        for cfgfile in _config_types['included']:

            # Load the file
            self.load(cfgfile, 'included')

        # Print a message that the Custom Addon cfg files are being loaded
        es.dbgmsg(0, langstring('Load_CustomConfigs'))

        # Loop through all Custom Addon _config.py files
        for cfgfile in _config_types['custom']:

            # Load the file
            self.load(cfgfile, 'custom')

        # Execute all cfg files in one tick
        delayed(0, self.execute_cfg_files)

    def load(self, cfgfile, cfg_type):
        '''Loads the _config.py file and stores it's location to be executed'''

        # Get the _config.py file
        config = self._import_config(cfgfile.namebase, cfg_type)

        # Does the file have a load() function?
        if 'load' in config.__dict__:

            # Load all cvars and write the cfg file
            config.load()

        # Is the current file one of the base cfg files?
        if cfg_type == 'main':

            # If so, return
            return

        # Get the path of the _config.py file
        basepath = path(config.__dict__['__file__']).namebase[:~6]

        # Does the basepath need added to the stored paths?
        if not basepath in self._config_files:

            # Loop through all objects in the _config.py file
            for item in config.__dict__:

                # Is the object a cfglib.AddonCFG object?
                if not isinstance(config.__dict__[item], AddonCFG):

                    # If not, continue
                    continue

                # Get the AddonCFG instance
                cfg = config.__dict__[item]

                # Store the addon file's path with it's AddonCFG instance
                self._config_files[basepath] = cfg

                # Loop through all cvars in the AddonCFG instance
                for cvar, value, description in cfg.getCvars().values():

                    # Add the cvar by default value to __cvardefaults__
                    self.__cvardefaults__[cvar] = value

                # Stop looping
                return

    def execute_cfg_files(self):
        '''Executes all .cfg files on load'''

        # Allow server_cvar to be called
        self.files_have_been_executed = True

        # Let it be known that cfg files are being executed
        self.cfg_executing = True

        # After cfg files are executed, reset self.cfg_executing
        delayed(0.01, self._reset_config_execution)

        # Get a list of all valid addons
        valid_addons = get_valid_addons()

        # Loop through all stored cfg files
        for cfg in self._config_files.values():

            # Execute the cfg file
            es.mexec('gungame51' + cfg.cfgpath.rsplit('gungame51', 1)[1] + '"')

            # Loop through all cvar's for the cfg file
            for cvar, value, description in cfg.getCvars().values():

                # Is the cvar the base cvar for an included/custom addon?
                if cvar in valid_addons:

                    # Get the current value
                    value = str(es.ServerVar(cvar))

                    # Does the cvar need reloaded?
                    if value != '0':

                        # Set the value to 0 without calling server_cvar
                        es.forcevalue(cvar, 0)

                        # Set the value back to the current setting
                        es.server.queuecmd('%s %s' % (cvar, value))

    def _import_config(self, name, cfg_type):
        '''Imports a *_config.py and returns it's instance'''

        # Has the file already been imported?
        if name in self.__loaded__:

            # Return the file's instance
            return self.__loaded__[name]

        # Is the current file one of the base *_config.py files?
        if cfg_type == 'main':

            # Import the file
            self.__loaded__[name] = __import__('gungame51.core.cfg.files.%s'
                % name, globals(), locals(), [''])

        # Is the current file an included/custom addon *_config.py file?
        else:

            # Remove the trailing _config from the path to get the addon name
            addon = name.replace('_config', '')

            # Import the addon's *_config.py file
            self.__loaded__[name] = __import__('gungame51.scripts.%s.%s.%s'
                % (cfg_type, addon, name), globals(), locals(), [''])

        # Reload the file to make sure the correct instance is returned
        reload(self.__loaded__[name])

        # Return the instance
        return self.__loaded__[name]

    def _reset_config_execution(self):
        '''Resets cfg_executing after the cfg files have been exectued'''

        # Set the value back to False
        self.cfg_executing = False

    def unload_configs(self):
        '''Unloads all cfg instances when unloading gungame51'''

        # Loop through all stored cfg file instances
        for cfg in self._config_files.values():

            # Loop through all cvars in the AddonCFG instance
            for cvar, value, description in cfg.getCvars().values():

                # Set the cvar back to it's default value
                es.ServerVar(cvar).set(self.__cvardefaults__[cvar])

                # Remove the notify flag from the cvar
                es.ServerVar(cvar).removeFlag('notify')

                # Remove the cvar from the default value dictionary
                del self.__cvardefaults__[cvar]

        # Loop through all *_config.py instances
        for name in self.__loaded__.keys():

            # Reload the instance to make sure it returns correctly
            reload(self.__loaded__[name])

            # Does the instance have an unload() function?
            if 'unload' in self.__loaded__[name].__dict__:

                # Run the instance's unload function
                self.__loaded__[name].unload()

            # Remove the instance from the storage dictionary
            del self.__loaded__[name]

        # Unregister the server_cvar event
        es.addons.unregisterForEvent(self, 'server_cvar')

    def server_cvar(self, event_var):
        '''
        Handles CVARs that are loaded via GunGame's ConfigManager.
        '''

        # Have the cfg files been executed on load?
        if not self.files_have_been_executed:

            # If not, return
            return

        # Get the event variables
        cvar_name = event_var['cvarname']
        cvar_value = event_var['cvarvalue']

        # Is the cvar the name of an included/custom addon
        if cvar_name not in get_valid_addons():

            # If not, return
            return

        # Is the cvar set to a "load" value (not 0, '', or a float equal to 0)
        if (bool(str(cvar_value)) and
          False in [x == '0' for x in str(cvar_value).split('.')]):

            # Is the addon already loaded?
            if cvar_name in AddonManager().__loaded__:

                # If so, return
                return

            # Check to see if the user has tried to disable the addon, or if it
            # was executed by a config
            if self.cfg_executing and cvar_name in conflicts.keys():
                if str(self.__cvardefaults__[cvar_name]) == str(cvar_value):
                    return

            # Load the addon
            delayed(0, load, (cvar_name))

        # Unload addons with the value of 0 (including floats) or ''
        else:

            # Make sure that the addon is loaded
            if cvar_name not in AddonManager().__loaded__:
                return

            # Check to see if the user has tried to disable the addon, or if it
            # was executed by a config
            if self.cfg_executing and cvar_name in dependencies.keys():
                if str(self.__cvardefaults__[cvar_name]) == str(cvar_value):
                    return

            # Unload the addon
            delayed(0, unload, (cvar_name))


# =============================================================================
# >> LIST MANAGEMENT CLASSES
# =============================================================================
class ListManagement(list):
    '''A base list class to create .cfg files'''

    # Create the base attributes
    header = ''
    first = ''
    indent = 0

    def __init__(self, config):
        '''Create an instance of the list and store it's config file'''

        # Store the config file that the cvar is stored in
        self.config = config

    def print_to_text(self):
        '''Creates the text in the cfg file'''

        # Are there any items to be printed to the file?
        if not len(self):

            # If not, return
            return

        # Does the header need added?
        if self.header:

            # Add the header
            self.config.text(self.header)

        # Loop through all items in the list
        for section in self:

            for line in self.get_all_lines(section):

                self.config.text(line)

    def get_all_lines(self, section):
        '''Gets all lines for the given section'''

        # Is the line already less than 80 characters?
        if len(self.first + section) + self.config.indention < 80:

            # If so, simply return the section
            return [self.first + section]

        # Create a list to store the sections
        lines = []

        # Get the first line.  This is done separately since
        # the indention is different for the remaining lines
        first_line, remainder = self.get_line(self.first + section)

        # Add the first line to the list
        lines.append(first_line)

        # Use a "while" statement to get remaining lines under 80 characters
        while (len(remainder) + self.indent + self.config.indention > 80
          or '\n' in remainder):

            # Get the current line
            current_line, remainder = self.get_line(
                            ' ' * self.indent + remainder)

            # Add the current line to the list
            lines.append(current_line)

        # Add the last line to the list
        lines.append(' ' * self.indent + remainder)

        # Return the list of lines
        return lines

    def get_line(self, message):
        '''Gets the current line so that it is under 80 characters'''

        # Get the starting point to find the closest <space> to 80 characters
        start = message[:80 - self.config.indention]

        # Use a "while" statement to find the last <space> before 80 characters
        while start[~0] != ' ':

            # Move the end of the line 1 character
            # to the left until a <space> is found
            start = start[:~0]

        # Is there any remaining text in "start"?
        if not start.strip(' '):

            # Set start back to the original message
            start = str(message)

        # Is there a newline character in the start text?
        if '\n' in start:

            # If so, split the text at the newline character
            start, remainder = start.split('\n', 1)

            # Return the start and remainder
            return start.rstrip(), remainder.lstrip(' ')

        # Return the current line and the remainder
        return start[:~0], message.replace(start, '').lstrip(' ')


class ListDescription(ListManagement):
    '''Creates a list of Description lines'''

    # Create the base attributes for Description
    header = 'Description:'
    first = ' ' * 3
    indent = 6


class ListInstructions(ListManagement):
    '''Creates a list of Instruction lines'''

    # Create the base attributes for Instructions
    header = 'Instructions:'
    first = '   * '
    indent = 7


class ListNotes(ListManagement):
    '''Creates a list of Notes lines'''

    # Create the base attributes for Notes
    header = 'Notes:'
    first = '   * '
    indent = 6

    def __init__(self, config):
        self.config = config

        # Create a list of required addons and conflicting addons
        self.requires = list()
        self.conflict = list()

    def __getattribute__(self, item):
        '''Checks if printing to text, and if so,
            interject required and conflicting addons'''

        # Is the attribute "print_to_text"?
        if item == 'print_to_text':

            # Are there any required or conflicting addons?
            if self.requires or self.conflict:

                # Add the header
                self.config.text(self.header)

                # Change the header so it doesn't get added again later
                self.header = ''

                # Loop through all required addons
                for addon in self.requires:

                    # Add both lines about required addons
                    self.config.text(self.first + '"'
                        + addon + '" will automatically be enabled.')
                    self.config.text(self.first +
                        'Will not load if "' + addon + '" can not be enabled.')

                # Loop through all conflicting addons
                for addon in self.conflict:

                    # Add the conflicting addon text
                    self.config.text(self.first +
                        'Will not load with "' + addon + '" enabled.')

        # Return the attribute
        return super(ListNotes, self).__getattribute__(item)


class ListExamples(ListManagement):
    '''Creates a list of Examples lines'''

    # Create the base attributes for Examples
    header = 'Examples:'
    first = '   * '
    indent = 9


class ListOptions(ListManagement):
    '''Creates a list of Options lines'''

    # Create the base attributes for Options
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
            self.default_text = None
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
                raise ValueError('No "name" set for "' + self.cvarname + '"')

            # Does the cvar have a default value?
            if self.default is None:

                # Raise an error
                raise ValueError(
                    'No default value set for "' + self.cvarname + '"')

            # Does the cvar have a text value?
            if self.text is None:

                # Raise an error
                raise ValueError('No "text" set for "' + self.cvarname + '"')

            # Add the cvar with it's default value to ConfigManager
            ConfigManager().__cvardefaults__[self.cvarname] = self.default

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

        # Return the section
        return section

    def cfg_section(self, section_name):
        '''Used to create separated sections within the .cfg file'''

        # Add the new section name to the list of sections
        self.sections.append(section_name.upper())

    def __exit__(self, exc_type, exc_value, _traceback):
        '''Verifies that there is a description and creates the .cfg file'''

        # Was there an error encountered
        if _traceback:

            # Print the traceback
            es.dbgmsg(0, _traceback)

            # Return
            return False

        # Does the .cfg file have a description
        if self.description is None:

            # Raise an error
            raise ValueError(
                'No description set for .cfg file "' + self.filename + '"')

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

            # Is the current section just text?
            if isinstance(section, str):

                # Add 2 blank lines for separation
                self.config.text('\n')

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

                if section.name:

                    # Add a blank line for separation
                    self.config.text('')

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

                # Print any extra text
                section.extra.print_to_text()

                # Print the notes
                section.notes.print_to_text()

                # Print the examples
                section.examples.print_to_text()

                # Print the options
                section.options.print_to_text()

                # Is there default_text to print?
                if not section.default_text is None:

                    # Is the default_text a string?
                    if isinstance(section.default_text, str):

                        # Is there any text to print?
                        if section.default_text:

                            # Add the string to the cfg file
                            self.config.text(section.default_text)

                    # Is the default_text a list?
                    elif isinstance(section.default_text, list):

                        # Loop through each line in the list
                        for line in section.default_text:

                            # Add the line to the cfg file
                            self.config.text(line)

                # Is the default value a string?
                elif isinstance(section.default, str):

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

        # Write the .cfg file
        self.config.write()

        # Return
        return True


class ConfigTypeDictionary(dict):
    '''A dictionary that stores config files
        by type (main, included, and custom)'''

    def __getitem__(self, item):
        '''Override the __getitem__ method of dict
            type to return the config files by type'''

        # Is the item already in the dictionary
        if item in self:

            # Return the list of cfg files
            return super(ConfigTypeDictionary, self).__getitem__(item)

        # Add the item to the dictionary and get a list of cfg files
        values = self[item] = get_configs_by_type(item)

        # Return the list of cfg files
        return values

# Get the instance of the ConfigTypeDictionary()
_config_types = ConfigTypeDictionary()


# =============================================================================
# >> FUNCTIONS
# =============================================================================
def get_configs_by_type(name):
    '''Returns a list of cfg files by type'''

    # Is the name a correct value?
    if not name in ('main', 'included', 'custom'):

        # If not, raise an error
        raise ValueError('"%s" is not a valid config type' % name)

    # Create an empty list to add to
    cfg_list = []

    # Is the name wanting the base configs?
    if name == 'main':

        # Get the path to the base *_config.py files
        cfgpaths = path(__file__).parent.joinpath('files')

    # Is the name wanting included/custom addon configs?
    else:

        # Get the path to the *_config.py files
        cfgpaths = path(
            path(__file__).parent.rsplit('core')[0]).joinpath('scripts', name)

    # Loop through all files ending in _config.py in the directory
    for cfgpath in cfgpaths.walkfiles('*_config.py'):

        # Add the file to the list
        cfg_list.append(cfgpath)

    # Return the list
    return cfg_list


def get_config_list(cfg_type=None):
    '''Returns a list of filenames by type'''

    # Is it wanting to return "all" config files?
    if cfg_type is None:

        # Create an empty list
        cfg_list = []

        # Loop through all config types
        for each_type in ('main', 'included', 'custom'):

            # Add the config filenames to the list
            cfg_list.extend(
                [item.namebase for item in _config_types[each_type]])

        # Return the list
        return cfg_list

    # Is the name a proper cfg type?
    if not cfg_type in ('main', 'included', 'custom'):

        # If not, raise an error
        raise ValueError('"%s" is not a valid config type' % name)

    # Return a list of cfg filenames for the given type
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

ConfigManager().load_configs()
