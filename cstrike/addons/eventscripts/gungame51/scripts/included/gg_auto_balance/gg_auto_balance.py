# ../addons/eventscripts/gungame/scripts/included/gg_auto_balance/gg_auto_balance.py

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
mp_limitteams_backup = int(es.ServerVar('mp_limitteams'))
mp_autoteambalance_backup = int(es.ServerVar('mp_limitteams'))


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
        self.set = [] # holder for iterator from generator

    # Gets the gungame levels for the team
    def getLevels(self):
        for player in getUseridList('#%s' % self.team):
            self.players.append(player)
            ggPlayer = Player(player)
            if ggPlayer.weapon == 'hegrenade' and int(gg_auto_balance_nade):
                self.levels.append(int(gg_auto_balance_nade))
            elif ggPlayer.weapon == 'knife' and int(gg_auto_balance_knife):
                self.levels.append(int(gg_auto_balance_knife))
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
    def getPlayer(self, level):

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
        # Grabbing next level set that has no immunity
        while True:

            # Generating next combination
            combo = self.generator.next()

            # Checking through all levels in the combination
            for level in combo:

                # Checking for immunity
                if self.getPlayer(level) == False:
                    break

            # No immunity found
            else:
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
        elif self.teamid == 3:
            newTeamid = 2

        moving = []

        # Moving through solution set
        for level in set:
            userid = self.getPlayer(level)
            ggPlayer = Player(userid)

            # Set attributes for alive players
            ggPlayer.newTeam = newTeamid
            ggPlayer.changeTeam = True

            # Force swap ?
            if float(gg_auto_balance_force):
                gamethread.delayed(float(gg_auto_balance_force), forceSwap,
                (ggPlayer))

            # Notify to chat enabled ?
            if int(gg_auto_balance_notify_all):
                moving.append('\3%s\1' % getPlayer(userid).name)

        # Notify Everyone ?
        if not moving:
            return

        index = ggPlayer.index
        if self.teamid == 2:
            teamname = '\3Terrorist\1'
        else:
            teamname = '\3Counter-Terrorist\1'
        if len(moving) == 1:
            saytext2('#human', index, 'RespawningPlayer',
                {'player': ', '.join(moving), 'team': teamname}, True)
        else:
            saytext2('#human', index, 'RespawningPlayerP',
                {'player': ', '.join(moving), 'team': teamname}, True)

# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    # Checking for DeathMatch
    if es.exists('variable', 'gg_deathmatch'):
        checkForDM(True)
    else:
        gamethread.delayed(1, checkForDM, (False))

    # Adding attributes
    setAttribute('#all', 'changeTeam', False)
    setAttribute('#all', 'newTeam', None)

    # Make immune list
    makeImmuneList()

    # Sending debug message
    es.dbgmsg(0, 'Loaded: %s' % info.name)

    if int(mp_autoteambalance):
        es.server.queuecmd('mp_autoteambalance 0')

    if int(mp_limitteams) != 1:
        es.server.queuecmd('mp_limitteams 1')

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
    checkForDM(True)

def es_map_start(event_var):
    # Flushing immunity list every map
    immune.clear()

    # Flushing notify list every map
    del notify[:]

    # Make immune list
    makeImmuneList()

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

def round_end(event_var):
    if int(gg_deathmatch):
        return

    newBalance = True

    # Move the remaining players
    for userid in getUseridList('#all'):

        ggPlayer = Player(userid)

        # Player needs to move ?
        if ggPlayer.changeTeam:

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

    if newBalance:
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
    # Looking for userid in notify list
    userid = int(event_var['userid'])
    if userid in notify:
        sendNotify(userid)

def gg_win(event_var):
    # Stop the timer if it is running
    find_timer = repeat.find('gg_auto_balance')
    if find_timer:
        find_timer.stop()

def server_cvar(cvar_name):
    # gg_deathmatch changed ?
    if cvar_name == 'gg_deathmatch':
        if int(gg_deathmatch):
            checkForDM(True)
        else:
            find_timer = repeat.find('gg_auto_balance')
            if find_timer:
                find_timer.stop()
                find_timer.delete()

    # mp_autoteambalance changed ?
    elif cvar_name == 'mp_autoteambalance':
        if int(mp_autoteambalance) != 0:
            mp_autoteambalance_backup = int(mp_autoteambalance)
            es.server.queuecmd('mp_autoteambalance 0')
            es.dbgmsg(0, '%s Error: "mp_autoteambalance" was ' % info.title +
                         'back to "0"!')

    # mp_limitteams changed ?
    elif cvar_name == 'mp_limitteams':
        if int(mp_limitteams) != 1:
            mp_limitteams_backup = int(mp_limitteams)
            es.server.queuecmd('mp_limitteams 1')
            es.dbgmsg(0, '%s Error: "mp_limitteams" was ' % info.title +
                         'back to "1"!')

# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
def checkForDM(ok):
    # Check if gg_deathmatch var exists
    if not ok:
        if es.exists('variable', 'gg_deathmatch'):
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
        autoBalanceTimer.start()
        return

    # Start a new timer
    autoBalanceTimer = repeat.create('gg_auto_balance', autoBalance)
    autoBalanceTimer.start((float(gg_auto_balance_timer) * 60), 0)

def forceSwap(ggPlayer):
    # Still on server ?
    if not es.exists('userid', ggPlayer.userid):
        return

    # Allready moved ?
    if not ggPlayer.changeTeam:
        return

    # Moved to spec ?
    if ggPlayer.team < 2:
        return

    # Normal round ? (Don't move the last player yet.)
    if not int(gg_deathmatch):

        # Last player alive ?
        if (ggPlayer.team == 2 and len(getUseridList('#t, #alive')) == 1) or \
         (ggPlayer.team == 3 and len(getUseridList('#ct, #alive')) == 1):
            return

    ggPlayer.changeTeam = False
    ggPlayer.team = ggPlayer.newTeam
    sendNotify(ggPlayer.userid)

def sendNotify(userid):
    ''' Notifty a player he has changed teams.'''
    if userid in notify:
        notify.remove(userid)

    # Making sure notify is enabled
    if not int(gg_auto_balance_notify):
        return

    # Is a bot ?
    if es.isbot(userid):
        return

    ggPlayer = Player(userid)

    # Notify CT
    if ggPlayer.team == 3:
        fade(userid, 1, 1000, 100, 0, 0, 255, 100)
        teamname = 'Counter-Terrorist'

    # Notify T
    elif ggPlayer.team == 2:
        fade(userid, 1, 1000, 100, 255, 0, 0, 100)
        teamname = 'Terrorist'

    else:
        return

    ggPlayer.centermsg('NotifyPlayerCenter', {'team': teamname})

    # Play sound
    if int(gg_auto_balance_notify) > 1:
        ggPlayer.playsound('notify')

def autoBalance():
    ''' This function starts the automatic team balancing sequence. '''

    '''Setting the high and low objects'''
    es.msg('Balancing...')
    # Lists
    ct_list = getUseridList('#ct')
    t_list = getUseridList('#t')

    # Enough players ?
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
    CTavg = sum([Player(player).level for player in ct_list]) /\
        float(len(ct_list))
    Tavg = sum([Player(player).level for player in t_list]) /\
        float(len(t_list))
    es.msg('CT: %s T: %s Balance: %s' % (CTavg, Tavg, abs(CTavg - Tavg)))

    # Checking to see if the average level difference exceeds the config range
    if abs(CTavg - Tavg) < float(gg_auto_balance_threshold):
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
    elif Tavg > CTavg:
        low.team = 'ct'
        low.teamid = 3
        high.team = 't'
        high.teamid = 2
    else:
        return False

    # Populating level information
    high.getLevels()
    low.getLevels()

    ''' Calculating a value '''

    # Finding our team population difference
    offset = float(float(high.count - low.count)/2)

    # Calculating the server average level
    average = float(low.sum + high.sum)
    average /= (low.count + high.count)

    # Calculating the amount of levels to be moved
    value = average * float(low.count + offset) - low.sum

    # Rounding and removing floats
    value = int(round(value))
    offset = int(round(offset))
    close_solution = None

    ''' Finding a solution '''

    # Starting loop to find balancing solution
    for n in range((high.count - offset)):

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
                    return True

                # Checking for best solution thus far
                if not close_solution:
                    bestChoice = [high.set, low.set]
                    close_solution = x

                elif x < close_solution:
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

    # No list ?
    if str(gg_auto_balance_immunity) in ('0', ''):
        return

    # Make list
    immunity_list.extend([x.strip() for x in \
        str(gg_auto_balance_immunity).split(',') if x.strip()[:5] == 'STEAM'])

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

