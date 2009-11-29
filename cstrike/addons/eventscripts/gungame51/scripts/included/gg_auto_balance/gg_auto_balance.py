# ../addons/eventscripts/gungame/scripts/included/gg_auto_balance/gg_auto_balance.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
# Python Imports
from time import time

# Eventscripts Imports
import es
import gamethread
import repeat
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
gg_auto_balance_timer = es.ServerVar('gg_auto_balance_timer')
gg_auto_balance_notify_all = es.ServerVar('gg_auto_balance_notify_all')
gg_auto_balance_nade = es.ServerVar('gg_auto_balance_nade')
gg_auto_balance_knife = es.ServerVar('gg_auto_balance_knife')

# Misc
gg_deathmatch = es.ServerVar('gg_deathmatch')
mp_autoteambalance = es.ServerVar('mp_autoteambalance')
mp_limitteams = es.ServerVar('mp_limitteams')

# ============================================================================
# >> ADDON REGISTRATION/INFORMATION
# ============================================================================
info = AddonInfo()
info.name = 'gg_auto_balance'
info.title = 'GG Auto Balance'
info.author = 'GG Dev Team'
info.version = '0.1'
info.translations = ['gg_auto_balance']

# ============================================================================
# >> CLASSES
# ============================================================================
class GetTeam(object):
    # Initializing
    def __init__(self):
        self.levels = [] # levels
        self.players = [] # userids
        self.team = '' # 'ct' or 't'
        self.teamid = 0 # 2 or 3
        self.generator = None # holder for generator object
        self.set = [] # holder for iterator from generator

    # Gets the gungame levels for the team
    def get_levels(self):
        ''' Populates the class with player levels and userids '''
        for player in getUseridList('#%s' % self.team):
            self.players.append(player)
            ggPlayer = Player(player)

            # Use another level for nade ?
            if ggPlayer.weapon == 'hegrenade' and int(gg_auto_balance_nade):
                self.levels.append(int(gg_auto_balance_nade))

            # Use another level for knife ?
            elif ggPlayer.weapon == 'knife' and int(gg_auto_balance_knife):
                self.levels.append(int(gg_auto_balance_knife))

            # Normal level
            else:
                self.levels.append(ggPlayer.level)

    # Returns the amount of players in the average
    @property
    def count(self):
        return len(self.levels)

    # Returns the sum of all levels for the team
    @property
    def sum(self):
        return sum(self.levels)

    # Returns a userid for the gungame level
    def get_player(self, level):
        '''
        Returns the first available player who is not immune and of the right
        level requested by the balancer
        '''
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
        else:
            return False

        # Returning userid for level
        return player

    # Iterator filter
    def combo(self):
        ''' Grabs the next solution set from the generator '''
        while True:
            # Generating next combination
            next = self.generator.next()

            # Checking through all levels in the combination
            for level in next:

                # Checking for immunity
                if self.get_player(level) == False:
                    break

            # No immunity found
            else:
                return next

    # Generator creation function
    def make_generator(self, r):
        self.generator = combinations(self.levels, r)

    # Change the attributes of players to change teams
    def start_swap(self, level_set=None):
        '''
        Initiates the moving of players after a balance has completed
        successfully.
        '''
        # Use defined set ?
        if level_set == None:
            level_set = self.set

        elif level_set == []:
            return

        # Find out which new teamid to use
        if self.teamid == 2:
            newTeamid = 3
        elif self.teamid == 3:
            newTeamid = 2

        moving = []

        # Moving through solution set
        for level in level_set:
            userid = self.get_player(level)
            ggPlayer = Player(userid)

            # Set attributes for alive players
            ggPlayer.newTeam = newTeamid
            ggPlayer.changeTeam = True

            # Force swap ?
            if float(gg_auto_balance_force):
                gamethread.delayedname(float(gg_auto_balance_force),
                          'gg_autobal_%s' % userid, force_swap, ggPlayer)

            # Notify to chat enabled ?
            if int(gg_auto_balance_notify_all):
                moving.append('\3%s\1' % getPlayer(userid).name)

            # Add player to immunity list
            add_immunity(userid)

        # Notify Everyone ?
        if moving == []:
            return

        # Terrorist ?
        if self.teamid == 2:
            teamname = '\3Terrorist\1'

        # Counter-Terrorist ?
        else:
            teamname = '\3Counter-Terrorist\1'

        # 1 Player moved ?
        if len(moving) == 1:
            saytext2('#human', ggPlayer.index, 'NotifyTeamChange',
                {'player': moving[0], 'team': teamname}, True)

        # 2 or more players moved
        else:
            moving[(len(moving) -1)] = 'and %s' % moving[(len(moving) -1)]
            saytext2('#human', ggPlayer.index, 'NotifyTeamChangeP',
                {'player': ', '.join(moving), 'team': teamname}, True)

# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    global mp_limitteams_backup
    global mp_autoteambalance_backup
    mp_autoteambalance_backup = int(mp_autoteambalance)
    mp_limitteams_backup = int(mp_limitteams)

    # Checking for DeathMatch
    if es.exists('variable', 'gg_deathmatch'):
        check_for_dm(True)
    else:
        gamethread.delayed(1, check_for_dm, (False))

    # Adding attributes
    setAttribute('#all', 'changeTeam', False)
    setAttribute('#all', 'newTeam', None)

    # Make immune list
    make_immune_list()

    if int(mp_autoteambalance):
        mp_autoteambalance.set(0)

    if int(mp_limitteams) != 1:
        mp_limitteams.set(1)

    es.dbgmsg(0, 'Loaded: %s' % info.name)

def unload():
    # Did we have a timer ?
    find_timer = repeat.find('gg_auto_balance')
    if find_timer:
        find_timer.stop()
        find_timer.delete()

    # Change back mp_autoteambalance ?
    if int(mp_autoteambalance) != mp_autoteambalance_backup:
        es.server.queuecmd('mp_autoteambalance %s' % mp_autoteambalance_backup)

    # Change back mp_limitteams ?
    if int(mp_limitteams) != mp_limitteams_backup:
        es.server.queuecmd('mp_limitteams %s' % mp_limitteams_backup)

    es.dbgmsg(0, 'Unloaded: %s' % info.name)

# ============================================================================
# >> GAME EVENTS
# ============================================================================
def gg_start(event_var):
    # Setting attributes
    setAttribute('#all', 'changeTeam', False)
    setAttribute('#all', 'newTeam', None)

    # Check for DM timer
    check_for_dm(True)

def es_map_start(event_var):
    # Flushing immunity list every map
    immune.clear()

    # Flushing notify list every map
    del notify[:]

    # Make immune list
    make_immune_list()

def player_death(event_var):
    if not int(gg_deathmatch):
        return

    userid = int(event_var['userid'])

    ggPlayer = Player(userid)

    # Checking to see if player needs to change teams
    if ggPlayer.changeTeam:

        # Changing teams
        ggPlayer.team = ggPlayer.newTeam

        # Sending notification
        notify.append(userid)

        # Changing attribute
        ggPlayer.changeTeam = False

def player_disconnect(event_var):
    userid = int(event_var['userid'])

    # Was the player supposed to change teams ?
    ggPlayer = Player(userid)

    if ggPlayer.changeTeam:
        ggPlayer.changeTeam = False

    gamethread.cancelDelayed('gg_autobal_%s' % userid)
            
def round_end(event_var):
    if int(gg_deathmatch):
        return

    newBalance = True

    '''
    This try/exception needs to be done because sometimes bots join and end
    the round before they can be assigned attritbutes to the Player class
    '''
    try:
        # Move the remaining players
        for userid in getUseridList('#all'):

            ggPlayer = Player(userid)

            # Player needs to move ?
            if ggPlayer.changeTeam:
                # Cancel any delays
                gamethread.cancelDelayed('gg_autobal_%s' % userid)

                # Player allready moved or in spec?
                if ggPlayer.team in [1, ggPlayer.newTeam]:
                    ggPlayer.changeTeam = False

                else:
                    # Move player & Notify
                    ggPlayer.team = ggPlayer.newTeam
                    notify.append(userid)

                    # Don't balance this round
                    if newBalance:
                        newBalance = False

            # Set player health/armor if alive
            pPlayer = getPlayer(userid)
            if not pPlayer.isdead:
                pPlayer.health += 1500
                pPlayer.armor += 1000

    # Bots caused an error while joining an empty server
    except AttributeError:
        return

    if newBalance:
        auto_balance_exec()

def player_activate(event_var):
    userid = int(event_var['userid'])

    # Checking to see if the steamid is immune
    if event_var['es_steamid'] in immunity_list:
        immune[userid] = int(gg_auto_balance_useimmune)

    # Setting player attributes
    setAttribute(userid, 'changeTeam', False)
    setAttribute(userid, 'newTeam', None)

def player_spawn(event_var):
    # Looking for userid in notify list
    userid = int(event_var['userid'])
    if userid in notify:
        send_notify(userid)

def gg_win(event_var):
    # Stop the timer if it is running
    find_timer = repeat.find('gg_auto_balance')
    if find_timer:
        find_timer.stop()

