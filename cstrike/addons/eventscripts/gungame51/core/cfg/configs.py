# ../core/cfg/context.py

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
# ES
import es
#   Cfglib
from cfglib import AddonCFG

# GunGame Imports
#   Cfg
from cvars import CvarContextManager
from manager import ConfigManager


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
base_config_path = path(
    path(__file__).parent.rsplit('addons', 1)[0]).joinpath('cfg/gungame51')


# =============================================================================
# >> CLASSES
# =============================================================================
class ConfigContextManager(object):
    '''Context Management class used to create config files'''

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

            # Set name to None to be set later by the *_config.py file itself
            self.name = None

            # Set desc to None to be set later by the *_config.py file itself
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
        section = CvarContextManager(cvarname, notify, self.config)

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

        # Was an error encountered?
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
