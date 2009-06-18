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

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.messaging.shortcuts import msg
from gungame51.core.messaging.shortcuts import saytext2
from gungame51.core.players.shortcuts import Player
from gungame51.core.players.shortcuts import isDead
from gungame51.core.players.shortcuts import isSpectator

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

roundActive = 0
currentRound = 0
playersEliminated = {}

# ============================================================================
# >> CLASSES
# ============================================================================


# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    # Get userids of all connected players
    for userid in es.getUseridList():
        dict_playersEliminated[str(userid)] = []
    
# ============================================================================
# >> GAME EVENTS
# ============================================================================

def es_map_start(event_var):
    global roundActive, currentRound
    
    # Reset round tracking
    roundActive = 0
    currentRound = 0

def round_start(event_var):
    global roundActive, currentRound
    
    # Round tracking
    roundActive = 0
    currentRound = 0
    
    # Reset all eliminated player counters
    for player in dict_playersEliminated:
        playersEliminated[player] = []
    
    msg('#all', 'RoundInfo')

def round_end(event_var):
    global roundActive
    
    # Set round inactive
    roundActive = 0

def player_activate(event_var):
    # Create player dictionary
    playersEliminated[event_var['userid']] = []

def player_disconnect(event_var):
    userid = event_var['userid']
    
    # Remove diconnecting player from player dict
    if userid in playersEliminated:
        respawnEliminated(userid, currentRound)
        del dict_playersEliminated[userid]

def player_death(event_var):
    # Check to see if the round is active
    if not roundActive:
        return
    
    # Get userid and attacker userids
    userid = event_var['userid']    
    attacker = event_var['attacker']
    
    # Was suicide?
    if userid == attacker or attacker == '0':
        gamethread.delayed(5, respawnPlayer, (userid, currentRound))
        msg(userid, 'SuicideAutoRespawn')
    
    # Was a teamkill?
    elif event_var['es_userteam'] == event_var['es_attackerteam']:
        gamethread.delayed(5, respawnPlayer, (userid, currentRound))
        msg(userid, 'TeamKillAutoRespawn')
    
    # Was a normal death
    else:
        # Add victim to the attackers eliminated players
        playersEliminated[attacker].append(userid)
        
        # Tell them they will respawn when their attacker dies
        index = gungamelib.getPlayer(attacker)['index']
        saytext2('gg_elimination', userid, index, 'RespawnWhenAttackerDies', {'attacker': event_var['es_attackername']})
    
    # Check if victim had any Eliminated players
    gamethread.delayed(1, respawnEliminated, (userid, currentRound))

# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================

def respawnPlayer(userid, respawnRound):
    # Make sure the round is active
    if not roundActive:
        return
    
    # Check if respawn was issued in the current round
    if currentRound != respawnRound:
        return
    
    # Make sure the player is respawnable
    if not isDead(userid) or not isSpectator(userid):
        return
    
    index = getPlayer(userid).index
    
    # Tell everyone that they are respawning
    saytext2('#all', index, 'RespawningPlayer', {'player': es.getplayername(userid)})
    
    # Respawn player
    Player(userid).respawn()

def respawnEliminated(userid, respawnRound):    
    # Check if round is over
    if not roundActive:
        return
    
    # Check if respawn was issued in the current round
    if currentRound != respawnRound:
        return
    
    # Check to make sure that the userid still exists in the dictionary
    if userid not in playersEliminated:
        return
    
    # Check the player has any eliminated players
    if not playersEliminated[userid]:
        return
    
    # Set variables
    players = []
    index = 0
    
    # Respawn all victims eliminated players
    for playerid in playersEliminated[userid]:
        # Make sure the player exists
        if not isDead(userid) or not isSpectator(userid):
            continue
        
        # Respawn player
        Player(playerid).respawn()
        
        # Add to message format
        players.append('\3%s\1' % es.getplayername(playerid))
        
        # Get index
        if not index:
            index = getPlayer(userid).index
    
    # Tell everyone that they are respawning
    saytext2('#all', index, 'RespawningPlayer', {'player': ', '.join(players)})
    
    # Clear victims eliminated player list
    playersEliminated[userid] = []