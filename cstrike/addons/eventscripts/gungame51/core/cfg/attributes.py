# ../core/cfg/attributes.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''


# =============================================================================
# >> CLASSES
# =============================================================================
class ListManagement(list):
    '''A base list class to create .cfg files'''

    # Create the base attributes
    header = ''
    first = ''
    indent = 0

    def __init__(self, config):
        '''Create an instance of the list and store its config file'''

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

            for line in self._get_all_lines(section):

                self.config.text(line)

    def _get_all_lines(self, section):
        '''Gets all lines for the given section'''

        # Is the line already less than 80 characters?
        if len(self.first + section) + self.config.indention < 80:

            # If so, simply return the section
            return [self.first + section]

        # Create a list to store the sections
        lines = []

        # Get the first line.  This is done separately since
        # the indention is different for the remaining lines
        first_line, remainder = self._get_line(self.first + section)

        # Add the first line to the list
        lines.append(first_line)

        # Use a "while" statement to get remaining lines under 80 characters
        while (len(remainder) + self.indent + self.config.indention > 80
          or '\n' in remainder):

            # Get the current line
            current_line, remainder = self._get_line(
                            ' ' * self.indent + remainder)

            # Add the current line to the list
            lines.append(current_line)

        # Add the last line to the list
        lines.append(' ' * self.indent + remainder)

        # Return the list of lines
        return lines

    def _get_line(self, message):
        '''Gets the current line so that it is under 80 characters'''

        # Get the starting point to find the closest <space> to 80 characters
        start = message[:80 - self.config.indention]

        # Use a "while" statement to find the last <space> before 80 characters
        while start[~0] != ' ' and start:

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

    def __getattribute__(self, attr):
        '''Checks if printing to text, and if so,
            interject required and conflicting addons'''

        # Is the attribute "print_to_text"?
        if attr == 'print_to_text':

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
        return super(ListNotes, self).__getattribute__(attr)


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
