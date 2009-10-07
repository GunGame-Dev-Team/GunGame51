# ../addons/eventscripts/gungame/scripts/included/gg_elimination/gg_elimination.py

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
import gamethread

# GunGame Imports
#    Core
from gungame51.core import inMap
#   Addons
from gungame51.core.addons.shortcuts import AddonInfo
#   Messaging
from gungame51.core.messaging.shortcuts import msg
from gungame51.core.messaging.shortcuts import saytext2
#   Players
from gungame51.core.players.shortcuts import Player
from gungame51.core.players.shortcuts import setAttribute

# ============================================================================
# >> ADDON REGISTRATION/INFORMATION
# ============================================================================
info = AddonInfo()
info.name = 'gg_elimination'
info.title = 'GG Elimination' 
info.author = 'GG Dev Team' 
info.version = '0.1'
info.requires = ['gg_turbo', 'gg_dead_strip', 'gg_dissolver']
info.conflicts = ['gg_deathmatch', 'gg_knife_elite']
info.translations = ['gg_elimination']

# ============================================================================
# >> GLOBAL VARIABLES
# ============================================================================

# ============================================================================
# >> CLASSES
# ============================================================================
class RoundInfo(object):
    def __init__(self):
        self.active = False
        self.round = 0

roundInfo = RoundInfo()

# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    if inMap():
        roundInfo.active = True

    # Get userids of all connected players
    setAttribute('#all', 'eliminated', [])
    

# ============================================================================
# >> GAME EVENTS
# ============================================================================
def es_map_start(event_var):
    # Reset round tracking
    roundInfo.active = False
    roundInfo.round = 0

def round_start(event_var):
    # Round tracking
    roundInfo.active = True
    roundInfo.round += 1

    # Reset all eliminated player counters
    setAttribute('#all', 'eliminated', [])

    # Send the round information message
    msg('#human', 'RoundInfo', prefix=True)

def round_end(event_var):
    # Set round inactive
    roundInfo.active = False

def player_activate(event_var):
    # Create player dictionary
    userid = int(event_var['userid'])
    setAttribute(userid, 'eliminated', [])

def player_disconnect(event_var):
    userid = int(event_var['userid'])
    ggPlayer = Player(userid)

    # Respawn eliminated players if needed
    if ggPlayer.eliminated:
        respawnEliminated(userid, currentRound)

    # Delete the "eliminated" attribute from the disconnecting player
    del ggPlayer.eliminated

def player_death(event_var):
    
    # Check to see if the round is active
    if not roundInfo.active:
        return

    # Get userid and attacker userids
    userid = int(event_var['userid'])
    attacker = int(event_var['attacker'])
    ggVictim = Player(userid)
    ggAttacker = Player(attacker)

    # Was suicide?
    if userid == attacker or attacker == 0:
        gamethread.delayed(5, respawnPlayer, (userid, roundInfo.round))
        ggVictim.msg('SuicideAutoRespawn', prefix=True)

    # Was a teamkill?
    elif event_var['es_userteam'] == event_var['es_attackerteam']:
        gamethread.delayed(5, respawnPlayer, (userid, roundInfo.round))
        ggVictim.msg('TeamKillAutoRespawn', prefix=True)

    # Was a normal death
    else:
        # Add victim to the attackers eliminated players
        ggAttacker.eliminated.append(userid)

        # Tell them they will respawn when their attacker dies
        index = ggAttacker.index

        ggVictim.saytext2(index, 'RespawnWhenAttackerDies', 
        {'attacker': event_var['es_attackername']}, True)

    # Check if victim had any Eliminated players
    gamethread.delayed(1, respawnEliminated, (userid, roundInfo.round))

# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
def respawnPlayer(userid, respawnRound):
    # Make sure the round is active
    if not roundInfo.active:
        return
    
    # Check if respawn was issued in the current round
    if roundInfo.round != respawnRound:
        return
    
    # Retrieve the playerlib player object
    plPlayer = getPlayer(userid)

    # Make sure the player is respawnable
    if not plPlayer.isdead or es.getplayerteam(userid) < 2:
        return
    
    # Retrieve the GunGame player object
    ggPlayer = Player(userid)
    
    # Tell everyone that they are respawning
    saytext2('#human', ggPlayer.index, 'RespawningPlayer', 
    {'player': es.getplayername(userid)}, True)
    
    # Respawn player
    ggPlayer.respawn()

def respawnEliminated(userid, respawnRound):       
    # Check if round is over
    if not roundInfo.active:
        return

    # Check if respawn was issued in the current round
    if roundInfo.round != respawnRound:
        return

    # Get the GunGame player object
    ggPlayer = Player(userid)

    # Check the player has any eliminated players
    if not ggPlayer.eliminated:
        return

    # Set variables
    players = []
    index = 0

    # Respawn all victims eliminated players
    for playerid in ggPlayer.eliminated:
        # Make sure the player is respawnable
        if not getPlayer(playerid).isdead or es.getplayerteam(playerid) < 2:
            continue

        # Respawn player
        Player(playerid).respawn()

        # Add to message format
        players.append('\3%s\1' % getPlayer(playerid).name)

        # Get index
        if not index:
            index = Player(playerid).index

    # Tell everyone that they are respawning
    saytext2('#human', index, 'RespawningPlayer', 
    {'player': ', '.join(players)}, True)

    # Clear victims eliminated player list
    ggPlayer.eliminated = []