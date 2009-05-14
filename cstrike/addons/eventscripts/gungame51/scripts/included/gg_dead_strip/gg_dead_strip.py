# gungame/scripts/included/gg_dead_strip.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
# Python Imports


# Eventscripts Imports
import es
from playerlib import getPlayer
from weaponlib import getWeaponNameList

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.players.shortcuts import Player

# ============================================================================
# >> ADDON REGISTRATION/INFORMATION
# ============================================================================
info = AddonInfo()
info.name = 'gg_dead_strip'
info.title = 'GG Dead Strip' 
info.author = 'GG Dev Team' 
info.version = '0.1'

# ============================================================================
# >> GLOBAL VARIABLES
# ============================================================================
gg_nade_bonus = es.ServerVar('gg_nade_bonus')

# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():

    # Register the drop command to prevent it from being used.
    es.addons.registerClientCommandFilter(filterDrop)
    es.dbgmsg(0, 'Loaded: %s' % info.name)
    
def unload():

    # Unregister the drop command
    es.addons.unregisterClientCommandFilter(filterDrop)
    es.dbgmsg(0, 'Unloaded: %s' % info.name)
    
# ============================================================================
# >> GAME EVENTS
# ============================================================================
def round_start(event_var):
    # Remove all idle weapons that exist on the map.
    es.fire(es.getuserid(), 'game_weapon_manager AddOutput "maxpieces 0"')
    #es.server.cmd('es_xfire %s game_weapon_manager AddOutput "maxpieces 0"' % es.getuserid())

def item_pickup(event_var):
    # Get variables
    item = event_var['item']
    userid = int(event_var['userid'])

    # Is a weapon?
    if ("weapon_%s" %item) not in getWeaponNameList():
        return
        
    # Don't strip the knife
    if item == "knife":
        return
    
    # Client exists?
    if not es.exists('userid', userid):
        return
    
    # Get the player's GunGame weapon
    currentWeapon = Player(userid).weapon
    
    # Check to see if the weapon is their gungame weapon or in their strip exceptions
    #if item == weapon or item in gungamePlayer.stripexceptions + ['flashbang', 'smokegrenade']:
    if item == currentWeapon:
        return
    
    # Remove player's weapon
    removeWeapon(userid, item)

    # If the player did not switch to the weapon they just picked up, no need to switch them back to their previous weapon
    if currentWeapon != item:
        return
    
    # Check if player is on nade level
    if weapon == 'hegrenade':
        # Switch the player knife if they are on nade level but don't have a nade
        if not getPlayer(userid).he:
            es.sexec(userid, 'use weapon_knife')
            return
    
    # Switch to their gungame weapon
    es.sexec(userid, 'use weapon_%s' % weapon)

# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
def removeWeapon(userid, item):
    # Remove weapon
    es.remove(getPlayer(userid).getWeaponIndex("weapon_%s" %item))
    
def filterDrop(userid, args):
    # If command not drop, continue
    if args[0].lower() != 'drop':
        return 1
    
    # Get player's GunGame weapon
    weapon = Player(userid).weapon
    
    # Get the player's current weapon
    curWeapon = getPlayer(userid).attributes['weapon']
    
    # Check to see if their current weapon is their level weapon
    if weapon != 'hegrenade':
        return int(curWeapon != 'weapon_%s' %weapon)
    
    # ================
    # NADE BONUS CHECK
    # ================
    nadeBonusWeapons = str(gg_nade_bonus).split(',')
    
    # Is nade bonus enabled?
    if nadeBonusWeapons[0] == '0':
        return int(curWeapon != "weapon_%s" %weapon)
    
    # Loop through the nade bonus weapons
    for nadeWeapon in nadeBonusWeapons:
        # Prefix weapon_
        if not nadeWeapon.startswith('weapon_'):
            nadeWeapon = "weapon_%s" %nadeWeapon
        
        # Don't allow them to drop it
        if nadeWeapon == curWeapon:
            return 0
    
    # Allow them to drop it
    return 1