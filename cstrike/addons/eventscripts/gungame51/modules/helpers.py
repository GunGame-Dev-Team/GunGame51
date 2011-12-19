# ../modules/helpers.py

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
#   Playerlib
from playerlib import getPlayer

# GunGame Imports
#   Modules
from info import credits
#   Addons
from gungame51.core.addons.priority import PriorityAddon
#   Events
from gungame51.core.events import GG_Start
#   Messaging
from gungame51.core.messaging.shortcuts import msg
#   Players
from gungame51.core.players.shortcuts import Player
#   Weapons
from gungame51.core.weapons import WeaponOrderManager


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
gg_player_armor = es.ServerVar('gg_player_armor')

_first_gg_start = False


# =============================================================================
# >> HELPER FUNCTIONS
# =============================================================================
def give_weapon_check(userid):
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


def equip_player():
    userid = es.getuserid()
    cmd = ('es_xremove game_player_equip;' +
          'es_xgive %s game_player_equip;' % userid +
          'es_xfire %s game_player_equip ' % userid +
          'AddOutput "weapon_knife 1";')

    # Retrieve the armor type
    armor_type = int(gg_player_armor)

    # Give the player full armor
    if armor_type == 2:
        cmd += ('es_xfire %s ' % userid +
            'game_player_equip AddOutput "item_assaultsuit 1";')

    # Give the player kevlar only
    elif armor_type == 1:
        cmd += ('es_xfire %s ' % userid +
            'game_player_equip AddOutput "item_kevlar 1";')

    es.server.queuecmd(cmd)


def check_first_gg_start():
    global _first_gg_start
    _first_gg_start = True
    check_gg_start()


def check_gg_start():
    # If there is nothing in priority addons, fire event gg_start
    if not PriorityAddon:
        if _first_gg_start:
            GG_Start().fire()


def thanks(userid, args):
    msg(userid, 'CheckConsole')
    es.cexec(userid, 'echo [GG Thanks] ')

    # Loop through the credits
    for x in credits:

        # Print category
        es.cexec(userid, 'echo [GG Thanks] %s:' % (x))

        # Show all in this category
        for y in credits[x]:
            es.cexec(userid, 'echo [GG Thanks] \t%s' % y)

        es.cexec(userid, 'echo [GG Thanks] ')


# Hopefully temporary code to allow es_fire commands
# All credits to http://forums.eventscripts.com/viewtopic.php?t=42620
def disable_auto_kick(userid):
    es.server.mp_disable_autokick(userid)
