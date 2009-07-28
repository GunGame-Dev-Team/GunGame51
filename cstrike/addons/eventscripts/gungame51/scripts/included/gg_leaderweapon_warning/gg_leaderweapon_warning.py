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
from gungame51.core.leaders.shortcuts import getLeaderLevel
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
    leaderWeapon = getLevelWeapon(getLeaderLevel())

    '''
    STILL HAVE TO FIGURE OUT HOW TO IMPLEMENT SOUNDS

    # Play knife sound
    if leaderWeapon == 'knife':
        gungamelib.playSound('#human', 'knifelevel')

    # Play nade sound
    if leaderWeapon == 'hegrenade':
        gungamelib.playSound('#human', 'nadelevel')
    '''

def gg_levelup(event_var):
    # Get attacker info
    ggPlayer = Player(event_var['attacker'])

    '''
    STILL HAVE TO FIGURE OUT HOW TO IMPLEMENT SOUNDS

    # Player on knife level?
    if ggPlayer.weapon == 'knife':
        gungamelib.playSound('#human', 'knifelevel')

    # Player on nade level?
    if ggPlayer.weapon == 'hegrenade':
        gungamelib.playSound('#human', 'nadelevel')
    '''