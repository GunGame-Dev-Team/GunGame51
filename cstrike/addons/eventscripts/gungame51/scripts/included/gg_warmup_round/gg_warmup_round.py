# ../addons/eventscripts/gungame/scripts/included/gg_warmup_round/gg_warmup_round.py

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
import repeat
import gamethread
from playerlib import getPlayerList
from playerlib import getPlayer

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.players.shortcuts import Player
from gungame51.core.messaging.shortcuts import hudhint
from gungame51.core.events.shortcuts import EventManager

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
# Get the es.ServerVar() instance of "gg_warmup_round"
gg_warmup_round = es.ServerVar('gg_warmup_round')
# Get the es.ServerVar() instance of "gg_warmup_timer"
gg_warmup_timer = es.ServerVar('gg_warmup_timer')
# Get the es.ServerVar() instance of "gg_warmup_weapon"
gg_warmup_weapon = es.ServerVar('gg_warmup_weapon')
# Get the es.ServerVar() instance of "gg_warmup_deathmatch"
gg_warmup_deathmatch = es.ServerVar('gg_warmup_deathmatch')
# Get the es.ServerVar() instance of "gg_warmup_elimination"
gg_warmup_elimination = es.ServerVar('gg_warmup_elimination')
# Get the es.ServerVar() instance of "gg_deathmatch"
gg_deathmatch = es.ServerVar('gg_deathmatch')
# Get the es.ServerVar() instance of "mp_freezetime"
mp_freezetime = es.ServerVar('mp_freezetime')

# Create a backup variable for "mp_freezetime"
mp_freezetime_backup = None
# Create a backup variable for "gg_deathmatch"
gg_deathmatch_backup = None
# Create a backup variable for "gg_elimination"
gg_elimination_backup = None

# ============================================================================
# >> CLASSES
# ============================================================================
class WarmUpWeaponError(Exception):
    pass

# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    # Set the preventlevel attribute for all players on the server
    for userid in es.getUseridList():
        Player(userid).preventlevel.append('gg_warmup_round')
        
    # Check to see if we should load gg_deathmatch for warmup round
    if int(gg_warmup_deathmatch):
        # See if gg_deathmatch is loaded
        if not int(gg_deathmatch):
            # Back up gg_deathmatch's original value
            gg_deathmatch_backup = int(gg_deathmatch)
            
            # If gg_deathmatch is not loaded, load it
            es.server.queuecmd('gg_deathmatch 1')
        
    # Check to see if we should load gg_elimination for warmup round
    if int(gg_warmup_elimination):
        # See if gg_elimination is loaded
        if not int(gg_elimination):
            # Back up gg_elimination's original value
            gg_elimination_backup = int(gg_elimination)
            
            # If gg_elimination is not loaded, load it
            es.server.queuecmd('gg_elimination 1')
            
    # Make sure there is supposed to be a warmup weapon
    if str(gg_warmup_weapon) != '0':
        # Make sure the warmup weapon is a valid weapon choice
        if str(gg_warmup_weapon) not in gungamelib.getWeaponList('valid') + ['flashbang', 'smokegrenade']:
            # Nope, the admin typoed it. Let's set it to 0 so that we don't have to worry about this later
            es.ServerVar('gg_warmup_weapon').set(0)
            
            # Raise an error due to the typo by the admin
            raise WarmUpWeaponError, warmupWeapon + ' is not a valid weapon. Setting \'gg_warmup_weapon\' to level 1\'s weapon.'
            
    # Backup "mp_freezetime" variable to reset it later
    mp_freezetime_backup = int(mp_freezetime)
    
    # Set "mp_freezetime" to 0
    mp_freezetime.set(0)
    
    # Start the countdown timer
    gamethread.delayed(3, startTimer, ())
    
    es.dbgmsg(0, 'Loaded: %s' % info.name)
    
