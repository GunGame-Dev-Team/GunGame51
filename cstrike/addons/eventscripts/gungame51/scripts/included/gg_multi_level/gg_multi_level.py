# gungame/scripts/included/gg_multi_level.py

'''
$Rev: 13 $
$LastChangedBy: micbarr $
$LastChangedDate: 2009-04-06 20:23:27 -0400 (Mon, 06 Apr 2009) $
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
playerList = []
multiLevelSound = "null.wav"

# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    global playerList

    # Load up each player and set their multikill attribute
    for userid in es.getUseridList():
        Player(userid).multikills = 0
        
        # Also add the userid to our playerList
        Player(userid).multikillEntities = []

    es.dbgmsg(0, 'Loaded: %s' % info.name)
    
def unload():
    es.dbgmsg(0, 'Unloaded: %s' % info.name)
    
# ============================================================================
# >> GAME EVENTS
# ============================================================================
def player_activate(event_var):
    global playerList
    
    # Add the player's multikill attribute
    userid = int(event_var['userid'])
    Player(userid).multikills = 0
    Player(userid).multikillEntities = []
    
def player_disconnect(event_var):
    userid = int(event_var['userid'])
    
    # Remove this player and any of their entities
    if userid in playerList:
        # Get rid of their multilevel
        doRemoveMultiLevel(userid)

def player_death(event_var):
    userid = int(event_var['userid'])
    attackerid = int(event_var['attacker'])
    
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
    attacker.multikills += 1
    
    # Is it greater than or equal to our threshold?
    if attacker.multikills >= int(es.ServerVar("gg_multi_level")):
        # Multi-Level them
        doMultiLevel(attackerid)
        
        # Reset their kills
        attacker.multikills = 0
        
        # Remove multilevel in 10
        gamethread.delayedname(10, "%i_multilevel" % attackerid, removeMultiLevel, attackerid)
        
# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
def doMultiLevel(userid):
    global playerList
    global multiLevelSound
    
    es.msg(userid)
    
    # Check userid validity
    if es.exists('userid', userid):
        
        # Tell everyone we leveled!
        es.centermsg("%s multi-leveled!" % es.getplayername(userid))
        
        # Play game sound
        # ...
        
        # Create env_spark
        cmdFormat = 'es_xgive %s env_spark; ' %userid
        cmdFormat += 'es_xfire %s env_spark SetParent !activator;' %userid
        cmdFormat += 'es_xfire %s env_spark AddOutput "spawnflags 896";' %userid
        cmdFormat += 'es_xfire %s env_spark AddOutput "angles -90 0 0";' %userid
        cmdFormat += 'es_xfire %s env_spark AddOutput "magnitude 8"; ' %userid
        cmdFormat += 'es_xfire %s env_spark AddOutput "traillength 3";' %userid
        cmdFormat += 'es_xfire %s env_spark StartSpark' %userid
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
            Player(userid).multikillEntities.append(spark_index)
        if speedmod_index:
            Player(userid).multikillEntities.append(speedmod_index)
        
def removeMultiLevel(userid):
    # Check validity
    if es.exists('userid', userid):

        # Reset player speed and gravity (yes, I know this is the lame way but hey ;D
        playerlib.getPlayer(userid).set('speed', 1.0)
        es.server.queuecmd('es_xfire %s !self "gravity 400"' % userid)
        
        # Remove the ent indexes
        es.dbgmsg(0, Player(userid).multikillEntities)
        while Player(userid).multikillEntities:
            ind = Player(userid).multikillEntities.pop()
            #es.msg(ind)
            validIndexes = es.createentitylist('player_speedmod')
            validIndexes.update(es.createentitylist('env_spark'))
            es.dbgmsg(0, validIndexes.keys())
            
            if ind not in validIndexes.keys():
                es.dbgmsg(0, '')
                es.dbgmsg(0, '-'*30)
                es.dbgmsg(0, 'OH LOOOOOOOOOOOOOOKIE!!! I PREVENTED A CRASH JUST NOW!')
                es.dbgmsg(0, '-'*30)
                es.dbgmsg(0, '')
                
            
            es.server.queuecmd('es_xremove %i' % ind)
            
        # Clear the list
        del Player(userid).multikillEntities[:]