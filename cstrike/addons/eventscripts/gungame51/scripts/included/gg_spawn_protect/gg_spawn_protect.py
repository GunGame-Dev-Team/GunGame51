# ../addons/eventscripts/gungame51/scripts/included/gg_spawn_protect/gg_spawn_protect.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
# Eventscripts Imports
import es
import gamethread
from playerlib import getPlayer

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.players.shortcuts import Player

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
# Get the es.ServerVar() instance of "gg_spawn_protect"
gg_spawn_protect = es.ServerVar('gg_spawn_protect')

# Get the es.ServerVar() instance of "gg_spawn_protect_cancelonfire"
gg_spawn_protect_cancelonfire = es.ServerVar('gg_spawn_protect_cancelonfire')

# Get the es.ServerVar() instance of "gg_spawn_protect_can_level_up"
gg_spawn_protect_can_level_up = es.ServerVar('gg_spawn_protect_can_level_up')

# Get the es.ServerVar() instance of "gg_spawn_protect_red"
gg_spawn_protect_red = es.ServerVar('gg_spawn_protect_red')

# Get the es.ServerVar() instance of "gg_spawn_protect_green"
gg_spawn_protect_green = es.ServerVar('gg_spawn_protect_green')

# Get the es.ServerVar() instance of "gg_spawn_protect_blue"
gg_spawn_protect_blue = es.ServerVar('gg_spawn_protect_blue')

# Get the es.ServerVar() instance of "gg_spawn_protect_alpha"
gg_spawn_protect_alpha = es.ServerVar('gg_spawn_protect_alpha')

# Get the es.ServerVar() instance of "eventscripts_noisy"
eventscripts_noisy = es.ServerVar('eventscripts_noisy')

noisySave = 0
protectedList = []

# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    global noisySave

    if gg_spawn_protect_cancelonfire:
        noisySave = int(eventscripts_noisy)
        eventscripts_noisy.set(1)

    es.dbgmsg(0, 'Loaded: %s' % info.name)

def unload():
    eventscripts_noisy.set(noisySave)

    es.dbgmsg(0, 'Unloaded: %s' % info.name)

# ============================================================================
# >> GAME EVENTS
# ============================================================================
def server_cvar(event_var):
    global noisySave

    # Change "eventscripts_noisy" due to "gg_spawn_protect_cancelonfire"?
    if event_var['cvarname'] == 'gg_spawn_protect_cancelonfire':

        if int(event_var['cvarvalue']) >= 1:
            # Set noisy vars
            noisySave = int(eventscripts_noisy)
            eventscripts_noisy.set(1)
        else:
            # Set noisy back
            eventscripts_noisy.set(noisySave)

def weapon_fire(event_var):
    if not int(gg_spawn_protect_cancelonfire):
        return

    userid = int(event_var['userid'])

    if userid in protectedList:
        # Cancel the delay if protected
        gamethread.cancelDelayed('ggSpawnProtect%s' % userid)

        # End the protection
        endProtect(userid)

def player_spawn(event_var):
    # Get userid
    userid = int(event_var['userid'])

    # Is player alive?
    if getPlayer(userid).isdead or int(event_var['es_userteam']) < 2:
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
    pPlayer = getPlayer(userid)

    # Add them to the list of protected players
    protectedList.append(userid)

    # Set color
    pPlayer.color = (gg_spawn_protect_red,
                     gg_spawn_protect_green,
                     gg_spawn_protect_blue,
                     gg_spawn_protect_alpha)

    # Start Invincible
    pPlayer.godmode = 1

    # Set PreventLevel if needed
    if not int(gg_spawn_protect_can_level_up):
        ggPlayer = Player(userid)

        if not 'gg_spawn_protect' in ggPlayer.preventlevel:
            ggPlayer.preventlevel.append('gg_spawn_protect')

    # Start the delay to cancel spawn protection
    gamethread.delayedname(int(gg_spawn_protect), 
        'ggSpawnProtect%s' % userid, endProtect, (userid))

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
    pPlayer = getPlayer(userid)

    # Remove the player from the list of protected players
    protectedList.remove(userid)

    # Color
    pPlayer.color = (255, 255, 255, 255)

    # End Invincible
    pPlayer.godmode = 0

    # Remove PreventLevel if it was enabled
    if not int(gg_spawn_protect_can_level_up):
        ggPlayer = Player(userid)

        if 'gg_spawn_protect' in ggPlayer.preventlevel:
            ggPlayer.preventlevel.remove('gg_spawn_protect')