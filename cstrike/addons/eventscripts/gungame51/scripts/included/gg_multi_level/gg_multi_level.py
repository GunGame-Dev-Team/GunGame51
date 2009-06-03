# ../addons/eventscripts/gungame/scripts/included/gg_multi_level/gg_multi_level.py

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
import gamethread
import playerlib

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.players import Player

# ============================================================================
# >> ADDON REGISTRATION/INFORMATION
# ============================================================================
info = AddonInfo()
info.name = 'gg_multi_level'
info.title = 'GG Multi Level' 
info.author = 'GG Dev Team' 
info.version = '0.1'

# ============================================================================
# >> GLOBAL VARIABLES
# ============================================================================
multiLevelSound = "null.wav"

# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():

    # Load up each player and set their multikill attribute
    for userid in es.getUseridList():
        Player(userid).multiKills = 0
        
        # Also add the userid to our playerList
        Player(userid).multiKillEntities = []

    es.dbgmsg(0, 'Loaded: %s' % info.name)
    
def unload():
    es.dbgmsg(0, 'Unloaded: %s' % info.name)
    
# ============================================================================
# >> GAME EVENTS
# ============================================================================
def player_activate(event_var):

    # Add the player's multikill attribute
    userid = int(event_var['userid'])
    Player(userid).multiKills = 0
    Player(userid).multiKillEntities = []
    
def player_disconnect(event_var):
    userid = int(event_var['userid'])
    
    # Remove this player and any of their entities
    if Player(userid).multiKillEntities:
        # Get rid of their multilevel
        removeMultiLevel(userid)

def gg_levelup(event_var):
    userid = int(event_var['userid'])
    attackerid = int(event_var['attacker'])   
    
    # Remove the multi-level for the victim
    victim = Player(userid)
    if victim.multiKillEntities:
        
        # Remove the multiLevel
        removeMultiLevel(userid)
        
        # Cancel the gamethread
        gamethread.cancelDelayed("%i_multilevel" % userid)
        
        # Reset their kills
        victim.multiKills = 0
        
    # Was it a suicide?
    if userid == attackerid:
        return
        
    if attackerid == 0:
        return
        
    # Teamkill?
    if int(es.getplayerteam(userid)) == int(es.getplayerteam(attackerid)):
        return
    
    # Increment multi-kills for attacker
    attacker = Player(attackerid)
    attacker.multiKills += 1
    
    # Is it greater than or equal to our threshold?
    if attacker.multiKills >= int(es.ServerVar("gg_multi_level")):
        # Multi-Level them
        doMultiLevel(attackerid)
        
        # Reset their kills
        attacker.multiKills = 0
        
        # Remove multilevel in 10
        gamethread.delayedname(10, "%i_multilevel" % attackerid, removeMultiLevel, attackerid)
        
# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
def doMultiLevel(userid):
    global multiLevelSound
    
    es.msg(userid)
    
    # Check userid validity
    if es.exists('userid', userid):
        
        # Tell everyone we leveled!
        es.centermsg("%s multi-leveled!" % es.getplayername(userid))
        
        # Play game sound
        # ...
        
        # Create env_spark
        cmdFormat = 'es_xgive %s env_spark; ' % userid
        cmdFormat += 'es_xfire %s env_spark SetParent !activator;' % userid
        cmdFormat += 'es_xfire %s env_spark AddOutput "spawnflags 896";' % userid
        cmdFormat += 'es_xfire %s env_spark AddOutput "angles -90 0 0";' % userid
        cmdFormat += 'es_xfire %s env_spark AddOutput "magnitude 8"; ' % userid
        cmdFormat += 'es_xfire %s env_spark AddOutput "traillength 3";' % userid
        cmdFormat += 'es_xfire %s env_spark StartSpark' % userid
        es.server.cmd(cmdFormat)
        
        # Grab it's index
        spark_index = int(es.ServerVar("eventscripts_lastgive"))
        
        # Create player_speedmod
        cmdFormat = 'es_xgive %i player_speedmod; ' %userid
        cmdFormat += 'es_xfire %i player_speedmod ModifySpeed 1.5; ' %userid
        es.server.cmd(cmdFormat)
        
        # Grab it's index
        speedmod_index = int(es.ServerVar("eventscripts_lastgive"))
        
        # Append it to this player's list
        if spark_index:
            Player(userid).multiKillEntities.append(spark_index)
        if speedmod_index:
            Player(userid).multiKillEntities.append(speedmod_index)
            
        # Fire gg_multi_level
        es.dbgmsg(0, "Firing gg_multi_level event!")
        es.event('initialize', 'gg_multi_level')
        es.event('setint', 'gg_multi_level', 'userid', userid)
        es.event('setint', 'gg_multi_level', 'leveler', userid)
        es.event('fire', 'gg_multi_level')
        
def removeMultiLevel(userid):
    # Check validity
    if es.exists('userid', userid):

        # Reset player speed and gravity (yes, I know this is the lame way but hey ;D
        playerlib.getPlayer(userid).set('speed', 1.0)
        es.server.queuecmd('es_xfire %s !self "gravity 400"' % userid)
        
        # Remove the ent indexes
        while Player(userid).multiKillEntities:
            ind = Player(userid).multiKillEntities.pop()

            validIndexes = es.createentitylist('player_speedmod')
            validIndexes.update(es.createentitylist('env_spark'))
            
            if ind not in validIndexes.keys():
                es.dbgmsg(0, '')
                es.dbgmsg(0, '-'*30)
                es.dbgmsg(0, 'OH LOOOOOOOOOOOOOOKIE!!! I PREVENTED A CRASH JUST NOW!')
                es.dbgmsg(0, '-'*30)
                es.dbgmsg(0, '')
                
            else:
                es.server.queuecmd('es_xremove %i' % ind)
            
        # Clear the list
        del Player(userid).multiKillEntities[:]