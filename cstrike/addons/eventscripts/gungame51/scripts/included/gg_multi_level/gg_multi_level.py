# ../addons/eventscripts/gungame/scripts/included/gg_multi_level/gg_multi_level.py

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
list_currentMultiLevel = []

# ============================================================================
# >> CLASSES
# ============================================================================

# Manages and maintains Gravity when it is reset by touching specific entities
# Thanks to Freddukes for creating the original
class gravityManager(object):
    """ Class to manager the tick listener, and to manage the players gravity """
    def __init__(self):
        """ Create 2 self. variables """
        self.gravityList = {}

    def addGravityChange(self, userid, amount):
        """ Check if there are already any players in the gravityChange list.
            If there isn't, start the tick listener. Following this, check
            if the userid is in the dictionary, if so, remove them. Then create
            a new instance. """
        userid = str(userid)
        if not len(self.gravityList):
            gamethread.delayedname(0.25, 'gravity_check', self._ticker)
        if userid in self.gravityList:
            self.removeGravityChange(userid)
        if es.exists('userid', userid):
            self.gravityList[userid] = {'lastairvalue': es.getplayerprop(userid, 'CBasePlayer.m_fFlags'), 'gravity': amount, 'lastmovementvalue': es.getplayerprop(userid, 'CBaseEntity.movetype')}
        else:
            self.gravityList[userid] = {'lastairvalue': 0, 'gravity': amount, 'lastmovementvalue': 2}
        self._resetGravity(userid, amount)

    def removeGravityChange(self, userid):
        """ Check if the player is in the dictioanry. If so, reset their gravity to 1
            and delete their instance from the dictionary. If there are no more players
            within the gravityList, remove the tick listener """
        userid = str(userid)
        if userid in self.gravityList:
            del self.gravityList[userid]
            self._resetGravity(userid, 1.0)
        else:
            es.server.queuecmd('es_xfire %s !self addoutput "gravity %s" 0.1 1'%(userid, 1.0))
        if not len(self.gravityList):
            for player in self.gravityList:
                _resetGravity(player, 1.0)
            gamethread.cancelDelayed('gravity_check')

    def deleteGravityList(self):
        """ Loop through all the players, reset their gravity to 1, delete the gravity
            list then unregister the tick listener. """
        for player in self.gravityList:
            _resetGravity(player, 1.0)
        del self.gravityList
        gamethread.cancelDelayed('gravity_check')

    def _ticker(self):
        """ Here we loop through all of the players, and check their gravity etc. """
        for player in self.gravityList:
            try:
                if es.exists('userid', player):
                    newaval = es.getplayerprop(player, 'CBasePlayer.m_fFlags')
                    newmval = es.getplayerprop(player, 'CBaseEntity.movetype')
                else:
                    newaval = 0
                    newmval = 2
                if self.gravityList[player]['lastairvalue'] != newaval or self.gravityList[player]['lastmovementvalue'] != newmval:
                    """ Player has jumped or came off a ladder """
                    self._resetGravity(player, self.gravityList[player]['gravity'])
                self.gravityList[player]['lastairvalue']      = newaval
                self.gravityList[player]['lastmovementvalue'] = newmval
            except:
                continue
        gamethread.delayedname(0.25, 'gravity_check', self._ticker)

    def _resetGravity(self, userid, amount):
        """ Change the players gravity to value amount. """
        es.server.queuecmd('es_xfire %s !self addoutput "gravity %s" 0.1 1'%(userid, amount))

gravity = gravityManager()

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
    # For all users currently multi-leveling
    for userid in list_currentMultiLevel:
        # Cancel the gamethread
        gamethread.cancelDelayed("%i_multilevel" % userid)

        # Remove bonus effects
        removeMultiLevel(userid)

    # Make sure that the listener shuts down
    gravity.deleteGravityList()
    
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
    # Get event information
    userid = int(event_var['userid'])

    # Remove this player and any of their entities
    if userid in list_currentMultiLevel:
        # Get rid of their multilevel
        removeMultiLevel(userid)

        gravity.removeGravityChange(userid)

        # Cancel the gamethread
        gamethread.cancelDelayed("%i_multilevel" % userid)

def player_death(event_var):
    # Get event information
    userid = int(event_var['userid'])

    # Does the player currently have a multi-level bonus?
    if userid in list_currentMultiLevel:
        # Cancel the gamethread
        gamethread.cancelDelayed("%i_multilevel" % userid)

        # Remove bonus effects
        removeMultiLevel(userid)

def round_start(event_var):
    global list_currentMultiLevel

    # For all players
    for userid in es.getUseridList():
        # Make sure they 
        user = Player(userid)
        user.multiKills = 0
        if userid in list_currentMultiLevel:
            # Cancel the gamethread
            gamethread.cancelDelayed("%i_multilevel" % userid)

            # Remove bonus effects
            removeMultiLevel(userid)

    # Clear the list of players currently multi-leveling
    list_currentMultiLevel = []

def gg_levelup(event_var):
    # Get event information
    userid = int(event_var['userid'])
    attackerid = int(event_var['attacker'])   

    # Was it a suicide?
    if userid == attackerid:
        return

    # Did the player fall to their death?
    if not attackerid:
        return

    # Teamkill?
    if int(es.getplayerteam(userid)) == int(es.getplayerteam(attackerid)):
        return

    # Increment multi-kills for attacker
    attacker = Player(attackerid)
    attacker.multiKills += 1

    # Is it greater than or equal to our threshold?
    if attacker.multiKills >= int(es.ServerVar("gg_multi_level")):
        # If they currently have the bonus
        if attackerid in list_currentMultiLevel:
            # Cancel the gamethread
            gamethread.cancelDelayed("%i_multilevel" % attackerid)

            # Remove the bonus
            removeMultiLevel(attackerid)

        # Multi-Level them
        doMultiLevel(attackerid)

        # Add the player to the multi level list
        list_currentMultiLevel.append(attackerid)

        # Reset their kills
        attacker.multiKills = 0

        # Remove multilevel in 10
        gamethread.delayedname(10, "%i_multilevel" % attackerid, removeMultiLevel, attackerid)

# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
def doMultiLevel(userid):
    global multiLevelSound

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

        # If gg_multi_level_gravity is enabled, ajust the player's gravity
        gg_multi_level_gravity = es.ServerVar('gg_multi_level_gravity')
        if gg_multi_level_gravity != 100 and gg_multi_level_gravity >= 0:
            gravity.addGravityChange(userid, int(gg_multi_level_gravity) * 0.01)

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
        gravity.removeGravityChange(userid)

        # Remove the ent indexes
        while Player(userid).multiKillEntities:
            ind = Player(userid).multiKillEntities.pop()

            # Create entitylists for the speed and sparks
            validIndexes = es.createentitylist('player_speedmod')
            validIndexes.update(es.createentitylist('env_spark'))

            # If the saved index of the index given to the player still exists, remove it
            if ind in validIndexes.keys():
                es.server.queuecmd('es_xremove %i' % ind)

        # Remove the player from the current multi level list
        list_currentMultiLevel.remove(userid)