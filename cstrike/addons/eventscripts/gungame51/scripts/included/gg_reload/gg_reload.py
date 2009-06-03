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
    # Get event info
    attackerid = int(event_var['attacker'])
    victimid = int(event_var['userid'])
    
    # Fallen to death?
    if not attackerid:
        return
    
    # Killed self?
    if attackerid == victimid:
        return
    
    # Get weapon
    weapon = event_var['weapon']
    
    # We will only reload weapons that the attacker is on the level for
    if weapon != Player(attackerid).weapon:
        return
    
    # Is a hegrenade or knife kill?
    if weapon in ('hegrenade', 'knife'):
        return
    
    # DEV NOTE: We need to add a weapon info system to find the ammo / slots etc for each weapon