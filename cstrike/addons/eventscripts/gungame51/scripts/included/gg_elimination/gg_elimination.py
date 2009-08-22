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
from playerlib import getPlayer as plPlayer
import gamethread

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.messaging.shortcuts import msg
from gungame51.core.messaging.shortcuts import saytext2
from gungame51.core.players.shortcuts import Player as ggPlayer

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
        playersEliminated[str(userid)] = []
    
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
    roundActive = 1
    currentRound = +1
    
    # Reset all eliminated player counters
    for player in playersEliminated:
        playersEliminated[player] = []
    
    msg('#human', 'RoundInfo', prefix=True)

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
        del playersEliminated[userid]

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
        msg(userid, 'SuicideAutoRespawn', prefix=True)
    
    # Was a teamkill?
    elif event_var['es_userteam'] == event_var['es_attackerteam']:
        gamethread.delayed(5, respawnPlayer, (userid, currentRound))
        msg(userid, 'TeamKillAutoRespawn', prefix=True)
    
    # Was a normal death
    else:
        es.msg('norm death 1')
        # Add victim to the attackers eliminated players
        playersEliminated[attacker].append(userid)
        
        es.msg('norm death 2')
        
        # Tell them they will respawn when their attacker dies
        index = plPlayer(attacker).index
        
        es.msg('norm death 3')
        saytext2(userid, index, 'RespawnWhenAttackerDies', {'attacker': event_var['es_attackername']}, True)
        es.msg('norm death 4')
    
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
    if not plPlayer(userid).isdead or not plPlayer(userid).isobserver:
        return
    
    index = plPlayer(userid).index
    
    # Tell everyone that they are respawning
    saytext2('#human', index, 'RespawningPlayer', {'player': es.getplayername(userid)}, True)
    
    # Respawn player
    ggPlayer(userid).respawn()

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
        if not plPlayer(userid).isdead or not plPlayer(userid).isobserver:
            continue
        
        # Respawn player
        ggPlayer(playerid).respawn()
        
        # Add to message format
        players.append('\3%s\1' % es.getplayername(playerid))
        
        # Get index
        if not index:
            index = plPlayer(userid).index
    
    # Tell everyone that they are respawning
    saytext2('#human', index, 'RespawningPlayer', {'player': ', '.join(players)}, True)
    
    # Clear victims eliminated player list
    playersEliminated[userid] = []