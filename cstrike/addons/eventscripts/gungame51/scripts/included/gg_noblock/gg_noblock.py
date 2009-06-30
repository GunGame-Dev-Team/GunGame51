# ../addons/eventscripts/gungame/scripts/included/gg_noblock/gg_noblock.py

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
info.version = '0.1'

# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    es.dbgmsg(0, 'Loaded: %s' % info.name)
    
    # Enable noblock for every player that is alive and on a team
    for userid in getPlayerList('#alive'):
        getPlayer(userid).noblock = 1
    
def unload():
    es.dbgmsg(0, 'Unloaded: %s' % info.name)
    
    # Disable noblock for every player that is alive and on a team
    for userid in getPlayerList('#alive'):
        getPlayer(userid).noblock = 0
    
# ============================================================================
# >> GAME EVENTS
# ============================================================================
def player_spawn(event_var):

    userid = int(event_var['userid'])
    
    # Enable noblock for this player
    getPlayer(userid).noblock = 1