# ../modules/gameevents.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# EventScripts Imports
#   ES
import es
#   Gamethread
from gamethread import delayed
#   Playerlib
from playerlib import getPlayer
from playerlib import getUseridList
#   Weaponlib
from weaponlib import getWeaponList

# SPE Imports
from spe import removeEntityByIndex

# GunGame Imports
#   Modules
from active import ActiveInfo
from helpers import check_gg_start
from helpers import disable_auto_kick
from helpers import equip_player
from helpers import give_weapon_check
#   Events
from gungame51.core.events import gg_resource_file
#   Leaders
from gungame51.core.leaders.shortcuts import LeaderManager
#   Messaging
from gungame51.core.messaging.shortcuts import langstring
from gungame51.core.messaging.shortcuts import msg
#   Players
from gungame51.core.players.shortcuts import Player
from gungame51.core.players.shortcuts import reset_players
#   Sounds
from gungame51.core.sound import make_downloadable
#   Sql
from gungame51.core.sql.shortcuts import prune_winners_db
from gungame51.core.sql.shortcuts import update_winner
from gungame51.core.sql.shortcuts import Database
#   Weapons
from gungame51.core.weapons.shortcuts import get_level_multikill
from gungame51.core.weapons.shortcuts import get_weapon_order


# =========================================================================
# >> GLOBAL VARIABLES
# =========================================================================
gg_weapon_order_sort_type = es.ServerVar('gg_weapon_order_sort_type')
gg_map_strip_exceptions = es.ServerVar('gg_map_strip_exceptions')
gg_player_defuser = es.ServerVar('gg_player_defuser')
gg_map_obj = es.ServerVar('gg_map_obj')
gg_allow_afk_levels = es.ServerVar('gg_allow_afk_levels')
gg_allow_afk_levels_nade = es.ServerVar('gg_allow_afk_levels_nade')
gg_allow_afk_levels_knife = es.ServerVar('gg_allow_afk_levels_knife')


# =========================================================================
# >> MAP EVENTS
# =========================================================================
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
    delayed(2, check_gg_start)


# =========================================================================
# >> SERVER EVENTS
# =========================================================================
def server_cvar(event_var):
    '''Called when a cvar is set to any value'''

    cvar_name = event_var['cvarname']
    cvar_value = event_var['cvarvalue']

    if cvar_value == '0':
        return

    if cvar_name in ['gg_weapon_order_file', 'gg_weapon_order_sort_type']:
        # For weapon order file and sort type, call gg_start again
        check_gg_start()


# =========================================================================
# >> ROUND EVENTS
# =========================================================================
def round_start(event_var):
    '''Called at the start of every round'''

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

            removeEntityByIndex(index)

    # Equip players with a knife and
    # possibly item_kevlar or item_assaultsuit
    equip_player()


# =========================================================================
# >> PLAYER EVENTS
# =========================================================================
def player_spawn(event_var):
    '''Called any time a player spawns'''

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
        delayed(0.25, give_weapon_check, (userid))
        delayed(0.35, ggPlayer.strip)

    # Player is human
    else:
        # Reset AFK
        delayed(0.60, ggPlayer.afk.reset)

        # Give the player their weapon
        delayed(0.05, give_weapon_check, (userid))


def player_death(event_var):
    '''Called every time a player dies'''

    # Is the round active?
    if not ActiveInfo.round:

        # If not, do nothing
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


def player_disconnect(event_var):
    '''Called any time a player disconnects from the server'''

    # Check to see if player was the leader
    LeaderManager().disconnected_leader(int(event_var['userid']))


def player_team(event_var):
    '''Called any time a player changes teams'''

    # If it was a disconnect, stop here
    if int(event_var['disconnect']) == 1:
        return

    # If the player joined from a non-active
    # team to an active team, play the welcome sound
    if int(event_var['oldteam']) < 2 and int(event_var['team']) > 1:
        Player(int(event_var['userid'])).playsound('welcome')


def player_changename(event_var):
    '''Called when a player changes their name while on the server'''

    # Update the player's name in the winners database if they are in it
    if Player(int(event_var['userid'])).wins:
        update_winner('name', event_var['newname'],
            uniqueid=event_var['es_steamid'])


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
# >> GUNGAME EVENTS
# =========================================================================
def gg_start(event_var):
    # Reset all player levels and multikills when GG Starts
    reset_players()


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


def gg_addon_loaded(event_var):
    '''Called when a sub-addon is loaded'''

    es.dbgmsg(0, langstring('Addon_Loaded',
        {'addon': event_var['addon'], 'type': event_var['type']}))


def gg_addon_unloaded(event_var):
    '''Called when a sub-addon is unloaded'''

    es.dbgmsg(0, langstring('Addon_UnLoaded',
        {'addon': event_var['addon'], 'type': event_var['type']}))
