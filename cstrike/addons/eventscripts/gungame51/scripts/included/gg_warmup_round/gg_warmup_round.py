# ../addons/eventscripts/gungame/scripts/included/gg_warmup_round/gg_warmup_round.py

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
import repeat
import gamethread
from playerlib import getPlayer
from playerlib import getPlayerList

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.players.shortcuts import Player
from gungame51.core.messaging.shortcuts import hudhint
from gungame51.core.events.shortcuts import EventManager
from gungame51.core.addons import PriorityAddon

# ============================================================================
# >> ADDON REGISTRATION/INFORMATION
# ============================================================================
info = AddonInfo()
info.name = 'gg_warmup_round'
info.title = 'GG Warmup Round' 
info.author = 'GG Dev Team' 
info.version = '0.1'
info.translations = ['gg_warmup_round']

# ============================================================================
# >> GLOBAL VARIABLES
# ============================================================================
mp_freezetime = es.ServerVar('mp_freezetime')
gg_warmup_round = es.ServerVar('gg_warmup_round')
gg_warmup_timer = es.ServerVar('gg_warmup_timer')
gg_warmup_weapon = es.ServerVar('gg_warmup_weapon')
gg_warmup_deathmatch = es.ServerVar('gg_warmup_deathmatch')
gg_warmup_elimination = es.ServerVar('gg_warmup_elimination')
gg_deathmatch = es.ServerVar('gg_deathmatch')
gg_elimination = es.ServerVar('gg_elimination')
priority_addons_added = []

# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    # Start warmup timer
    if es.exists('variable', 'gg_deathmatch') and \
      es.exists('variable', 'gg_elimination'):
        doWarmup()

    else:
        gamethread.delayed(1, doWarmup, ())
    
    # Loaded message
    es.dbgmsg(0, 'Loaded: %s' % info.name)
    
def unload():
    # Deleting warmup timer
    warmupCountDown = repeat.find('gungameWarmupTimer') 
    if warmupCountDown:    
        warmupCountDown.stop()
        repeat.delete('gungameWarmupTimer')
    
    # Unload message
    es.dbgmsg(0, 'Unloaded: %s' % info.name)
        
# ============================================================================
# >> GAME EVENTS
# ============================================================================
def es_map_start(event_var):
    # Start warmup timer
    doWarmup()     
        
def hegrenade_detonate(event_var):
    # Making sure warmup round is running
    warmupCountDown = repeat.find('gungameWarmupTimer')
    
    if not warmupCountDown:
        return

    # Get player userid and player object
    userid = int(event_var['userid'])
    
    # Is the client on the server?
    if not es.exists('userid', userid):
        return
    
    # Give user a hegrenade, if eligable
    if int(event_var['es_userteam']) > 1 and not getPlayer(userid).isdead and \
        str(gg_warmup_weapon) == 'hegrenade':
            Player(userid).give('hegrenade')

def player_spawn(event_var):
    # Making sure warmup round is running
    warmupCountDown = repeat.find('gungameWarmupTimer')
    
    if not warmupCountDown:
        return
        
    userid = int(event_var['userid'])

    # Is a spectator or dead?
    if int(event_var['es_userteam']) < 2 or getPlayer(userid).isdead:
        return
    
    # Get player object
    ggPlayer = Player(userid)
    
    # Check if the warmup weapon is the level 1 weapon
    if str(gg_warmup_weapon) in ('0', '', '0.0'):
        ggPlayer.giveWeapon()
        return
    
    # Check if the warmup weapon is a knife
    if str(gg_warmup_weapon) == 'knife':
        es.sexec(userid, 'use weapon_knife')
        return
    
    # Strip the player's weapons (split second delay)
    gamethread.delayed(0.10, ggPlayer.strip, True)
    
    # Delay giving the weapon by a split second, because the code in round 
    #   start removes all weapons
    gamethread.delayed(0.11, ggPlayer.give, '%s' % gg_warmup_weapon)

# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
def addPriorityAddon(name):
    if name not in PriorityAddon():
        priority_addons_added.append(name)
        PriorityAddon().append(name)            

