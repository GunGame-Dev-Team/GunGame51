# ../scripts/included/gg_warmup_round/gg_warmup_round.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
from random import shuffle

# Eventscripts Imports
import es
import cmdlib
import repeat
import gamethread
from playerlib import getPlayer
from playerlib import getPlayerList
from playerlib import getUseridList
from weaponlib import getWeaponNameList

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.addons import AddonManager
from gungame51.core.addons import PriorityAddon
from gungame51.core.addons import load as addon_load
from gungame51.core.addons import unload as addon_unload
from gungame51.core.players.shortcuts import Player
from gungame51.core.messaging.shortcuts import hudhint
from gungame51.core.messaging.shortcuts import msg
from gungame51.core.events import GG_Start
from gungame51.core.weapons.shortcuts import get_level_weapon


# =============================================================================
# >> ADDON REGISTRATION/INFORMATION
# =============================================================================
info = AddonInfo()
info.name = 'gg_warmup_round'
info.title = 'GG Warmup Round'
info.author = 'GG Dev Team'
info.version = "5.1.%s" % "$Rev$".split('$Rev: ')[1].split()[0]
info.translations = ['gg_warmup_round']


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
mp_freezetime = es.ServerVar('mp_freezetime')
gg_warmup_round = es.ServerVar('gg_warmup_round')
gg_warmup_timer = es.ServerVar('gg_warmup_timer')
gg_warmup_weapon = es.ServerVar('gg_warmup_weapon')
gg_warmup_deathmatch = es.ServerVar('gg_warmup_deathmatch')
gg_warmup_elimination = es.ServerVar('gg_warmup_elimination')
gg_dead_strip = es.ServerVar('gg_dead_strip')
gg_deathmatch = es.ServerVar('gg_deathmatch')
gg_elimination = es.ServerVar('gg_elimination')

# possible_random_weapons includes all primaries, secondaries, and hegrenade
possible_random_weapons = getWeaponNameList("#primary")
possible_random_weapons.extend(getWeaponNameList("#secondary"))
possible_random_weapons.append("hegrenade")

# Used to make sure we don't set the warmup weapon twice on load
warmupWeaponSetOnLoad = False

priority_addons_added = []
random_warmup_weapons = []
warmup_weapon = None

# If we are in the middle of the overlap from warmup ending to gg_start, give
# newly spawned players godmode
giveGodMode = False

# Approximates the number of seconds from round start to play beginning
GG_WARMUP_EXTRA_TIME = 3

# Backup variables
mp_freezetime_backup = 0
gg_dead_strip_backup = 0
gg_deathmatch_backup = 0
gg_elimination_backup = 0


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    global warmupWeaponSetOnLoad

    # Set the warmup weapon
    set_warmup_weapon()

    # Make sure we don't set the warmup weapon twice on load
    warmupWeaponSetOnLoad = True

    # Load warmup round (delayed)
    gamethread.delayedname(1, "gg_do_warmup", do_warmup)

    # Register a server command to to cancel an in-progress warmup round
    cmdlib.registerServerCommand('gg_end_warmup', servercmd_end_warmup,
        "Immediately ends the warmup round if there is one in progress.")


def unload():
    # Cancel any do_warmup delays
    gamethread.cancelDelayed("gg_do_warmup")

    # Deleting warmup timer
    warmupCountDown = repeat.find('gungameWarmupTimer')

    # If the warmup timer exists, stop and delete it
    if warmupCountDown:
        warmupCountDown.stop()
        warmupCountDown.delete()

    # Reset server vars
    reset_server_vars()

    # Unregister the server command that cancels an in-progress warmup round
    cmdlib.unregisterServerCommand('gg_end_warmup')


# =============================================================================
# >> COMMAND CALLBACKS
# =============================================================================
def servercmd_end_warmup(args):  # args are ignored, but needed for server cmd
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


# =============================================================================
# >> GAME EVENTS
# =============================================================================
def es_map_start(event_var):
    # Cancel any do_warmup delays
    gamethread.cancelDelayed("gg_do_warmup")

    # Looking for running warmup timer
    warmupCountDown = repeat.find('gungameWarmupTimer')
    if warmupCountDown:

        # We are comming in from another warmup round ?
        if warmupCountDown.status() == 2:

            # Stop timer
            warmupCountDown.stop()

            gamethread.delayedname(1, "gg_do_warmup", do_warmup, False)
            return

    # Start warmup timer. This is delayed to ensure that all addons get to fire
    # es_map_start events before priority addons are set.
    gamethread.delayedname(1, "gg_do_warmup", do_warmup)


def hegrenade_detonate(event_var):
    # Making sure warmup round is running
    warmupCountDown = repeat.find('gungameWarmupTimer')

    if not warmupCountDown:
        return

    # Is the warmup weapon hegrenade?
    if warmup_weapon != 'hegrenade':
        return

    # Get player userid and player object
    userid = int(event_var['userid'])

    # Is the client on the server?
    if not es.exists('userid', userid) and userid != 0:
        return

    # Is spectator?
    if int(event_var['es_userteam']) < 2:
        return

    # Is player dead?
    if getPlayer(userid).isdead:
        return

    Player(userid).give('hegrenade')


