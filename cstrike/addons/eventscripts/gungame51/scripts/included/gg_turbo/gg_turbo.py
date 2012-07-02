# ../scripts/included/gg_turbo/gg_turbo.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# Eventscripts Imports
#   ES
from es import exists
from es import getplayerteam
from es import ServerVar
from es import setplayerprop
#   Gamethread
from gamethread import delayed
#   Playerlib
from playerlib import getPlayer

# GunGame Imports
#   Addons
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.addons.loaded import LoadedAddons
#   Player
from gungame51.core.players.shortcuts import Player
from gungame51.core.players.shortcuts import add_attribute_callback
from gungame51.core.players.shortcuts import remove_callbacks_for_addon
#   Weapon
from gungame51.core.weapons.shortcuts import get_level_weapon
from gungame51.core.weapons.shortcuts import get_total_levels

# =============================================================================
# >> ADDON REGISTRATION/INFORMATION
# =============================================================================
info = AddonInfo()
info.name = 'gg_turbo'
info.title = 'GG Turbo'
info.author = 'GG Dev Team'
info.version = "5.1.%s" % "$Rev$".split('$Rev: ')[1].split()[0]


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    add_attribute_callback('level', level_call_back, info.name)


def unload():
    remove_callbacks_for_addon(info.name)


# =============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# =============================================================================
def level_call_back(name, value, ggPlayer):
    # If the player has been assigned a level already
    if hasattr(ggPlayer, 'level'):
        # Get their previous level, before it was changed
        previousLevel = ggPlayer.level
    # Otherwise
    else:
        # Assume they are on level 1
        previousLevel = 1

    # Delay to give them a new weapon (callbacks are too fast)
    delayed(0.005, give_weapon, (ggPlayer.userid, previousLevel))


def give_weapon(userid, previousLevel):
    if not exists('userid', userid) and userid != 0:
        return

    # Is spectator?
    if getplayerteam(userid) < 2:
        return

    # Is player dead?
    if getPlayer(userid).isdead:
        return

    # Give them their next weapon
    ggPlayer = Player(userid)
    ggPlayer.give_weapon()

    # If previousLevel is not in the order due to weapon orders changing,
    # stop here
    if previousLevel > get_total_levels():
        return

    weapsToStrip = [get_level_weapon(previousLevel)]

    # If the player is was on hegrenade level, and gg_nade_bonus is enabled,
    # and the current level is not hegrenade as well, get the list of their
    # bonus weapons
    if (weapsToStrip[0] == "hegrenade" and
      'gg_nade_bonus' in LoadedAddons and ggPlayer.weapon != "hegrenade"):

        from ..gg_nade_bonus.gg_nade_bonus import get_weapon

        # Add the Nade Bonus Weapon
        weapsToStrip.extend(get_weapon(userid))

    # If any weapons to be removed were just given, do not strip them
    if ggPlayer.weapon in weapsToStrip:
        weapsToStrip.remove(ggPlayer.weapon)

    # Strip the previous weapons
    ggPlayer.strip_weapons(weapsToStrip)

    # Is quick weapon activated
    if ServerVar('gg_turbo_quick'):

        # Set the NextAttack property
        setplayerprop(userid,
            'CBaseCombatCharacter.bcc_localdata.m_flNextAttack', 0)