def doWarmup():
    # Setting globals for backup variables
    global mp_freezetime_backup
    global gg_deathmatch_backup
    global gg_elimination_backup
    
    # Setting backup variables
    mp_freezetime_backup = int(mp_freezetime)
    gg_deathmatch_backup = int(gg_deathmatch)
    gg_elimination_backup = int(gg_elimination)
        
    # Added priority addons list
    del priority_addons_added[:]
    
    # Checking for warmup in the priority addons list
    addPriorityAddon('gg_warmup_round')      
    
    # Setting mp_freezetime 
    mp_freezetime.set(0)
    
    # Checking for warmup deathmatch
    if (int(gg_warmup_deathmatch) or int(gg_deathmatch)) and \
        not int(gg_warmup_elimination):
        
        # Making sure elimination is off
        if int(gg_elimination):
            es.server.queuecmd('gg_elimination 0')            
        
        # Enable gg_deathmatch
        if not int(gg_deathmatch):
            es.server.queuecmd('gg_deathmatch 1')
        
        # Checking for deathmatch in the priority addons list
        addPriorityAddon('gg_deathmatch')      
    
    # Checking for warmup elimination
    elif (int(gg_warmup_elimination) or int(gg_elimination)) and \
        not int(gg_warmup_deathmatch):
        
        # Making sure deathmatch is off
        if int(gg_deathmatch):
            es.server.queuecmd('gg_deathmatch 0')   
        
        # Enable gg_elimination
        if not int(gg_elimination):
            es.server.queuecmd('gg_elimination 1')
    
        # Checking for elimination in the priority addons list
        addPriorityAddon('gg_elimination')        
    
    # Looking for warmup timer
    warmupCountDown = repeat.find('gungameWarmupTimer')
    
    # Start it up if it exists
    if warmupCountDown:
        warmupCountDown.stop()
        warmupCountDown.start(1, int(gg_warmup_timer) + 3)
        return
            
    # Create a timer
    warmupCountDown = repeat.create('gungameWarmupTimer', countDown)
    warmupCountDown.start(1, int(gg_warmup_timer) + 3)
    
def countDown():
    warmupCountDown = repeat.find('gungameWarmupTimer')
    
    # Making sure the count-down is going
    if not warmupCountDown:
        return
        
    # If the remaining time is greater than 1
    if warmupCountDown['remaining'] >= 1:
        
        # Send hint
        if warmupCountDown['remaining'] > 1:
            hudhint('#human', 'Timer_Plural', 
            {'time': warmupCountDown['remaining']})
        else:
            hudhint('#human', 'Timer_Singular')
        
        # Countdown 5 or less?
        if warmupCountDown['remaining'] <= 5:
            
            # Play beep
            playBeep()
        
        # mp_restartgame and trigger round_end
        if warmupCountDown['remaining'] == 1:
            es.server.queuecmd('mp_restartgame 1')
    
    # No time left
    elif warmupCountDown['remaining'] == 0:
        # Send hint
        hudhint('#human', 'Timer_Ended')
        
        # Play beep
        playBeep()
        
        # Delete the timer
        repeat.delete('gungameWarmupTimer')
        
        # Removing addons added to priority_addons
        for addedAddon in priority_addons_added:
            PriorityAddon().remove(addedAddon)                   
                
        # Warmup elimination ?
        if int(gg_warmup_elimination):

            # Back to DM ?
            if gg_deathmatch_backup:
                es.server.queuecmd('gg_elimination 0')
                es.server.queuecmd('gg_deathmatch 1')

            # Back to normal ?
            elif not gg_elimination_backup:
                es.server.queuecmd('gg_elimination 0')

        
        # Warmup DM ?
        elif int(gg_warmup_deathmatch):

            # Back to elimination ?
            if gg_elimination_backup:
                es.server.queuecmd('gg_deathmatch 0')
                es.server.queuecmd('gg_elimination 1')

            # Back to normal ?
            elif not gg_deathmatch_backup:
                es.server.queuecmd('gg_deathmatch 0')
        
        # Changing mp_freezetime back
        if int(mp_freezetime) != mp_freezetime_backup:
            mp_freezetime.set(mp_freezetime_backup)
        
        # Fire gg_start event
        EventManager().gg_start()

def playBeep():
    for userid in getPlayerList('#human'):
        Player(userid).playsound('countDownBeep')
            