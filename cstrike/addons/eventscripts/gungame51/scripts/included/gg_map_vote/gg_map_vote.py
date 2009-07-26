# ../addons/eventscripts/gungame/scripts/included/gg_dead_strip/gg_dead_strip.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
# Python Imports
from os import listdir
from os.path import splitext
import random

# Eventscripts Imports
import es
import votelib

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core import getGameDir
from gungame51.core.players.shortcuts import Player
from gungame51.core.messaging.shortcuts import saytext2
from gungame51.core.events.shortcuts import EventManager
from gungame51.core.leaders.shortcuts import getLeaderLevel
from gungame51.core.weapons.shortcuts import getTotalLevels

# ============================================================================
# >> ADDON REGISTRATION/INFORMATION
# ============================================================================
info = AddonInfo()
info.name = 'gg_map_vote'
info.title = 'GG Map Vote' 
info.author = 'GG Dev Team' 
info.version = '0.1'
info.translations = ['gg_map_vote']

# ============================================================================
# >> GLOBAL VARIABLES
# ============================================================================
# Get the es.ServerVar() instance of "gg_map_vote"
gg_map_vote = es.ServerVar('gg_map_vote')
# Get the es.ServerVar() instance of "gg_map_vote_command"
gg_map_vote_command = es.ServerVar('gg_map_vote_command')
# Get the es.ServerVar() instance of "gg_map_vote_size"
gg_map_vote_size = es.ServerVar('gg_map_vote_size')
# Get the es.ServerVar() instance of "gg_map_vote_trigger"
gg_map_vote_trigger = es.ServerVar('gg_map_vote_trigger')
# Get the es.ServerVar() instance of "gg_map_vote_time"
gg_map_vote_time = es.ServerVar('gg_map_vote_time')
# Get the es.ServerVar() instance of "gg_map_vote_dont_show_last_maps"
gg_map_vote_dont_show_last_maps = es.ServerVar('gg_map_vote_dont_show_last_maps')
# Get the es.ServerVar() instance of "gg_map_vote_show_player_vote"
gg_map_vote_show_player_vote = es.ServerVar('gg_map_vote_show_player_vote')
# Get the es.ServerVar() instance of "gg_vote_bots_vote"
gg_vote_bots_vote = es.ServerVar('gg_vote_bots_vote')
# Get the es.ServerVar() instance of "gg_map_vote_file"
gg_map_vote_file = es.ServerVar('gg_map_vote_file')
# Get the es.ServerVar() instance of "gg_map_vote_list_source"
gg_map_vote_list_source = es.ServerVar('gg_map_vote_list_source')
# Get the es.ServerVar() instance of "eventscripts_currentmap"
eventscripts_currentmap = es.ServerVar('eventscripts_currentmap')

# TEMP TEMP TEMP TEMP TEMP
gg_map_vote_file.set('cfg/gungame51/gg_maplist.txt')
#gg_map_vote.set(1)
gg_map_vote_size.set(4)
gg_map_vote_dont_show_last_maps.set(4)
gg_map_vote_time.set(30)
gg_map_vote_show_player_vote.set(1)

# Dictionary to store the location of the source of the map files
dict_mapListSource = {1:getGameDir('mapcycle.txt'),
                      2:getGameDir('maplist.txt'),
                      3:getGameDir('%s.txt' %str(gg_map_vote_file) if not \
                                   '.txt' in str(gg_map_vote_file) else \
                                   str(gg_map_vote_file)),
                      4:getGameDir('maps')}

# List to store the maps previously voted for "gg_map_vote_dont_show_last_maps"
list_lastMaps = []
                            
'''
WE NEED TO SEND THE VOTE TO ONLY DEAD PLAYERS.
OPTION OF USING "!vote" or "vote" TO BRING UP THE VOTE WHILE ALIVE.
'''

# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    # Check to see if GunGame's voting system is to be used
    if int(gg_map_vote) == 2:
        return
        
    # Store the map to the list of recently played maps
    if int(gg_map_vote_dont_show_last_maps):
        # Make sure that we don't somehow append a map that is already in the list
        if not str(eventscripts_currentmap) in list_lastMaps:
            list_lastMaps.append(str(eventscripts_currentmap))
            
    print getMapList()

