# ../addons/eventscripts/gungame/scripts/included/gg_handicap/gg_handicap.py

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
from gungame51.core.leaders.shortcuts import getLeaderLevel

# ============================================================================
# >> ADDON REGISTRATION/INFORMATION
# ============================================================================
info = AddonInfo()
info.name = 'gg_handicap'
info.title = 'GG Handicap' 
info.author = 'GG Dev Team' 
info.version = '0.1'

# ============================================================================
# >> GLOBAL VARIABLES
# ============================================================================


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
def player_activate(event_var):
    userid = int(event_var['userid'])

    # Get the level of the lowest level player other than themself
    handicapLevel = getLevelAboveUser(userid)
    # Get the player
    ggPlayer = Player(userid)

    # If their level is below the handicap level, set them to it
    if ggPlayer.level < handicapLevel:
        ggPlayer.level = handicapLevel

        # Tell the player that their level was adjusted
        """
        REPLACE WHEN TRANSLATIONS ARE WORKING
        ggPlayer.msg('LevelLowest', {'level':handicapLevel})
        """
        es.tell(userid, '#multi', 'Your level was set to #green%s#default because it was below the rest.' % handicapLevel)

# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
def getLowestLevelUsers():
    lowestLevel = getLeaderLevel()
    userList = []

    # Loop through the users
    for userid in es.getUseridList():
        # If the player is not on an active team, skip them
        if int(es.getplayerteam(userid)) <= 1:
            continue

        # Get the player's level
        playerLevel = Player(userid).level

        # If their level is lower than the previous lowestLevel, reset it
        if playerLevel < lowestLevel:
            lowestLevel = playerLevel

            # Add the player to the userList for the lowestLevel
            userList = [userid]

        # If their level is equal to the lowestLevel, add them to userList
        elif playerLevel == lowestLevel:
            userList.append(userid)

    return userList

def getLevelAboveLowest():
    levels = []

    # Loop through the users
    for userid in es.getUseridList():
        # If the player is not on an active team, skip them
        if int(es.getplayerteam(userid)) <= 1:
            continue


        # Get the player's level
        playerLevel = Player(userid).level

        # If the player's level is not in levels already, add it
        if not playerLevel in levels:
            levels.append(playerLevel)

    # If there is only one level, return it
    if len(levels) == 1:
        return levels[0]

    # Sort levels, and return the level above lowest
    levels.sort()
    return levels[1]

def getLevelAboveUser(uid):
    levels = []

    # Loop through the users
    for userid in es.getUseridList():
        # If the player is not on an active team, skip them
        if int(es.getplayerteam(userid)) <= 1:
            continue

        # If the player is the one we are checking for, skip them
        if userid == uid:
            continue

        # Get the player's level
        playerLevel = Player(userid).level

        # If the player's level is not in levels already, add it
        if not playerLevel in levels:
            levels.append(playerLevel)

    # Sort levels, and return the level above lowest
    levels.sort()
    return levels[0]