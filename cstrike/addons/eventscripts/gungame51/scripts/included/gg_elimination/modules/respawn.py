# ../scripts/included/gg_elimination/modules/respawn.py

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
from es import exists
from es import getplayername
from es import getplayerteam
from es import getuserid
#   Gamethread
from gamethread import cancelDelayed
from gamethread import delayedname

# GunGame Imports
#   Modules
from gungame51.modules.active import RoundInfo
#   Players
from gungame51.core.players.shortcuts import Player
#   Messaging
from gungame51.core.messaging.shortcuts import saytext2


# =============================================================================
# >> CLASSES
# =============================================================================
class _RespawnPlayers(list):
    '''Class used to store players that need to respawn'''

    def append(self, item):
        '''Appends a list of userids to the respawn list
            and removes the list after 1 second'''

        # Is the round active?
        if not RoundInfo.active:

            # If not, do not add the list to the respawn list
            return

        # Add the list to the respawn list
        super(_RespawnPlayers, self).append(item)

        # Remove the list from the respawn list after 1 second
        delayedname(1, 'gg_elimination_respawn', self.remove, item)

    def remove(self, item):
        '''Removes a list of userids from the respawn list
            and spawns the players if necessary'''

        # Create a list to store names of players being respawned
        players = list()

        # Loop through all userids in the current list
        for userid in item:

            # Does the current userid exist on the server?
            if not exists('userid', userid):

                # If not, do not respawn them
                continue

            # Is the player still on a team?
            if getplayerteam(userid) < 2:

                # If not, do not respawn them
                continue

            # Respawn the player
            Player(userid).respawn()

            # Add the player's name to the list of names
            players.append(getplayername(userid))

        # Are any players being respawned?
        if players:

            # Get the first player's index
            index = Player(getuserid(players[0])).index

            # Send a message about all the players being respawned
            saytext2('#human', index, 'RespawningPlayer',
                {'player': '\x01, \x03'.join(players)}, True)

        # Remove the list from the respawn list
        super(_RespawnPlayers, self).remove(item)

    def clear(self):
        '''Clears the list and stops any active delay'''

        # Cancel the delay (if one exists)
        cancelDelayed('gg_elimination_respawn')

        # Clear the list
        self[:] = list()

# Get the _RespawnPlayers instance
respawn_players = _RespawnPlayers()
