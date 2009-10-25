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
    addAttributeCallBack('level', levelCallback, info.name)
    es.dbgmsg(0, 'Loaded: %s' % info.name)

def unload():
    es.dbgmsg(0, 'Unloaded: %s' % info.name)

# ============================================================================
# >> GUNGAME EVENTS
# ============================================================================
def gg_levelup(event_var):

    userid = int(event_var['leveler'])

    # Strip and give weapon
    giveWeapon(userid, int(event_var['old_level']))

def gg_leveldown(event_var):

    userid = int(event_var['leveler'])

    # Strip and give weapon
    giveWeapon(userid, int(event_var['old_level']))

# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
def giveWeapon(userid, previousLevel):

    # Do player checks first
    if not playerChecks(userid):
        return

    # Get player
    player = Player(userid)

    # Give them their next weapon
    player.giveWeapon()
    
    # Get the names of the previous and current level weapons
    previousWeapon = "weapon_%s" % getLevelWeapon(previousLevel)
    currentWeapon = "weapon_%s" % player.weapon
    
    # Retrieve a playerlib.Player() instance
    pPlayer = getPlayer(userid)
    
    if previousWeapon:
        # Set strip to 1 if previousWeapon and currentWeapon are primary and secondary or visa-versa
        if ((previousWeapon in list_sWeapons and currentWeapon in list_pWeapons) or \
            (previousWeapon in list_pWeapons and currentWeapon in list_sWeapons)):
            strip = 1
        else:
            strip = 0
        
        # If a weapon will be stripped, get the name of the weapon that is being held
        if strip:
            if previousWeapon in list_pWeapons:
                pWeapon = pPlayer.getPrimary()
            elif previousWeapon in list_sWeapons:
                pWeapon = pPlayer.getSecondary()
            
            # If they are they holding the previous level's weapon, remove it
            if pWeapon == previousWeapon:
                es.remove(pPlayer.getWeaponIndex(pWeapon))

    # Make them use it
    es.sexec(userid, "use weapon_%s" % player.weapon)

def playerChecks(userid):
    # Get player
    player = Player(userid)

    # Is player dead?
    if getPlayer(userid).isdead:
        return False

    # Is player a spectator?
    if getPlayer(userid).isobserver:
        return False

    return True

def levelCallback(name, value, ggPlayer):
    # If the player has been assigned a level already
    if hasattr(ggPlayer, 'level'):
        # Get their previous level, before it was changed
        previousLevel = ggPlayer.level
    # Otherwise
    else:
        # Assume they are on level 1
        previousLevel = 1

    # Delay the check to see if they have the correct turbo weapon
    gamethread.delayed(0.05, checkCallBackWeapon, (ggPlayer, previousLevel))

def checkCallBackWeapon(ggPlayer, previousLevel):
    weapon = 'weapon_%s' % ggPlayer.weapon

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
        giveWeapon(ggPlayer.userid, previousLevel)