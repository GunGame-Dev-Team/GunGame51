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

# ============================================================================
# >> GLOBALS
# ============================================================================
list_pWeapons = getWeaponNameList("#primary")
list_sWeapons = getWeaponNameList("#secondary")

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

    # Get ggPlayer
    pPlayer = getPlayer(userid)

    # Is player dead or a spectator?
    if pPlayer.isdead or es.getplayerteam(userid) < 2:
        return

    # Give them their next weapon
    ggPlayer = Player(userid)
    ggPlayer.give_weapon()

    # Get the player's current Held weapons
    pWeapon = pPlayer.getPrimary()
    sWeapon = pPlayer.getSecondary()
    
    # Get the player's current GunGame weapons
    currentWeapon = "weapon_%s" % ggPlayer.weapon
    previousWeapon = "weapon_%s" % get_level_weapon(previousLevel)
    
    stripWeapon = None
    
    # Strip secondary weapon ? (Move to primary)
    if previousWeapon == sWeapon and currentWeapon in list_pWeapons:
        stripWeapon = sWeapon

    # Strip primary weapon ? (Move to seconary)
    elif previousWeapon == pWeapon and currentWeapon in list_sWeapons:
        stripWeapon = pWeapon

    # Did we find a weapon to strip ?
    if stripWeapon:
        spe.removeEntityByIndex( pPlayer.getWeaponIndex(stripWeapon) )

    # Make them use it ?
    if pPlayer.weapon != currentWeapon:
        es.server.queuecmd('es_xsexec %s "use %s"' % (userid, currentWeapon))