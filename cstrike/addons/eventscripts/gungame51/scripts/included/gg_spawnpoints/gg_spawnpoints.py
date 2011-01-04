# ../addons/eventscripts/gungame51/scripts/included/gg_spawnpoints/gg_spawnpoints.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
from os import path

# Eventscripts Imports
import es
from cmdlib import registerServerCommand
from cmdlib import unregisterServerCommand
from playerlib import getPlayer

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.messaging.shortcuts import langstring

# =============================================================================
# >> ADDON REGISTRATION/INFORMATION
# =============================================================================
info = AddonInfo()
info.name = "gg_spawnpoints"
info.title = "GG Spawnpoints" 
info.author = "GG Dev Team" 
info.version = "5.1.%s" %"$Rev$".split('$Rev: ')[1].split()[0]
info.translations = ["gg_spawnpoints"]

# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
filePath = None
# Used to store prop information for spawn_show
propIndexes = {}
# The model used for spawn_show
propModel = "player/ct_gign.mdl"

# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    es.dbgmsg(0, "Loaded: %s" % info.name)

    # Register server commands
    registerServerCommand("spawn_add", cmd_spawn_add, "Adds a spawnpoint at " +
                                                        "the users location")
    registerServerCommand("spawn_remove", cmd_spawn_remove, "Remove the " +
                "spawnpoint closest to the userid passed after the command")
    registerServerCommand("spawn_remove_all", cmd_spawn_remove_all, "Removes"+
                                                        " all spawn points")
    registerServerCommand("spawn_print", cmd_spawn_print, "Prints " +
                                        "spawnpoints into the server console")
    registerServerCommand("spawn_show", cmd_spawn_show, "Toggles spawn point" +
                                                        " models on and off")
    get_map_file()
    
def unload():
    es.dbgmsg(0, 'Unloaded: %s' % info.name)

    # Unregister server commands
    unregisterServerCommand("spawn_add")
    unregisterServerCommand("spawn_remove")
    unregisterServerCommand("spawn_remove_all")
    unregisterServerCommand("spawn_print")
    unregisterServerCommand("spawn_show")

# =============================================================================
# >> GAME EVENTS
# =============================================================================
def es_map_start(event_var):
    get_map_file()

def round_start(event_var):
    # Clear the list of saved props for spawn_show because they are removed on
    # round_start
    propIndexes.clear()

# =============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# =============================================================================
def get_map_file():
    '''
    Stores the spawnpoint file for the current map in filePath
    '''
    global filePath
    filePath = es.ServerVar("eventscripts_gamedir") + "/cfg/gungame51/" + \
    "spawnpoints/" + str(es.ServerVar("eventscripts_currentmap")) + ".txt"

def invalid_syntax(syntax):
    es.dbgmsg(0, "Invalid Syntax. Use: %s" % syntax)

def cmd_spawn_add(args):
    # More than one argument was passed
    if len(args) != 1:
        invalid_syntax("spawn_add <userid>")
        return

    # A non-integer was passed
    userid = args[0]
    if not userid.isdigit():
        invalid_syntax("spawn_add <userid>")
        return

    # The userid does not exist
    if not es.exists("userid", userid):
        es.dbgmsg(0, langstring("OperationFailed:InvalidUserid",
                                                            {"userid":userid}))
        return

    pPlayer = getPlayer(userid)
    location = es.getplayerlocation(userid)
    angle = pPlayer.get("viewangle")

    spawnPoint = "%s %s %s %s %s %s\n" % (location[0], location[1], \
    location[2], angle[0], angle[1], angle[2])
    currentSpawnPoints = read_spawn_points()
    
    # If the spawnpoint already exists, stop here
    for sp in currentSpawnPoints:
        if sp.split(" ")[0:3] == spawnPoint.split(" ")[0:3]:
            es.dbgmsg(0, "Spawnpoint already exists.")
            return

    # Add the spawnpoint
    currentSpawnPoints.append(spawnPoint)

    write_spawn_points(currentSpawnPoints)
    es.dbgmsg(0, langstring("AddedSpawnpoint", {"point": \
                                                    spawnPoint.strip("\n")}))

    # If spawnpoints are currently being shown, toggle spawn_show off and on to
    # update the spawnpoints shown
    if len(propIndexes):
        cmd_spawn_show()
        cmd_spawn_show()

