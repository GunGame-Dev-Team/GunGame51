# ../scripts/included/gg_map_vote/gg_map_vote.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
from __future__ import with_statement
import random
from os import listdir
from os.path import splitext
from os.path import exists
from operator import itemgetter

# Eventscripts Imports
import es
from cmdlib import registerSayCommand
from cmdlib import unregisterSayCommand
import gamethread
import repeat
import popuplib
from playerlib import getUseridList

# GunGame Imports
from gungame51.core import get_game_dir
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.players.shortcuts import Player
from gungame51.core.messaging.shortcuts import saytext2
from gungame51.core.messaging.shortcuts import msg
from gungame51.core.messaging.shortcuts import hudhint
from gungame51.core.messaging.shortcuts import langstring
from gungame51.core.events.shortcuts import EventManager
from gungame51.core.leaders.shortcuts import get_leader_level
from gungame51.core.weapons.shortcuts import get_total_levels

# =============================================================================
# >> ADDON REGISTRATION/INFORMATION
# =============================================================================
info = AddonInfo()
info.name = 'gg_map_vote'
info.title = 'GG Map Vote'
info.author = 'GG Dev Team'
info.version = "5.1.%s" % "$Rev$".split('$Rev: ')[1].split()[0]
info.translations = ['gg_map_vote']

# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Server Vars
gg_map_vote = es.ServerVar('gg_map_vote')
gg_map_vote_command = es.ServerVar('gg_map_vote_command')
gg_map_vote_size = es.ServerVar('gg_map_vote_size')
gg_map_vote_trigger = es.ServerVar('gg_map_vote_trigger')
gg_map_vote_time = es.ServerVar('gg_map_vote_time')
gg_map_vote_dont_show_last_maps = es.ServerVar(
                                    'gg_map_vote_dont_show_last_maps')
gg_map_vote_show_player_vote = es.ServerVar('gg_map_vote_show_player_vote')
gg_map_vote_file = es.ServerVar('gg_map_vote_file')
gg_map_vote_list_source = es.ServerVar('gg_map_vote_list_source')
gg_map_vote_player_command = es.ServerVar('gg_map_player_command')
gg_map_vote_after_death = es.ServerVar('gg_map_vote_after_death')

gg_map_vote_rtv = es.ServerVar('gg_map_vote_rtv')
gg_map_vote_rtv_command = es.ServerVar('gg_map_vote_rtv_command')
gg_map_vote_rtv_levels_required = es.ServerVar('' +
    'gg_map_vote_rtv_levels_required')
gg_map_vote_rtv_percent = es.ServerVar('gg_map_vote_rtv_percent')
gg_map_vote_nominate = es.ServerVar('gg_map_vote_nominate')
gg_map_vote_nominate = es.ServerVar('gg_map_vote_nominate')
gg_map_vote_nominate_command = es.ServerVar('gg_map_vote_nominate_command')

eventscripts_currentmap = es.ServerVar('eventscripts_currentmap')
eventscripts_maphandler = es.ServerVar('eventscripts_maphandler')
eventscripts_maphandler_backup = int(eventscripts_maphandler)
eventscripts_maphandler.set(1)

# Player command backup var
player_command_backup = '%s' % gg_map_vote_player_command

# Dictionary to store the location of the source of the map files
dict_mapListSource = {1: get_game_dir('mapcycle.txt'),
                      2: get_game_dir('maplist.txt'),
                      3: get_game_dir('%s.txt' % str(gg_map_vote_file) if not \
                                   '.txt' in str(gg_map_vote_file) else \
                                   str(gg_map_vote_file)),
                      4: get_game_dir('maps')}

# List to store the maps previously voted for "gg_map_vote_dont_show_last_maps"
list_lastMaps = []

# Holds options and the userids that voted for them
mapVoteOptions = {}

# Holds a list of userid's that have been sent the vote (for dead players)
voteSentUserids = []

# Holds userids that have recenty used the !vote command
voteCmdUserids = []

# Holds map nominations
nominations = []

# Instance of popuplib
ggVote = None

