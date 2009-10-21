# ../addons/eventscripts/gungame/scripts/included/gg_leaderweapon_warning/gg_leaderweapon_warning.py

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

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.players.shortcuts import Player
from gungame51.core.leaders.shortcuts import get_leader_level
from gungame51.core.weapons.shortcuts import getLevelWeapon

# ============================================================================
# >> ADDON REGISTRATION/INFORMATION
# ============================================================================
info = AddonInfo()
info.name = 'gg_leaderweapon_warning'
info.title = 'GG Leader Weapon Warning' 
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
def round_start(event_var):
    # Play sounds ?
    weaponWarning()

def gg_levelup(event_var):
    # Play sounds ?
    weaponWarning()

# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================  
def weaponWarning():
    # Get leader weapon
    leaderWeapon = getLevelWeapon(get_leader_level())
    
    # Knife level ?
    if leaderWeapon == 'knife':
        sound = 'knifelevel'
    
    # Nade level ?
    elif leaderWeapon == 'hegrenade':
        sound = 'nadelevel'
    
    # No warning ?
    else:
        return
    
    # Play sounds
    for userid in getPlayerList('#human'):
        Player(userid).playsound(sound)