# ../addons/eventscripts/gungame/scripts/included/gg_spawnpoints/gg_spawnpoints.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
# Python Imports
from os import path

# Eventscripts Imports
import es
from cmdlib import registerServerCommand
from cmdlib import unregisterServerCommand
from playerlib import getPlayer

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
filePath = es.ServerVar('eventscripts_gamedir') + '/cfg/gungame51/' + \
    'spawnpoints/' + str(es.ServerVar('eventscripts_currentmap')) + '.txt'

# ============================================================================
# >> CLASSES
# ============================================================================


# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    es.dbgmsg(0, 'Loaded: %s' % info.name)
    
    registerServerCommand('spawn_add', cmd_spawn_add, 'Adds a spawnpoint at the users location')
    registerServerCommand('spawn_remove_all', cmd_spawn_remove_all, 'Removes all spawn points')
    registerServerCommand('spawn_print', cmd_spawn_print, 'Prints spawnpoints into the server console')
    """
    registerServerCommand('spawn_remove', cmd_spawn_remove, 'Remove spawnpoint at index')
    registerServerCommand('spawn_show', cmd_spawn_show, 'Toggles spawn point models on and off')
    """
    
def unload():
    es.dbgmsg(0, 'Unloaded: %s' % info.name)
    
    unregisterServerCommand('spawn_add')
    unregisterServerCommand('spawn_remove_all')
    unregisterServerCommand('spawn_print')
    """
    unregisterServerCommand('spawn_remove')
    unregisterServerCommand('spawn_show')
    """

# ============================================================================
# >> GAME EVENTS
# ============================================================================


# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
def invalid_syntax(syntax):
    es.dbgmsg(0, 'Invalid Syntax. Use: %s' % syntax)

def cmd_spawn_add(args):
    if len(args) != 1:
        invalid_syntax('spawn_add <userid>')
        return

    userid = args[0]
    if not userid.isdigit():
        invalid_syntax('spawn_add <userid>')
        return

    if not es.exists('userid', userid):
        es.dbgmsg(0, 'Userid does not exist.')
        return

    pPlayer = getPlayer(userid)
    location = es.getplayerlocation(userid)
    angle = pPlayer.get('viewangle')

    spawnPoint = '%s %s %s %s %s %s\n' % (location[0], location[1], \
    location[2], angle[0], angle[1], angle[2])
    currentSpawnPoints = read_spawn_points()
    
    for sp in currentSpawnPoints:
        if sp.split(' ')[0:3] == spawnPoint.split(' ')[0:3]:
            es.dbgmsg(0, 'Spawnpoint already exists.')
            return

    currentSpawnPoints.append(spawnPoint)

    write_spawn_points(currentSpawnPoints)
    es.dbgmsg(0, 'SpawnPoint Added: %s' % spawnPoint.strip('\n'))

def cmd_spawn_remove_all(args):
    write_spawn_points([])

def cmd_spawn_print(args):
    for spawnPoint in read_spawn_points():
        es.dbgmsg(0, spawnPoint.strip('\n'))

def read_spawn_points():
    if not path.isfile(filePath):
        return []

    spawnPointFile = open(filePath, 'r')
    spawnPoints = spawnPointFile.readlines()
    spawnPointFile.close()

    return spawnPoints

def write_spawn_points(spawnpoints):
    spawnPointFile = open(filePath, 'w')
    spawnPointFile.writelines(spawnpoints)
    spawnPointFile.close()