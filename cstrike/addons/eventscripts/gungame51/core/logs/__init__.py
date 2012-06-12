# ../core/logs/__init__.py

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

# EventScripts Imports
#   Gamethread
from gamethread import delayedname

# GunGame Imports
from gungame51.core import get_game_dir
from gungame51.core import GunGameInfo
#   Logs
from header import _HeaderManager
from dictionary import stored_errors
from errors import _TracebackManager


# =============================================================================
# >> CLASSES
# =============================================================================
class _LogManager(_HeaderManager, _TracebackManager):
    '''Class used to manage GunGame error logging'''

    def __init__(self):
        '''Called when the class instance is initialized'''

        # Store the path instance of the log file
        self.filepath = get_game_dir(
            'cfg/gungame51/logs/GunGame%s_Log.txt' %
            '_'.join(GunGameInfo.version.split('.')))

        # Set file_created to False until it is created
        self.file_created = False

    def initialize_logging(self):
        '''Method used to initialize logging on load'''

        # Hook the exceptions
        self.hook_excepter()

        # Delay a few seconds to create the log file
        delayedname(3.5, 'gg_logging_main', self.create_log_file)

    def clean_logging(self):
        '''Method used to clean up logging on unload'''

        # Unhook the exceptions
        self.unhook_excepter()

        # Clear the dictionary
        stored_errors.clear()

    def create_log_file(self):
        '''Creates a log file, if necessary, and
            parses the current one if it already exists'''

        # Does the log file already exist?
        if self.filepath.isfile():

            # Have any variables changed since the last file was updated?
            if self.header != self.old_header:

                # Get the new name for the old error log
                old_filename = self.get_filename_for_old_file()

                # Rename the old error log
                self.filepath.rename(old_filename)

                # Create the new error log file
                self.create_file()

            # Is the old file being used?
            else:

                # Parse the old file to add any errors to the dictionary
                self.parse_old_errors()

        # Does a log file not exist for the current version?
        else:

            # Create the new log file
            self.create_file()

        # Set file_created to True, so error logging can occur
        self.file_created = True

    def create_file(self):
        '''Method that simply creates the log file'''

        # Open the log file
        with self.filepath.open('w') as open_file:

            # Write the header to the log file
            open_file.writelines(self.header)

    def get_filename_for_old_file(self):
        '''Method used to get the new filename for an old log'''

        # Set a variable to be used to find the new filename
        old_log = 0

        # Get the basename for the new file
        new_filename_base = ('cfg/gungame51/logs/GunGame%s' %
            '_'.join(GunGameInfo.version.split('.')) + '_Log_Old[%s].txt')

        # Use a loop to determine if the file
        # exists for the current variable value
        while get_game_dir(new_filename_base % n).isfile():

            # Increase the variable by 1
            n += 1

        # Return the path instance to the new filename
        return get_game_dir(new_filename_base % n)

    def parse_old_errors(self):
        '''Method used to parse the current log file
            for errors that have already been logged'''

        # Open the log file
        with self.filepath.open() as open_file:

            # Store the log file's contents
            contents = open_file.read()

        # Loop through the errors in the log file
        for x in contents.split('\n\n\n')[1:~0]:

            # Store the attributes and traceback
            attributes, trace_back = x.split('-=' * 39 + '-\n')[1:]

            # Strip the leading \n from the traceback
            trace_back = trace_back.lstrip()

            # Store the individual attributes
            last_event, count = attributes.split(']')[:~0]

            # Get the last time this error occurred
            last_event = last_event.split(': ')[1] + ']'

            # Get the number of times this error has occurred
            count = int(count.split('[')[1])

            # Add the traceback to the dictionary
            value = stored_errors[trace_back + '\n']

            # Set the count for the traceback
            value.count = count

            # Set the last event for the traceback
            value.last_event = last_event

# Get the _LogManager instance
LogManager = _LogManager()