def cmd_spawn_remove(args):
    # More than one argument was passed
    if len(args) != 1:
        invalid_syntax("spawn_remove <userid>")
        return

    # A non-integer was passed
    userid = args[0]
    if not userid.isdigit():
        invalid_syntax("spawn_remove <userid>")
        return

    # The userid does not exist
    if not es.exists('userid', userid) and userid != 0:
        es.dbgmsg(0, langstring("OperationFailed:InvalidUserid",
                                                            {"userid":userid}))
        return

    pPlayer = getPlayer(userid)
    location = es.getplayerlocation(userid)

    x, y, z = location[0], location[1], location[2]
    currentSpawnPoints = read_spawn_points()

    # There are no spawnpoints to remove
    if not currentSpawnPoints:
        es.dbgmsg(0, langstring("OperationFailed:NoSpawnpoints"))
        return

    index = 0
    count = 0
    lowestTotal = -1
    # Loop through the current spawnpoints
    for sp in currentSpawnPoints:
        spList = sp.split(' ')

        # Format the spawnpoint into a list of floats
        i = 0
        for s in spList:
            spList[i] = float(s)
            i += 1

        # Get the total distance from the spawnpoint (on x, y, and z axes)
        total = 0
        total += abs(x - spList[0])
        total += abs(y - spList[1])
        total += abs(z - spList[2])

        # If this is the first spawnpoint, or the new lowest total, save it
        if lowestTotal == -1 or total < lowestTotal:
            lowestTotal = total
            index = count

        count += 1

    # Remove the spawnpoint saved for having the lowest total distance
    spawnPoint = currentSpawnPoints.pop(index)

    write_spawn_points(currentSpawnPoints)
    es.dbgmsg(0, langstring("RemovedSpawnpoint", {"point": \
                                                    spawnPoint.strip("\n")}))

    # If spawnpoints are currently being shown, toggle spawn_show off and on to
    # update the spawnpoints shown
    if len(propIndexes):
        cmd_spawn_show()
        cmd_spawn_show()

def cmd_spawn_remove_all(args):
    write_spawn_points([])
    es.dbgmsg(0, langstring("RemovedAllSpawnpoints"))
    
    # If spawnpoints are currently being shown, toggle spawn_show off and on to
    # update the spawnpoints shown
    if len(propIndexes):
        cmd_spawn_show()
        cmd_spawn_show()

def cmd_spawn_print(args):
    es.dbgmsg(0, langstring("SpawnpointsFor", {"map": \
                                str(es.ServerVar("eventscripts_currentmap"))}))

    # Loop through all spawnpoints
    index = 0
    for spawnPoint in read_spawn_points():
        sp = spawnPoint.strip("\n").split(" ")
        es.dbgmsg(0, langstring("SpawnpointInfo", {"index":index, "x":sp[0],
                                                        "y":sp[1], "z":sp[2]}))
        index += 1

def cmd_spawn_show(args=None):
    userid = es.getuserid()

    # If there are no players on the map, stop here
    if not userid:
        return

    # If spawnpoints are currently being shown, toggle them off and stop here
    if len(propIndexes):
        entityIndexes = es.createentitylist("prop_dynamic").keys()

        for index in propIndexes:
            if propIndexes[index] in entityIndexes:
                es.server.cmd("es_xremove gg_sp_prop%i" % int(index))
        propIndexes.clear()
        return

    # Loop through the spawnpoints
    count = 0
    for spawnPoint in read_spawn_points():
        spawnPoint = spawnPoint.strip("\n")
        location = []
        angle = []
        location.extend(spawnPoint.split(" ")[0:3])
        angle.extend(spawnPoint.split(" ")[3:6])

        # Create prop and name it
        playerView = getPlayer(userid).get("viewangle")
        es.server.cmd("es_xprop_dynamic_create %s %s" % (userid, propModel))
        es.server.cmd("es_xentsetname %s gg_sp_prop%i" % (userid, count))
        es.server.cmd("es_xsetang %i %f %f" % (userid, playerView[0], 
                                                playerView[1]))

        # Get index
        propIndex = int(es.ServerVar("eventscripts_lastgive"))

        # Set position and collision group
        es.setindexprop(propIndex, "CBaseEntity.m_CollisionGroup", 2)
        es.setindexprop(propIndex, "CBaseEntity.m_vecOrigin", 
                                                "%s, %s, %s" % (location[0],
                                                                location[1],
                                                                location[2]))
        es.setindexprop(propIndex, "CBaseEntity.m_angRotation", 
                                                "0, %s, 0" % angle[1])

        # Set aestetics
        es.server.cmd('es_xfire %s ' % userid + 
            'prop_dynamic SetAnimation "walk_lower"')
        es.server.cmd('es_xfire %s ' % userid + 
            'prop_dynamic SetDefaultAnimation  "walk_lower"')
        es.server.cmd('es_xfire %s ' % userid + 
            'prop_dynamic AddOutput "rendermode 1"')
        es.server.cmd('es_xfire %s prop_dynamic alpha "160"' % userid)

        # Add to prop index points
        propIndexes[count] = propIndex
        count += 1

    # If there were no spawnpoitns to be shown, tell them
    if count == 0:
        es.dbgmsg(0, langstring("OperationFailed:NoSpawnpoints"))

def read_spawn_points():
    if not path.isfile(filePath):
        return []

    spawnPointFile = open(filePath, "r")
    spawnPoints = spawnPointFile.readlines()
    spawnPointFile.close()

    return spawnPoints

def write_spawn_points(spawnpoints):
    spawnPointFile = open(filePath, "w")
    spawnPointFile.writelines(spawnpoints)
    spawnPointFile.close()