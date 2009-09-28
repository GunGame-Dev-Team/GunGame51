# ../addons/eventscripts/gungame/scripts/included/gg_unl_grenade/gg_unl_grenade.py

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

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.players.shortcuts import Player

# ============================================================================
# >> ADDON REGISTRATION/INFORMATION
# ============================================================================
info = AddonInfo()
info.name = 'gg_unl_grenade'
info.title = 'GG Unlimited Grenades' 
info.author = 'GG Dev Team' 
info.version = '0.1'
info.conflicts = ['gg_earn_nade']

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
def hegrenade_detonate(event_var):
    userid = int(event_var['userid'])
    
    # If the player is not on an active team, return
    if int(event_var['es_userteam']) <= 1:
        return
    
    # If the player is not on hegrenade level, return
    if Player(userid).weapon != 'hegrenade':
        return
    
    # If the player is dead, return
    if getPlayer(userid).isdead:
        return
    
    # Give the player a new hegrenade
    es.server.queuecmd('es_xgive %s weapon_hegrenade' % userid)