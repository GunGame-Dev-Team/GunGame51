# ../addons/eventscripts/gungame51/scripts/included/gg_retry_punish/gg_retry_punish.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# Eventscripts Imports
import es

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.players.shortcuts import Player

# =============================================================================
# >> ADDON REGISTRATION/INFORMATION
# =============================================================================
info = AddonInfo()
info.name = 'gg_retry_punish'
info.title = 'GG Retry Punish' 
info.author = 'GG Dev Team' 
info.version = "5.1.%s" %"$Rev$".split('$Rev: ')[1].split()[0]

# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
dict_savedLevels = {}

# Get the es.ServerVar() instance of "gg_retry_punish"
gg_retry_punish = es.ServerVar('gg_retry_punish')

# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    es.dbgmsg(0, 'Loaded: %s' % info.name)

def unload():
    # Clear out the dictionary on unload
    dict_savedLevels.clear()

    es.dbgmsg(0, 'Unloaded: %s' % info.name)

# =============================================================================
# >> GAME EVENTS
# =============================================================================
def es_map_start(event_var):
    # Clear our the dictionary on es_map_start
    dict_savedLevels.clear()

def player_activate(event_var):
    # Get the Player() object
    ggPlayer = Player(event_var['userid'])

    # Get the player's uniqueid
    steamid = ggPlayer.steamid

    # We don't want this to happen for BOTs
    if 'BOT' in steamid:
        return

    # Reconnecting?
    if not steamid in dict_savedLevels:
        return

    # Reset level
    ggPlayer.level = dict_savedLevels[steamid]

    # Delete the saved level
    del dict_savedLevels[steamid]

def player_disconnect(event_var):
    # Get the Player() object
    # Players may disconnect before activating, causing an error
    try:
        ggPlayer = Player(event_var['userid'])
    except ValueError:
        return

    # Get the player's uniqueid
    steamid = ggPlayer.steamid

    # If the steamid is "None", return
    if not steamid:
        return

    # Don't save level
    if 'BOT' in steamid:
        return

    # Set reconnect level
    reconnectLevel = ggPlayer.level - int(gg_retry_punish)

    if reconnectLevel > 0:
        dict_savedLevels[steamid] = reconnectLevel
    else:
        dict_savedLevels[steamid] = 1

def gg_win(event_var):
    # Clear our the dictionary on gg_win
    dict_savedLevels.clear()