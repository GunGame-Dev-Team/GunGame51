# ../gungame51.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python imports
import sys

# EventScripts Imports
import es
import gamethread
from playerlib import getPlayer
from playerlib import getUseridList
from weaponlib import getWeaponList
from cmdlib import registerSayCommand
from cmdlib import unregisterSayCommand

# SPE Imports
try:
    import spe
except ImportError:
    es.unload('gungame51')
    raise ImportError('SPE Is not installed on this server! Please visit ' +
        'http://forums.eventscripts.com/viewtopic.php?t=29657 and download ' +
        'the latest version! SPE is required to run GunGame 5.1.')


# GunGame Imports

#   Core Function Imports
from core import get_game_dir

#    Error Logging Function Imports
from core.logs import make_log_file

#    Weapon Function Imports
from core.weapons.shortcuts import set_weapon_order
from core.weapons.shortcuts import get_level_multikill
from core.weapons import WeaponManager
from core.weapons import load_weapon_orders

#    Config Function Imports
from core.cfg.shortcuts import ConfigManager

#    Addon Function Imports
from core.addons import AddonManager
from core.addons import PriorityAddon
from core.addons import gungame_info

#    Player Function Imports
from core.players.players import _PlayerContainer
from core.players.shortcuts import Player
from core.players.shortcuts import resetPlayers
from core.players.shortcuts import setAttribute

#    Leaders Function Imports
from core.leaders.shortcuts import LeaderManager

#   Messaging Function Imports
from core.messaging.shortcuts import langstring
from core.messaging.shortcuts import loadTranslation
from core.messaging.shortcuts import unloadTranslation
from core.messaging.shortcuts import msg

#   Event Function Imports
from core.events import ggResourceFile
from core.events import GG_Load
from core.events import GG_Unload
from core.events import GG_Start

#   Sound Function Imports
from core.sound import make_downloadable

#   Database
from core.sql.shortcuts import prune_winners_db
from core.sql.shortcuts import update_winner
from core.sql.shortcuts import Database

#   Menus
from core.menus import MenuManager

# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
gg_allow_afk_levels = es.ServerVar('gg_allow_afk_levels')
gg_allow_afk_levels_knife = es.ServerVar('gg_allow_afk_levels_knife')
gg_allow_afk_levels_nade = es.ServerVar('gg_allow_afk_levels_nade')
gg_map_strip_exceptions = es.ServerVar('gg_map_strip_exceptions')
gg_multi_round = es.ServerVar('gg_multi_round')
gg_multi_round_intermission = es.ServerVar('gg_multi_round_intermission')
gg_multikill_override = es.ServerVar('gg_multikill_override')
gg_player_armor = es.ServerVar('gg_player_armor')
gg_map_obj = es.ServerVar('gg_map_obj')
gg_player_defuser = es.ServerVar('gg_player_defuser')
gg_warmup_round = es.ServerVar('gg_warmup_round')
gg_warmup_round_backup = None
gg_weapon_order_file = es.ServerVar('gg_weapon_order_file')
gg_weapon_order_sort_type = es.ServerVar('gg_weapon_order_sort_type')
#firstPlayerSpawned = False
firstGGStart = False

sv_tags = es.ServerVar('sv_tags')

# Credits used for the !thanks command
credits = {
    'Project Leaders':
        ['XE_ManUp',
        'Warren Alpert',
        'your-name-here',
        'Monday'],

    'Developers':
        ['satoon101',
        'cagemonkey',
        'llamaelite',
        'RideGuy'],

    'Beta Testers':
        ['Sir_Die',
        'pyro',
        'D3X',
        'nad',
        'Knight',
        'Evil_SNipE',
        'k@rma',
        'tnarocks',
        'Warbucks'],

    'Special Thanks':
        ['gameservers.pro',
        'Predator',
        'tnb=[porsche]911',
        'RG3 Community',
        'counter-strike.com',
        'The Cheebs']
}


