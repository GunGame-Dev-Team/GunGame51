# ../core/logs/dictionary.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
#   Time
from time import strftime


# =============================================================================
# >> CLASSES
# =============================================================================
class _Error(object):
    '''Class used to store individual errors'''

    def __init__(self, trace_back):
        '''Called when the errors instance is initialized'''

        # Store the traceback
        self.trace_back = trace_back

        # Set the count to 0
        self.count = 0

    def __add__(self, value):
        '''Method used to add to the count and
            store the last time the error occurred'''

        # Add the value to the current count
        self.count += value

        # Get the value for the latest time the error has occurred
        self.last_event = strftime('[%m/%d/%Y @ %H:%M:%S]')

        # Return the instance itself
        return self

    def __str__(self):
        '''Method used to return a string header for the traceback'''

        # Return a formatted string for the traceback's
        # last occurrence and total occurrences
        return ('-=' * 39 + '-\n' + ('LAST EVENT: ' + self.last_event +
          ' ' * 9 + ' TOTAL OCCURENCES: [%04i]' % self.count).center(79) +
          '\n' + '-=' * 39 + '-\n\n' + self.trace_back + '\n\n')


class _ErrorDictionary(dict):
    '''Ordered Dictionary class used to store tracebacks'''

    def __init__(self):
        '''Called when the class instance is initialized'''

        # Store the order as an empty list
        self.order = list()

    def __iter__(self):
        '''Method used to iterate over the tracebacks
            in the dictionary in the proper order'''

        # Loop through the tracebacks
        for error in self.order:

            # Yield the current traceback
            yield error

    def __getitem__(self, trace_back):
        '''Override __getitem__ to make sure the
            traceback does not include userids'''

        # Store a backup for the traceback to use in case the
        # current traceback has not been added to the dictionary
        trace_back_backup = trace_back

        # Split the traceback by line
        trace_back = [line + '\n' for line in trace_back.split('\n')]

        # Remove the new-line character from the last line in the traceback
        trace_back[~0] = trace_back[~0].rstrip()

        # Store the last line in the actual traceback
        last_line = trace_back[~1]

        # Loop through all single digit numbers
        for x in xrange(10):

            # Remove the number from the last line in the traceback.
            # This is done to remove userids, so that the same error
            # will only show up once instead of for each userid.
            last_line = last_line.replace(str(x), '')

        # Set the last line as the new last line
        trace_back[~1] = last_line

        # Set the traceback back to a string
        trace_back = ''.join(trace_back)

        # Is the traceback in the dictionary?
        if trace_back in self:

            # If it is, simply return its instance
            return super(_ErrorDictionary, self).__getitem__(trace_back)

        # Add the traceback to the ordered list
        self.order.append(trace_back)

        # Get the _Error instance for the traceback
        value = self[trace_back] = _Error(trace_back_backup)

        # Return the _Error instance
        return value

    def clear(self):
        '''Override the clear method to clear the list as well'''

        # Clear the list of tracebacks
        self.order = list()

        # Clear the dictionary
        super(_ErrorDictionary, self).clear()

# Get the _ErrorDictionary instance
stored_errors = _ErrorDictionary()
