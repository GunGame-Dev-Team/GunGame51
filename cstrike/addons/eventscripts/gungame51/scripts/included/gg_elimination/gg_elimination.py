# ../scripts/included/gg_elimination/gg_elimination.py

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
import es

# GunGame Imports
from gungame51.core import get_version
#   Modules
from gungame51.modules.active import ActiveInfo
#   Addons
from gungame51.core.addons.shortcuts import AddonInfo
#   Messaging
from gungame51.core.messaging.shortcuts import msg
#   Players
from gungame51.core.players.shortcuts import Player

# Script Imports
from modules.dictionary import players
from modules.respawn import respawn_players


# =============================================================================
# >> ADDON REGISTRATION/INFORMATION
# =============================================================================
info = AddonInfo()
info.name = 'gg_elimination'
info.title = 'GG Elimination'
info.author = 'GG Dev Team'
info.version = get_version(info.name)
info.requires = ['gg_dead_strip', 'gg_dissolver']
info.conflicts = ['gg_deathmatch']
info.translations = [info.name]


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    '''Called when Elimination is loaded'''

    # Register the joinclass/jointeam filter
    es.addons.registerClientCommandFilter(join_filter)


def unload():
    '''Called when Elimination is unloaded'''

    # Unegister the joinclass/jointeam filter
    es.addons.unregisterClientCommandFilter(join_filter)


# =============================================================================
# >> REGISTERED CALLBACKS
# =============================================================================
def join_filter(userid, args):
    '''Checks to see if the player needs spawned'''

    # Is the command being used "joinclass"?
    if len(args) and args[0].lower() == 'joinclass':

        # Check if the player needs to be spawned
        players[userid].check_spawn()

    # Always return True so that the command runs
    return True


# =============================================================================
# >> GAME EVENTS
# =============================================================================
def es_map_start(event_var):
    '''Called every map start'''

    # Clear the player dictionary
    players.clear()


def round_start(event_var):
    '''Called at the start of every round'''

    # Send a message about Elimination running
    msg('#human', 'RoundInfo', prefix=True)


def round_end(event_var):
    '''Called at the end of every round'''

    # Clear the respawn list
    respawn_players.clear()

    # Clear the player dictionary
    players.clear()


def player_spawn(event_var):
    '''Called any time a player spawns'''

    # Is the player on a team?
    if int(event_var['es_userteam']) < 2:

        # If not, return
        return

    # Create a Player instance for the player
    players[int(event_var['userid'])]


def player_death(event_var):
    '''Called when a player dies'''

    # Is the round active?
    if not ActiveInfo.round:

        # If not, simply return
        return

    # Get the victim's userid
    victim = int(event_var['userid'])

    # Get the attacker's userid
    attacker = int(event_var['attacker'])

    # Was this a suicide?
    if attacker in (victim, 0):

        # If so, send the suicide message to the victim
        players[victim].auto_respawn('SuicideAutoRespawn')

    # Was this a team kill?
    elif event_var['es_userteam'] == event_var['es_attackerteam']:

        # If so, send the team kill message to the victim
        players[victim].auto_respawn('TeamKillAutoRespawn')

    # Was this a good kill?
    else:

        # Add the victim to the attacker's eliminated set
        players[attacker].eliminated.add(victim)

        # Send the victim a message about respawning when their attacker dies
        Player(victim).saytext2(
            players[attacker].gg_player.index, 'RespawnWhenAttackerDies',
            {'attacker': event_var['es_attackername']}, True)

    # Respawn all players that had been eliminated by the victim
    players[victim].eliminated.clear()


def player_disconnect(event_var):
    '''Called when a player disconnects from the server'''

    # Get the player's userid
    userid = int(event_var['userid'])

    # Did the player eliminate any other players?
    if not userid in players:

        # If not, simply return
        return

    # Respawn all players that had been eliminated by the disconnecting player
    players[userid].eliminated.clear()
