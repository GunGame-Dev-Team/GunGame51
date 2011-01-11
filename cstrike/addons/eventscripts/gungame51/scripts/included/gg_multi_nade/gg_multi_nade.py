# ../scripts/included/gg_multi_nade/gg_multi_nade.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports


# Eventscripts Imports
import es
import spe
from playerlib import getPlayer

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.players.shortcuts import Player

# =============================================================================
# >> ADDON REGISTRATION/INFORMATION
# =============================================================================
info = AddonInfo()
info.name = 'gg_multi_nade'
info.title = 'GG Multiple Grenades'
info.author = 'GG Dev Team'
info.version = "5.1.%s" % "$Rev$".split('$Rev: ')[1].split()[0]

# =============================================================================
# >> GLOBALS
# =============================================================================

# A global variable to hold the value of the server var by the same name
gg_multi_nade_max_nades = es.ServerVar("gg_multi_nade_max_nades")


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    es.dbgmsg(0, 'Loaded: %s' % info.name)


def unload():
    es.dbgmsg(0, 'Unloaded: %s' % info.name)


# =============================================================================
# >> GAME EVENTS
# =============================================================================
def player_spawn(event_var):
    # Set the grenades_detonated counter for the spawning player to 0
    Player(int(event_var['userid'])).grenades_detonated = 0


def gg_levelup(event_var):
    # If someone levels up, from nade to nade level, do this
    Player(int(event_var['leveler'])).grenades_detonated = 0


def hegrenade_detonate(event_var):
    # Get the userid as int
    userid = int(event_var['userid'])

    # If the player is not on an active team, return
    if int(event_var['es_userteam']) <= 1:
        return

    # If the player is not on hegrenade level, return
    if Player(userid).weapon != 'hegrenade':
        return

    # If the player is dead, return
    if getPlayer(userid).isdead:
        return

    # If there is a limit to the number of nades a player can get...
    if int(gg_multi_nade_max_nades) > 0:

        # Don't keep counting if the player has already hit the max
        if Player(userid).grenades_detonated < int(gg_multi_nade_max_nades):
            # Increment the player's grenades_detonated count
            Player(userid).grenades_detonated += 1

        # Find out if they exceeded the limit and break out if so
        if Player(userid).grenades_detonated >= int(gg_multi_nade_max_nades):
            return

    # Give the player a new hegrenade
    spe.giveNamedItem(userid, "weapon_hegrenade")
