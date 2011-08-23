# ../scripts/included/gg_handicap/gg_handicap.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''


# =============================================================================
# >> IMPORTS
# =============================================================================
# Eventscripts Imports
import es
import gamethread
import repeat

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.players.shortcuts import Player
from gungame51.core.leaders.shortcuts import get_leader_level
from gungame51.core.players.shortcuts import setAttribute


# =============================================================================
# >> ADDON REGISTRATION/INFORMATION
# =============================================================================
info = AddonInfo()
info.name = 'gg_handicap'
info.title = 'GG Handicap'
info.author = 'GG Dev Team'
info.version = "5.1.%s" % "$Rev$".split('$Rev: ')[1].split()[0]
info.conflicts = ['gg_teamplay', 'gg_teamwork']
info.translations = ['gg_handicap']


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
gg_handicap_update = es.ServerVar('gg_handicap_update')
gg_handicap_max = es.ServerVar('gg_handicap_max')
gg_handicap = es.ServerVar('gg_handicap')
gg_handicap_no_reconnect = es.ServerVar('gg_handicap_no_reconnect')
gg_handicap_legacy_mode = es.ServerVar('gg_handicap_legacy_mode')

# Players that have joined a team this map [<joined a team?>, <reconnecting?>]
handicap_players = {}


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    # Creating repeat loop
    loopStart()


def unload():
    # Delete the repeat loop
    if repeat.status('gungameHandicapLoop'):
        repeat.delete('gungameHandicapLoop')


# =============================================================================
# >> GAME EVENTS
# =============================================================================
def es_map_start(event_var):
    # Delete all player information since we are starting a new map
    handicap_players.clear()


def player_activate(event_var):
    userid = int(event_var['userid'])

    # Is the player new to the map?
    if userid not in handicap_players:
        handicap_players[userid] = [False, False]

    # Player must have reconnected
    else:
        handicap_players[userid][1] = True

    # For legacy mode, delegate work to helper function
    handicap(userid, True)


def player_team(event_var):
    # Ignore everything but T/CT
    if int(event_var['team']) not in (2, 3):
        return

    userid = int(event_var['userid'])

    # Delegate work to helper function
    handicap(userid, False)


def round_start(event_var):
    # Start loop
    loopStart()


def gg_win(event_var):
    # Stop loop
    loopStop()


# =============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# =============================================================================
def handicap(userid, from_player_activate):
    # Did the request come from player_activate? (for legacy mode only)
    if from_player_activate:

        # Use legacy mode?
        if int(gg_handicap_legacy_mode):

            # Disallow reconnecting players?
            if int(gg_handicap_no_reconnect) and handicap_players[userid][1]:
                return

        # Stop here if we are not using legacy mode
        else:
            return

    # This must be a bot, they get goofy sometimes
    if userid not in handicap_players:
        handicap_players[userid] = [False, False]

    # Has the player joined a team this map?
    elif handicap_players[userid][0]:

        # Reconnecting player?
        if handicap_players[userid][1]:

            # Stop here if no reconnections allowed
            if int(gg_handicap_no_reconnect):
                return

            # Set the player's reconnecting status to no, so they don't get
            # a new weapon while switching teams
            handicap_players[userid][1] = False

        # Stop here, player isn't reconnecting
        else:
            return

    # Get the player
    ggPlayer = Player(userid)

    # Get the level of the lowest level player other than himself?
    if gg_handicap == 1:
        handicapLevel = getLevelAboveUser(userid)

    # Get the average level of the players other than himself?
    elif gg_handicap == 2:
        handicapLevel = getAverageLevel(userid)

    # Max level for joining for the first time?
    if handicapLevel > int(gg_handicap_max) > 1:
        handicapLevel = int(gg_handicap_max)

    # If their level is below the handicap level, set them to it
    if ggPlayer.level < handicapLevel:
        ggPlayer.level = handicapLevel

        # Tell the player that their level was adjusted
        ggPlayer.msg('LevelLowest', {'level': handicapLevel}, prefix=True)

    # Record the player joined a team this map
    handicap_players[userid][0] = True


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
            ggPlayer.msg('LevelLowest', {'level': handicapLevel}, prefix=True)

            # Play the update sound
            ggPlayer.playsound('handicap')


def getLowestLevelUsers():
    lowestLevel = get_leader_level()
    userList = []

    # Loop through the users
    for userid in es.getUseridList():
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
        if int(es.getplayerteam(userid)) <= 1:
            continue

        # Get the player's level
        playerLevel = Player(userid).level

        # If the player's level is not in levels already, add it
        if not playerLevel in levels:
            levels.append(playerLevel)

    # If there are no valid players to base the handicap on, return level 1
    if not levels:
        return 1

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


def getAverageLevel(uid):
    # Everyone on level 1?
    if get_leader_level() == 1:
        return 1

    levels = []

    # Loop through the players
    for userid in es.getUseridList():
        if int(es.getplayerteam(userid)) <= 1:
            continue

        # If the player is the one we are checking for, skip them
        if userid == uid:
            continue

        # Add level to the list
        levels.append(Player(userid).level)

    # Make sure the levels list is not empty (can't divide by 0)
    if len(levels) == 0:
        return 1

    # Get the average
    average = sum(levels) / len(levels)

    # Is the average 1 or less?
    if average <= 1:
        return 1

    return average
