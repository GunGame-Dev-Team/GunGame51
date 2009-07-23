# ../addons/eventscripts/gungame/scripts/included/gg_reload/gg_reload.py

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
from weaponlib import getWeapon
from playerlib import getPlayer

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.players.shortcuts import Player

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
    attacker = int(event_var['attacker'])
    userid = int(event_var['userid'])
    
    # If there is no attacker (falling to death), return
    if not attacker:
        return

    # If the kill was a suicide, return
    if attacker == userid:
        return

    # If the kill was a teamkill, return
    if event_var['es_attackerteam'] == event_var['es_userteam']:
        return

    # Get the name of the weapon used to get the kill
    weapon = event_var['weapon']

    # If the weapon name doesn't match the player's level's weapon name, return
    if weapon != Player(attacker).weapon:
        return

    # If the player is on hegrenade or knife level, return
    if weapon in ('hegrenade', 'knife'):
        return

    # Get the weapon object and the size if its clip
    weaponObject = getWeapon(weapon)

    # Find the attacker's weapon index to be used to reload the weapon
    playerHandle = es.getplayerhandle(attacker)

    for index in weaponObject.indexlist:
        # When the attacker's handle matches the index handle we have found the attacker's weapon index
        if es.getindexprop(index, 'CBaseEntity.m_hOwnerEntity') == playerHandle:
            # Set the clip to the maximum ammo allowed
            getPlayer(attacker)['clip'][weaponObject] = weaponObject.clip
            break