def unload():
    # Remove "gg_warmup_round" from preventlevel for all players on the server
    for userid in es.getUseridList():
        Player(userid).preventlevel.remove('gg_warmup_round')

    # Cancel the "gungameWarmUpRound" delay
    gamethread.cancelDelayed('gungameWarmUpRound')
    
    # Check to see if repeat is still going
    if repeat.find('gungameWarmupTimer'):
        if repeat.status('gungameWarmupTimer'):
            repeat.delete('gungameWarmupTimer')
    
    # Return "mp_freezetime" to what it was originally
    mp_freezetime.set(mp_freezetime_backup)

    es.dbgmsg(0, 'Unloaded: %s' % info.name)
    
# ============================================================================
# >> GAME EVENTS
# ============================================================================
def es_map_start(event_var):
    warmupCountDown = repeat.find('gungameWarmupTimer')
    
    if warmupCountDown:
        # Restart the repeat
        warmupCountDown.stop()
        warmupCountDown.start(1, int(gg_warmup_timer) + 3)
        
def player_spawn(event_var):
    userid = int(event_var['userid'])

    # Is a spectator or dead?
    if int(event_var['es_userteam']) <= 1 or getPlayer(userid).isdead:
        return
    
    # Get player object
    ggPlayer = Player(userid)
    
    # Check if the warmup weapon is the level 1 weapon
    if str('gg_warmup_weapon') == '0':
        ggPlayer.giveWeapon()
        return
    
    # Check if the warmup weapon is a knife
    if str('gg_warmup_weapon') == 'knife':
        es.sexec(userid, 'use weapon_knife')
        return
    
    # Delay giving the weapon by a split second, because the code in round start removes all weapons
    gamethread.delayed(0, ggPlayer.give, (str(gg_warmup_weapon)))
        
def player_activate(event_var):
    userid = int(event_var['userid'])
    
    # Set the preventlevel attribute to for late joiners
    Player(userid).preventlevel.append('gg_warmup_round')
    
def hegrenade_detonate(event_var):
    # Get player userid and player object
    userid = event_var['userid']
    
    # Is the client on the server?
    if not es.exists('userid', userid):
        return
    
    # Give user a hegrenade, if eligable
    if int(event_var['es_userteam']) > 1 and not getPlayer(userid).isdead and \
        str(gg_warmup_weapon) == 'hegrenade':
            Player(userid).give('hegrenade')

# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
def startTimer():
    # Create a repeat
    warmupCountDown = repeat.create('gungameWarmupTimer', countDown)
    warmupCountDown.start(1, int(gg_warmup_timer) + 3)
    
def countDown():
    warmupCountDown = repeat.find('gungameWarmupTimer')
    
    if not warmupCountDown:
        return
        
    # If the remaining time is greater than 1
    if warmupCountDown['remaining'] >= 1:
        # Send hint
        if warmupCountDown['remaining'] > 1:
            hudhint('#human', 'Timer_Plural', {'time': warmupCountDown['remaining']})
        else:
            hudhint('#human', 'Timer_Singular')
        
        # Countdown 5 or less?
        if warmupCountDown['remaining'] <= 5:
            #gungamelib.playSound('#all', 'countDownBeep')
        
        # mp_restartgame and trigger round_end
        if warmupCountDown['remaining'] == 1:
            es.server.queuecmd('mp_restartgame 1')
    
    # No time left
    elif warmupCountDown['remaining'] == 0:
        # Send hint
        hudhint('#human', 'Timer_Ended')
        
        # Play beep
        #gungamelib.playSound('#human', 'countDownBeep')
        
        # Stop the timer
        repeat.delete('gungameWarmupTimer')
        
        # Fire gg_start event
        EventManager().gg_start()
        
        # Check to see if we should load deathmatch for warmup round
        if gg_deathmatch_backup:
            es.server.queuecmd('gg_deathmatch 0')
        
        # Check to see if we should load elimination for warmup round
        if gg_elimination_backup:
            es.server.queuecmd('gg_elimination 0')