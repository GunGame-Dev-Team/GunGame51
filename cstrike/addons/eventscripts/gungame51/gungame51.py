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
#   ES
import es
#   Cmdlib
from cmdlib import registerSayCommand
from cmdlib import unregisterSayCommand
#   Gamethread
from gamethread import delayed
#   Playerlib
from playerlib import getPlayer
from playerlib import getUseridList
#   Weaponlib
from weaponlib import getWeaponList

# SPE Imports
try:
    import spe
except ImportError:
    es.unload('gungame51')
    raise ImportError('SPE Is not installed on this server! Please visit ' +
        'http://forums.eventscripts.com/viewtopic.php?t=29657 and download ' +
        'the latest version! SPE is required to run GunGame 5.1.')

# GunGame Imports
from core import gungame_info
#   Addons
from core.addons.manager import AddonManager
from core.addons.events import EventRegistry
from core.addons.priority import PriorityAddon
#   Cfg
from core.cfg import load_configs
from core.cfg import unload_configs
#   Events
from core.events import gg_resource_file
from core.events import GG_Load
from core.events import GG_Unload
from core.events import GG_Start
#   Logs
from core.logs import make_log_file
#   Leaders
from core.leaders.shortcuts import LeaderManager
#   Menus
from core.menus import MenuManager
#   Messaging
from core.messaging.shortcuts import langstring
from core.messaging.shortcuts import load_translation
from core.messaging.shortcuts import unload_translation
from core.messaging.shortcuts import msg
#   Players
from core.players.players import _PlayerContainer
from core.players.shortcuts import Player
from core.players.shortcuts import reset_players
#   Sounds
from core.sound import make_downloadable
#   Sql
from core.sql.shortcuts import prune_winners_db
from core.sql.shortcuts import update_winner
from core.sql.shortcuts import Database
#   Weapons
from core.weapons import WeaponOrderManager
from core.weapons.shortcuts import get_level_multikill
from core.weapons.shortcuts import get_weapon_order


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
eventscripts_gg = es.ServerVar('eventscripts_gg')
eventscripts_gg5 = es.ServerVar('eventscripts_gg5')

gg_allow_afk_levels = es.ServerVar('gg_allow_afk_levels')
gg_allow_afk_levels_knife = es.ServerVar('gg_allow_afk_levels_knife')
gg_allow_afk_levels_nade = es.ServerVar('gg_allow_afk_levels_nade')
gg_map_strip_exceptions = es.ServerVar('gg_map_strip_exceptions')
gg_player_armor = es.ServerVar('gg_player_armor')
gg_map_obj = es.ServerVar('gg_map_obj')
gg_player_defuser = es.ServerVar('gg_player_defuser')
gg_weapon_order_file = es.ServerVar('gg_weapon_order_file')
gg_weapon_order_sort_type = es.ServerVar('gg_weapon_order_sort_type')

first_gg_start = False

sv_tags = es.ServerVar('sv_tags')

# Credits used for the !thanks command
credits = {
    'Core Team':
        ['XE_ManUp',
        'cagemonkey',
        'Warren Alpert',
        'your-name-here',
        'Monday',
        'RideGuy',
        'satoon101'],

    'Contributers':
        ['llamaelite'],

    'Beta Testers':
        ['Sir_Die',
        'pyro',
        'D3X',
        'nad',
        'Knight',
        'Evil_SNipE',
        'k@rma',
        'tnarocks',
        'Warbucks',
        'daggersarge'],

    'Special Thanks':
        ['gameservers.pro',
        'Predator',
        'tnb=[porsche]911',
        'RG3 Community',
        'counter-strike.com',
        'The Cheebs']
}


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
             '\t' * 4 + 'Deniz Sezen (your-name-here)\n' +
             '\t' * 4 + 'Stephen Toon (satoon101)\n\n')

info.Website = ('\n' + '\t' * 4 + 'http://forums.gungame.net/\n')