# =============================================================================
# >> CLASSES
# =============================================================================
class RoundInfo(object):
    def __new__(cls, *p, **k):
        if not '_the_instance' in cls.__dict__:
            cls._the_instance = object.__new__(cls)
            # Set round information variables
            cls._the_instance.round = 1
        return cls._the_instance

    @property
    def remaining(self):
        total = int(gg_multi_round) - self.round
        return total if total > 0 else 0


# =============================================================================
# >> ADDON REGISTRATION
# =============================================================================
info = es.AddonInfo()
del info['keylist'][:]

info.About = ('\n' +
                '\t' * 4 + 'GunGame 5.1 (v%s)\n\n' % gungame_info('version'))

info.Authors = ('\n' +
             '\t' * 4 + 'Michael Barr (XE_ManUp)\n' +
             '\t' * 4 + 'Luke Robinson (Monday)\n' +
             '\t' * 4 + 'Warren Alpert\n' +
             '\t' * 4 + 'Paul Smith (RideGuy)\n' +
             '\t' * 4 + 'Deniz Sezen (your-name-here)\n\n')

info.Website = ('\n' + '\t' * 4 + 'http://forums.gungame.net/\n')


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    # Load translations
    loadTranslation('gungame', 'gungame')

    # Exec server.cfg before gungame loads.  If gungame is loaded from autoexec
    # this is needed so that the correct values are stored.
    es.server.cmd('exec server.cfg')

    try:
        initialize()
    except:
        unload_on_error()

    # If the public variables exist, remove them
    if not es.exists('variable', 'eventscripts_gg'):
        es.ServerVar('eventscripts_gg').removeFlag('notify')
        es.ServerVar('eventscripts_gg').removeFlag('replicated')
    if not es.exists('variable', 'eventscripts_gg5'):
        es.ServerVar('eventscripts_gg5').removeFlag('notify')
        es.ServerVar('eventscripts_gg5').removeFlag('replicated')

    # Create the public variables
    es.ServerVar('eventscripts_gg').set(gungame_info('version'))
    es.ServerVar('eventscripts_gg').makepublic()
    es.ServerVar('eventscripts_gg5').set(gungame_info('version'))
    es.ServerVar('eventscripts_gg5').makepublic()

    # Register !thanks command
    registerSayCommand('!thanks', thanks, 'Displays a list of those involved' +
                       'with development and testing of GunGame.')

    # Add gungame to sv_tags
    tags = set(str(sv_tags).split(','))
    tags.add('gungame')
    sv_tags.set(','.join(tags))

    # Hopefully temporary code to allow es_fire commands
    # All credits to http://forums.eventscripts.com/viewtopic.php?t=42620
    for userid in es.getUseridList():
        disable_auto_kick(userid)


def unload():
    # Remove gungame from sv_tags
    tags = set(str(sv_tags).split(','))
    tags.discard('gungame')
    sv_tags.set(','.join(tags))

    # Remove the public variables
    es.ServerVar('eventscripts_gg').removeFlag('notify')
    es.ServerVar('eventscripts_gg').removeFlag('replicated')
    es.ServerVar('eventscripts_gg5').removeFlag('notify')
    es.ServerVar('eventscripts_gg5').removeFlag('replicated')

    from core.addons import dependencies
    # Create a copy of the dependencies dictionary
    dict_dependencies = dependencies.copy()

    # Unload Menus
    MenuManager().unload('#all')

    # Loop through addons that have required dependencies
    for addon in list(set(map((lambda (x, y): y), [(x, y) for x in \
        dict_dependencies for y in dict_dependencies[x]]))):

        # If an addon we just unloaded unloaded this addon, skip it
        if not addon in AddonManager().__loaded__:
            continue

        # Unload the addons that have required dependencies
        AddonManager().unload(addon, True)

    # Unload any remaining addons now that dependencies are handled
    for addon in AddonManager().__order__[:]:
        # If an addon we just unloaded unloaded this addon, skip it
        if not addon in AddonManager().__loaded__:
            continue

        AddonManager().unload(addon, True)

    # Unload translations
    unloadTranslation('gungame', 'gungame')

    # Remove all player instances
    _PlayerContainer().clear()

    # Close the database
    Database().close()

    # Unload configs (removes flags from CVARs)
    ConfigManager().unload_configs()

    # Enable Buyzones
    es.server.queuecmd('es_xfire %s func_buyzone Enable' % es.getuserid())

    # Fire gg_unload event
    GG_Unload().fire()

    # Unregister !thanks command
    unregisterSayCommand('!thanks')


