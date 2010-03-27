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
from os import name as platform

# Eventscripts Imports
import es
import cmdlib
import repeat
import gamethread
from playerlib import getPlayer
from playerlib import getPlayerList

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.players.shortcuts import Player
from gungame51.core.messaging.shortcuts import hudhint
from gungame51.core.messaging.shortcuts import msg
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

# Approximates the number of seconds from round start to play beginning
GG_WARMUP_EXTRA_TIME = 3

# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    # Load warmup round (delayed)
    gamethread.delayed(1, do_warmup)

    # Loaded message
    es.dbgmsg(0, 'Loaded: %s' % info.name)

    # Register a server command to to cancel an in-progress warmup round
    cmdlib.registerServerCommand('gg_end_warmup', servercmd_end_warmup,
    	"Immediately ends the warmup round if there is one in progress.")

def unload():
    # Deleting warmup timer
    warmupCountDown = repeat.find('gungameWarmupTimer') 

    # If the warmup timer exists, stop and delete it
    if warmupCountDown:    
        warmupCountDown.stop()
        warmupCountDown.delete()

    # Reset server vars
    reset_server_vars(True)

    # Unload message
    es.dbgmsg(0, 'Unloaded: %s' % info.name)
    
    # Unregister the server command that cancels an in-progress warmup round
    cmdlib.unregisterServerCommand('gg_end_warmup')

# ============================================================================
# >> COMMAND CALLBACKS
# ============================================================================
def servercmd_end_warmup(args): # args are ignored, but needed for server cmd
    # Get the timer/repeat instance
    warmupCountDown = repeat.find('gungameWarmupTimer')

    # Break out if the timer is invalid (implies warmup is not in progress)
    if not warmupCountDown:
        return

    # Restart the round ourselves in 1 second
    es.server.queuecmd('mp_restartgame 1')

    # Before the round ends up restarting, prepare gungame to be ready
    # for the first round of play
    gamethread.delayed(0.7, prepare_game)

    # Make sure that during the first round nobody has godmode
    gamethread.delayed(1.4, remove_godmode)

    # End the warmup round
    # Delayed to allow mp_restartgame to strip all weapons before gg gives them
    # (Emulating behavior of call to mp_restartgame in count_down() below)
    gamethread.delayed(1, end_warmup, ('Warmup_End_Forced'))

    # Display a chat message with the same message
    msg("#human", 'Warmup_End_Forced', prefix=True)

# ============================================================================
# >> GAME EVENTS
# ============================================================================
def es_map_start(event_var):
    # Looking for running warmup timer
    warmupCountDown = repeat.find('gungameWarmupTimer')
    if warmupCountDown:

        # We are comming in from another warmup round ?
        if warmupCountDown.status() == 2:

            # Stop timer
            warmupCountDown.stop()

            do_warmup(False)
            return

    # Start warmup timer. This is delayed to ensure that all addons get to fire
    # es_map_start events before priority addons are set.
    do_warmup()

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

    # If it is the last split second before mp_restartgame fires, protect the
    # player
    if not 'gg_warmup_round' in PriorityAddon():
        getPlayer(userid).godmode = 1

    # Get player object
    ggPlayer = Player(userid)

    # Check if the warmup weapon is the level 1 weapon
    if str(gg_warmup_weapon) in ('0', '', '0.0'):
        ggPlayer.give_weapon()
        return

    # Check if the warmup weapon is a knife
    if str(gg_warmup_weapon) == 'knife':
        es.sexec(userid, 'use weapon_knife')
        return

    delay = 0.07

    if es.isbot(userid):
        delay += 0.25

    # Strip the player's weapons (split second delay)
    gamethread.delayed(delay, ggPlayer.strip, (True, [gg_warmup_weapon]))

    # Delay giving the weapon by a split second, because the code in round
    #   start removes all weapons
    gamethread.delayed((delay + 0.05), ggPlayer.give, (str(gg_warmup_weapon),
                                                            True, True))

# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
def add_priority_addon(name):
    priority_addons_added.append(name)
    PriorityAddon().append(name)            

def do_warmup(useBackupVars=True):
    # Looking for warmup timer
    warmupCountDown = repeat.find('gungameWarmupTimer')

    if useBackupVars:
        # Setting globals for backup variables
        global mp_freezetime_backup
        global gg_deathmatch_backup
        global gg_elimination_backup

        # Setting backup variables
        mp_freezetime_backup = int(mp_freezetime)
        gg_deathmatch_backup = int(gg_deathmatch)
        gg_elimination_backup = int(gg_elimination)

    # Setting mp_freezetime
    mp_freezetime.set(0)

    # Added priority addons list
    del priority_addons_added[:]

    # Checking for warmup in the priority addons list
    add_priority_addon('gg_warmup_round')

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
        add_priority_addon('gg_deathmatch')

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
        add_priority_addon('gg_elimination')

    # Start it up if it exists
    if warmupCountDown:
        warmupCountDown.stop()
        warmupCountDown.start(1, int(gg_warmup_timer) + GG_WARMUP_EXTRA_TIME)
        return

    # Create a timer
    warmupCountDown = repeat.create('gungameWarmupTimer', count_down)
    warmupCountDown.start(1, int(gg_warmup_timer) + GG_WARMUP_EXTRA_TIME)

def count_down():
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
            play_beep()

        # 1 second left in warmup
        if warmupCountDown['remaining'] == 1:
            # Restart the round ourselves in 1 second
            es.server.queuecmd('mp_restartgame 1')

            # Before the round ends up restarting, prepare gungame to be ready
            # for the first round of play
            gamethread.delayed(0.7, prepare_game)
            
            # Make sure that during the first round nobody has godmode
            gamethread.delayed(1.4, remove_godmode)

    # No time left
    elif warmupCountDown['remaining'] == 0:
        end_warmup('Timer_Ended')

def prepare_game():
    # Give players godmode so that they can't level up
    for userid in getPlayerList("#alive"):
        getPlayer(userid).godmode = 1

    # Remove addons added to priority_addons
    for addedAddon in priority_addons_added:
        PriorityAddon().remove(addedAddon)

    # Fire gg_start event
    EventManager().gg_start()

def remove_godmode():
    '''
    Ran during the first round to make sure no players have godmode.
    '''
    for userid in getPlayerList("#alive"):
        getPlayer(userid).godmode = 0

def end_warmup(message):
    # Send hint
    hudhint('#human', message)

    # Play beep
    play_beep()

    # Delete the timer
    repeat.delete('gungameWarmupTimer')             

    # Reset server vars back
    reset_server_vars(False)

def play_beep():
    for userid in getPlayerList('#human'):
        Player(userid).playsound('countDownBeep')

def reset_server_vars(unload):
    # Warmup elimination or deathmatch previously loaded?
    if int(gg_warmup_elimination) or int(gg_deathmatch_backup):

        # Back to DM ?
        if gg_deathmatch_backup:
            es.server.queuecmd('gg_elimination 0')

            if unload:
                gg_deathmatch.set(1)
            else:
                es.server.queuecmd('gg_deathmatch 1')

        # Back to normal ?
        elif not gg_elimination_backup:
            es.server.queuecmd('gg_elimination 0')

    # Warmup DM or elimination previously loaded?
    elif int(gg_warmup_deathmatch) or int(gg_elimination_backup):
        # Back to elimination ?
        if gg_elimination_backup:
            es.server.queuecmd('gg_deathmatch 0')

            if unload:
                gg_elimination.set(1)
            else:
                es.server.queuecmd('gg_elimination 1')

        # Back to normal ?
        elif not gg_deathmatch_backup:
            es.server.queuecmd('gg_deathmatch 0')

    # Changing mp_freezetime back
    if int(mp_freezetime) != mp_freezetime_backup:
        mp_freezetime.set(mp_freezetime_backup)