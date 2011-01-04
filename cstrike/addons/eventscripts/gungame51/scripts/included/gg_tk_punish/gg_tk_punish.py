# ../addons/eventscripts/gungame51/scripts/included/gg_tk_punish/gg_tk_punish.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# Eventscripts Imports
import es

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.players.shortcuts import Player

# =============================================================================
# >> ADDON REGISTRATION/INFORMATION
# =============================================================================
info = AddonInfo()
info.name = 'gg_tk_punish'
info.title = 'GG TK Punish' 
info.author = 'GG Dev Team' 
info.version = "5.1.%s" %"$Rev$".split('$Rev: ')[1].split()[0]
info.translations = ['gg_tk_punish']

# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Get the es.ServerVar() instance of "gg_tk_punish"
gg_tk_punish = es.ServerVar('gg_tk_punish')

# Is the round live?
liveRound = True

# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    es.dbgmsg(0, 'Loaded: %s' % info.name)
    
def unload():
    es.dbgmsg(0, 'Unloaded: %s' % info.name)
    
# =============================================================================
# >> GAME EVENTS
# =============================================================================
def round_start(event_var):
    global liveRound
    liveRound = True

def round_end(event_var):
    global liveRound
    liveRound = False

def player_death(event_var):
    # Has the round ended?
    if not liveRound:
        return

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
        ggAttacker.msg('TeamKill_LevelDown', {'newlevel':ggAttacker.level}, 
                        prefix='gg_tk_punish')

        # Play the leveldown sound
        ggAttacker.playsound('leveldown')