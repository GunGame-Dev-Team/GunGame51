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
from gungame51.core.players.shortcuts import isDead
from gungame51.core.players.shortcuts import isSpectator
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
    es.dbgmsg(0, 'Loaded: %s' % info.name)

def unload():
    es.dbgmsg(0, 'Unloaded: %s' % info.name)

# ============================================================================
# >> GUNGAME EVENTS
# ============================================================================
def gg_levelup(event_var):

    userid = int(event_var['leveler'])

    # Strip and give weapon
    giveWeapon(userid)

def gg_leveldown(event_var):

    userid = int(event_var['leveler'])

    # Strip and give weapon
    giveWeapon(userid)

# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
def giveWeapon(userid):

    # Do player checks first
    if not playerChecks(userid):
        return

    # Get player
    player = Player(userid)

    # Give them their next weapon
    player.giveWeapon()
    
    # Get the names of the previous and current level weapons
    previousWeapon = "weapon_%s" % getLevelWeapon(int(player.level) - 1)
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
    if isDead(userid):
        return False

    # Is player a spectator?
    if isSpectator(userid):
        return False

    return True