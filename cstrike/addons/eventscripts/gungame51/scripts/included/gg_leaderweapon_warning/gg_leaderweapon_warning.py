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
from playerlib import getUseridList

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.players.shortcuts import Player
from gungame51.core.leaders.shortcuts import get_leader_level
from gungame51.core.weapons.shortcuts import get_level_weapon

# ============================================================================
# >> GLOBALS
# ============================================================================
playedKnife = False
playedNade = False

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
def es_map_start(event_var):
    global playedKnife
    playedKnife = False
    global playedNade
    playedNade = False

def round_start(event_var):
    # Get leader weapon
    leaderWeapon = get_level_weapon(get_leader_level())

    # Knife level ?
    if leaderWeapon == 'knife':
        sound = 'knifelevel'

    # Nade level ?
    elif leaderWeapon == 'hegrenade':
        sound = 'nadelevel'

    # No warning
    else:
        return

    # Play sounds
    for userid in getUseridList('#human'):
        Player(userid).playsound(sound)

def gg_levelup(event_var):
    attacker = int(event_var['attacker'])
    
    # Play nade warning ? (One time during a round per map)
    if Player(attacker).weapon == 'hegrenade' and not playedNade:
        sound = 'nadelevel'
        global playedNade
        playedNade = True
            
    # Play knife warning ? (One time during a round per map)
    elif Player(attacker).weapon == 'knife' and not playedKnife:
        sound = 'knifelevel'
        global playedKnife
        playedKnife = True
        
    # Don't play any sounds
    else:
        return

    # Play sound to all players
    for userid in getUseridList('#human'):
        Player(userid).playsound(sound)

# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================  

