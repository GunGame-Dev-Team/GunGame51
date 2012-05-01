# ../scripts/included/gg_map_vote/modules/nominations.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''


# =============================================================================
# >> CLASSES
# =============================================================================
class NominatedMaps(list):
    '''Class used to store nominated maps for the MapVote'''

    def clear(self):
        '''Add a clear method to clear the list'''

        # Clear the list
        self[:] = []
