# ../addons/eventscripts/gungame/scripts/included/gg_spawn_protect/gg_spawn_protect.py

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
import gamethread
import playerlib

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.players.shortcuts import Player
from gungame51.core.players.shortcuts import isDead
from gungame51.core.players.shortcuts import isSpectator

# ============================================================================
# >> ADDON REGISTRATION/INFORMATION
# ============================================================================
info = AddonInfo()
info.name = 'gg_spawn_protect'
info.title = 'GG Spawn Protection' 
info.author = 'GG Dev Team' 
info.version = '0.1'

# ============================================================================
# >> GLOBAL VARIABLES
# ============================================================================
noisySave = 0
cancelonfire = es.ServerVar('gg_spawn_protect_cancelonfire')
canLevelup = es.ServerVar('gg_spawn_protect_can_level_up')
protectedList = []

# ============================================================================
# >> CLASSES
# ============================================================================


# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    global noisySave

    if cancelonfire:
        noisySave = int(es.ServerVar('eventscripts_noisy'))
        es.ServerVar('eventscripts_noisy').set(1)
    
    es.dbgmsg(0, 'Loaded: %s' % info.name)

def unload():
    es.ServerVar('eventscripts_noisy').set(noisySave)
    
    es.dbgmsg(0, 'Unloaded: %s' % info.name)

# ============================================================================
# >> GAME EVENTS
# ============================================================================
def server_cvar(event_var):
    global noisySave

    if event_var['cvarname'] == 'gg_spawn_protect_cancelonfire':

        if int(event_var['cvarvalue']) >= 1:
            # Set noisy vars
            noisySave = int(es.ServerVar('eventscripts_noisy'))
            es.ServerVar('eventscripts_noisy').set(1)
        else:
            # Set noisy back
            es.ServerVar('eventscripts_noisy').set(noisyBefore)

def weapon_fire(event_var):
    if not cancelonfire:
        return
    
    userid = int(event_var['userid'])
    
    if userid in protectedList:
        gamethread.cancelDelayed('ggSpawnProtect%s' % userid)
    
        endProtect(userid)

def player_spawn(event_var):
    
    # Get userid
    userid = int(event_var['userid'])
    
    # Is player alive?
    if isDead(userid) or isSpectator(userid):
        return
    
    if userid in protectedList:
        return
    
    # Start protecting the player
    startProtect(userid)
    
def player_death(event_var):
    userid = int(event_var['userid'])
    
    if userid in protectedList:
        gamethread.cancelDelayed('ggSpawnProtect%s' % userid)
        protectedList.remove(userid)

def player_disconnect(event_var):
    userid = int(event_var['userid'])
    
    # Remove from protected list
    if userid in protectedList:
        gamethread.cancelDelayed('ggSpawnProtect%s' % userid)
        protectedList.remove(userid)

# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
def startProtect(userid):
    # Retrieve player objects
    playerlibPlayer = playerlib.getPlayer(userid)
    
    # Add them to the list of protected players
    protectedList.append(userid)
    
    # Set color
    playerlibPlayer.set('color', (  es.ServerVar('gg_spawn_protect_red'),
                                    es.ServerVar('gg_spawn_protect_green'),
                                    es.ServerVar('gg_spawn_protect_blue'),
                                    es.ServerVar('gg_spawn_protect_alpha')))
    
    # Start Invincible
    es.setplayerprop(userid, 'CCSPlayer.baseclass.m_lifeState', 0)
    
    # Set PreventLevel if needed
    if not canLevelup:
        ggPlayer = Player(userid)
        
        if not 'gg_spawn_protect' in ggPlayer.preventlevel:
            ggPlayer.preventlevel.append('gg_spawn_protect')
    
    # Start the delay to cancel spawn protection
    gamethread.delayedname(es.ServerVar('gg_spawn_protect'), 'ggSpawnProtect%s' % userid, endProtect, (userid))

def endProtect(userid):
    # Are they even protected?
    if not userid in protectedList:
        return
    
    # Check the client hasn't left during the protection period
    if not es.exists('userid', userid):
        # Fix potential memory leak:
        protectedList.remove(userid)
        return
    
    # Retrieve player objects
    playerlibPlayer = playerlib.getPlayer(userid)
    
    # Remove the player from the list of protected players
    protectedList.remove(userid)
    
    # Color
    playerlibPlayer.set('color', (255, 255, 255, 255))
    
    # End Invincible
    es.setplayerprop(userid, 'CCSPlayer.baseclass.m_lifeState', 512)
    
    # Remove PreventLevel if it was enabled
    if not canLevelup:
        ggPlayer = Player(userid)
        
        if 'gg_spawn_protect' in ggPlayer.preventlevel:
            ggPlayer.preventlevel.remove('gg_spawn_protect')