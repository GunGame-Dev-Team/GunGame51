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

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.players.shortcuts import Player
from gungame51.core.players.shortcuts import addAttributeCallBack
from gungame51.core.players.shortcuts import removeCallBacksForAddon
from gungame51.core.weapons.shortcuts import getLevelWeapon

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
    addAttributeCallBack('level', level_call_back, info.name)
    es.dbgmsg(0, 'Loaded: %s' % info.name)

def unload():
    es.dbgmsg(0, 'Unloaded: %s' % info.name)

# ============================================================================
# >> GUNGAME EVENTS
# ============================================================================
def gg_levelup(event_var):
    userid = int(event_var['leveler'])

    # Strip and give weapon
    give_weapon(userid, int(event_var['old_level']))

def gg_leveldown(event_var):
    userid = int(event_var['leveler'])

    # Strip and give weapon
    give_weapon(userid, int(event_var['old_level']))

# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
def give_weapon(userid, previousLevel):
    # Do player checks first
    if not player_checks(userid):
        return

    # Get player
    ggPlayer = Player(userid)

    # Give them their next weapon
    ggPlayer.giveWeapon()

    # Retrieve a playerlib.Player() instances
    pPlayer = getPlayer(userid)
    pWeapon = pPlayer.getPrimary()
    sWeapon = pPlayer.getSecondary()

    # Get the player's current weapons
    currentWeapon = "weapon_%s" % ggPlayer.weapon
    previousWeapon = "weapon_%s" % getLevelWeapon(previousLevel)

    strip = None

    # Strip secondary weapon ? (Move to primary)
    if previousWeapon == sWeapon and currentWeapon in list_pWeapons:
        strip = sWeapon

    # Strip primary weapon ? (Move to seconary)
    elif previousWeapon == pWeapon and currentWeapon in list_sWeapons:
        strip = pWeapon

    # Did we find a weapon to strip ?
    if strip:
        es.server.queuecmd('es_xremove %s' % (
                                            pPlayer.getWeaponIndex(strip)))

    # Make them use it ?
    if pPlayer.weapon != currentWeapon:
        es.server.queuecmd('es_xsexec %s "use %s"' % (userid, currentWeapon))

def player_checks(userid):
    # Get ggPlayer
    ggPlayer = Player(userid)

    # Is player dead?
    if getPlayer(userid).isdead:
        return False

    # Is player a spectator?
    if getPlayer(userid).isobserver:
        return False

    return True

def level_call_back(name, value, ggPlayer):
    # If the player has been assigned a level already
    if hasattr(ggPlayer, 'level'):
        # Get their previous level, before it was changed
        previousLevel = ggPlayer.level
    # Otherwise
    else:
        # Assume they are on level 1
        previousLevel = 1

    # Delay the check to see if they have the correct turbo weapon
    gamethread.delayed(0.1, check_call_back_weapon, (ggPlayer, previousLevel))

def check_call_back_weapon(ggPlayer, previousLevel):
    weapon = 'weapon_%s' % ggPlayer.weapon

    # Check whether or not the userid exists
    if not es.exists('userid', ggPlayer.userid):
        return

    # Retrieve a playerlib.Player() instance
    pPlayer = getPlayer(ggPlayer.userid)

    # Get the weapon that is in the slot that their level's weapon should be in
    if weapon in list_pWeapons:
        weaponHeld = pPlayer.getPrimary()
    elif weapon in list_sWeapons:
        weaponHeld = pPlayer.getSecondary()
    else:
        return

    # If they are they holding the previous level's weapon, remove it
    if weapon != weaponHeld:
        give_weapon(ggPlayer.userid, previousLevel)