# Holds a list of userids at the time the vote was started
voteUserids = []

winningMap = None

# True/False if vote has allready been ran this map
voteHasStarted = False

# The level which, once the leader hits, disables RTV
rtv_DisableLevel = get_total_levels() * gg_map_vote_rtv_levels_required / 100

# The list of userids who have voted to RTV
rtvList = []

# Has the vote been rocked?
voteRocked = False


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    # Check to see if GunGame's voting system is to be used
    if int(gg_map_vote) == 1:

        # Create player vote command
        registerPlayerCmd()

        # Register RTV and nomination commands
        registerSayCommand(str(gg_map_vote_rtv_command), rtv_cmd, '' +
                                                            'RTV command.')
        registerSayCommand(str(gg_map_vote_nominate_command), nominate_cmd,
                                                        'Nominate command.')

        # Store the current map in the list of recently played maps
        if int(gg_map_vote_dont_show_last_maps):
            list_lastMaps.append(str(eventscripts_currentmap))

        # Check file location if using list_source = 3
        mapFileClean(True)

    # Loaded message
    es.dbgmsg(0, 'Loaded: %s' % info.name)


def unload():
    # Unregister player command ?
    if int(es.exists('saycommand', '%s' % gg_map_vote_player_command)):
        es.unregsaycmd('%s' % gg_map_vote_player_command)
    if int(es.exists('saycommand', '%s' % gg_map_vote_rtv_command)):
        unregisterSayCommand(str(gg_map_vote_rtv_command))
    if int(es.exists('saycommand', '%s' % gg_map_vote_nominate_command)):
        unregisterSayCommand(str(gg_map_vote_nominate_command))

    eventscripts_maphandler.set(eventscripts_maphandler_backup)

    cleanVote()

    # Unloaded message
    es.dbgmsg(0, 'Unloaded: %s' % info.name)


# =============================================================================
#  GAME EVENTS
# =============================================================================
def server_cvar(event_var):
    cvarName = event_var['cvarname']

    # If the weapon order changed, get the new rtv_DisableLevel
    if cvarName in ['gg_weapon_order_file', 'gg_weapon_order_sort_type']:
        global rtv_DisableLevel
        rtv_DisableLevel = (get_total_levels() *
            gg_map_vote_rtv_levels_required / 100)


def gg_win(event_var):
    if winningMap:
        es.set('nextlevel', winningMap)


def es_map_start(event_var):
    global voteHasStarted
    global voteRocked
    voteHasStarted = False

    # Clear any nominations and RTV userids
    del nominations[:]
    del rtvList[:]

    # Reset RTV
    voteRocked = False

    # Check to see if GunGame's voting system is to be used
    if int(gg_map_vote) > 1:
        return

    # Store the map to the list of recently played maps
    if int(gg_map_vote_dont_show_last_maps):

        # Make sure isn't already in the list
        if not event_var['mapname'] in list_lastMaps:
            list_lastMaps.append(event_var['mapname'])

        # Check to make sure that we remove maps once we have reached the count
        if len(list_lastMaps) > int(gg_map_vote_dont_show_last_maps):
            del list_lastMaps[0]

    cleanVote()
    mapFileClean()


def gg_levelup(event_var):
    global voteHasStarted
    # Vote has allready been started?
    if voteHasStarted:
        return

    # Start vote ?
    if get_leader_level() < (get_total_levels() - int(gg_map_vote_trigger)):
        return

    # Change global so we dont fire the vote twice
    voteHasStarted = True

    # Use 3rd party voting system ?
    if int(gg_map_vote) > 1:
        es.server.queuecmd('%s' % gg_map_vote_command)
        return

    voteStart()


def player_death(event_var):
    # Using 3rd party voting system ?
    if int(gg_map_vote) > 1:
        return

    # Only send to dead players ?
    if not int(gg_map_vote_after_death):
        return

    userid = int(event_var['userid'])

    # Is map vote running ?
    if popuplib.exists('gg_map_vote'):
        ggVote.send(userid)