def server_cvar(event_var):
    # Values
    cvar_name = event_var['cvarname']
    cvar_value = event_var['cvarvalue']

    # gg_deathmatch changed ?
    if cvar_name == 'gg_deathmatch':
        if int(cvar_value):
            check_for_dm(True)
        else:
            autoBalanceTimer = repeat.find('gg_auto_balance')
            if autoBalanceTimer:
                autoBalanceTimer.delete()

    # mp_autoteambalance changed ?
    elif cvar_name == 'mp_autoteambalance':
        if int(cvar_value) != 0:
            mp_autoteambalance_backup = int(cvar_value)
            es.server.queuecmd('mp_autoteambalance 0')
            es.dbgmsg(0, '    %s ::: Error: ' % info.title +
                         '"mp_autoteambalance" was changed back to "0"')

    # mp_limitteams changed ?
    elif cvar_name == 'mp_limitteams':
        if int(cvar_value) != 1:
            mp_limitteams_backup = int(cvar_value)
            es.server.queuecmd('mp_limitteams 1')
            es.dbgmsg(0, '    %s ::: Error: "mp_limitteams" was' % info.title +
                         ' changed back to "1"')

    # gg_auto_balance_timer changed ?
    elif cvar_name == 'gg_auto_balance_timer':
        autoBalanceTimer = repeat.find('gg_auto_balance')
        if autoBalanceTimer:
            autoBalanceTimer.delete()
        check_for_dm(False)

# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
def check_for_dm(ok):
    '''
    Check to see if deathmatch is loaded, and if the balancer needs to start
    a repeat timer.
    '''
    # Check if gg_deathmatch var exists
    if not ok:
        if not es.exists('variable', 'gg_deathmatch'):
            raise ValueError('Could not read from gg_deathmatch setting!')

    # We using DeathMatch ?
    if not int(gg_deathmatch):
        return

    # The DeathMatch Settings Ok?
    if not (float(gg_auto_balance_force) and float(gg_auto_balance_timer)):
        raise ValueError('Please check the settings for ' +
                         '"gg_auto_balance_force" and "gg_auto_balance_timer"')

    autoBalanceTimer = repeat.find('gg_auto_balance')

    # Allready have a timer ?
    if autoBalanceTimer:
        autoBalanceTimer.stop()
        autoBalanceTimer.start((float(gg_auto_balance_timer) * 60), 0)
        return

    # Start a new timer
    autoBalanceTimer = repeat.create('gg_auto_balance', auto_balance_exec)
    autoBalanceTimer.start((float(gg_auto_balance_timer) * 60), 0)

def auto_balance_exec():
    es.dbgmsg(0, '    %s ::: Running Balancer... [ver: %s]' % (info.title,
                                                                info.version))
    _time = time()
    if auto_balance():
        es.dbgmsg(0, '    %s ::: Balance Preformed!' % info.title)
    else:
        es.dbgmsg(0, '    %s ::: No Balance Needed!' % info.title)
    es.dbgmsg(0, '    %s ::: Executed in %s seconds' % (info.title,
                                                             (time() - _time)))

def auto_balance():
    ''' This function starts the automatic team balancing sequence. '''

    ''' Setting the high and low objects '''
    # Lists
    ct_list = getUseridList('#ct')
    t_list = getUseridList('#t')

    # Don't balance less than 4 players
    if (len(t_list) + len(ct_list)) < 4:
        return False

    # Checking for death match (Make sure its not still balancing)
    if int(gg_deathmatch):
        if any([Player(x).changeTeam for x in getUseridList('#t, #ct')]):
            es.dbgmsg(0, '%s has not finished balancing ' % info.title +
                        'from last loop, you may want to increase the ' +
                         'value of "gg_auto_balance_timer"')
            return False

    # Grabbing averages
    CTavg = (sum([Player(uid).level for uid in ct_list]) / float(len(ct_list)))
    Tavg = (sum([Player(uid).level for uid in t_list]) / float(len(t_list)))
    es.dbgmsg(0, '    %s ::: T AVG: %0.02f  ' % (info.title, Tavg) +
             'CT AVG: %0.02f  Difference: %0.02f' % (CTavg, abs(CTavg - Tavg)))

    es.dbgmsg(0, '    %s ::: Threshold: %s' % (info.title,
                                            float(gg_auto_balance_threshold)))
    
    # Checking to see if the average level difference exceeds the threshold
    if abs(CTavg - Tavg) < float(gg_auto_balance_threshold):
        return False

    # Creating high/low
    high = GetTeam()
    low = GetTeam()

    # Assigning teams to high/low
    if CTavg > Tavg:
        high.team = 'ct'
        high.teamid = 3
        low.team = 't'
        low.teamid = 2
    elif Tavg > CTavg:
        low.team = 'ct'
        low.teamid = 3
        high.team = 't'
        high.teamid = 2

    # Teams are perfectly balanced
    else:
        return False

    # Populating level information
    high.get_levels()
    low.get_levels()

    # Making sure there is more than 1 player with a level above 1
    level_check = 0
    for level in high.levels + low.levels:
        if level > 1:
            level_check += 1
        if level_check > 1:
            break
    else:
        return False

    ''' Calculating a value '''

    # Finding our team population difference
    offset = ((high.count - low.count) / 2.0)

    # Calculating the server average level
    average = ((low.sum + high.sum) / float(low.count + high.count))

    # Calculating the amount of levels to be moved
    value = (average * (low.count + offset) - low.sum)

    # Rounding and removing floats
    value = int(round(value))
    offset = int(round(offset))
    close_solution = None
    bestChoice = []

    ''' Finding solution '''

    # Starting loop to find balancing solution
    for n in range((high.count - offset)):

        # Setting iterator objects
        high.make_generator(max(0, (n + offset)))
        low.make_generator(n)

        # Getting first high team combo
        high.set = high.combo()

        # Looping through the iterators
        while True:
            try:
                # Generating next combination
                low.set = low.combo()

                # Blank iterators ?
                if len(low.set + high.set) == 0:
                    continue

                # Checking how close we are to 0
                solution = abs(sum(high.set) - sum(low.set) - value)

                # Checking for solution
                if solution == 0:

                    # Solution found
                    high.start_swap()
                    low.start_swap()
                    return True

                # Checking for best solution thus far
                if not close_solution:
                    bestChoice.extend([high.set, low.set])
                    close_solution = solution

                elif solution < close_solution:
                    del bestChoice[:]
                    bestChoice.extend([high.set, low.set])
                    close_solution = solution

            # Iterator no longer generating new low team combos
            except StopIteration:
                try:
                    # Generating next combination
                    high.set = high.combo()

                    # Generating another low team list
                    low.make_generator(n)

                    # Check again
                    continue

                # Iterator is done
                except StopIteration:
                    break

    low.start_swap(bestChoice[1])
    high.start_swap(bestChoice[0])
    return True