def initialize():
    # Load custom events
    ggResourceFile.declare_and_load()

    es.dbgmsg(0, langstring("Load_Start",
        {'version': gungame_info('version')}))

    # Load all configs
    ConfigManager().load_configs()

    # Parse Weapon Order Files
    es.dbgmsg(0, langstring("Load_WeaponOrders"))
    load_weapon_orders()

    # Pause a moment for the configs to be loaded (OB engine requires this)
    gamethread.delayed(0.1, completeInitialize)


def completeInitialize():
    try:
        finishInitialize()
    except:
        unload_on_error()


def finishInitialize():
    # Print load started
    #es.dbgmsg(0, '[GunGame]' + '=' * 79)

    # Fire the gg_server.cfg
    es.server.cmd('exec gungame51/gg_server.cfg')

    # Clear out the GunGame system
    resetPlayers()

    # Restart map
    msg('#human', 'Loaded')

    # Fire gg_load event
    GG_Load().fire()

    # Print load completed
    #es.dbgmsg(0, '[GunGame] %s' % ('=' * 79))

    # Prune the DB
    prune_winners_db()

    # Set es.AddonInfo()
    gungame_info('addoninfo', info)

    # Load error logging
    gamethread.delayed(3.50, make_log_file)

    # Load menus
    es.dbgmsg(0, langstring("Load_Commands"))
    MenuManager().load('#all')

    # Make the sounds downloadable
    es.dbgmsg(0, langstring("Load_SoundSystem"))
    make_downloadable(True)

    # Set up "gg_multi_round"
    if int(gg_multi_round):
        RoundInfo().round = 1

    es.dbgmsg(0, langstring("Load_Completed"))

    # Change the value of gg_weapon_order_file to make sure we call
    # server_cvar when reloading gungame51
    gg_weapon_order_file_backup = str(gg_weapon_order_file)
    gg_weapon_order_file.set(0)
    gg_weapon_order_file.set(gg_weapon_order_file_backup)

    # See if we need to fire event gg_start after everything is loaded
    gamethread.delayed(2, first_gg_start)


def unload_on_error():
    es.dbgmsg(0, '[GunGame51] %s' % ('=' * 79))
    es.excepter(*sys.exc_info())
    es.dbgmsg(0, '[GunGame51] %s' % ('=' * 79))
    for delayname in ('gg_mp_restartgame',):
        gamethread.cancelDelayed(delayname)
    es.unload('gungame51')


# =============================================================================
# >> GAME EVENTS
# =============================================================================
def es_map_start(event_var):
    # Set firstPlayerSpawned to False, so player_spawn will know when the first
    # spawn is
    """
    global firstPlayerSpawned
    firstPlayerSpawned = False
    """

    # Make the sounds downloadable
    make_downloadable()

    # Load custom GunGame events
    ggResourceFile.load()

    # Execute GunGame's autoexec.cfg
    es.delayed('1', 'exec gungame51/gg_server.cfg')

    # Reset the GunGame players
    resetPlayers()

    # Reset the GunGame leaders
    LeaderManager().reset()

    # Prune the DB
    prune_winners_db()

    # Update players in winner's database
    for userid in getUseridList('#human'):
        Player(userid).database_update()

    # Set up "gg_multi_round"
    if int(gg_multi_round):
        RoundInfo().round = 1

    # Make sure gungameorder is set as the "current" order
    # This fixes an issue that caused gg_nade_bonus order to be
    # re-randomized instead of the gungame weapon_order
    WeaponManager().currentorder = WeaponManager().gungameorder

    # If gg_weapon_order_sort_type is #random, re-randomize it
    if str(gg_weapon_order_sort_type) == "#random":
        WeaponManager().type = "#random"

    # See if we need to fire event gg_start after everything is loaded
    gamethread.delayed(2, check_priority)


