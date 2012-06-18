# ../scripts/included/gg_map_vote/modules/lastmaps.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# EventScripts Imports
#   ES
from es import ServerVar


# =============================================================================
# >> CLASSES
# =============================================================================
class _LastMaps(list):
    '''Class used to store the last x maps that have been played'''

    def append(self, item):
        '''Override the append method to make
            sure only to store x number of maps'''

        # Add the map to the list
        super(_LastMaps, self).append(item)

        # Get the number of maps to store
        last_maps = int(ServerVar('gg_map_vote_dont_show_last_maps'))

        # Are there too many maps being stored
        if len(self) > last_maps:

            # Remove any maps that shouldn't be stored
            self[:] = self[last_maps - 1:]

    def clear(self):
        '''Clears the last x maps list'''

        # Clear the list
        self[:] = []

# Get the _LastMaps instance
last_x_maps = _LastMaps()
