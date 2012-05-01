# ../scripts/included/gg_map_vote/modules/maplists.py

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
#   ES
from es import ServerVar

# GunGame Imports
from gungame51.core import get_game_dir

# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
source_types = {
    1: 'mapcycle.txt',
    2: 'maplist.txt',
    3: ServerVar('gg_map_vote_file')
}


# =============================================================================
# >> CLASSES
# =============================================================================
class _DictionaryOfMapLists(dict):
    '''Class used to store all map lists when initiated'''

    def __getitem__(self, item):
        '''Override the __getitem__ method to
            store items as a _MapList instance'''

        # Does the given item need .txt added to the end?
        if item != 'maps' and not item.endswith('.txt'):

            # Add .txt to the end of the item
            item = item + '.txt'

        # Is the item already in the dictionary?
        if item in self:

            # If so, return the item
            return super(_DictionaryOfMapLists, self).__getitem__(item)

        # Get the _MapList instance of the item
        value = self[item] = _MapList(item)

        # Return the _MapList instance
        return value

    @property
    def current(self):
        '''Returns the current maplist'''

        # Get the source of the current maplist
        source = int(ServerVar('gg_map_vote_list_source'))

        # Is the source a file?
        if source in source_types:

            # Return the file's maplist
            return self[str(source_types[source])]

        # Return all maps in a list
        return self['maps']

# Get the _DictionaryOfMapLists instance
maplists = _DictionaryOfMapLists()


class _MapList(dict):
    '''
        Class used to store maps for a maplist with their min/max player values
    '''

    def __init__(self, item):
        '''Override the __init__ method to get all
            maps and their min/max player values'''

        # Is the given item just wanting "all" maps?
        if item == 'maps':

            # Get the path instance to the maps directory
            source = get_game_dir('maps')

            # Loop through all .bsp files in the maps directory
            for bsp in source.walkfiles('*.bsp'):

                # Is the file a test_ file?
                if not bsp.namebase.startswith('test_'):

                    # If not, add the map to the dictionary
                    self[bsp.namebase] = _MapPlayerMinMax(0, 0)

            # No need to go further
            return

        # Get the path instance of the given file
        source = get_game_dir(item)

        # Does the file exist?
        if not source.isfile():

            # If not, raise an error
            raise ValueError('Maplist file "%s" does not exist' % (item))

        # Get the path instance to the maps directory
        map_dir = get_game_dir('maps')

        # Open the maplist file
        with source.open() as open_file:

            # Get all lines in the file
            lines = open_file.readlines()

        # Loop through all the lines in the file
        for line in lines:

            # Strip the line
            line = line.strip()

            # Does the line contain any information?
            if not line:

                # If not, continue to the next line
                continue

            # Is the line a comment?
            if line.startswith('//'):

                # If so, continue to the next line
                continue

            # Split the line
            values = line.split()

            # Get the map on the line
            map_name = values[0]

            # Does the map exist on the server?
            if not map_dir.joinpath(map_name + '.bsp').isfile():

                # If not, continue to the next line
                continue

            # Add two zeros to the split line
            values.extend([0, 0])

            # Are there too many values in the split?
            if len(values) > 3:

                # If so, only use the first three values
                values = values[:3]

            # Use a try/except to verify that the values are correct
            try:

                # Typecast the min/max player values to integer
                values[1] = int(values[1])
                values[2] = int(values[2])

            # If the typecasting fails
            except:

                # Continue to the next line
                continue

            # Add the map to the dictionary using the min/max player values
            self[map_name] = _MapPlayerMinMax(*values[1:3])


class _MapPlayerMinMax(object):
    '''Class used to store min/max player values per map per maplist'''

    def __init__(self, min, max):
        '''Called when the class is initialized'''

        # Store the min/max player values
        self.min = min
        self.max = max