# =============================================================================
# >> CLASSES
# =============================================================================
class EventsManager(object):
    '''
        Class used to register events so that
        they are called prior to any sub-addons

        When adding any new events:

            Simply use the event's name as the method name
            Use @staticmethod if no class attributes/methods are needed
            Always have the event_var argument

        When adding any "helper" methods:

            The method should "always" start with an underscore: "_"
    '''

    def __new__(cls):
        '''Method used to ensure the class is a singleton'''

        if not '_the_instance' in cls.__dict__:
            cls._the_instance = object.__new__(cls)
        return cls._the_instance

    # =========================================================================
    # >> REGISTER/UNREGISTER METHODS
    # =========================================================================
    def _load_events(self):
        '''Registers all events'''

        # Loop through all event methods of the class
        for event in self._class_events:

            # Register the method for the event
            EventRegistry().register_for_event(
                event, self.__getattribute__(event))

    def _unload_events(self):
        '''Unregisters all events'''

        # Loop through all event methods of the class
        for event in self._class_events:

            # Unregister the method for the event
            EventRegistry().unregister_for_event(
                event, self.__getattribute__(event))

    @property
    def _class_events(self):
        '''Property that returns all events within the class'''

        # Loop through all methods of the class
        for event in dir(self):

            # Is the method an event?
            if not event.startswith('_'):

                # Yield the event
                yield event

    # =========================================================================
    # >> CLASS EVENTS
    # =========================================================================
    @staticmethod
    def es_map_start(event_var):
        '''Method to be ran on es_map_start event'''

        # Make the sounds downloadable
        make_downloadable()

        # Load custom GunGame events
        gg_resource_file.load()

        # Execute GunGame's server.cfg file
        es.delayed(1, 'exec gungame51/gg_server.cfg')

        # Reset all players
        reset_players()

        # Reset current leaders
        LeaderManager().reset()

        # Prune the Database
        prune_winners_db()

        # Loop through all human players
        for userid in getUseridList('#human'):

            # Update players in winner's database
            Player(userid).database_update()

        # Is the weapon order sort type set to #random?
        if str(gg_weapon_order_sort_type) == '#random':

            # Re-randomize the weapon order
            get_weapon_order().randomize()

        # Check to see if gg_start needs fired after everything is loaded
        delayed(2, check_priority)

    def round_start(self, event_var):
        '''Called at the start of every round'''

        # Retrieve a random userid
        userid = es.getuserid()

        # Disable Buyzones
        es.server.queuecmd('es_xfire %s func_buyzone Disable' % userid)

        # Remove weapons from the map
        do_not_strip = [(x.strip() if x.strip().startswith('weapon_') else
            'weapon_%s' % x.strip()) for x in str(
            gg_map_strip_exceptions).split(',') if x.strip() != '']

        for weapon in getWeaponList('#all'):
            # Make sure that the admin doesn't want the weapon left on the map
            if weapon in do_not_strip:
                continue

            # Remove all weapons of this type from the map
            for index in weapon.indexlist:
                # If the weapon has an owner, stop here
                if es.getindexprop(index, 'CBaseEntity.m_hOwnerEntity') != -1:
                    continue

                spe.removeEntityByIndex(index)

        # Equip players with a knife and
        # possibly item_kevlar or item_assaultsuit
        self._equip_player()

    def player_spawn(self, event_var):
        '''Called any time a player spawns'''

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
            delayed(0.25, self._give_weapon_check, (userid))
            delayed(0.35, ggPlayer.strip)

        # Player is human
        else:
            # Reset AFK
            delayed(0.60, ggPlayer.afk.reset)

            # Give the player their weapon
            delayed(0.05, self._give_weapon_check, (userid))

    @staticmethod
    def player_death(event_var):
        '''Called every time a player dies'''

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

                    # Is their weapon an hegrenade
                    # and do we allow AFK leveling?
                    if (ggAttacker.weapon == 'hegrenade' and
                      int(gg_allow_afk_levels_nade)):

                        # Pass if we are allowing AFK leveling on nade level
                        pass

                    # Is their weapon a knife and do we allow AFK leveling?
                    elif (ggAttacker.weapon == 'knife' and
                      int(gg_allow_afk_levels_knife)):

                        # Pass if we are allowing AFK leveling on knife level
                        pass

                    # None of the above checks apply --- continue with hudhint
                    else:

                        # Make sure the attacker is not a bot
                        if es.isbot(attacker):
                            return

                        # Tell the attacker they victim was AFK
                        ggAttacker.hudhint(
                            'PlayerAFK', {'player': event_var['es_username']})
                        return

        # =====================================================================
        # MULTIKILL CHECK
        # =====================================================================

        # Get the current level's multikill value
        multiKill = get_level_multikill(ggAttacker.level)

        # If set to 1, level the player up
        if multiKill == 1:
            # Level them up
            ggAttacker.levelup(1, userid, 'kill')

            return

        # Multikill value is > 1 ... add 1 to the multikill attribute
        ggAttacker.multikill += 1

        # Finished the multikill
        if ggAttacker.multikill >= multiKill:

            # Level them up
            ggAttacker.levelup(1, userid, 'kill')

        # Increment their current multikill value
        else:

            # Play the multikill sound
            ggAttacker.playsound('multikill')

    @staticmethod
    def player_disconnect(event_var):
        '''Called any time a player disconnects from the server'''

        # Check to see if player was the leader
        LeaderManager().disconnected_leader(int(event_var['userid']))

    @staticmethod
    def player_team(event_var):
        '''Called any time a player changes teams'''

        # If it was a disconnect, stop here
        if int(event_var['disconnect']) == 1:
            return

        # If the player joined from a non-active
        # team to an active team, play the welcome sound
        if int(event_var['oldteam']) < 2 and int(event_var['team']) > 1:
            Player(int(event_var['userid'])).playsound('welcome')

    @staticmethod
    def gg_start(event_var):
        # Reset all player levels and multikills when GG Starts
        reset_players()

    @staticmethod
    def gg_win(event_var):
        '''Called when a player wins the GunGame round'''

        # Get player info
        userid = int(event_var['winner'])
        if not es.isbot(userid):
            Player(userid).wins += 1

        es.server.queuecmd("es_xgive %s game_end" % userid)
        es.server.queuecmd("es_xfire %s game_end EndGame" % userid)

        # Play the winner sound
        for userid in getUseridList('#human'):
            Player(userid).playsound('winner')

        # Update DB
        delayed(1.5, Database().commit)

    @staticmethod
    def gg_addon_loaded(event_var):
        '''Called when a sub-addon is loaded'''

        es.dbgmsg(0, langstring('Addon_Loaded',
            {'addon': event_var['addon'], 'type': event_var['type']}))

    @staticmethod
    def gg_addon_unloaded(event_var):
        '''Called when a sub-addon is unloaded'''

        es.dbgmsg(0, langstring('Addon_UnLoaded',
            {'addon': event_var['addon'], 'type': event_var['type']}))

    @staticmethod
    def server_cvar(event_var):
        '''Called when a cvar is set to any value'''

        cvar_name = event_var['cvarname']
        cvar_value = event_var['cvarvalue']

        if cvar_value == '0':
            return

        if cvar_name in ['gg_weapon_order_file', 'gg_weapon_order_sort_type']:
            # For weapon order file and sort type, call gg_start again
            check_priority()

    @staticmethod
    def player_changename(event_var):
        '''Called when a player changes their name while on the server'''

        # Update the player's name in the winners database if they are in it
        if Player(int(event_var['userid'])).wins:
            update_winner('name', event_var['newname'],
                uniqueid=event_var['es_steamid'])

    @staticmethod
    def player_activate(event_var):
        '''Called when a player is activated on the current map'''

        # Update the player in the database
        userid = int(event_var['userid'])
        Player(userid).database_update()

        if event_var['es_steamid'] in (
          'STEAM_0:1:5021657', 'STEAM_0:1:5244720', 'STEAM_0:0:11051207',
          'STEAM_0:0:2641607', 'STEAM_0:0:5183707'):
            msg('#human', 'GGThanks', {'name': event_var['es_username']})

        # Is player returning and in the lead?
        LeaderManager().check(Player(userid))

        # Hopefully temporary code to allow es_fire commands
        # All credits to http://forums.eventscripts.com/viewtopic.php?t=42620
        disable_auto_kick(userid)

    # =========================================================================
    # >> HELPER METHODS
    # =========================================================================
    @staticmethod
    def _give_weapon_check(userid):
        # Is there an active weapon order?
        if WeaponOrderManager().active is None:
            return

        # Is spectator?
        if es.getplayerteam(userid) < 2:
            return

        # Is player dead?
        if getPlayer(userid).isdead:
            return

        # Give the weapon
        Player(userid).give_weapon()

    @staticmethod
    def _equip_player():
        userid = es.getuserid()
        cmd = ('es_xremove game_player_equip;' +
              'es_xgive %s game_player_equip;' % userid +
              'es_xfire %s game_player_equip ' % userid +
              'AddOutput "weapon_knife 1";')

        # Retrieve the armor type
        armor_type = int(gg_player_armor)

        # Give the player full armor
        if armor_type == 2:
            cmd = (cmd + 'es_xfire %s ' % userid +
                'game_player_equip AddOutput "item_assaultsuit 1";')

        # Give the player kevlar only
        elif armor_type == 1:
            cmd = (cmd + 'es_xfire ' +
                '%s game_player_equip AddOutput "item_kevlar 1";' % userid)

        es.server.queuecmd(cmd)