def player_spawn(event_var):
    # Is spectator?
    if int(event_var['es_userteam']) < 2:
        return

    # Set player's id
    userid = int(event_var['userid'])

    # Is player dead?
    if getPlayer(userid).isdead:
        return

    # If it is the last split second before mp_restartgame fires, protect the
    # player
    if giveGodMode:
        getPlayer(userid).godmode = 1

    # Making sure warmup round is running
    warmupCountDown = repeat.find('gungameWarmupTimer')

    if not warmupCountDown:
        return

    # Get player object
    ggPlayer = Player(userid)

    # Check if the warmup weapon is a knife
    if warmup_weapon == 'knife':
        es.sexec(userid, 'use weapon_knife')
        return

    delay = 0.05

    if es.isbot(userid):
        delay += 0.2

    # Strip the player's weapons (split second delay)
    gamethread.delayed(delay, ggPlayer.strip, (True, [warmup_weapon]))

    # Delay giving the weapon by a split second, because the code in round
    #   start removes all weapons
    gamethread.delayed((delay), ggPlayer.give, (warmup_weapon, True, True))


# =============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# =============================================================================
def get_warmup_weapon():
    '''
    Used to get the warmup weapon from other addons.
    '''
    return warmup_weapon


def set_warmup_weapon():
    global warmup_weapon, random_warmup_weapons, warmupWeaponSetOnLoad

    # If the warmup weapon was just set when gg_warmup_round was loaded, do not
    # set it again
    if warmupWeaponSetOnLoad:
        warmupWeaponSetOnLoad = False
        return

    # If the random weapons list has more than one item in it
    if len(random_warmup_weapons) > 1:
        # Remove the first item and set the warmup weapon to the next in line
        random_warmup_weapons.pop(0)
        warmup_weapon = random_warmup_weapons[0]
        # If the warmup weapon includes weapon_, remove the prefix
        if warmup_weapon[:7] == "weapon_":
            warmup_weapon = warmup_weapon[7:]
    # If there is nothing in the random weapons list
    else:
        # If the warmup weapon is set to #random
        if str(gg_warmup_weapon) == "#random":
            # Make a random list, and select the first one
            random_warmup_weapons = possible_random_weapons
            shuffle(random_warmup_weapons)
            warmup_weapon = random_warmup_weapons[0][7:]
        # If the warmup weapon is set to a list of possible weapons
        elif "," in str(gg_warmup_weapon):
            # Get the list of possible weapons, shuffle it, and select the
            # first one
            random_warmup_weapons = str(gg_warmup_weapon).split(",")
            shuffle(random_warmup_weapons)
            warmup_weapon = random_warmup_weapons[0]
        # If the warmup weapon is neither #random or a list
        else:
            # If the warmup weapon is 0, , or 0.0, set it to the first level
            # weapon
            if str(gg_warmup_weapon) in ('0', '', '0.0'):
                warmup_weapon = get_level_weapon(1)
            # The warmup weapon must be the name of a single weapon
            else:
                warmup_weapon = str(gg_warmup_weapon)


def add_priority_addon(name):
    priority_addons_added.append(name)
    PriorityAddon().append(name)


def do_warmup(useBackupVars=True):
    # Set the new warmup weapon
    set_warmup_weapon()

    # Looking for warmup timer
    warmupCountDown = repeat.find('gungameWarmupTimer')

    if useBackupVars:
        # Setting globals for backup variables
        global mp_freezetime_backup
        global gg_dead_strip_backup
        global gg_deathmatch_backup
        global gg_elimination_backup

        # Setting backup variables
        mp_freezetime_backup = int(mp_freezetime)
        gg_dead_strip_backup = int(gg_dead_strip)
        gg_deathmatch_backup = int(gg_deathmatch)
        gg_elimination_backup = int(gg_elimination)

    # Setting mp_freezetime
    mp_freezetime.set(0)

    # Added priority addons list
    del priority_addons_added[:]

    # Adding warmup and dead strip, and other addons we don't mind running
    # during gg_warmup_round to the priority addons list
    add_priority_addon('gg_warmup_round')
    add_priority_addon("gg_dead_strip")
    add_priority_addon("gg_noblock")
    add_priority_addon("gg_dissolver")

    # If gg_dead_strip is not loaded, load it
    if not int(gg_dead_strip):
        gg_dead_strip.set(1)
        addon_load("gg_dead_strip")

    # If deathmatch is enabled on the server, and elimination is not
    if int(gg_deathmatch_backup) and not int(gg_elimination_backup):
        # If we have no warmup deathmatch, we need to unload deathmatch
        if not int(gg_warmup_deathmatch) and int(gg_deathmatch):
            gg_deathmatch.set(0)
            check_unload("gg_deathmatch")
    # Otherwise, if elimination is on the server
    elif int(gg_elimination_backup):
        # If we have no warmup elimination, we need to unload elimination
        if not int(gg_warmup_elimination) and int(gg_elimination):
            gg_elimination.set(0)
            check_unload("gg_elimination")

    # If only one warmup mode is selected, proceed
    if not (int(gg_warmup_deathmatch) and int(gg_warmup_elimination)):

        # Added a delay, so we don't encounter an error when loading
        # one right after unloading the other (due to dependencies)
        gamethread.delayed(0, load_warmup_addons)

    # Start it up if it exists
    if warmupCountDown:
        warmupCountDown.stop()
        warmupCountDown.start(1, int(gg_warmup_timer) + GG_WARMUP_EXTRA_TIME)
        return

    # Create a timer
    warmupCountDown = repeat.create('gungameWarmupTimer', count_down)
    warmupCountDown.start(1, int(gg_warmup_timer) + GG_WARMUP_EXTRA_TIME)


