# =============================================================================
# IMPORTS
# =============================================================================
# Python Imports
from __future__ import with_statement
from path import path

# EventScripts Imports
import es
from keyvalues import KeyValues

# Eventlib Imports
from exceptions import ESEventError


# =============================================================================
# GLOBAL VARIABLES/CONSTANTS
# =============================================================================
__all__ = ['ResourceFile']
DATAKEYS = {'none': None, 'bool': bool, 'byte': int, 'short': int,
            'long': float, 'float': float, 'string': str}


# =============================================================================
# CLASSES
# =============================================================================
class ResourceFile(object):
    def __init__(self, path_to_res):
        # Validate the path to the resource file
        path_to_res = path(str(path_to_res).replace('\\', '/'))
        if not path_to_res.ext == '.res':
            self.path = path(str(path_to_res) + '.res')
        else:
            self.path = path_to_res
        self.name = self.path.namebase

    def __str__(self):
        return self.path

    def declare(self):
        """Declares the resource file. Typically used when a script is
        loaded.

        """
        es.loadevents('declare', str(self))

    def load(self):
        """Loads the resource file. Typically used on map start and when a
        script is loaded.

        """
        es.loadevents(str(self))

    def declare_and_load(self):
        """Declares and loads the resource file. Typically used when a script
        is loaded.

        """
        es.loadevents('declare', str(self))
        es.loadevents(str(self))

    def write(self, events=[], overwrite=False):
        """Writes the given events to the resource file. If the overwrite
        argument is set to False and the resource file exists, the resource
        file will not be overwritten.

        """
        # Do not overwrite if the resource file exists
        if not overwrite:
            if self.path.exists():
                return

        # Create the line list to write to file
        line_list = ['"%s"\n' % self.name, '{\n']

        # Loop through each ESEvent instance
        for event in events:
            # Retrieve the event name
            event_name = event().get_event_name()

            # Retrieve the event docstring and add to the line list
            doc = event.__doc__
            if doc:
                doc = ' '.join([x.strip() for x in event.__doc__.split('\n') \
                                if x.strip()])
            line_list.append('\t%-29s%s' % ('"%s"' % event_name,
                             '// %s' % doc if doc else ''))

            # Open the event
            line_list.append('\t{')

            # Retrieve EventFields fields and order them based on creation
            fields = [(name, event._fields[name]) for name,
                      obj in event._fields.items()]
            fields.sort(lambda x, y: cmp(x[1].creation_counter,
                        y[1].creation_counter))

            # Prepare a list of field values to place on each line
            field_list = [{'n': '"%s"' % name, 'k': '"%s"' % field.data_key,
                           'c': '%s' % ('// %s' % (
                           field.comment if field.comment else ''))} for name,
                           field in fields]

            # Add the event names, data keys, and comments
            for field_dict in field_list:
                line_list.append('\t\t%(n)-25s%(k)-25s%(c)-25s' % field_dict)

            # Close the event
            line_list.append('\t}')

        # Add the closing bracket
        line_list.append('}')

        # Clean up excess spacing and add carriage returns to each line
        line_list = ['%s\n' % x.rstrip() for x in line_list]

        # Write the lines to file
        with open(self.path, 'w') as f:
            f.writelines(line_list)

    def to_dict(self):
        """Converts a resource file to a python dictionary which contains the
        event names as keys and a sub-dictionary containing the event variables
        as keys, and the data keys as values.

        """
        if not self.path.exists():
            raise ESEventError('Resource file (%s) does not ' % self.path +
                               'exist!')

        # Set up the dictionary that will be returned
        return_dict = {}

        # Retrieve the keygroup
        res = KeyValues(filename=self.path)

        # Loop through each event and retrieve its variables
        for event in res:
            return_dict[str(event)] = {}

            for ev in res[event]:
                # Prints the event variable and data key
                return_dict[str(event)][str(ev)] = str(res[event][ev])

        return return_dict

    def get_events(self):
        """Returns a list of events found in the resource file."""
        if not self.path.exists():
            raise ESEventError('Resource file (%s) does not ' % self.path +
                               'exist!')

        return KeyValues(filename=self.path).keys()
