# ../addons/eventscripts/gungame/scripts/included/gg_auto_balance/gg_auto_balance.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''


'''
TO DO:
    1) FIGURE OUT BEST WAY TO APPLY IMMUNITY
    2) ADDRESS MOVING PLAYERS WHILE ALIVE
        a) MAYBE A BETTER WAY TO MOVE ALL PLAYERS? (SPE)
    3) ADD TIMED AUTOBALANCE FOR DEATHMATCH
    4) ADD MESSAGES USING SAYTEXT2 TO LIST ALL PLAYERS MOVED LAST ROUND OR
        DURING THE DEATHMATCH TIME LIMIT
    5) CLEAN UP CODE
    6) TEST
          

'''

# ============================================================================
# >> IMPORTS
# ============================================================================
# Eventscripts Imports
import es
from usermsg import fade
from playerlib import getPlayer
from playerlib import getUseridList

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.players.shortcuts import Player
from gungame51.core.messaging.shortcuts import saytext2
from gungame51.core.players.shortcuts import setAttribute

# ============================================================================
# >> GLOBALS
# ============================================================================
immune = {} # Dict to hold userids for moved players and the amount of moves
notify = [] # List of players that need to be notified
immunity_list = [] # List of userids immune to being swapped

# Settings
gg_auto_balance_threshold = es.ServerVar('gg_auto_balance_threshold')
gg_auto_balance_useimmune = es.ServerVar('gg_auto_balance_useimmune')
gg_auto_balance_force = es.ServerVar('gg_auto_balance_force')
gg_auto_balance_notify = es.ServerVar('gg_auto_balance_notify')
gg_auto_balance_immunity = es.ServerVar('gg_auto_balance_immunity')

# Misc
gg_deathmatch = es.ServerVar('gg_deathmatch')

# ============================================================================
# >> ADDON REGISTRATION/INFORMATION
# ============================================================================
info = AddonInfo()
info.name = 'gg_auto_balance'
info.title = 'GG Auto Balance' 
info.author = 'GG Dev Team'
info.version = '0.1'

# ============================================================================
# >> CLASSES
# ============================================================================ 
class getTeam(object):
    # Initializing
    def __init__(self):
        self.levels = [] # levels
        self.players = [] # userids
        self.team = '' # 'ct' or 't'
        self.teamid = 0 # 2 or 3
        self.generator = None # holder for generator object
        self.set = () # holder for iterator from generator
    
    # Gets the gungame levels for the team    
    def getLevels(self):
        for player in getUseridList('#%s' % self.team):
            self.players.append(player)
            self.levels.append(Player(player).level)       
        
    # Returns the amount of players in the average
    def count(self):
        return len(self.levels)
        
    # Returns the sum of all levels for the team
    def sum(self):
        return sum(self.levels)
    
    # Returns a userid for the gungame level
    def getPlayer(self, level):
        # Initial variable
        player = False
        
        # Making sure someone has that level
        if level not in self.levels:
            return False
        
        # Organizing lists
        _temp = dict(zip(self.players, self.levels))
        
        # Searching for userid
        for player in [x for x in self.players if _temp[x] == level]:
            
            # Looking for player in immune list
            if player not in immune:
                break
            
            # Making sure player is not immune yet
            if immune[player] < int(gg_auto_balance_useimmune):
                break
                        
        # Checking to see if every player at that level was immune.
        if not player:
            return False
        
        # Returning userid for level
        return player
        
    # Iterator filter
    def combo(self):
        # Grabbing next level set that has no immunity
        while True:
    
            # Generating next combination
            combo = self.generator.next()
    
            # Defaulting immune check to no
            immuneCheck = False
    
            # Checking through all levels in the combination
            for level in combo:
    
                # Checking for immunity
                if self.getPlayer(level) == False:
                    immuneCheck = True
                    break
    
            # No immunity found
            if not immuneCheck:
                break
        
        # Sending next combo        
        return combo
    
    # Generator creation function
    def makeGenerator(self, r):
        self.generator = combinations(self.levels, r)
    
    # Change the attributes of players to change teams
    def startSwap(self, set=None):
        # Use defined set ?
        if not set:
            set = self.set
        
        # Find out which new teamid to use
        if self.teamid == 2:
            newTeamid = 3
        if self.teamid == 3:
            newTeamid = 2
        
        # Moving through solution set
        for level in set:
            userid = self.getPlayer(level)
            player = Player(userid)
            pPlayer = getPlayer(userid)
            
            # If player is dead, go ahead and move them
            if pPlayer.isdead:

                # Change team
                es.changeteam(userid, newTeamid)

                # Notify ?
                if int(gg_auto_balance_notify):
                    notify.append(userid)

                es.msg('Player (%s) is dead, moving now.' % userid)
                continue
        
            es.msg('Player (%s) is being moved when they die' % userid)
            # Set attributes for alive players
            player.newTeam = newTeamid
            player.changeTeam = True
            
# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    # Adding attributes
    setAttribute('#all', 'changeTeam', False)
    setAttribute('#all', 'newTeam', None)
    
    # Make immune list
    makeImmuneList()
    
    # Sending debug message
    es.dbgmsg(0, 'Loaded: %s' % info.name)

def unload():
    es.dbgmsg(0, 'Unloaded: %s' % info.name)

# ============================================================================
# >> GAME EVENTS
# ============================================================================
def gg_start():
    userid = event_var['userid']
    
    # Setting attributes
    setAttribute(userid, 'changeTeam', False)
    setAttribute(userid, 'newTeam', None)

def es_map_start(event_var):
    # Flushing immunity list every map
    immune.clear()
    
    # Flushing notify list every map
    del notify[:]
    
    # Make immune list
    makeImmuneList()

def player_death(event_var):
    userid = int(event_var['userid'])
    
    ggPlayer = Player(userid)
    
    # Checking to see if player needs to change teams
    if ggPlayer.changeTeam:
        
        # Changing teams
        es.msg('Moving dead player (%s)' % userid)
        es.changeteam(userid, ggPlayer.newTeamid)
        
        # Sending notification
        notify.append(userid)
        
        # Changing attribute
        ggPlayer.changeTeam = False
    
def player_disconnect(event_var):
    userid = int(event_var['userid'])
    return
            
def round_end(event_var):
    if int(gg_deathmatch):
        return

    balance = True

    # Move the remaining players
    for userid in getUseridList('#all'):

        ggPlayer = Player(userid)
        pPlayer = getPlayer(userid)

        # Player needs to move ?
        if ggPlayer.changeTeam:

            # Player allready moved ?
            if pPlayer.teamid == ggPlayer.newTeam:
                ggPlayer.changeTeam = False
                continue

            # Do not run balance (team changes have not finished)
            balance = False
            
            # Dead ?
            if pPlayer.isdead:
                es.changeteam(userid, ggPlayer.newTeamid)
                ggPlayer.changeTeam = False
                continue

            else:
                es.msg('change on fly (%s)' % userid)
                ggPlayer.teamid = ggPlayer.newTeamid

    if balance:
        autoBalance()
            
def player_activate(event_var):
    userid = int(event_var['userid'])
    
    # Checking to see if the steamid is immune
    if event_var['es_steamid'] in immunity_list:
        immune[userid] = int(gg_auto_balance_useimmune)
    
    # Setting player attributes
    setAttribute(userid, 'changeTeam', False)
    setAttribute(userid, 'newTeam', None)

def player_spawn(event_var):
    userid = int(event_var['userid'])
    
    # Looking for userid in notify list
    if userid in notify:
        
        # Sending notification
        sendNotify(userid)
        notify.remove(userid)
        
# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
def sendNotify(userid):
    ''' Notifty a player he has changed teams.'''
    # Making sure notify is enabled
    if not int(gg_auto_balance_notify):
        return
        
    pPlayer = getPlayer(userid) 
            
    # Notify CT
    if player.teamid == 3:
        fade(userid, 1, 1000, 100, 0, 0, 255, 100)
        es.centertell(userid, 'You have been moved to the ' + 
                                                    'Counter-Terrorist.')
    
    # Notify T
    if player.teamid == 2:
        fade(userid, 1, 1000, 100, 255, 0, 0, 100)
        es.centertell(userid, 'You have been moved to the Terrorist.')

