# gungame/scripts/included/gg_spawnpoints.py

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
from cmdlib import registerClientCommand
from cmdlib import unregisterClientCommand

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.messaging.shortcuts import msg

# ============================================================================
# >> ADDON REGISTRATION/INFORMATION
# ============================================================================
info = AddonInfo()
info.name = 'gg_spawnpoints'
info.title = 'GG Spawnpoints' 
info.author = 'GG Dev Team' 
info.version = '0.1'
info.translations = ['gg_spawnpoints']

# ============================================================================
# >> GLOBAL VARIABLES
# ============================================================================


# ============================================================================
# >> CLASSES
# ============================================================================


# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    es.dbgmsg(0, 'Loaded: %s' % info.name)
    
    registerClientCommand('spawn_add', cmd_spawn_add, 'Adds a spawnpoint at the users location', 'ADMIN')
    registerClientCommand('spawn_remove', cmd_spawn_remove, 'Remove spawnpoint at index', 'ADMIN')
    registerClientCommand('spawn_remove_all', cmd_spawn_remove_all, 'Removes all spawn points', 'ADMIN')
    registerClientCommand('spawn_show', cmd_spawn_show, 'Toggles spawn point models on and off', 'ADMIN')
    registerClientCommand('spawn_print', cmd_spawn_print, 'Prints spawnpoints by index into the players console', 'ADMIN')
    
def unload():
    es.dbgmsg(0, 'Unloaded: %s' % info.name)
    
    unregisterClientCommand('spawn_add')
    unregisterClientCommand('spawn_remove')
    unregisterClientCommand('spawn_remove_all')
    unregisterClientCommand('spawn_show')
    unregisterClientCommand('spawn_print')

# ============================================================================
# >> GAME EVENTS
# ============================================================================


# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================

def cmd_spawn_add(userid):
    global spawnPoints
    
    # Get player info
    playerlibPlayer = playerlib.getPlayer(userid)
    playerLoc = es.getplayerlocation(userid)
    playerViewAngle = playerlibPlayer.get('viewangle')
    
    # Create spawnpoint
    addSpawnPoint(playerLoc[0], playerLoc[1], playerLoc[2], playerViewAngle[1])
    
    msg(userid, 'AddedSpawnpoint', {'index': spawnPoints.getTotalPoints()-1})

