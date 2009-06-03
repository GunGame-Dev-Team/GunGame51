# ../addons/eventscripts/gungame/scripts/included/gg_random_spawn/gg_random_spawn.py

'''
$Rev: 84 $
$LastChangedBy: WarrenAlpert $
$LastChangedDate: 2009-06-03 13:08:04 -0400 (Wed, 3 Jun 2009) $
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
# Eventscripts Imports
import os

# GunGame Imports
import es

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
pointsLoaded = 0

# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    es.dbgmsg(0, 'Loaded: %s' % info.name)
    
def unload():
    es.dbgmsg(0, 'Unloaded: %s' % info.name)
    
# ============================================================================
# >> GUNGAME EVENTS
# ============================================================================

def es_map_start(event_var):

    loadSpawnFile(event_var['mapname'])

def player_activate(event_var):
    global pointsLoaded
    
    if pointsLoaded:
        return
    
    pointsLoaded = 1
    
    if not spawnPoints:
        return
    
    loadRandomPoints(event_var['userid'])

# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================

def loadSpawnFire(mapname):
    global spawnPoints
    global pointsLoaded
    
    spawnPoints = []
    pointsLoaded = 0
    
    # Get spawnpoint file
    self.spawnFile = '%s/%s/%s.txt' % mapname.replace('\\', '/'), spawnPointDirectory, self.mapName)
    
    # Does the file exist?
    if not self.exists():
        return
    
    # Get spawnpoint lines
    spawnPointFile = open(self.spawnFile, 'r')
    fileLines = [x.strip() for x in spawnPointFile.readlines()]
    spawnPointFile.close()
    
    # Set up spawnpoints
    spawnPoints = [x.split(' ', 6) for x in fileLines]

def loadRandomPoints(userid):
    
    # Remove existing spawnpoints
    for tSpawn in es.createentitylist('info_player_terrorist'):
        es.server.cmd('es_xremove info_player_terrorist')
    for ctSpawn in es.createentitylist('info_player_counterterrorist'):
        es.server.cmd('es_xremove info_player_counterterrorist')
    
    # Loop through the spawnpoints
    for spawn in spawnPoints:
        for team in ('info_player_terrorist', 'info_player_counterterrorist'):
            # Create the spawnpoint and get the index
            es.server.cmd('es_xgive %s %s' % (userid, team))
            index = int(es.ServerVar('eventscripts_lastgive'))
            
            # Set the spawnpoint position and rotation
            es.setindexprop(index, 'CBaseEntity.m_vecOrigin', '%s,%s,%s' % (spawn[0], spawn[1], spawn[2]))
            es.setindexprop(index, 'CBaseEntity.m_angRotation', '0,%s,0' % spawn[4])