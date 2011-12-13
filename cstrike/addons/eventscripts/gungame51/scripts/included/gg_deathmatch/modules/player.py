# ../scripts/included/gg_deathmatch/modules/player.py

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
from es import isbot

# SPE Tools Imports
#   Player
from spe.tools.player import SPEPlayer

# GunGame Imports
#   Players
from gungame51.core.players.shortcuts import Player

# Script Imports
from countdown import PlayerCountdown


# =============================================================================
# >> CLASSES
# =============================================================================
class BasePlayer(PlayerCountdown):
    '''Class used to interact with a specific player'''

    def __init__(self, userid):
        '''Called when the class is first initialized'''

        # Store the player's base attributes
        self.userid = userid
        self.gg_player = Player(self.userid)
        self.spe_player = SPEPlayer(self.userid)
        self.isbot = isbot(self.userid)

    def dm_loaded(self):
        '''Called when DeathMatch is first loaded'''

        # Is the player alive?
        if not self.spe_player.isdead:

            # No need to spawn the player
            return

        # Is the player a spectator?
        if self.spe_player.team < 2:

            # No need to spawn the player
            return

        # Start the player's repeat
        self.start_repeat()

    def send_hudhint(self, message, tokens={}):
        '''Checks if a player is a bot, and sends a hudhint if not'''

        # Is the player a bot?
        if not self.isbot:

            # If not, send the player a hudhint message
            self.gg_player.hudhint(message, tokens)

    def check_join_team(self, args):
        '''Checks to see if the player needs spawned when joining a team'''

        # Does the command used have arguments?
        if not len(args) > 1:

            # If not, return
            return True

        # Is the player joining spectators?
        if args[0].lower() == 'jointeam' and int(args[1]) == 1:

            # Is the player's repeat active?
            if self.repeat.status != 1:

                # Stop the player's repeat
                self.stop_repeat()

                # Send a message to the player that they will not be respawned
                self.send_hudhint('RespawnCountdown_CancelTeam')

            # No need to go further
            return True

        # Is the player joining a class?
        if args[0].lower() == 'joinclass':

            # Start the player's repeat
            self.start_repeat()

        # Finally, return
        return True
