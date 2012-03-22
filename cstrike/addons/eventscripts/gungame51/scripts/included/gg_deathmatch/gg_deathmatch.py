# ../scripts/included/gg_deathmatch/gg_deathmatch.py

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
from gungame51.modules.active import RoundInfo
from gungame51.modules.backups import VariableBackups
#   Addons
from gungame51.core.addons.shortcuts import AddonInfo

# Script Imports
from modules.dictionary import players


# =============================================================================
# >> ADDON REGISTRATION/INFORMATION
# =============================================================================
info = AddonInfo()
info.name = 'gg_deathmatch'
info.title = 'GG Deathmatch'
info.author = 'GG Dev Team'
info.version = get_version('gg_deathmatch')
info.requires = ['gg_dead_strip', 'gg_dissolver']
info.conflicts = ['gg_elimination', 'gg_teamplay', 'gg_teamwork']
info.translations = ['gg_deathmatch']


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# ServerVar instances
mp_freezetime = es.ServerVar('mp_freezetime')
mp_roundtime = es.ServerVar('mp_roundtime')


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    '''Called when DeathMatch is loaded'''

    # Store the freezetime and roundtime values on load
    VariableBackups['mp_freezetime'].add(info.name)
    VariableBackups['mp_roundtime'].add(info.name)

    # Set freezetime and roundtime
    mp_freezetime.set('0')
    mp_roundtime.set('9')

    # Register the joinclass filter
    es.addons.registerClientCommandFilter(joinclass_filter)

    # Loop through all players on the server
    for userid in es.getUseridList():

        # Check to see if the player needs spawned
        players[userid].dm_loaded()


def unload():
    '''Called when DeathMatch is unloaded'''

    # Reset freezetime and roundtime
    VariableBackups['mp_freezetime'].remove(info.name)
    VariableBackups['mp_roundtime'].remove(info.name)

    # Unregister the joinclass filter
    es.addons.unregisterClientCommandFilter(joinclass_filter)

    # Clear the players dictionary
    players.clear()


# =============================================================================
# >> REGISTERED CALLBACKS
# =============================================================================
def joinclass_filter(userid, args):
    '''Checks to see if the player needs spawned'''

    # Check if the player needs spawned
    return players[userid].check_join_team(args)


# =============================================================================
# >> GAME EVENTS
# =============================================================================
def es_map_start(event_var):
    '''Called each time a new map is loaded'''

    # Clear the players dictionary
    players.clear()


def gg_start(event_var):
    '''Called everytime a GunGame match starts'''

    # Set mp_freezetime to 0 to make compatible with Warmup Round
    mp_freezetime.set(0)


def gg_win(event_var):
    '''Called when someone wins the match'''

    # Clear the players dictionary
    players.clear()


def player_disconnect(event_var):
    '''Called when a player disconnects from the server'''

    # Remove the player from the players dictionary
    del players[event_var['userid']]


def player_death(event_var):
    '''Called when a player dies'''

    # Is the round active?
    if RoundInfo.active:

        # Start the player's repeat
        players[event_var['userid']].start_repeat()
