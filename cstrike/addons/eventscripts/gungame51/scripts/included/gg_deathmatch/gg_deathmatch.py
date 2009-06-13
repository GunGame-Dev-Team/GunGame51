# ../addons/eventscripts/gungame/scripts/included/gg_deathmatch/gg_deathmatch.py

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
from playerlib import getUseridList
import repeat

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.messaging.shortcuts import hudhint

# ============================================================================
# >> ADDON REGISTRATION/INFORMATION
# ============================================================================
info = AddonInfo()
info.name = 'gg_deathmatch'
info.title = 'GG Deathmatch' 
info.author = 'GG Dev Team' 
info.version = '0.1' 
info.requires = ['gg_turbo', 'gg_dead_strip', 'gg_dissolver'] 
info.conflicts= ['gg_map_obj', 'gg_knife_elite', 'gg_elimination']
info.translations = ['gg_deathmatch']

# ============================================================================
# >> GLOBAL VARIABLES
# ============================================================================

respawnDelay = es.ServerVar('gg_dm_respawn_delay')
respawnAllowed = 0

mp_freezetime = es.ServerVar('mp_freezetime')
mp_roundtime = es.ServerVar('mp_roundtime')
mpFreezetimeBackup = int(mp_freezetime)
mpRoundtimeBackup = int(mp_roundtime)

# ============================================================================
# >> CLASSES
# ============================================================================


# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    
    # Don't allow respawn
    global respawnAllowed
    respawnAllowed = 0
    
    # Set freezetime and roundtime to avoid gameplay interuptions
    mp_freezetime.set('0')
    mp_roundtime.set('9')
    
    # Create repeats for all players on the server
    for userid in es.getUseridList():
        respawnPlayer = repeat.find('gungameRespawnPlayer%s' % userid)
        
        if not respawnPlayer:
            repeat.create('gungameRespawnPlayer%s' % userid, respawnCountDown, (userid))
    
    # Respawn all dead players
    for userid in getUseridList('#dead'):
        repeat.start('gungameRespawnPlayer%s' % userid, 1, spawnDelay)
    
def unload():
    es.dbgmsg(0, 'Unloaded: %s' % info.name)
    
    # Set freezetime and roundtime back to their value before deathmatch was loaded
    mp_freezetime.set(mpFreezetimeBackup)
    mp_roundtime.set(mpRoundtimeBackup)
    
    # Delete all player respawns
    for userid in es.getUseridList():
        if repeat.find('gungameRespawnPlayer%s' % userid):
            repeat.delete('gungameRespawnPlayer%s' % userid)
    
# ============================================================================
# >> GAME EVENTS
# ============================================================================

def es_map_start(event_var):
    
    # Don't allow respawn
    global respawnAllowed
    respawnAllowed = 0

def round_start(event_var):
    
    # Allow respawn
    global respawnAllowed
    respawnAllowed = 1

def round_end(event_var):
    
    # Don't allow respawn
    global respawnAllowed
    respawnAllowed = 0

def gg_win(event_var):
    
    #Cancel pending respawns
    for userid in es.getUseridList():
        if repeat.find('gungameRespawnPlayer%s' % userid):
            repeat.delete('gungameRespawnPlayer%s' % userid)

def player_team(event_var):
    
    if event_var['disconnect'] != '0':
        return
    
    # Get the userid
    userid = event_var['userid']
    
    # If the player does not have a respawn repeat, create one
    respawnPlayer = repeat.find('gungameRespawnPlayer%s' % userid)
    if not respawnPlayer:
        repeat.create('gungameRespawnPlayer%s' % userid, respawnCountDown, (userid))
    
    # Don't allow spectators or players that are unassigned to respawn
    if int(event_var['team']) < 2:
        if repeat.status('gungameRespawnPlayer%s' % userid) != 1:
            repeat.stop('gungameRespawnPlayer%s' % userid)
            hudhint(userid, 'RespawnCountdown_CancelTeam')
        
        return
    
    # Respawn the player
    repeat.start('gungameRespawnPlayer%s' % userid, 1, respawnDelay)

def player_disconnect(event_var):
    # Get userid
    userid = event_var['userid']
    
    # Delete the player-specific repeat
    if repeat.find('gungameRespawnPlayer%s' % userid):
        repeat.delete('gungameRespawnPlayer%s' % userid)

def player_death(event_var):
    
    # Get the userid
    userid = event_var['userid']
    
    # Respawn the player if the round hasn't ended
    if gungamelib.getGlobal('respawn_allowed'):
        repeat.start('gungameRespawnPlayer%s' % userid, 1, respawnDelay)

# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================