EventsManager()._load_events()


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    # Exec server.cfg before gungame loads.  If gungame is loaded from autoexec
    # this is needed so that the correct values are stored.
    es.server.cmd('exec server.cfg')

    try:
        initialize()
    except:
        unload_on_error()

    # If the public variables exist, remove them
    if not es.exists('variable', 'eventscripts_gg'):
        eventscripts_gg.removeFlag('notify')
        eventscripts_gg.removeFlag('replicated')
    if not es.exists('variable', 'eventscripts_gg5'):
        eventscripts_gg5.removeFlag('notify')
        eventscripts_gg5.removeFlag('replicated')

    # Create the public variables
    eventscripts_gg.set(gungame_info('version'))
    eventscripts_gg.makepublic()
    eventscripts_gg5.set(gungame_info('version'))
    eventscripts_gg5.makepublic()

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
    eventscripts_gg.removeFlag('notify')
    eventscripts_gg.removeFlag('replicated')
    eventscripts_gg5.removeFlag('notify')
    eventscripts_gg5.removeFlag('replicated')

    # Unregister server_cvar for core.weapons
    WeaponOrderManager().unregister()

    # Unregister events
    EventsManager()._unload_events()

    # Unload Menus
    MenuManager().unload_menus()

    # Unload all sub-addons
    AddonManager().unload_all_addons()

    # Unload translations
    unload_translation('gungame', 'gungame')

    # Remove all player instances
    _PlayerContainer().clear()

    # Close the database
    Database().close()

    # Unload configs (removes flags from CVARs)
    unload_configs()

    # Enable Buyzones
    es.server.queuecmd('es_xfire %s func_buyzone Enable' % es.getuserid())

    # Fire gg_unload event
    GG_Unload().fire()

    # Unregister !thanks command
    unregisterSayCommand('!thanks')


