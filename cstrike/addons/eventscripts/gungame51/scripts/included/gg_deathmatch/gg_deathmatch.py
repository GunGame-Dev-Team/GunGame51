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
#   Addons
from gungame51.core.addons.shortcuts import AddonInfo

# Script Imports
from modules.active import RoundInfo
from modules.dictionary import players


# =============================================================================
# >> ADDON REGISTRATION/INFORMATION
# =============================================================================
info = AddonInfo()
info.name = 'gg_deathmatch'
info.title = 'GG Deathmatch'
info.author = 'GG Dev Team'
info.version = "5.1.%s" % "$Rev$".split('$Rev: ')[1].split()[0]
info.requires = ['gg_dead_strip', 'gg_dissolver']
info.conflicts = ['gg_elimination', 'gg_teamplay', 'gg_teamwork']
info.translations = ['gg_deathmatch']


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# ServerVar instances
mp_freezetime = es.ServerVar('mp_freezetime')
mp_roundtime = es.ServerVar('mp_roundtime')

# Backups
mp_freezetime_backup = int(mp_freezetime)
mp_roundtime_backup = int(mp_roundtime)


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    '''Called when DeathMatch is loaded'''

    # Set freezetime and roundtime
    mp_freezetime.set('0')
    mp_roundtime.set('9')

    # Register the joinclass filter
    es.addons.registerClientCommandFilter(joinclass_filter)

    # Mark round as inactive
    RoundInfo.active = False

    # Loop through all players on the server
    for userid in es.getUseridList():

        # Check to see if the player needs spawned
        players[userid].dm_loaded()


def unload():
    '''Called when DeathMatch is unloaded'''

    # Reset freezetime and roundtime
    mp_freezetime.set(mp_freezetime_backup)
    mp_roundtime.set(mp_roundtime_backup)

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

    # Mark round as inactive
    RoundInfo.active = False

    # Clear the players dictionary
    players.clear()


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


def round_start(event_var):
    '''Called at the start of every round'''

    # Mark round as active
    RoundInfo.active = True


def round_end(event_var):
    '''Called at the end of every round'''

    # Mark round as inactive
    RoundInfo.active = False