def first_gg_start():
    global firstGGStart
    firstGGStart = True
    check_priority()

def check_priority():
    # If there is nothing in priority addons, fire event gg_start
    if not PriorityAddon():
        if firstGGStart:
            GG_Start().fire()


def round_start(event_var):
    # Retrieve a random userid
    userid = es.getuserid()

    # Disable Buyzones
    es.server.queuecmd('es_xfire %s func_buyzone Disable' % userid)

    # Remove weapons from the map
    list_noStrip = [(x.strip() if x.strip().startswith('weapon_') else \
                    'weapon_%s' % x.strip()) for x in \
                    str(gg_map_strip_exceptions).split(',') if x.strip() != \
                    '']

    for weapon in getWeaponList('#all'):
        # Make sure that the admin doesn't want the weapon left on the map
        if weapon in list_noStrip:
            continue

        # Remove all weapons of this type from the map
        for index in weapon.indexlist:
            # If the weapon has an owner, stop here
            if es.getindexprop(index, 'CBaseEntity.m_hOwnerEntity') != -1:
                continue

            spe.removeEntityByIndex(index)

    # Equip players with a knife and possibly item_kevlar or item_assaultsuit
    equip_player()


def player_spawn(event_var):
    """
    # This should not matter any longer if my theory is correct:
    # When _PlayerContainer().reset() is called, old userids are removed.
    global firstPlayerSpawned

    if not firstPlayerSpawned:
        # Replace this with whatever _PlayerContainer() uses to remove
        # non-existant players
        _PlayerContainer().remove_old()

        # The first player has spawned
        firstPlayerSpawned = True

    """
    # Check for priority addons
    if PriorityAddon():
        return

    userid = int(event_var['userid'])

    # Is a spectator?
    if int(event_var['es_userteam']) < 2:
        return

    # Is player dead?
    if getPlayer(userid).isdead:
        return

    ggPlayer = Player(userid)

    # Do we need to give the player a defuser?
    if int(gg_player_defuser):

        # Is the player a CT?
        if int(event_var['es_userteam']) == 3:

            # Are we removing bomb objectives from map?
            if not int(gg_map_obj) in (1, 2):

                # Does the map have a bombsite?
                if len(es.getEntityIndexes('func_bomb_target')):

                    # Does the player already have a defuser?
                    if not getPlayer(userid).defuser:

                        # Give the player a defuser:
                        getPlayer(userid).defuser = 1

    # Strip bots (sometimes they keep previous weapons)
    if es.isbot(userid):
        gamethread.delayed(0.25, give_weapon_check, (userid))
        gamethread.delayed(0.35, ggPlayer.strip)

    # Player is human
    else:
        # Reset AFK
        gamethread.delayed(0.60, ggPlayer.afk.reset)

        # Give the player their weapon
        gamethread.delayed(0.05, give_weapon_check, (userid))


