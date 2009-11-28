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
import gamethread
from playerlib import getPlayer

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.players import Player

# ============================================================================
# >> GLOBAL VARIABLES
# ============================================================================

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
    attacker = int(event_var['attacker'])

    # Make sure it wasn't a suicide
    if attacker == 0:
        return

    # Make sure it wasn't a teamkill
    if event_var['es_attackerteam'] == event_var['es_userteam']:
        return

    # Make sure the player didn't kill with an hegrenade
    if event_var['weapon'] == 'hegrenade':
        return

    # Only give a nade to a player on nade level
    if Player(attacker).weapon == 'hegrenade':
        gamethread.delayed(0.11, give_nade, attacker)

# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
def give_nade(userid):
    pPlayer = getPlayer(userid)

    # Is the player dead ?
    if pPlayer.isdead:
        return
        
    # Is the player on a team ?
    if pPlayer.teamid < 2:
        return

    # Only give a nade if this player does not have one.
    if int(getPlayer(userid).get('he')) == 0:
        es.server.queuecmd('es_xgive %s weapon_hegrenade' % userid)