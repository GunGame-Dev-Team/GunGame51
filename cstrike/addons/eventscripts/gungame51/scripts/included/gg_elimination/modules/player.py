# ../scripts/included/gg_elimination/modules/player.py

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
from es import getplayerteam
from es import ServerVar
#   Gamethread
from gamethread import cancelDelayed
from gamethread import delayedname
#   Playerlib
from playerlib import getPlayer

# GunGame Imports
#   Modules
from gungame51.modules.active import RoundInfo
#   Players
from gungame51.core.players.shortcuts import Player as ggPlayer

# Script Imports
from eliminated import EliminatedPlayers
from respawn import respawn_players


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
gg_elimination_spawn = ServerVar('gg_elimination_spawn')


# =============================================================================
# >> CLASSES
# =============================================================================
class Player(object):
    '''Class used to interact with a specific player'''

    def __init__(self, userid):
        '''Called when the class is first initialized'''

        # Store the player's base attributes
        self.userid = userid
        self.gg_player = ggPlayer(userid)
        self.eliminated = EliminatedPlayers()
        self.reconnect = False

    def check_spawn(self):
        '''Used to check if a player should be
            spawned when joining a round late'''

        # Should players be spawned during the mid round?
        if not int(gg_elimination_spawn):

            # If not, return
            return

        # Is the round active?
        if not RoundInfo.active:

            # If not, return
            return

        # Is the player on a team?
        if getplayerteam(self.userid) < 2:

            # If not, return
            return

        if self.reconnect:

            # If they are reconnecting, return
            return

        # Cancel the current delay (if it exists)
        cancelDelayed('gg_elimination_respawn_%s' % self.userid)

        # Add the player to the respawn list in 3 seconds
        delayedname(3,
            'gg_elimination_respawn_%s' % self.userid,
            respawn_players.append, [self.userid])

    def auto_respawn(self, message):
        '''Respawns the player in 5 seconds if suicide or team-killed'''

        # Add the player to the respawn list in 3 seconds
        delayedname(4,
            'gg_elimination_respawn_%s' % self.userid,
            respawn_players.append, [self.userid])

        # Send the player a message that they will be respawned soon
        ggPlayer(self.userid).msg(message, prefix=True)