def player_death(event_var):
    # Check for priority addons
    if PriorityAddon():
        return

    # Set player ids
    userid = int(event_var['userid'])
    attacker = int(event_var['attacker'])

    # Is the attacker on the server?
    if not es.exists('userid', attacker):
        return

    # Suicide check
    if (attacker == 0 or attacker == userid):
        return

    # TEAM-KILL CHECK
    if (event_var['es_userteam'] == event_var['es_attackerteam']):
        return

    # Get victim object
    ggVictim = Player(userid)

    # Get attacker object
    ggAttacker = Player(attacker)

    # Check the weapon was correct (Normal Kill)
    if event_var['weapon'] != ggAttacker.weapon:
        return

    # Don't continue if the victim is AFK
    if not int(gg_allow_afk_levels):

        # Make sure the victim is not a bot
        if not es.isbot(userid):

            # Is AFK ?
            if ggVictim.afk():

                # Is their weapon an hegrenade and do we allow AFK leveling?
                if ggAttacker.weapon == 'hegrenade' and \
                    int(gg_allow_afk_levels_nade):

                        # Pass if we are allowing AFK leveling on nade level
                        pass

                # Is their weapon a knife and do we allow AFK leveling?
                elif ggAttacker.weapon == 'knife' and \
                    int(gg_allow_afk_levels_knife):
                        # Pass if we are allowing AFK leveling on knife level
                        pass

                # None of the above checks apply --- continue with hudhint
                else:
                    # Make sure the attacker is not a bot
                    if es.isbot(attacker):
                        return

                    # Tell the attacker they victim was AFK
                    ggAttacker.hudhint('PlayerAFK', {'player':
                                                     event_var['es_username']})
                    return

    # =========================================================================
    # MULTIKILL CHECK
    # =========================================================================

    # Get the current level's multikill value
    multiKill = get_level_multikill(ggAttacker.level)

    # If set to 1, level the player up
    if multiKill == 1:
        # Level them up
        ggAttacker.levelup(1, userid, 'kill')

        # Play the levelup sound
        ggAttacker.playsound('levelup')

        return

    # Multikill value is > 1 ... add 1 to the multikill attribute
    ggAttacker.multikill += 1

    # Finished the multikill
    if ggAttacker.multikill >= multiKill:
        # Level them up
        ggAttacker.levelup(1, userid, 'kill')

        # Play the levelup sound
        ggAttacker.playsound('levelup')

    # Increment their current multikill value
    else:

        # Play the multikill sound
        ggAttacker.playsound('multikill')


def player_disconnect(event_var):
    userid = int(event_var['userid'])

    # Check to see if player was the leader
    LeaderManager()._disconnected_leader(userid)


def player_team(event_var):
    # If it was a disconnect, stop here
    if int(event_var['disconnect']) == 1:
        return

    # If the player joined from a non-active team to an active team, play the
    # welcome sound
    if int(event_var['oldteam']) < 2 and int(event_var['team']) > 1:
        Player(int(event_var['userid'])).playsound('welcome')


def gg_win(event_var):
    # Get player info
    userid = int(event_var['winner'])
    if not es.isbot(userid):
        Player(userid).wins += 1

    if event_var['round'] == '0':
        # =====================================================================
        # MAP WIN
        # =====================================================================
        # End game
        es.server.queuecmd("es_xgive %s game_end" % userid)
        es.server.queuecmd("es_xfire %s game_end EndGame" % userid)

        # Play the winner sound
        for userid in getUseridList('#human'):
            Player(userid).playsound('winner')

    else:
        # =====================================================================
        # ROUND WIN
        # =====================================================================
        # Calculate round number
        RoundInfo().round += 1

        # Reset the players
        resetPlayers()

        # Freeze players and put them in god mode
        for playerid in es.getUseridList():
            getPlayer(playerid).freeze = True
            getPlayer(playerid).godmode = True

        # End the GunGame Round
        es.server.queuecmd('mp_restartgame 2')

        # Check to see if the warmup round needs to be activated
        if int(es.ServerVar('gg_multi_round_intermission')):
            if not int(gg_warmup_round):
                # Back up gg_warmup_round's value
                global gg_warmup_round_backup
                gg_warmup_round_backup = int(gg_warmup_round)

                # Load gg_warmup_round - loading will start the warmup timer
                es.server.queuecmd('gg_warmup_round 1')
            else:
                # Import and execute "do_warmup()" - starts the warmup timer
                from scripts.included.gg_warmup_round import do_warmup
                do_warmup()
        else:
            gamethread.delayed(2, GG_Start().fire())

        # Play the winner sound
        for userid in getUseridList('#human'):
            Player(userid).playsound('winner')

    # Update DB
    gamethread.delayed(1.5, Database().commit)


