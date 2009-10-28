# ../addons/eventscripts/gungame/scripts/included/gg_suicide_punish/gg_suicide_punish.py

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
info.name = 'gg_suicide_punish'
info.title = 'GG Suicide Punish' 
info.author = 'GG Dev Team' 
info.version = '0.1'
info.translations = ['gg_suicide_punish']

# ============================================================================
# >> GLOBAL VARIABLES
# ============================================================================
# Get the es.ServerVar() instance of "gg_suicide_punish"
gg_suicide_punish = es.ServerVar('gg_suicide_punish')

# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    es.dbgmsg(0, 'Loaded: %s' % info.name)

def unload():
    es.dbgmsg(0, 'Unloaded: %s' % info.name)

def player_death(event_var):
    '''
    Note to devs:
        Strangely enough, player_death no longer fires anymore when a player
        is killed by the bomb exploding. Therefore, we no longer need to keep
        track of counting bomb deaths as suicide.
    '''
    # Set player ids
    userid = int(event_var['userid'])
    attacker = int(event_var['attacker'])

    # Is the attacker on the server?
    if not es.exists('userid', attacker):
        return

    # If the attacker is not "world or the userid of the victim, it is not a suicide
    if not ((attacker == 0) or (attacker == userid)):
        return

    # Get victim object
    ggVictim = Player(userid)

    # Trigger level down
    ggVictim.leveldown(int(gg_suicide_punish), userid, 'suicide')

    # Message
    ggVictim.msg('Suicide_LevelDown', {'newlevel':ggVictim.level}, prefix='gg_suicide_punish')

    # Play the leveldown sound
    ggVictim.playsound('leveldown')