def player_disconnect(event_var):
    userid = int(event_var['userid'])

    # Player had voting ability ?
    if userid not in voteUserids:
        return

    # Player did vote ?
    if userid in reduce(lambda a, b: a + b, mapVoteOptions.values()):
        return

    # Remove userid from list
    voteUserids.remove(userid)

    # Everyone voted ?
    if isVoteDone():
        voteEnd()


# =============================================================================
#  HELPER FUNCTIONS
# =============================================================================
def rtv_cmd(userid, args):
    global voteRocked
    # The vote has already been rocked for this map
    if voteRocked:
        msg(userid, "RTVInitiated", {}, True)
        return

    # The leader level is past the level to disable RTV
    if  get_leader_level() >= rtv_DisableLevel:
        msg(userid, "RTVPastLevel", {"level": rtv_DisableLevel}, True)
        return

    # Removed userids no longer in the server
    checkList = rtvList
    for uid in checkList:
        if not es.exists("userid", uid):
            rtvList.remove(uid)

    # The number of total votes required to RTV
    votesRequired = int((len(getUseridList("#human")) *
                                gg_map_vote_rtv_percent / 100.0) + 0.999)
    # The user has already voted
    if userid in rtvList:
        if not len(rtvList) >= votesRequired:
            saytext2("#human", Player(userid).index, "RTVVote",
                {"name": es.getplayername(userid), "votes": len(rtvList),
                "required": votesRequired})
            return
    else:
        rtvList.append(userid)

    # The vote passed
    if len(rtvList) >= votesRequired:
        msg("#human", "RTVPassed", {}, True)
        voteStart()
        voteRocked = True
    else:
        saytext2("#human", Player(userid).index, "RTVVote",
            {"name": es.getplayername(userid), "votes": len(rtvList),
            "required": votesRequired})


def nominate_cmd(userid, args):
    # The nominations list is full
    if len(nominations) >= int(gg_map_vote_size):
        msg(userid, "NominationsFull", {"size": int(gg_map_vote_size)}, True)
        return

    nomVote = popuplib.easymenu('gg_map_vote_nominate', None, nominateSubmit)

    # Set title and add some options
    nomVote.settitle('Nominate map for next vote:')

    # Add maps as options
    mapList = sorted(getMapList(allMaps=True, excludeNominations=True))
    if not mapList:
        msg(userid, "VoteListEmpty", {}, True)
        return

    for map_name in mapList:
        if map_name in list_lastMaps or map_name in nominations:
            continue

        nomVote.addoption(map_name, map_name.lower())

    # Send the menu
    nomVote.send(userid)


def nominateSubmit(userid, choice, popupname):
    # It has already been chosen while their popup was open
    if choice in nominations:
        msg(userid, "NominatedAlready", {"map": choice}, True)
        return

    # The nominations list is full
    if len(nominations) >= int(gg_map_vote_size):
        msg(userid, "NominationsFull", {"size": int(gg_map_vote_size)}, True)
        return

    # Add the chosen nomination
    nominations.append(choice)
    saytext2("#human", Player(userid).index, "Nominated",
        {"pName": es.getplayername(userid), "map": choice,
        "cmd": str(gg_map_vote_nominate_command)}, True)


def mapFileClean(fromLoad=False):
    # Using a custom list ?
    if int(gg_map_vote_list_source) != 3:
        return

    # Skip this part on initial load
    if not fromLoad:
        # Current source file
        current_file = get_game_dir('%s.txt' % str(gg_map_vote_file) if not \
                    '.txt' in str(gg_map_vote_file) else str(gg_map_vote_file))

        # Did it change ?
        if dict_mapListSource[3] != current_file:
            dict_mapListSource[3] = current_file

    # Look for it in /cstrike
    if exists(dict_mapListSource[3]):
        return

    # Look for file in other common folders
    for folder in ('cfg/', 'cfg/gungame51/'):
        possible_path = get_game_dir(folder + '%s.txt' % str(gg_map_vote_file)
             if not '.txt' in str(gg_map_vote_file) else str(gg_map_vote_file))

        # File exists in the other location ?
        if exists(possible_path):
            dict_mapListSource[3] = possible_path
            es.dbgmsg(0, '>>>> GunGame has found "%s" ' % gg_map_vote_file +
                    'in (%s) Please change your config file to ' % folder +
                    'reflect the location! (I.E. cfg/gungame51/myfile.txt)')
            return

    # File couldn't be found, raising error
    raise IOError('The file (%s) ' % gg_map_vote_file +
                  'could not be found!  GunGame attempted to find the ' +
                  'file in other locations and was unsuccessful.  The ' +
                  'server will default to the mapcycle.txt')


