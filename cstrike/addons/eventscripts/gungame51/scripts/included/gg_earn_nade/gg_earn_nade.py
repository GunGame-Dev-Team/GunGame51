# ../addons/eventscripts/gungame/scripts/included/gg_earn_nade/gg_earn_nade.py

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
import playerlib

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.players import Player

# ============================================================================
# >> ADDON REGISTRATION/INFORMATION
# ============================================================================
info = AddonInfo()
info.name = 'gg_earn_nade'
info.title = 'GG Earn Grenade' 
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

    victimid = int(event_var['userid'])
    attackerid = int(event_var['attacker'])
    
    # Make sure it wasn't a suicide
    if attackerid == 0:
        return
        
    # Make sure it wasn't a teamkill
    if event_var['es_attackerteam'] == event_var['es_userteam']:
        return
        
    # Is this player on nade level?
    if Player(attackerid).weapon == 'hegrenade':
    
        # Make sure the player didn't kill with an hegrenade
        if event_var['weapon'] == 'hegrenade':
            return 
        
        # Are we in warmup?
        if int(es.ServerVar("gg_warmup_round")) > 0 :
            return

        # Give them another grenade
        giveGrenade(attackerid)

# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
def giveGrenade(userid):

    # Does this player already have a grenade?
    if int(playerlib.getPlayer(userid).get('he')) != 0:
        # Don't give them one, return
        return

    cmdFormat = 'es_xgive %i weapon_hegrenade' % userid
    es.server.queuecmd(cmdFormat)

