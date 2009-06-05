# ../addons/eventscripts/gungame/scripts/included/gg_reload/gg_reload.py

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
import weaponlib

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.players import Player

# ============================================================================
# >> ADDON REGISTRATION/INFORMATION
# ============================================================================
info = AddonInfo()
info.name = 'gg_reload'
info.title = 'GG Reload' 
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
# >> GAME EVENTS
# ============================================================================

def player_death(event_var):
    # Get the userids of the attacker and victim
    attackerid = int(event_var['attacker'])
    victimid = int(event_var['userid'])
    
    # If there is no attacker (falling to death), return
    if not attackerid:
        return
    
    # If the kill was a suicide, return
    if attackerid == victimid:
        return
    
    # Get the name of the weapon used to get the kill
    weapon = event_var['weapon']
    
    # If the weapon name doesn't match the player's level's weapon name, return
    if weapon != Player(attackerid).weapon:
        return
    
    # If the player is on hegrenade or knife level, return
    if weapon in ('hegrenade', 'knife'):
        return
    
    # Get the weapon object and the size if its clip
    weaponObject = weaponlib.getWeapon(weapon)
    clip = weaponObject.clip
    
    # Find the attacker's weapon index to be used to reload the weapon
    playerHandle = es.getplayerhandle(attackerid)
    for index in weaponObject.indexlist:
        # When the attacker's handle matches the index handle we have found the attacker's weapon index
        if es.getindexprop(index, 'CBaseEntity.m_hOwnerEntity') == playerHandle:
            # When a match is found, reload the clip
            es.setindexprop(index, 'CBaseCombatWeapon.LocalWeaponData.m_iClip1', clip)
            break