def load_warmup_addons():
    # If warmup deathmatch is enabled, add it to priority addons
    if int(gg_warmup_deathmatch):
        add_priority_addon('gg_deathmatch')
        # If deathmatch is not enabled, we need to load it now
        if not int(gg_deathmatch_backup) and not int(gg_deathmatch):
            gg_deathmatch.set(1)
            addon_load("gg_deathmatch")
    # Otherwise, if warmup elimination is enabled, add it to priority
    # addons
    elif int(gg_warmup_elimination):
        add_priority_addon('gg_elimination')
        # If elimination is not enabled, or deathmatch is enabled due to
        # both dm and elim set to 1 and dm overruling elim, we need to load
        # it now.
        if (not int(gg_elimination_backup) or (int(gg_deathmatch_backup)
          and int(gg_elimination_backup))) and not int(gg_elimination):
            gg_elimination.set(1)
            addon_load("gg_elimination")


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
    global giveGodMode
    # For newly spawning players, give them godMode
    giveGodMode = True

    # Give players godmode so that they can't level up
    for player in getPlayerList("#alive"):
        player.godmode = 1

    # Remove addons added to priority_addons
    for addedAddon in priority_addons_added:
        PriorityAddon().remove(addedAddon)

    # Fire gg_start event
    GG_Start().fire()


def remove_godmode():
    '''
    Ran during the first round to make sure no players have godmode.
    '''
    global giveGodMode
    # No longer give godMode to newly spawning players
    giveGodMode = False

    for player in getPlayerList("#alive"):
        player.godmode = 0


def end_warmup(message):
    # Send hint
    hudhint('#human', message)

    # Play beep
    play_beep()

    # Delete the timer
    repeat.delete('gungameWarmupTimer')

    # Reset server vars back
    reset_server_vars()


def play_beep():
    for userid in getUseridList('#human'):
        Player(userid).playsound('countDownBeep')


def reset_server_vars():
    # If both warmup addons were loaded, we did no loading, so do no unloading
    if not (int(gg_warmup_deathmatch) and int(gg_warmup_elimination)):
        # If warmup deathmatch was enabled
        if int(gg_warmup_deathmatch):
            # Unload gg_deathmatch if we are not going into deathmatch gameplay
            # now
            if not int(gg_deathmatch_backup) and int(gg_deathmatch):
                gg_deathmatch.set(0)
                check_unload("gg_deathmatch")
        # If warmup elimination was enabled
        elif int(gg_warmup_elimination):
            # Unload gg_elimination if we are not going into elimination
            # gameplay now
            if not int(gg_elimination_backup) and int(gg_elimination):
                gg_elimination.set(0)
                check_unload("gg_elimination")

    # Check if deathmatch or elimination needs loaded
    if int(gg_deathmatch_backup) or int(gg_elimination_backup):

        # Added delay due to sharing dependency errors
        gamethread.delayed(0, load_gg_addons)

    # If gg_dead_strip disabled before warmup, disable it again
    if not gg_dead_strip_backup and int(gg_dead_strip):
        gg_dead_strip.set(0)
        check_unload("gg_dead_strip")

    # Changing mp_freezetime back
    if int(mp_freezetime) != mp_freezetime_backup:
        mp_freezetime.set(mp_freezetime_backup)


def load_gg_addons():
    # If we are going into deathmatch gameplay
    if int(gg_deathmatch_backup):
        # If we didn't already choose to leave deathmatch on above, load it
        if not int(gg_warmup_deathmatch) and not int(gg_deathmatch):
            gg_deathmatch.set(1)
            addon_load("gg_deathmatch")
    # If we are going into elimination gameplay
    elif int(gg_elimination_backup):
        # If we didn't already choose to leave elimination on above, load it
        if not int(gg_warmup_elimination) and not int(gg_elimination):
            gg_elimination.set(1)
            addon_load("gg_elimination")


def check_unload(addon):
    if addon in AddonManager().__loaded__:
        addon_unload(addon)
