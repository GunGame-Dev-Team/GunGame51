# ../addons/eventscripts/gungame51/scripts/included/gg_random_spawn/gg_random_spawn.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
#Python Imports
import os

# SPE Imports
import spe

# Eventscripts Imports
import es

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo

# ============================================================================
# >> ADDON REGISTRATION/INFORMATION
# ============================================================================
info = AddonInfo()
info.name = 'gg_random_spawn'
info.title = 'GG Random Spawn' 
info.author = 'GG Dev Team' 
info.version = '0.1'

# ============================================================================
# >> GLOBAL VARIABLES
# ============================================================================

spawnPoints = []
pointsLoaded = False
es_gamedir = es.ServerVar('eventscripts_gamedir')

# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    loadSpawnFile(str(es.ServerVar("eventscripts_currentmap")))
    es.dbgmsg(0, 'Loaded: %s' % info.name)

    userid = es.getuserid()

    # If there are no players on the server, stop here
    if not userid:
        return

    pointsLoaded = True

    if not spawnPoints:
        return

    loadRandomPoints(userid)

def unload():
    es.dbgmsg(0, 'Unloaded: %s' % info.name)

# ============================================================================
# >> GUNGAME EVENTS
# ============================================================================

def es_map_start(event_var):
    global pointsLoaded

    pointsLoaded = False
    loadSpawnFile(event_var['mapname'])

def player_activate(event_var):
    global pointsLoaded

    if pointsLoaded:
        return

    pointsLoaded = True

    if not spawnPoints:
        return

    loadRandomPoints(event_var['userid'])

# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================

def loadSpawnFile(mapName):
    global spawnPoints
    global pointsLoaded

    spawnPoints = []
    pointsLoaded = False

    # Get spawnpoint file
    spawnFile = ('%s' % str(es_gamedir).replace('\\', '/') + 
                 '/cfg/gungame51/spawnpoints/%s.txt' % mapName)

    # Does the file exist?
    if not os.path.isfile(spawnFile):
        return

    # Get spawnpoint lines
    spawnPointFile = open(spawnFile, 'r')
    fileLines = [x.strip() for x in spawnPointFile.readlines()]
    spawnPointFile.close()

    # Set up spawnpoints
    spawnPoints = [x.split(' ', 6) for x in fileLines]

def loadRandomPoints(userid):
    # Remove existing spawnpoints
    for tSpawn in es.createentitylist('info_player_terrorist'):
        es.server.cmd('es_xremove %s' % tSpawn)
    for ctSpawn in es.createentitylist('info_player_counterterrorist'):
        es.server.cmd('es_xremove %s' % ctSpawn)

    # Loop through the spawnpoints
    for spawn in spawnPoints:
        for team in ('info_player_terrorist', 'info_player_counterterrorist'):
            # Create the spawnpoint and get the index
            index = spe.getIndexOfEntity(spe.giveNamedItem(userid, team))

            # Set the spawnpoint position and rotation
            es.setindexprop(index, 'CBaseEntity.m_vecOrigin', 
                '%s,%s,%s' % (spawn[0], spawn[1], spawn[2]))
            es.setindexprop(index, 'CBaseEntity.m_angRotation', 
                '0,%s,0' % spawn[4])