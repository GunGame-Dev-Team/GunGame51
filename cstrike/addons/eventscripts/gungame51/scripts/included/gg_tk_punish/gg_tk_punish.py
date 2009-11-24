# ../addons/eventscripts/gungame/scripts/included/gg_tk_punish/gg_tk_punish.py

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

# ============================================================================
# >> ADDON REGISTRATION/INFORMATION
# ============================================================================
info = AddonInfo()
info.name = 'gg_tk_punish'
info.title = 'GG TK Punish' 
info.author = 'GG Dev Team' 
info.version = '0.1'

# ============================================================================
# >> GLOBAL VARIABLES
# ============================================================================
# Get the es.ServerVar() instance of "gg_tk_punish"
gg_tk_punish = es.ServerVar('gg_tk_punish')

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
    # Set player ids
    userid = int(event_var['userid'])
    attacker = int(event_var['attacker'])

    # Is the attacker on the server?
    if not es.exists('userid', attacker):
        return

    # Suicide check
    if (attacker == 0 or attacker == userid):
        return

    # Get attacker object
    ggAttacker = Player(attacker)

    # ===============
    # TEAM-KILL CHECK
    # ===============
    if (event_var['es_userteam'] == event_var['es_attackerteam']):
        # Trigger level down
        ggAttacker.leveldown(int(gg_tk_punish), userid, 'tk')

        # Message
        ggAttacker.msg('TeamKill_LevelDown', {'newlevel':ggAttacker.level})

        # Play the leveldown sound
        ggAttacker.playsound('leveldown')