def gg_start(event_var):
    # Disable warmup due to "gg_multi_round"?
    if gg_warmup_round_backup != int(gg_warmup_round) and \
        gg_warmup_round_backup:
            es.server.queuecmd('gg_warmup_round 0')


def gg_addon_loaded(event_var):
    es.dbgmsg(0, langstring('Addon_Loaded',
        {'addon': event_var['addon'], 'type': event_var['type']}))


def gg_addon_unloaded(event_var):
    es.dbgmsg(0, langstring('Addon_UnLoaded',
        {'addon': event_var['addon'], 'type': event_var['type']}))


def server_cvar(event_var):
    cvarName = event_var['cvarname']

    # Make sure we have both set before setting the weapon order
    if cvarName == 'gg_weapon_order_file' and str(gg_weapon_order_sort_type) \
                == "0":
        return

    # Added just in case for print weapon order fix
    if cvarName == 'gg_weapon_order_file' and event_var['cvarvalue'] == '0':
        return

    if cvarName in ['gg_weapon_order_file', 'gg_weapon_order_sort_type',
                                                    'gg_multikill_override']:
        # For weapon order file and sort type,
        # reset player's levels and multikills to 1
        # and call gg_start again
        if cvarName != "gg_multikill_override":
            resetPlayers()
            check_priority()

        # Set the weapon order and set the weapon order type
        currentOrder = set_weapon_order(str(gg_weapon_order_file),
                                      str(gg_weapon_order_sort_type))

        # Set multikill override
        currentOrder.set_multikill_override(int(gg_multikill_override))


def player_changename(event_var):
    # Update the player's name in the winners database if they are in it
    if Player(int(event_var['userid'])).wins:
        update_winner('name', event_var['newname'],
            uniqueid=event_var['es_steamid'])


def player_activate(event_var):
    # Update the player in the database
    userid = int(event_var['userid'])
    Player(userid).database_update()

    if event_var['es_steamid'] in ('STEAM_0:1:5021657', 'STEAM_0:1:5244720',
      'STEAM_0:0:11051207', 'STEAM_0:0:2641607'):
        msg('#human', 'GGThanks', {'name': event_var['es_username']})

    # Is player returning and in the lead?
    LeaderManager().check(Player(userid))

    # Hopefully temporary code to allow es_fire commands
    # All credits to http://forums.eventscripts.com/viewtopic.php?t=42620
    disable_auto_kick(userid)


# =============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# =============================================================================
def thanks(userid, args):
    msg(userid, 'CheckConsole')
    es.cexec(userid, 'echo [GG Thanks] ')

    # Loop through the credits
    for x in credits.keys():
        # Print category
        es.cexec(userid, 'echo [GG Thanks] %s:' % (x))

        # Show all in this category
        for y in credits[x]:
            es.cexec(userid, 'echo [GG Thanks]    %s' % y)

        es.cexec(userid, 'echo [GG Thanks] ')


def equip_player():
    userid = es.getuserid()
    cmd = 'es_xremove game_player_equip;' + \
          'es_xgive %s game_player_equip;' % userid + \
          'es_xfire %s game_player_equip AddOutput "weapon_knife 1";' % userid

    # Retrieve the armor type
    armorType = int(gg_player_armor)

    # Give the player full armor
    if armorType == 2:
        cmd = cmd + \
            'es_xfire %s game_player_equip AddOutput "item_assaultsuit 1";' \
                % userid

    # Give the player kevlar only
    elif armorType == 1:
        cmd = cmd + \
            'es_xfire %s game_player_equip AddOutput "item_kevlar 1";' % userid

    es.server.queuecmd(cmd)


def give_weapon_check(userid):
    # Is spectator?
    if es.getplayerteam(userid) < 2:
        return

    # Is player dead?
    if getPlayer(userid).isdead:
        return

    # Give the weapon
    Player(userid).give_weapon()


# Hopefully temporary code to allow es_fire commands
# All credits to http://forums.eventscripts.com/viewtopic.php?t=42620
def disable_auto_kick(userid):
    es.server.mp_disable_autokick(userid)
