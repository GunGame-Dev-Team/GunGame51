# ../addons/eventscripts/gungame51/scripts/included/gg_multi_level/gg_multi_level.py

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
from playerlib import getPlayer

# SPE Imports
import spe

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.events import fireEvent
from gungame51.core.players import Player
from gungame51.core.players.shortcuts import setAttribute
from gungame51.core.players.shortcuts import deleteAttribute
from gungame51.core.messaging.shortcuts import centermsg
from gungame51.core.messaging.shortcuts import saytext2

# ============================================================================
# >> ADDON REGISTRATION/INFORMATION
# ============================================================================
info = AddonInfo()
info.name = 'gg_multi_level'
info.title = 'GG Multi Level' 
info.author = 'GG Dev Team' 
info.version = '0.1'
info.translations = ['gg_multi_level']

# ============================================================================
# >> GLOBAL VARIABLES
# ============================================================================
gg_multi_level = es.ServerVar("gg_multi_level")
gg_multi_level_tk_reset = es.ServerVar("gg_multi_level_tk_reset")
gg_multi_level_speed = es.ServerVar("gg_multi_level_speed")
gg_multi_level_gravity = es.ServerVar("gg_multi_level_gravity")

# Dict of players currently getting the multi-level boost and the sound played
# for them
currentMultiLevel = {}

# ============================================================================
# >> CLASSES
# ============================================================================

# Manages and maintains Gravity when it is reset by touching specific entities
# Thanks to Freddukes for creating the original
# http://forums.eventscripts.com/viewtopic.php?t=23958
class GravityManager(object):
    '''
    Class to manager the tick listener, and to manage the players gravity
    '''
    def __init__(self):
        '''
        Create 2 self. variables
        '''
        self.gravityList = {}

    def addGravityChange(self, userid, amount):
        '''
        Check if there are already any players in the gravityChange list.
        If there isn't, start the tick listener. Following this, check
        if the userid is in the dictionary, if so, remove them. Then create
        a new instance.
        '''
        userid = int(userid)

        if not len(self.gravityList):
            gamethread.delayedname(0.25, 'gravity_check', self._ticker)

        if userid in self.gravityList:
            self.removeGravityChange(userid)

        if es.exists('userid', userid):
            self.gravityList[userid] = {
                'lastairvalue': es.getplayerprop(userid, 
                                                 'CBasePlayer.m_fFlags'), 
                'gravity': amount, 
                'lastmovementvalue': es.getplayerprop(userid, 
                                                      'CBaseEntity.movetype')
            }
        else:
            self.gravityList[userid] = {
                'lastairvalue': 0, 
                'gravity': amount, 
                'lastmovementvalue': 2
            }

        self._resetGravity(userid, amount)

    def removeGravityChange(self, userid):
        '''
        Check if the player is in the dictioanry. If so, reset their gravity 
        to 1 and delete their instance from the dictionary. If there are no 
        more players within the gravityList, remove the tick listener.
        '''
        userid = int(userid)

        if userid in self.gravityList:
            del self.gravityList[userid]
            self._resetGravity(userid, 1.0)
        else:
            es.server.queuecmd('es_xfire %s !self ' % userid + 
                               'addoutput "gravity 1.0" 0.1 1')

        if not len(self.gravityList):
            for player in self.gravityList:
                _resetGravity(player, 1.0)
            gamethread.cancelDelayed('gravity_check')

    def deleteGravityList(self):
        '''
        Loop through all the players, reset their gravity to 1, delete the 
        gravity list then unregister the tick listener.
        '''
        for player in self.gravityList:
            _resetGravity(player, 1.0)

        del self.gravityList

        gamethread.cancelDelayed('gravity_check')

    def _ticker(self):
        '''
        Here we loop through all of the players, and check their gravity etc.
        '''
        # Loop through all players in the gravity dictionary
        for player in self.gravityList:
            try:
                if es.exists('userid', player):
                    newaval = es.getplayerprop(player, 'CBasePlayer.m_fFlags')
                    newmval = es.getplayerprop(player, 'CBaseEntity.movetype')
                else:
                    newaval = 0
                    newmval = 2

                if self.gravityList[player]['lastairvalue'] != newaval or \
                self.gravityList[player]['lastmovementvalue'] != newmval:
                    # Player has jumped or come off of a ladder
                    self._resetGravity(player, 
                                       self.gravityList[player]['gravity'])

                self.gravityList[player]['lastairvalue']      = newaval
                self.gravityList[player]['lastmovementvalue'] = newmval
            except:
                continue

        gamethread.delayedname(0.25, 'gravity_check', self._ticker)

    def _resetGravity(self, userid, amount):
        # Change the players gravity to value amount.
        es.server.queuecmd('es_xfire %s !self addoutput ' % userid + 
                           '"gravity %s" 0.1 1' % amount)