def autoBalance():
    ''' This function starts the automatic team balancing sequence. '''
    es.msg('Starting balance...')
    '''Setting the high and low objects'''
    
    # Grabbing CT avg
    count, sum = 0, 0
    list = getUseridList('#ct')
    for player in list:
        sum += Player(player).level
    count = len(list)
    CTavg =  sum/count
    
    # Grabbing T avg
    count, sum = 0, 0
    list = getUseridList('#t')
    for player in list:
        sum += Player(player).level
    count = len(list)
    Tavg =  sum/count
    es.msg('Difference: %s' % abs(CTavg - Tavg))
    # Checking to see if the average level difference exceeds the config range
    if abs(CTavg - Tavg) < int(gg_auto_balance_threshold):
        es.msg('Balance not needed...')
        return False
    
    # Creating high/low
    high = getTeam()
    low = getTeam()
    
    # Assigning teams to high/low
    if CTavg > Tavg:
        high.team = 'ct'
        high.teamid = 3
        low.team = 't'
        low.teamid = 2
    else:
        low.team = 'ct'
        low.teamid = 3
        high.team = 't'
        high.teamid = 2
    
    # Populating level information
    high.getLevels()
    low.getLevels()
       
    ''' Calculating a value '''

    # Finding our team population difference
    offset = float(float(high.count() - low.count())/2)
    
    # Calculating the server average level
    average = float(low.sum() + high.sum()) 
    average /= (low.count() + high.count())
    
    # Calculating the amount of levels to be moved
    value = average * float(low.count() + offset) - low.sum()
    
    # Rounding and removing floats
    value = int(round(value))
    offset = int(round(offset))
    es.msg('value: %s    offset: %s' % (value, offset))
    # Starting a closest solution (starting high)
    close_solution = 100
	
    ''' Finding a solution '''
    
    # Starting loop to find balancing solution
    for n in range((high.count() - offset)):
        
        # Setting iterator objects
        high.makeGenerator(max(0, (n + offset)))
        low.makeGenerator(n)
        
        # Getting first high team combo
        high.set = high.combo()

        # Looping through the iterators
        while True:
            try:
                # Generating next combination
                low.set = low.combo()
                
                # Checking how close we are to 0
                x = abs(sum(high.set) - sum(low.set) - value)
                
                # Checking for solution
                if x == 0:
                    
                    # Solution found
                    high.startSwap()
                    low.startSwap()
                    es.msg('Perfect solution found!')
                    return True
                
                # Checking for best solution thus far
                if x < close_solution:
                    bestChoice = [high.set, low.set]
                    close_solution = x
            
            # Iterator no longer generating new low team combos
            except StopIteration:
                try:
                    # Generating next combination
                    high.set = high.combo()
                    
                    # Generating another low team list
                    low.makeGenerator(n)
                    
                    # Check again
                    continue
                
                # Iterator no longer generating new high team comobos
                except StopIteration:
                    break
    
    # Use the best solution                
    low.startSwap(bestChoice[1])
    high.startSwap(bestChoice[0])
    es.msg('Best choice is being used...')
    return True

def addImmunity(userid):
    '''Adds a player to the team change immunity list'''
    # Making sure gg_auto_balance_useimmune isn't disabled
    if not int(gg_auto_balance_useimmune):
        return
    
    # Adding userid
    if userid in immune:
        immune[userid] += 1
        return
        
    immune[userid] = 1

def removeImmunity(userid):
    '''Removes a player from the team change immunity list'''
    if userid in immune:
        del immune[userid]

def makeImmuneList():
    # Making steamid immunity list
    del immunity_list[:]
    immunity_list.extend([x.strip() for x in \
        str(gg_auto_balance_immunity).split(',') if not (x.strip() == '' or \
        x.strip().isdigit())])

def combinations(pool, r):
    n = len(pool)

    # Out of range ?
    if r > n:
        return

    indices = range(r)

    # Send first
    yield [pool[i] for i in indices]

    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return

        indices[i] += 1

        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1

        # Send next
        yield [pool[i] for i in indices]

             