# ../addons/eventscripts/gungame/scripts/included/gg_map_vote/gg_map_vote.py

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

# Eventscripts Imports
import es
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
info.version = '0.1'
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
eventscripts_currentmap = es.ServerVar('eventscripts_currentmap')

# Player command backup var
player_command_backup = '%s' % gg_map_vote_player_command 

# Dictionary to store the location of the source of the map files
dict_mapListSource = {1:get_game_dir('mapcycle.txt'),
                      2:get_game_dir('maplist.txt'),
                      3:get_game_dir('%s.txt' % str(gg_map_vote_file) if not \
                                   '.txt' in str(gg_map_vote_file) else \
                                   str(gg_map_vote_file)),
                      4:get_game_dir('maps')}

# List to store the maps previously voted for "gg_map_vote_dont_show_last_maps"
list_lastMaps = []

# Holds options and the userids that voted for them
mapVoteOptions = {}

# Holds a list of userid's that have been sent the vote (for dead players)
voteSentUserids = []

# Holds userids that have recenty used the !vote command
voteCmdUserids = []

# Instance of popuplib
ggVote = None

# Holds a list of userids at the time the vote was started
voteUserids = []

# True/False if vote has allready been ran this map
voteHasStarted = None
                    
# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    # Check to see if GunGame's voting system is to be used
    if int(gg_map_vote) == 1:
    
        # Create player vote command
        registerPlayerCmd()
            
        # Store the current map in the list of recently played maps
        if int(gg_map_vote_dont_show_last_maps):
            list_lastMaps.append(eventscripts_currentmap)
    
        # Check file location if using list_source = 3
        mapFileClean(True)
    
    # Loaded message
    es.dbgmsg(0, 'Loaded: %s' % info.name)

def unload():
    # Unregister player command ?
    if int(es.exists('saycommand', '%s' % gg_map_vote_player_command)):        
        es.unregsaycmd('%s' % gg_map_vote_player_command)    
   
    cleanVote()
    
    # Unloaded message
    es.dbgmsg(0, 'Unloaded: %s' % info.name)

# =============================================================================
#  GAME EVENTS
# =============================================================================
def es_map_start(event_var):
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

    global voteHasStarted
    voteHasStarted = False
    
def gg_levelup(event_var):
    # Vote has allready been started?
    if voteHasStarted:
        return
    
    # Start vote ? 
    if get_leader_level() <= (get_total_levels() - int(gg_map_vote_trigger)):
        return
    
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
def mapFileClean(fromLoad=False):    
    # Using a custom list ?
    if int(gg_map_vote_list_source) != 3:
        return
        
    # Skip this part on initial load
    if not fromLoad:
        # Current source file
        current_file =  get_game_dir('%s.txt' % str(gg_map_vote_file) if not \
                    '.txt' in str(gg_map_vote_file) else str(gg_map_vote_file))
        
        # Did it change ?                            
        if dict_mapListSource[3] != current_file:
            dict_mapListSource[3] = current_file
    
    # Look for it in /cstrike
    if exists(dict_mapListSource[3]):
        return
        
    # Look for file in other common folders
    for folder in ('cfg/', 'cfg/gungame/', 'cfg/gungame51/'):
        possible_path = get_game_dir(folder + '%s.txt' % str(gg_map_vote_file) \
             if not '.txt' in str(gg_map_vote_file) else str(gg_map_vote_file))
        
        # File exists in the other location ?
        if exists(possible_path):                   
            dict_mapListSource[3] = possible_path
            es.dbgmsg(0,'>>>> GunGame has found "%s" ' % gg_map_vote_file +
                        'in (%s) Please change your config file to ' % folder + 
                        'reflect the location! (I.E. cfg/gungame/myfile.txt)')
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
            {'name':es.getplayername(userid), 'map':choice.lower()})
    
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
    
    # Set eventscripts_nextmapoverride to the winning map
    es.ServerVar('eventscripts_nextmapoverride').set(winner)
    
    # Set Mani 'nextmap' if Mani is loaded
    if str(es.ServerVar('mani_admin_plugin_version')) != '0':
        es.server.queuecmd('ma_setnextmap %s' % winner)
    
    # Set SourceMod 'nextmap' if SourceMod is loaded
    if str(es.ServerVar('sourcemod_version')) != '0':
        es.server.queuecmd('sm_nextmap %s' % winner)
    
    # Play sound
    for userid in getUseridList('#human'):
        Player(userid).playsound('endofvote')

    cleanVote()
        
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

    # Set var so we know the vote has started    
    global voteHasStarted
    voteHasStarted = True
            
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
    
    if timeleft == 1:
        hudhint('#human', 'Countdown_Singular', {'time': int(gg_map_vote_time), 
            'voteInfo': None, 'votes': votes, 
            'totalVotes': len(voteUserids)})
        return     
    
    if timeleft <= 5:
        hudhint('#human', 'Countdown_Plural', {'time': int(gg_map_vote_time), 
            'voteInfo': None, 'votes': votes, 
            'totalVotes': len(voteUserids)})

def getMapList():
    # Check to make sure the value of "gg_map_vote" is 1-4
    if int(gg_map_vote_list_source) not in range(1, 5):
        raise ValueError('"gg_map_vote_list_source" must be 1-4: current ' +
            'value "%s"' % int(gg_map_vote))
        
    # Check the maps directory for a list of all maps (option 4)
    if int(gg_map_vote_list_source) == 4:
        files = listdir(dict_mapListSource[4])
        maps = [x.strip('.bsp') for x in files if splitext(x)[1] == '.bsp']

    else:
        # Check a specific file for a list of all maps (options 1-3)
        with open(dict_mapListSource[int(gg_map_vote_list_source)], 'r') as f:
            # Normal list ?
            if int(gg_map_vote_list_source) != 3:
                maps = [x.strip() for x in f.readlines() if x.strip() != '']
            
            # Restriction list ?
            else:
            	maps = [z[0] for z in [y.replace(' ' * (y.count(' ') - 1), 
                        '').split(' ') for y in [x.strip().replace('\t', ' ') 
                        for x in f.readlines()] if not (y == '' or
                        y.startswith('/'))] if len(z) == 1 or (int(z[1]) if
                        z[1].isdigit() else 0) <= len(getUseridList('#all'))]
                        
    # Remove any maps from the list that were voted for previously
    if int(gg_map_vote_dont_show_last_maps):
        for map_name in list_lastMaps:
            if map_name in maps:
                maps.remove(map_name)  
          
    # Make sure that the maps list is not empty
    if not maps:
        error = 'The map list generated by "gg_map_vote" is empty.'
        
        # Could it be do to the restrictions ?
        if int(gg_map_vote_list_source) == 3:
            error += (' **You should add more maps or reduce your ' +
                     'min player restrictions ' +
                     '(Currently: %s).' % dict_mapListSource[3])            

        # Could it be do to too many last maps ?
        if int(gg_map_vote_dont_show_last_maps):
            error += (' **You should reduce ' + 
                      'gg_map_vote_dont_show_last_maps ' +
                      '(File: %s) ' % gg_map_vote_dont_show_last_maps +
                      'or add more maps.')
        
        raise ValueError(error)          
                
    # Only allow the number of maps as declared by "gg_map_vote_size"
    if int(gg_map_vote_size):
        while len(maps) > int(gg_map_vote_size):
            maps.remove(random.choice(maps))
    
    random.shuffle(maps)
    return maps

def registerPlayerCmd():   
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
    global player_command_backup
    player_command_backup = '%s' % gg_map_vote_player_command