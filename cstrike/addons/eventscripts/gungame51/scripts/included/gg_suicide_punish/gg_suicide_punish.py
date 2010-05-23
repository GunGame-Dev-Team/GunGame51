# ../addons/eventscripts/gungame51/scripts/included/gg_suicide_punish/gg_suicide_punish.py

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

# Store a list of those who recently changed teams, to not punish them if they
# committed suicide to do so
recentTeamChange = []

# Is the round live?
liveRound = True

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
    global liveRound
    liveRound = True

def round_end(event_var):
    global liveRound
    liveRound = False

def player_team(event_var):
    userid = int(event_var["userid"])
    
    # Store them here so we don't punish them if this team change caused a
    # suicide
    if not userid in recentTeamChange:
        recentTeamChange.append(userid)
        gamethread.delayed(0.2, recentTeamChange.remove, userid)

def player_death(event_var):
    '''
    Note to devs:
        Strangely enough, player_death no longer fires anymore when a player
        is killed by the bomb exploding. Therefore, we no longer need to keep
        track of counting bomb deaths as suicide.
    '''
    # Has the round ended?
    if not liveRound:
        return

    # Set player ids
    userid = int(event_var['userid'])
    attacker = int(event_var['attacker'])

    # Is the victim on the server?
    if not es.exists('userid', userid):
        return

    # If the attacker is not "world or the userid of the victim, it is not a
    # suicide
    if not ((attacker == 0) or (attacker == userid)):
        return

    # If the suicide was caused by a team change, stop here
    if userid in recentTeamChange:
        return

    # Get victim object
    ggVictim = Player(userid)

    # Trigger level down
    ggVictim.leveldown(int(gg_suicide_punish), userid, 'suicide')

    # Message
    ggVictim.msg('Suicide_LevelDown', {'newlevel':ggVictim.level}, 
                    prefix='gg_suicide_punish')

    # Play the leveldown sound
    ggVictim.playsound('leveldown')