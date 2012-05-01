# ../scripts/included/gg_map_vote/modules/players/rockers.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''


# =============================================================================
# >> CLASSES
# =============================================================================
class RockTheVotePlayers(set):
    '''Class used to store a set of RTV players'''

    def add(self, userid):
        '''Overwrite the add method to typecast the given userid'''

        # Typecast the userid
        userid = int(userid)

        # Add the userid to the set
        super(RockTheVotePlayers, self).add(userid)

    def discard(self, userid):
        '''Overwrite the discard method to typecast the given userid'''

        # Typecast the userid
        userid = int(userid)

        # Discard the userid from the set
        super(RockTheVotePlayers, self).discard(userid)