def force_swap(ggPlayer):
    ''' Forces a player to change teams in the middle of a round. '''
    # Is player okay to move ?
    if not es.exists('userid', ggPlayer.userid) or ggPlayer.team == 1:

        # Player is supposed to be moved ?
        if ggPlayer.changeTeam:
            ggPlayer.changeTeam = False
        return

    # Normal round ? (Don't move the last player yet.)
    if not int(gg_deathmatch):

        # Last player alive ?
        if (ggPlayer.team == 2 and len(getUseridList('#t, #alive')) == 1) or \
         (ggPlayer.team == 3 and len(getUseridList('#ct, #alive')) == 1):
            return

    ggPlayer.changeTeam = False
    ggPlayer.team = ggPlayer.newTeam
    send_notify(ggPlayer.userid)

def send_notify(userid):
    ''' Notifty a player he has changed teams. '''
    if userid in notify:
        notify.remove(userid)

    # Making sure notify is enabled
    if not int(gg_auto_balance_notify):
        return

    # Is a bot ?
    if es.isbot(userid):
        return

    ggPlayer = Player(userid)

    # Spec?
    if ggPlayer.team == 1:
        return

    # Notify T
    if ggPlayer.team == 3:
        fade(userid, 1, 1000, 100, 255, 0, 0, 100)
        teamname = 'Terrorist'

    # Notify CT
    else:
        fade(userid, 1, 1000, 100, 0, 0, 255, 100)
        teamname = 'Counter-Terrorist'

    ggPlayer.centermsg('NotifyPlayerCenter', {'team': teamname})

    # Play sound
    if int(gg_auto_balance_notify) > 1:
        ggPlayer.playsound('notify')

def add_immunity(userid):
    ''' Adds a player to the team change immunity list '''
    # Making sure gg_auto_balance_useimmune isn't disabled
    if not int(gg_auto_balance_useimmune):
        return

    # Adding userid
    if userid in immune:
        immune[userid] += 1
        return

    immune[userid] = 1

def make_immune_list():
    ''' Makes steamid immunity list '''
    del immunity_list[:]

    # No list ?
    if str(gg_auto_balance_immunity) in ('0', ''):
        return

    # Make list
    immunity_list.extend([x.strip() for x in \
        str(gg_auto_balance_immunity).split(',') if x.strip()[:5] == 'STEAM'])

def combinations(level_list, r):
    ''' Generator for solution iterators '''
    level_list_len = len(level_list)
    indexes = range(r)

    # Send first
    yield [level_list[i] for i in indexes]

    # Generate ...
    while True:
        # Get next possible index
        for i in reversed(range(r)):

            # Range is ok ?
            if indexes[i] != (i + level_list_len - r):
                break

        # Nothing found ?
        else:
            return

        indexes[i] += 1

        # Create set of indexes
        for j in range((i + 1), r):
            indexes[j] = indexes[j-1] + 1

        # Send next possible solution
        yield [level_list[i] for i in indexes]

