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

        # Create the resource file keygroup
        res = KeyValues(name=self.name)

        # Loop through each ESEvent instance
        for event in events:
            # Retrieve the event name
            event_name = event().get_event_name()

            # Add the event to the keygroup as a keyvalue
            res[event_name] = KeyValues(name=event_name)

            # Create a placeholder for the event description since a value is
            # required to generate the brackets in KeyValues
            if not event._fields:
                res[event_name]["eventlib_fake"] = 0
                continue

            # Retrieve ESEventVariable fields (should be the only items stored)
            for name, field in event._fields.items():
                # Add event variable and data key to the event
                res[event_name][name] = field.data_key

        # Save the keygroup to disk
        res.save(self.path)

        # Open file to add descriptions and remove temporary values
        self._clean_fakes()

        # Add comments
        ResourceFileParser(self).add_comments(events)

    def _clean_fakes(self):
        with open(self.path, 'r') as f:
            lines = f.readlines()

        lines = [x for x in lines if not '"eventlib_fake"' in x]

        with open(self.path, 'w') as f:
            f.writelines(lines)

    def to_dict(self):
        """Converts a resource file to a python dictionary which contains the
        event names as keys and a sub-dictionary containing the event variables
        as keys, and the data keys as values.

        Note:
            * The resource file must exist as a saved keygroup.
        """
        if not self.path.exists():
            raise ESEventError('Resource file (%s) does not ' % self.path +
                               'exist!')

        # Set up the dictionary that will be returned
        return_dict = {}

        # Retrieve the keygroup
        res = KeyValues(filename=self.path)

        for event in res:
            return_dict[str(event)] = {}

            for ev in res[event]:
                # Prints the event variable and data key
                return_dict[str(event)][str(ev)] = str(res[event][ev])

        return return_dict

    def get_events(self):
        """Returns a list of events found in the resource file.

        Note:
            * The resource file must exist as a saved keygroup

        """
        if not self.path.exists():
            raise ESEventError('Resource file (%s) does not ' % self.path +
                               'exist!')

        return KeyValues(filename=self.path).keys()


class ResourceFileParser(object):
    def __init__(self, path_to_res):
        self.path = str(path_to_res)
        self.opener = '{'
        self.closer = '}'
        self.comment = '\t\t// '

    def find_event_lines(self, event):
        event = str(event)

        with open(str(self.path), 'r') as f:
            lines = [x.strip() for x in f.readlines()]

        try:
            for line in lines:
                if line.startswith('"%s"' % event):
                    break

            start_index = lines.index(line)
            if lines[start_index + 1] == self.opener:
                for index in xrange(start_index, len(lines)):
                    if lines[index] == self.closer:
                        end_index = index
                        break
        except:
            raise ESEventError('Unable to find event "%s" in ' % event_name +
                               'resource file "%s"' % self.path)

        return (start_index, (start_index + 2, end_index))

    def add_comments(self, events):
        for event in events:
            event_lines = self.find_event_lines(event().get_event_name())
            event_line = event_lines[0]
            ev_start = event_lines[1][0]
            ev_end = event_lines[1][1]

            # Retrieve all lines in the resource file
            with open(self.path, 'r') as f:
                lines = f.readlines()

            # Modify the lines
            if event.__doc__:
                # Format the docstring
                doc = ' '.join([x.strip() for x in event.__doc__.split('\n') \
                                if x.strip()])

                # Retrieve the line
                ln = lines[event_line]

                # Make sure the line does not already have a comment
                if not self.comment in ln:
                    lines[event_line] = ln.replace('\n', '%s%s\n' % (
                                                   self.comment, doc))

            # Retrieve the max length of lines for aligning comments
            if event._fields:
                max_length = max([len(lines[index].replace('\t',
                             '')) for index in xrange(ev_start, ev_end)])

            # Loop through each event variable and add the commment
            for name, field in event._fields.items():
                comment = event._fields[name].comment
                if comment:
                    for index in xrange(ev_start, ev_end):
                        if lines[index].strip().startswith('"%s"' % name):
                            ln = lines[index]
                            if self.comment in ln:
                                break

                            # Align the comments for the event variables
                            if [len(x.strip()) % 8 for x in ln.split(
                                '\t') if x][1]:
                                ln = '%s\t\n' % (ln.rstrip())

                            # Add the comment
                            lines[index] = ln.replace('\n',
                                                      '%s%s\n' % (self.comment,
                                                      comment))

            # Write the new lines to the resource file
            with open(self.path, 'w') as f:
                f.writelines(lines)
