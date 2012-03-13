# ../scripts/included/gg_elimination/modules/eliminated.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# Script Imports
from respawn import respawn_players


# =============================================================================
# >> CLASSES
# =============================================================================
class EliminatedPlayers(set):
    '''Class used to store players that were eliminated by an individual player
        and set the list of players to respawn when the player has died'''

    def clear(self):
        '''Clears the player's set of eliminated players
            and sets the eliminated players to respawn'''

        # Add the eliminated players to the respawn list
        respawn_players.append(list(self))

        # Clear the set
        super(EliminatedPlayers, self).clear()
