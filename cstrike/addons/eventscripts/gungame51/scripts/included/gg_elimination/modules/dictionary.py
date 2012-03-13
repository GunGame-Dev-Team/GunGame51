# ../scripts/included/gg_elimination/modules/dictionary.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# EventScripts Imports
#   Gamethread
from gamethread import cancelDelayed
#   Playerlib
from playerlib import getPlayer

# Script Imports
from player import Player


# =============================================================================
# >> CLASSES
# =============================================================================
class _DictionaryOfPlayers(dict):
    '''Class that stores Player instances'''

    def __getitem__(self, userid):
        '''Returns the Player instance for the given userid'''

        # Typecast the userid
        userid = int(userid)

        # Is the userid already a member of the dictionary?
        if userid in self:

            # Return the instance
            return super(_DictionaryOfPlayers, self).__getitem__(userid)

        # Get the player's uniqueid
        uniqueid = getPlayer(userid).uniqueid(True)

        # Loop through all players in the dictionary
        for player in list(self):

            # Does the current player have the
            # same uniqueid of the given userid?
            if self[player].gg_player.steamid != uniqueid:

                # If not, continue to the next player
                continue

            # Get a new instance of Player for the player
            value = self[userid] = Player(userid)

            # Set the player's reconnect attribute since they have a new userid
            value.reconnect = True

            # Delete the old instance
            del self[player]

            # Return the current instance
            return value

        # Get an instance of Player for the userid
        value = self[userid] = Player(userid)

        # Return the instance
        return value

    def clear(self):
        '''Method used to clear the dictionary and cancel all player delays'''

        # Loop through all players in the dictionary
        for userid in self:

            # Cancel the player's delay (if it exists)
            cancelDelayed('gg_elimination_respawn_%s' % userid)

        # Clear the dictionary
        super(_DictionaryOfPlayers, self).clear()

# Get the _DictionaryOfPlayers instance
players = _DictionaryOfPlayers()