def isVoteDone():
    # Less votes than voters ?
    total_votes = len(reduce(lambda a, b: a + b, mapVoteOptions.values()))
    if len(voteUserids) > total_votes:
        return False
    return True


def cleanVote():
    # Clear options
    mapVoteOptions.clear()

    # Delete popup ?
    if popuplib.exists('gg_map_vote'):
        popuplib.delete('gg_map_vote')

    # Delete repeat ?
    if repeat.find('gg_map_vote'):
        repeat.delete('gg_map_vote')

    # Clear userid lists
    del voteSentUserids[:]
    del voteCmdUserids[:]
    del voteUserids[:]

    global ggVote
    ggVote = None


def voteSubmit(userid, choice, popupname):
    # Is a revote ?
    for option in mapVoteOptions.keys():
        if userid in mapVoteOptions[option]:

            # Is not the same choice ?
            if choice != option:
                mapVoteOptions[option].remove(userid)
                mapVoteOptions[choice].append(userid)
                break

            # Same choice, stop here
            else:
                return

    # Is a new vote
    else:
        mapVoteOptions[choice].append(userid)

    # Announce players choice if enabled
    if int(gg_map_vote_show_player_vote):
        saytext2('#human', Player(userid).index, 'VotedFor',
            {'name': es.getplayername(userid), 'map': choice.lower()})

    # Everyone voted ?
    if isVoteDone():
        voteEnd()


def voteEnd():
    # Stop repeat ?
    ggRepeat = repeat.find('gg_map_vote')
    if ggRepeat:
        ggRepeat.stop()

    # Unsend all menus
    ggVote.unsend(voteUserids)

    winner = []
    win_votes = None
    total_votes = len(reduce(lambda a, b: a + b, mapVoteOptions.values()))

    if not total_votes:
        msg('#human', 'NotEnoughVotes', {}, True)

        # Choose a random map
        winner = random.choice(mapVoteOptions.keys())

        # Set the server up for map change
        set_nextmap(winner)

        # Win message for the map that we randomely chose
        msg('#human', 'WinningMap', {'map': winner.lower(), 'totalVotes': 0,
                                                            'votes': 0}, True)
        cleanVote()
        return

    # Find winner
    for option in mapVoteOptions:
        votes = len(mapVoteOptions[option])
        # No votes ?
        if not votes:
            continue

        # First option with any votes ?
        if not winner:
            winner.append(option)
            continue

        win_votes = len(mapVoteOptions[winner[0]])

        # Loser ?
        if votes < win_votes:
            continue

        # Winner ?
        if votes > win_votes:
            del winner[:]
            winner.append(option)
            continue

        # Tie
        winner.append(option)

    # Make sure we have a winning vote count
    if not win_votes:
        win_votes = len(mapVoteOptions[winner[0]])

    # Random winner
    winner = random.choice(winner)

    # Win message
    msg('#human', 'WinningMap', {'map': winner.lower(),
                        'totalVotes': total_votes, 'votes': win_votes}, True)

    # Set the server up for map change
    set_nextmap(winner)

    # Play sound
    for userid in getUseridList('#human'):
        Player(userid).playsound('endofvote')

    # If this was a RTV, end the map
    if voteRocked:
        userid = es.getuserid()
        es.ServerVar("mp_chattime").set(5)
        es.server.queuecmd("es_xgive %s game_end" % userid)
        es.server.queuecmd("es_xfire %s game_end EndGame" % userid)

    cleanVote()


