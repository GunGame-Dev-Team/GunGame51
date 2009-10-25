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
import gamethread
import repeat

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.players.shortcuts import Player
from gungame51.core.leaders.shortcuts import get_leader_level

# ============================================================================
# >> ADDON REGISTRATION/INFORMATION
# ============================================================================
info = AddonInfo()
info.name = 'gg_handicap'
info.title = 'GG Handicap' 
info.author = 'GG Dev Team' 
info.version = '0.1'
info.translations = ['gg_handicap']

# ============================================================================
# >> GLOBAL VARIABLES
# ============================================================================
gg_handicap_update = es.ServerVar('gg_handicap_update')

# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    # Creating repeat loop
    loopStart()

    # Load message
    es.dbgmsg(0, 'Loaded: %s' % info.name)

def unload():
    # Delete the repeat loop
    if repeat.status('gungameHandicapLoop'):       
        repeat.delete('gungameHandicapLoop')

    # Unload message
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

        # Tell the player that their level was adjustedG
        ggPlayer.msg('LevelLowest', {'level':handicapLevel})

def round_start(event_var):
    # Start loop
    loopStart()

def gg_win(event_var):
    # Stop loop
    loopStop()

# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
def loopStart():
    myRepeat = repeat.find('gungameHandicapLoop')
    status = repeat.status('gungameHandicapLoop')

    # If the gg_handicap_update is removed
    if int(gg_handicap_update) == 0:

        # If the repeat exists, delete it
        if status > 0:
            myRepeat.delete()

        # Stop here
        return

    # Loop running ?
    if status == 0:
        # Create loop
        myRepeat = repeat.create('gungameHandicapLoop', handicapUpdate)
        myRepeat.start(int(gg_handicap_update), 0)
        return

    # If the gg_handicap_update was changed, re-create the loop
    if int(myRepeat['interval']) != float(gg_handicap_update):
        loopStop()
        gamethread.delayed(0.1, loopStart)
        return

    # Is the loop stopped?
    if status == 2:
        # Start loop
        myRepeat.start(int(gg_handicap_update), 0)

def loopStop():
    # Loop running ?
    if repeat.status('gungameHandicapLoop'):
        # Stop loop
        repeat.stop('gungameHandicapLoop')

def handicapUpdate():
    # Get the handicap level
    handicapLevel = getLevelAboveLowest()

    # Updating players    
    for userid in getLowestLevelUsers():
        # Get the player
        ggPlayer = Player(userid)

        # If the lowest level players are below the handicap level, continue
        if ggPlayer.level < handicapLevel:
            # Set player level
            ggPlayer.level = handicapLevel

            # Tell the player that their level was adjusted
            ggPlayer.msg('LevelLowest', {'level':handicapLevel})

            # Play the update sound
            ggPlayer.playsound('handicap') 

def getLowestLevelUsers():
    lowestLevel = get_leader_level()
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

    # If no levels are in the list, set 1 as the handicap level
    if len(levels) < 1:
        levels.append(1)

    # Sort levels, and return the level above lowest
    levels.sort()
    return levels[0]