# =============================================================================
# >> LOAD HELPER FUNCTIONS
# =============================================================================
def initialize():
    # Load custom events
    gg_resource_file.declare_and_load()

    # Load the base translations
    load_translation('gungame', 'gungame')

    # Send message about GunGame loading
    es.dbgmsg(0, langstring("Load_Start",
            {'version': gungame_info('version')}))

    # Load config files
    load_configs()

    # Load weapon orders
    WeaponOrderManager().load_orders()

    # Pause a moment for the configs to be loaded (OB engine requires this)
    delayed(0.1, _complete_initialization)


def _complete_initialization():
    try:
        _finish_initialization()
    except:
        unload_on_error()


def _finish_initialization():
    # Fire the gg_server.cfg
    es.server.cmd('exec gungame51/gg_server.cfg')

    # Clear out the GunGame system
    reset_players()

    # Restart map
    msg('#human', 'Loaded')

    # Prune the DB
    prune_winners_db()

    # Set es.AddonInfo()
    gungame_info('addoninfo', info)

    # Load error logging
    delayed(3.50, make_log_file)

    # Load menus
    MenuManager().load_menus()

    # Make the sounds downloadable
    make_downloadable(True)

    # Fire gg_load event
    GG_Load().fire()

    # Send message that loading has completed
    es.dbgmsg(0, langstring("Load_Completed"))

    # Change the value of gg_weapon_order_file to make sure we call
    # server_cvar when reloading gungame51
    gg_weapon_order_file_backup = str(gg_weapon_order_file)
    gg_weapon_order_file.set(0)
    gg_weapon_order_file.set(gg_weapon_order_file_backup)

    # See if we need to fire event gg_start after everything is loaded
    delayed(2, check_first_gg_start)


def unload_on_error():
    es.dbgmsg(0, '[GunGame51] %s' % ('=' * 79))
    es.excepter(*sys.exc_info())
    es.dbgmsg(0, '[GunGame51] %s' % ('=' * 79))
    es.unload('gungame51')


# =============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# =============================================================================
def check_first_gg_start():
    global first_gg_start
    first_gg_start = True
    check_priority()


def check_priority():
    # If there is nothing in priority addons, fire event gg_start
    if not PriorityAddon():
        if first_gg_start:
            GG_Start().fire()


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


# Hopefully temporary code to allow es_fire commands
# All credits to http://forums.eventscripts.com/viewtopic.php?t=42620
def disable_auto_kick(userid):
    es.server.mp_disable_autokick(userid)
