# ../addons/eventscripts/gungame51/scripts/included/gg_noblock/gg_noblock.py

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
from playerlib import getPlayer
from playerlib import getPlayerList

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo

# ============================================================================
# >> ADDON REGISTRATION/INFORMATION
# ============================================================================
info = AddonInfo()
info.name = 'gg_noblock'
info.title = 'GG No Block' 
info.author = 'GG Dev Team' 
info.version = "5.1.%s" %"$Rev$".split('$Rev: ')[1].split()[0]

# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    es.dbgmsg(0, 'Loaded: %s' % info.name)

    # Enable noblock for every player that is alive and on a team
    for player in getPlayerList('#alive'):
        player.noblock = 1

def unload():
    es.dbgmsg(0, 'Unloaded: %s' % info.name)

    # Disable noblock for every player that is alive and on a team
    for player in getPlayerList('#alive'):
        player.noblock = 0

# ============================================================================
# >> GAME EVENTS
# ============================================================================
def player_spawn(event_var):
    # Enable noblock for this player
    getPlayer(event_var['userid']).noblock = 1