gravity = GravityManager()

# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    # Set each player's multilevel attributes
    setAttribute('#all', 'multiLevels', 0)
    setAttribute('#all', 'multiLevelEntities', [])

    es.dbgmsg(0, 'Loaded: %s' % info.name)

def unload():
    # For all users currently multi-leveling
    for userid in currentMultiLevel:
        # Cancel the gamethread
        gamethread.cancelDelayed("%i_multilevel" % userid)

        # Remove bonus effects
        remove_multi_level(userid)

    # Make sure that the listener shuts down
    gravity.deleteGravityList()

    # Kill off our custom attributes
    deleteAttribute("#all", "multiLevels")
    deleteAttribute("#all", "multiLevelEntities")

    es.dbgmsg(0, 'Unloaded: %s' % info.name)

# ============================================================================
# >> GAME EVENTS
# ============================================================================
def player_activate(event_var):
    ggPlayer = Player(event_var['userid'])

    # Add the player's multikill attribute
    ggPlayer.multiLevels = 0
    ggPlayer.multiLevelEntities = []

def player_disconnect(event_var):
    # Get event information
    userid = int(event_var['userid'])

    # Remove this player and any of their entities
    if userid in currentMultiLevel:
        # Get rid of their multilevel
        remove_multi_level(userid)

        gravity.removeGravityChange(userid)

        # Cancel the gamethread
        gamethread.cancelDelayed("%i_multilevel" % userid)

    # Players may disconnect before activating, causing an error
    try:
        # Kill off our custom attributes
        deleteAttribute(userid, "multiLevels")
        deleteAttribute(userid, "multiLevelEntities")
    except ValueError:
        return

def player_death(event_var):
    # Get event information
    userid = int(event_var['userid'])

    # Does the player currently have a multi-level bonus?
    if userid in currentMultiLevel:
        # Cancel the gamethread
        gamethread.cancelDelayed("%i_multilevel" % userid)

        # Remove bonus effects
        remove_multi_level(userid)
    
    # Do we ignore team kills?
    if event_var['es_attackerteam'] == event_var['es_userteam']:
        if int(gg_multi_level_tk_reset):
            return
    
    # Resetting the player's multi-kills
    Player(userid).multiLevels = 0
    
def es_map_start(event_var):
    # For all players
    for userid in currentMultiLevel:
        # Cancel the gamethread
        gamethread.cancelDelayed("%i_multilevel" % userid)
        
        # Remove them from the gravity class
        gravity.removeGravityChange(userid)
    
    # Clear the list of players currently multi-leveling
    currentMultiLevel.clear()

def round_start(event_var):
    stop_multi_levelers()

def gg_win(event_var):
    stop_multi_levelers()

