# ../addons/eventscripts/gungame/scripts/included/gg_map_vote/gg_map_vote.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
# Python Imports
import random
from os import listdir
from os.path import splitext

# Eventscripts Imports
import es
import votelib
import repeat
from playerlib import getUseridList
from popuplib import easymenu

# GunGame Imports
from gungame51.core import getGameDir
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.players.shortcuts import Player
from gungame51.core.messaging.shortcuts import saytext2
from gungame51.core.events.shortcuts import EventManager
from gungame51.core.leaders.shortcuts import get_leader_level
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
player_command_backup = '%s' % gg_map_vote_command  

# Dictionary to store the location of the source of the map files
dict_mapListSource = {1:getGameDir('mapcycle.txt'),
                      2:getGameDir('maplist.txt'),
                      3:getGameDir('%s.txt' %str(gg_map_vote_file) if not \
                                   '.txt' in str(gg_map_vote_file) else \
                                   str(gg_map_vote_file)),
                      4:getGameDir('maps')}

# List to store the maps previously voted for "gg_map_vote_dont_show_last_maps"
list_lastMaps = []
                    
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
    
    # Loaded message
    es.dbgmsg(0, 'Loaded: %s' % info.name)

def unload():
    # Unregister player command ?
    if int(es.exists('saycommand', '%s' % gg_map_vote_player_command)):        
        es.unregsaycmd('%s' % gg_map_vote_player_command)    
   
    # Did we create a vote ?
    if not votelib.exists('gg_map_vote'):
        return  
    
    # Cancel vote ?
    if votelib.isrunning('gg_map_vote'):
        ggVotelib('gg_map_vote').stop(True)      
    
    votelib.delete('gg_map_vote')
    
    # Unloaded message
    es.dbgmsg(0, 'Unloaded: %s' % info.name)

# =============================================================================
#  CLASS
# =============================================================================
'''
    Note to developers:
        This is a child of votelib and was created so we could use a player
        filter with start().  This start() also uses repeat to stop the vote
        instead of the votelib method.
'''
class ggVotelib(votelib.Vote_vote):
    def start(self, time=0, filter='#human'):
        if filter != '#human':
            filter += ', #human'        
        if not self.running:
            self.time = time
            self.running = True
            self.votes = 0
            self.popup = easymenu("vote_"+str(self.name), 
                                  "_vote_choice", _submit)
            self.popup.settitle(self.question)
            self.popup.vguititle = self.question.replace('\\n', ' - ')
            for option in self.options:
                self.popup.addoption(option, self.options[option].text)
            if self.showmenu:
                self.send(getUseridList(filter), True, False)
            if self.time > 0:
                self.doRepeat(self.name, self.time)
            else:
                self.endtime = False
        else:
            es.dbgmsg(0,"Votelib: Cannot start vote '%s', " % self.name +
                        "it is already running")
    
    def doRepeat(self, name, time):
        self.repeat = repeat.find(name)
        if not self.repeat:
            self.repeat = repeat.create(name, self.repeat_cmd)
        self.repeat.stop()
        self.repeat.start(1, time)
  
    pass

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

def gg_levelup(event_var):
    # Start vote ? 
    es.msg('level up!')
    if get_leader_level() != (getTotalLevels() - int(gg_map_vote_trigger)):
        es.msg('not right level!')
        return
    
    # Use 3rd party voting system ?  
    if int(gg_map_vote) > 1:
        es.msg('3rd party!')
        es.server.queuecmd('%s' % gg_map_vote_command)
        return

    es.msg('start vote!')
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
    if votelib.isrunning('gg_map_vote'):
        ggVotelib('gg_map_vote').send(userid)
        
    
# =============================================================================
#  HELPER FUNCTIONS
# =============================================================================
def voteSubmit(userid, voteName, choice, choiceName):
    # Announce players choice if enabled
    if int(gg_map_vote_show_player_vote):
        saytext2('#human', Player(userid).index, 'VotedFor', 
            {'name':es.getplayername(userid), 'map':choiceName})

def voteEnd(voteName, win, winName, winVotes, winPercent, total, tie, 
                                                                    cancelled):
    if cancelled:
        es.msg("The vote "+votename+" was cancelled.")
        return
    
    # Win message    
    es.msg("The option "+winname+" ["+str(win)+"] has won the vote with "
            +str(winvotes)+" ("+str(winpercent)+"%) votes.")
    
    # Set eventscripts_nextmapoverride to the winning map
    es.ServerVar('eventscripts_nextmapoverride').set(winName)
    
    # Set Mani 'nextmap' if Mani is loaded
    if str(es.ServerVar('mani_admin_plugin_version')) != '0':
        es.server.queuecmd('ma_setnextmap %s' % winName)
    
    # Set SourceMods 'nextmap' if SourceMod is loaded
    if str(es.ServerVar('sourcemod_version')) != '0':
        es.server.queuecmd('sm_nextmap %s' % winName)
    
    # Play sound
    for userid in getUseridList('#human'):
        Player(userid).playsound('endofvote')
        
def voteSendcmd():
    # Is map vote running ?
    if not votelib.isrunning('gg_map_vote'):
        return
    
    userid = es.getcmduserid()
    
    ggVotelib('gg_map_vote').send(userid, True)

def voteStart():
    if votelib.find('gg_map_vote'):
        votelib.delete('gg_map_vote')
        
    # Create a new vote
    ggVote = votelib.create('gg_map_vote', voteEnd, voteSubmit)
    
    # Function to use for countdown
    ggVote.repeat_cmd = voteCountDown
    
    # Set question and add some options
    ggVote.setquestion('Please vote for the next map:')
    
    # Add maps as options
    for map_name in getMapList():
        ggVote.addoption(map_name)
    
    # Only send to dead players ?
    if int(gg_map_vote_after_death):
        ggVote.start(int(gg_map_vote_time), '#dead')
        return    
    
    # Start the vote
    ggVote.start(int(gg_map_vote_time))
    
    # Fire event
    EventManager().gg_vote()
        
def voteCountDown():
    ggRepeat = repeat.find('gg_map_vote')
    if not ggRepeat:
        return
    
    # Stop the vote ?    
    if ggRepeat['remaining'] == 0:
        ggVotelib('gg_map_vote').stop(False, True)  

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
    
    # Checking for specified file restrictions
    if int(gg_map_vote_list_source) == 3:
        for name in maps:
            # Cleanup and create list
            name = name.replace('\t','').replace(' '*(name.count(' ')-1), '')
            name = name.split(' ')
            
            # No restriction/filter ?
            if len(name) == 1:
                continue
            
            maps.remove(name)
            
            # Exclude map ? (restricted/filtered)
            if name[1] > len(es.getUseridList()):
                continue
            
            maps.append(name[0])

    # Remove any maps from the list that were voted for previously
    if int(gg_map_vote_dont_show_last_maps):
        for map in list_lastMaps:
            if map in maps:
                maps.remove(map)  
          
    # Make sure that the maps list is not empty
    if not maps:
        error = 'The map list generated by "gg_map_vote" is empty.'
        
        # Could it be do to the restrictions ?
        if int(gg_map_vote_list_source) == 3:
            error += (' **You should add more maps or reduce your ' +
                     'min player restrictions (%s).' % dict_mapListSource[3])            

        # Could it be do to too many last maps ?
        if int(gg_map_vote_dont_show_last_maps):
            error += (' **You should reduce ' + 
                      'gg_map_vote_dont_show_last_maps ' +
                      '(%s) ' % gg_map_vote_dont_show_last_maps +
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