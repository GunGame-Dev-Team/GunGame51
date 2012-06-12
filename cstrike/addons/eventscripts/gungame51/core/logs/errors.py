# ../core/logs/errors.py

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
#   Sys
import sys
#   Traceback
from traceback import format_exception

# EventScripts Imports
#   ES
from es import dbgmsg
from es import excepter
#   Gamethread
from gamethread import cancelDelayed
from gamethread import delayedname

# GunGame Imports
#   Logs
from dictionary import stored_errors


# =============================================================================
# >> CLASSES
# =============================================================================
class _TracebackManager(object):
    '''Inherited class that is used to handle GunGame exceptions'''

    def hook_excepter(self):
        '''Method used to hook excepthook and store its old hook'''

        # Store the old hook
        self.old_excepter = sys.excepthook

        # Set the handle_exception method as the excepthook
        sys.excepthook = self.handle_exception

    def unhook_excepter(self):
        '''Method used to restore the old excepthook'''

        # Restore the old excepthook
        sys.excepthook = self.old_excepter

    def handle_exception(self, tb_type, value, trace_back, mute_console=False):
        '''Method used to handle error logging/printing for GunGame'''

        # Format the traceback
        tb = format_exception(tb_type, value, trace_back)

        # Is this a GunGame error?
        if not 'gungame51' in str(tb).lower():

            # If not, let ES handle this error
            excepter(tb_type, value, trace_back)

            # Return as this is non-GunGame related
            return

        # Loop through the lines in the traceback
        for line in xrange(len(tb)):

            # Is the line referring to a file?
            if tb[line].strip().startswith('File "'):

                # Re-format the line to shorten it
                tb[line] = ('../eventscripts' +
                  tb[line].rsplit('eventscripts', 1)[1]).replace('\\', '/')

        # Add a new-line character prior to the last line in the traceback
        tb.insert(len(tb) - 1, '\n')

        # Convert the traceback into a string
        tb = ''.join(tb)

        # Is the traceback less than 255 characters?
        if len(tb) < 255:

            # Store the traceback as a list
            db_tb = [tb]

        # Is the traceback more than or equal to 255 characters?
        else:

            # Store the traceback as a list with the extra characters stripped
            db_tb = [x.strip() for x in tb.split('\n') if x != '']

        # Add the traceback to the dictionary (if it isn't already)
        # and add 1 to the number of occurrences
        stored_errors[tb] += 1

        # Is the console supposed to be printed to?
        if not mute_console:

            # Print the error to the server's console
            dbgmsg(0, ' \n')
            dbgmsg(0, '# ' + '=' * 48)
            dbgmsg(0, '# >>' + 'GunGame 5.1 Exception Caught!'.rjust(50))
            dbgmsg(0, '# ' + '=' * 48)
            for line in db_tb:
                dbgmsg(0, line)
            dbgmsg(0, '# ' + '=' * 48)
            dbgmsg(0, ' \n')

        # Has the log file been created?
        if not self.file_created:

            # If not, delay 5 seconds before trying to add the traceback again
            delayedname(5, 'gg_logging_main',
              self.handle_exception, (tb_type, value, trace_back, True))

            # The exception is not going to be
            # written to file at this time, so return
            return

        # Cancel the current delay
        # This is done so that if multiple errors occur in
        # the same tick, the log file is only written to once
        cancelDelayed('gg_logging_write')

        # Delay 1 tick to write the error to the log file
        delayedname(0, 'gg_logging_write', self.write_to_file)

    def write_to_file(self):
        '''Method used to write the log file'''

        # Open the log file to write to it
        with self.filepath.open('w') as open_file:

            # Write the header to the log file
            open_file.writelines(self.header)

            # Loop through each error in the dictionary
            for error in stored_errors:

                # Write the error to the log file
                open_file.writelines(str(stored_errors[error]))