def gg_levelup(event_var):
    # Get event information
    userid = int(event_var['userid'])
    attacker = int(event_var['attacker'])   

    # Was it a suicide?
    if userid == attacker:
        return

    # Did the player fall to their death?
    if not attacker:
        return

    # Teamkill?
    if int(es.getplayerteam(userid)) == int(es.getplayerteam(attacker)):
        return

    # Increment multi-kills for attacker
    ggPlayer = Player(attacker)
    ggPlayer.multiLevels += 1
    # Is it greater than or equal to our threshold?
    if ggPlayer.multiLevels >= int(gg_multi_level):
        # If they currently have the bonus
        if attacker in currentMultiLevel:
            
            # Cancel the gamethread
            gamethread.cancelDelayed("%i_multilevel" % attacker)

            # Remove the bonus
            remove_multi_level(attacker)

        # Multi-Level them
        do_multi_level(attacker)

        # Reset their kills
        ggPlayer.multiLevels = 0

        # Remove multilevel in 10
        gamethread.delayedname(10, "%i_multilevel" % attacker, 
                               remove_multi_level, attacker)

# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
def stop_multi_levelers():
    # For all players
    for userid in es.getUseridList():
        ggPlayer = Player(userid)
        
        # Make sure their multiLevels are reset
        ggPlayer.multiLevels = 0
        
        if userid in currentMultiLevel:
            # Cancel the gamethread
            gamethread.cancelDelayed("%i_multilevel" % userid)

            # Remove bonus effects
            remove_multi_level(userid)
        
        ggPlayer.multiLevelEntities = []

    # Clear the list of players currently multi-leveling
    currentMultiLevel.clear()

def do_multi_level(userid):
    # Check userid validity
    if es.exists('userid', userid):

        # Retrieve the player's name
        name = es.getplayername(userid)

        # Tell everyone we leveled!
        centermsg('#all', "CenterMultiLevelled", {'name':name})
        saytext2('#all', Player(userid).index, 'MultiLevelled', {'name': name})

        # Play game sound
        sound = Player(userid).emitsound('multilevel')
        
        # Add the player to the multi-leveling dictionary with the sound to
        # remove
        currentMultiLevel[userid] = sound

        # Create env_spark
        spark_instance = spe.giveNamedItem(userid, "env_spark")
        spark_index = spe.getIndexOfEntity(spark_instance)

        cmd = 'es_xfire %s env_spark SetParent !activator;' %userid
        cmd += 'es_xfire %s env_spark AddOutput "spawnflags 896";' %userid
        cmd += 'es_xfire %s env_spark AddOutput "angles -90 0 0";' %userid
        cmd += 'es_xfire %s env_spark AddOutput "magnitude 8";' %userid
        cmd += 'es_xfire %s env_spark AddOutput "traillength 3";' %userid
        cmd += 'es_xfire %s env_spark StartSpark' %userid
        es.server.queuecmd(cmd)

        # Set the player's speed
        getPlayer(userid).speed = int(gg_multi_level_speed) / 100.0

        # If gg_multi_level_gravity is enabled, ajust the player's gravity
        if int(gg_multi_level_gravity) != 100 and \
        int(gg_multi_level_gravity) >= 0:
            gravity.addGravityChange(userid, 
                                     int(gg_multi_level_gravity) * 0.01)

        # Append the spark's index to this player's list
        if spark_index:
            Player(userid).multiLevelEntities.append(spark_index)

        # Fire gg_multi_level
        event_values = {}
        event_values["userid"] = ("int", userid)
        event_values["leveler"] = ("int", userid)
        gamethread.delayed(0, fireEvent, ("gg_multi_level", event_values))

def remove_multi_level(userid):
    # Check validity
    if es.exists('userid', userid):

        # Reset player speed and gravity
        getPlayer(userid).speed = 1.0
        gravity.removeGravityChange(userid)
        
        # Get the Player() object
        ggPlayer = Player(userid)

        # Remove the ent indexes
        while ggPlayer.multiLevelEntities:
            ind = ggPlayer.multiLevelEntities.pop()

            # Create entitylists for the sparks
            validIndexes = es.createentitylist('env_spark')

            # If the saved index of the index given to the player still exists
            #   remove it.
            if ind in validIndexes.keys():
                spe.removeEntityByIndex( ind )

        # Stop the sound
        es.stopsound(userid, currentMultiLevel[userid])

        # Remove the player from the current multi level list
        del currentMultiLevel[userid]