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
# Get the es.ServerVar() instance of "gg_warmup_round"
gg_warmup_round = es.ServerVar('gg_warmup_round')

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

    # Is this player on nade level?
    if Player(attacker).weapon == 'hegrenade':

        # Make sure the player didn't kill with an hegrenade
        if event_var['weapon'] == 'hegrenade':
            return 

        # Give them another grenade
        gamethread.delayed(0.08, giveGrenade, (attacker))

# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
def giveGrenade(userid):
    # Does this player already have a grenade?
    if int(getPlayer(userid).get('he')) != 0:
        # Don't give them one, return
        return

    es.server.queuecmd('es_xgive %i weapon_hegrenade' % userid)