# ============================================================================
# >> GAME EVENTS
# ============================================================================
def es_map_start(event_var):
    # Check to see if GunGame's voting system is to be used
    if int(gg_map_vote) == 2:
        return
        
    # Store the map to the list of recently played maps
    if int(gg_map_vote_dont_show_last_maps):
        # Make sure that we don't somehow append a map that is already in the list
        if not event_var['mapname'] in list_lastMaps:
            list_lastMaps.append(event_var['mapname'])
        
        # Check to make sure that we remove maps once we have reached the count
        if len(list_lastMaps) > int(gg_map_vote_dont_show_last_maps):
            del list_lastMaps[0]
            
        print getMapList()

def gg_levelup(event_var):
    if getLeaderLevel() == (getTotalLevels() - int(gg_map_vote_trigger)):
        # Nextmap already set?
        if es.ServerVar('eventscripts_nextmapoverride') != '':
            gungamelib.echo('gungame', 0, 0, 'MapSetBefore')
            return
        
        # Vote already started?
        if dict_variables['gungame_voting_started']:
            return
        
        # GG MULTI ROUND CHECK
        if dict_variables['roundsRemaining'] < 2:
            EventManager().gg_vote()
            
def gg_vote(event_var):
    dict_variables['gungame_voting_started'] = True
    
    if int(gg_map_vote) == 2:
        es.server.queuecmd(str(gg_map_vote_command))

def player_say(event_var):
    if event_var['text'] == 'vote':
        voteStart()
# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
'''
def vote_submit(userid, votename, choice, choicename):
    es.msg('%s voted for %s (option %s)' %(es.getplayername(userid), choicename, choice))

def vote_end(votename, win, winname, winvotes, winpercent, total, tie, cancelled):
    es.msg('Votename: %s, win: %s, winname: %s, winpercent: %s, total: %s, tie: %s, cancelled: %s'
        %(votename, win, winname, winpercent, total, tie, cancelled))
'''
def voteStart():
    if votelib.find('gg_map_vote'):
        votelib.delete('gg_map_vote')
        
    # Create a new vote
    myVote = votelib.create('gg_map_vote', voteEnd, voteSubmit)
    
    # Set question and add some options
    myVote.setquestion('Does GunGame rock?')
    
    for map in getMapList():
        myVote.addoption(map)
    
    # Start the vote for 90 seconds and send the menu to everyone on the server
    myVote.start(int(gg_map_vote_time))
    
def voteSubmit(userid, voteName, choice, choiceName):
    # Announce players choice if enabled
    if int(gg_map_vote_show_player_vote):
        # Announce to the world
        saytext2('#human', Player(userid).index, 'VotedFor', {'name':es.getplayername(userid), 'map':choiceName})
'''
def voteCountDown():
'''
def voteEnd(voteName, win, winName, winVotes, winPercent, total, tie, cancelled):
    es.msg(winName, 'won!')

def getMapList():
    # Check to make sure the value of "gg_map_vote" is 1-4
    if not int(gg_map_vote_list_source) in range(1, 5):
        raise ValueError('"gg_map_vote_list_source" must be 1-4: current ' + \
            'value "%s"' %int(gg_map_vote))
        
    # Check the maps directory for a list of all maps (option 4)
    if int(gg_map_vote_list_source) == 4:
        files = listdir(dict_mapListSource[4])
        maps = [x.strip('.bsp') for x in files if splitext(x)[1] == '.bsp']
    else:
        # Check a specific file for a list of all maps (options 1-3)
        file = open(dict_mapListSource[int(gg_map_vote)], 'r')
        maps = [x.strip() for x in file.readlines()]
        file.close()
    
    # Make sure that the maps list is not empty
    if not maps:
        raise ValueError('The map list provided by "gg_map_vote" is empty.')
        
    # Remove any maps from the list that were voted for previously
    if int(gg_map_vote_dont_show_last_maps):
        for map in list_lastMaps:
            if map in maps:
                maps.remove(map)
                
    # Only allow the number of maps as declared by "gg_map_vote_size"
    if int(gg_map_vote_size):
        while len(maps) > int(gg_map_vote_size):
            maps.remove(random.choice(maps))
    
    random.shuffle(maps)
    return maps