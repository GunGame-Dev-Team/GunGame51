# ../addons/eventscripts/gungame/scripts/included/gg_retry_punish/gg_retry_punish.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
# Python Imports


# Eventscripts Imports
import es

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.players.shortcuts import Player

# ============================================================================
# >> ADDON REGISTRATION/INFORMATION
# ============================================================================
info = AddonInfo()
info.name = 'gg_retry_punish'
info.title = 'GG Retry Punish' 
info.author = 'GG Dev Team' 
info.version = '0.1'

# ============================================================================
# >> GLOBAL VARIABLES
# ============================================================================
dict_savedLevels = {}

# Get the es.ServerVar() instance of "gg_retry_punish"
gg_retry_punish = es.ServerVar('gg_retry_punish')

# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    es.dbgmsg(0, 'Loaded: %s' % info.name)

def unload():
    # Clear out the dictionary on unload
    dict_savedLevels.clear()

    es.dbgmsg(0, 'Unloaded: %s' % info.name)

# ============================================================================
# >> GAME EVENTS
# ============================================================================
def es_map_start(event_var):
    # Clear our the dictionary on es_map_start
    dict_savedLevels.clear()

def player_activate(event_var):
    userid = int(event_var['userid'])

    # Get the player's uniqueid
    steamid = Player(userid).steamid

    # We don't want this to happen for BOTs
    if 'BOT' in steamid:
        return

    # Reconnecting?
    if not steamid in dict_savedLevels:
        return

    # Reset level
    Player(userid).level = dict_savedLevels[steamid]

    # Delete the saved level
    del dict_savedLevels[steamid]

def player_disconnect(event_var):
    userid = int(event_var['userid'])

    # Get the player's uniqueid
    steamid = Player(userid).steamid

    # Don't save level
    if 'BOT' in steamid:
        return

    # Set reconnect level
    reconnectLevel = Player(userid).level - int(gg_retry_punish)

    if reconnectLevel > 0:
        dict_savedLevels[steamid] = reconnectLevel
    else:
        dict_savedLevels[steamid] = 1

def gg_win(event_var):
    # Clear our the dictionary on gg_win
    dict_savedLevels.clear()