def set_nextmap(mapName):
    global winningMap
    winningMap = mapName

    # Set eventscripts_nextmapoverride to the winning map
    es.ServerVar('eventscripts_nextmapoverride').set(mapName)

    # Set Mani 'nextmap' if Mani is loaded
    if str(es.ServerVar('mani_admin_plugin_version')) != '0':
        es.server.queuecmd('ma_setnextmap %s' % mapName)

    # Set SourceMod 'nextmap' if SourceMod is loaded
    if str(es.ServerVar('sourcemod_version')) != '0':
        es.server.queuecmd('sm_nextmap %s' % mapName)


def voteSendcmd():
    # Is map vote running ?
    if not popuplib.exists('gg_map_vote'):
        return

    userid = es.getcmduserid()

    if userid not in voteUserids:
        return

    if userid in voteCmdUserids:
        return

    voteCmdUserids.append(userid)
    gamethread.delayed(3, voteCmdUserids.remove, userid)
    ggVote.send(userid)


def voteStart():
    # Create a new vote
    global ggVote
    ggVote = popuplib.easymenu('gg_map_vote', None, voteSubmit)

    msg('#human', 'PlaceYourVotes', {}, True)

    # Set question and add some options
    ggVote.settitle('Please vote for the next map:')

    # Add maps as options
    for map_name in getMapList():
        ggVote.addoption(map_name, map_name.lower())
        mapVoteOptions[map_name] = []

    # Users eligable to vote
    voteUserids.extend(getUseridList('#human'))

    # Only send to dead players ?
    if int(gg_map_vote_after_death):
        voteSentUserids.extend(getUseridList('#human, #dead'))
        ggVote.send(voteSentUserids)

    # Send it to everyone
    else:
        ggVote.send(voteUserids)

    # Start the repeat
    voteRepeat = repeat.create('gg_map_vote', voteCountDown)
    voteRepeat.start(1, int(gg_map_vote_time))

    # Fire event
    EventManager().gg_vote()


def voteCountDown():
    ggRepeat = repeat.find('gg_map_vote')
    if not ggRepeat:
        return

    timeleft = ggRepeat['remaining']

    # Stop the vote ?
    if timeleft == 0:
        voteEnd()
        return

    votes = len(reduce(lambda a, b: a + b, mapVoteOptions.values()))

    voteInfo = ""
    mapsAdded = 0
    # For the map with the most votes to the least
    sortItems = []
    for map in mapVoteOptions.items():
        sortItems.append((map[0], len(map[1])))

    for map in sorted(sortItems, key=itemgetter(1), reverse=True):
        # Add up to three maps
        voteInfo += langstring('MapVotes', tokens={'map': map[0],
                                                        'votes': map[1]})
        mapsAdded += 1
        if mapsAdded >= 3:
            break

    # Should we play the countdown beep
    if timeleft <= 5:
        for userid in getUseridList('#human'):
            Player(userid).playsound('countDownBeep')

        # Show the singular hudhint and stop here
        if timeleft == 1:
            hudhint('#human', 'Countdown_Singular', {'time': timeleft,
                'voteInfo': voteInfo, 'votes': votes,
                'totalVotes': len(voteUserids)})
            return
    # Show the normal hudhint
    hudhint('#human', 'Countdown_Plural', {'time': timeleft,
        'voteInfo': voteInfo, 'votes': votes,
        'totalVotes': len(voteUserids)})


