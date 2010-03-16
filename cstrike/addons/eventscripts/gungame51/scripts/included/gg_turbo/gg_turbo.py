# ../addons/eventscripts/gungame/scripts/included/gg_turbo/gg_turbo.py

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
import gamethread
from playerlib import getPlayer
from weaponlib import getWeaponNameList

# SPE Imports
import spe

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.players.shortcuts import Player
from gungame51.core.players.shortcuts import add_attribute_callback
from gungame51.core.players.shortcuts import remove_callbacks_for_addon
from gungame51.core.weapons.shortcuts import get_level_weapon
from gungame51.core.weapons.shortcuts import get_total_levels
from gungame51.scripts.included.gg_nade_bonus.gg_nade_bonus import get_weapon

# ============================================================================
# >> GLOBALS
# ============================================================================
gg_nade_bonus = es.ServerVar("gg_nade_bonus")

# ============================================================================
# >> ADDON REGISTRATION/INFORMATION
# ============================================================================
info = AddonInfo()
info.name = 'gg_turbo'
info.title = 'GG Turbo' 
info.author = 'GG Dev Team' 
info.version = '0.1'

# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    add_attribute_callback('level', level_call_back, info.name)
    es.dbgmsg(0, 'Loaded: %s' % info.name)

def unload():
    es.dbgmsg(0, 'Unloaded: %s' % info.name)
    remove_callbacks_for_addon(info.name)

# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
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
    gamethread.delayed(0.005, give_weapon, (ggPlayer.userid, previousLevel))

def give_weapon(userid, previousLevel):
    if not es.exists('userid', userid):
        return

    # Get playerlib object
    pPlayer = getPlayer(userid)

    # Is player dead or a spectator?
    if pPlayer.isdead or es.getplayerteam(userid) < 2:
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
    # get the list of their bonus weapons
    if weapsToStrip[0] == "hegrenade" and str(gg_nade_bonus) != "0":
        weapsToStrip.extend(get_weapon(userid))

    # Strip the previous weapons
    ggPlayer.strip_weapons(weapsToStrip)