def getMapList(allMaps=False, showLastMaps=False, excludeNominations=False):
    # Check to make sure the value of "gg_map_vote" is 1-4
    if int(gg_map_vote_list_source) not in range(1, 5):
        raise ValueError('"gg_map_vote_list_source" must be 1-4: current ' +
            'value "%s"' % int(gg_map_vote))

    # Get the map files to check through later to make sure our capitalization
    # is correct and that all the files exist
    files = listdir(dict_mapListSource[4])
    mapFiles = [str(x)[:-4] for x in files if splitext(x)[1] == '.bsp']

    # Check the maps directory for a list of all maps (option 4)
    if int(gg_map_vote_list_source) == 4:
        maps = mapFiles
    else:
        # Check a specific file for a list of all maps (options 1-3)
        with open(dict_mapListSource[int(gg_map_vote_list_source)], 'r') as f:
            # Normal list ?
            if int(gg_map_vote_list_source) != 3:
                maps = [x.strip() for x in f.readlines() if x.strip() != ''
                        and not x.strip().startswith("//")]

            # Restriction list ?
            else:
                maps_from_file = x.strip().replace('\t', ' ')
                                    for x in f.readlines()
                                    
                maps = []
                for map in maps_from_file:
                    if map == "" or map.startswith("/"):
                        continue
                    map = map.replace('  ', ' ').split(' ')
                    
                    numPlayers = len(getUseridList('#all'))
                    # No min or max
                    if len(map) == 1:
                        maps.append(map[0])
                    # Just min
                    else if len(map) == 2:
                        if not map[1].isdigit():
                            continue

                        if numPlayers < map[1]:
                            continue
                        
                        maps.append(map[0])
                    # Min and max
                    else if len(map) == 3:
                        if not (map[1].isdigit() and map[2].isdigit()):
                            continue

                        if numPlayers < map[1] or numPlayers > map[2]:
                            continue
                        
                        maps.append(map[0])

    # Make sure the map exists on the server, and that the capitalization is
    # correct
    lowerCaseMaps = [x.lower() for x in maps]
    maps = []
    for map in mapFiles:
        if not map.lower() in lowerCaseMaps:
            continue

        maps.append(map)

    # Remove any maps from the list that were voted for previously
    if int(gg_map_vote_dont_show_last_maps) and not showLastMaps:
        for map_name in list_lastMaps:
            if map_name in maps:
                maps.remove(map_name)

    # Make sure that the maps list is not empty
    if not maps:
        error = 'The map list generated by "gg_map_vote" is empty.'

        # Could it be due to the restrictions ?
        if int(gg_map_vote_list_source) == 3:
            error += (' **You should add more maps or reduce your ' +
                     'min player restrictions ' +
                     '(Currently: %s).' % dict_mapListSource[3])

        # Could it be due to too many last maps ?
        if int(gg_map_vote_dont_show_last_maps):
            error += (' **You should reduce ' +
                      'gg_map_vote_dont_show_last_maps ' +
                      '(File: %s) ' % gg_map_vote_dont_show_last_maps +
                      'or add more maps.')

        raise ValueError(error)

    # Only allow the number of maps as declared by "gg_map_vote_size"
    if int(gg_map_vote_size) and not allMaps:
        while len(maps) > int(gg_map_vote_size):
            maps.remove(random.choice(maps))

    # Add nominated maps
    if not excludeNominations:
        for map_name in nominations:
            # If the nominated map is already in the vote, skip it
            if map_name in maps:
                continue

            maps.pop(0)
            maps.append(map_name)
        # Remove saved nominations
        del nominations[:]

    random.shuffle(maps)
    return maps


def registerPlayerCmd():
    global player_command_backup

    # Is blank/disabled ?
    if gg_map_vote_player_command in ['', '0']:
        return

    # New command ?
    if gg_map_vote_player_command != player_command_backup:

        # Does the new command allready exist?
        if int(es.exists('saycommand', gg_map_vote_player_command)):

            # Send error and stop
            raise ValueError('(%s) ' % gg_map_vote_player_command +
                        'is allready a registered command!')

        # Does the old command exist?
        if int(es.exists('saycommand', gg_map_vote_player_command)):

            # Unregister old command
            es.unregsaycmd(player_command_backup)

    # Command was allready loaded ?
    if int(es.exists('saycommand', gg_map_vote_player_command)):
        return

    # Register new command
    es.regsaycmd(gg_map_vote_player_command, voteSendcmd, 'Allows ' +
                     'players to vote for the next map. (gg_map_vote)')

    # Backup command
    player_command_backup = '%s' % gg_map_vote_player_command