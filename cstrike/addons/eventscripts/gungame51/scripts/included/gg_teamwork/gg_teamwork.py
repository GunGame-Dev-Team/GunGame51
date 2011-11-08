# ../scripts/included/gg_teamwork/gg_teamwork.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
#   Path
from path import path

# EventScripts Imports
#   ES
from es import getindexfromhandle
from es import getplayerhandle
from es import getplayername
from es import getplayerteam
from es import getuserid
from es import getUseridList
from es import isbot
from es import ServerCommand
from es import ServerVar
#   Gamethread
from gamethread import delayed

# GunGame Imports
#   Addons
from gungame51.core.addons.shortcuts import AddonInfo
#   Eventlib
#       Base
from gungame51.core.events.eventlib import ESEvent
#       Resource
from gungame51.core.events.eventlib.resource import ResourceFile
#       Fields
from gungame51.core.events.eventlib.fields import BooleanField
from gungame51.core.events.eventlib.fields import ShortField
#   Events
from gungame51.core.events import GG_Win
#   Messaging
from gungame51.core.messaging.shortcuts import langstring
#   Players
from gungame51.core.players import Player
#   Weapons
from gungame51.core.weapons.shortcuts import get_level_weapon


# =============================================================================
# >> ADDON REGISTRATION/INFORMATION
# =============================================================================
info = AddonInfo()
info.name = 'gg_teamwork'
info.title = 'GG Teamwork'
info.author = 'GG Dev Team'
info.version = '5.1.%s' % '$Rev$'.split('$Rev: ')[1].split()[0]
info.conflicts = ['gg_deathmatch', 'gg_handicap', 'gg_teamplay']
info.translations = ['gg_teamwork']


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
gg_teamwork_jointeam_level = ServerVar('gg_teamwork_jointeam_level')
gg_teamwork_round_messages = ServerVar('gg_teamwork_round_messages')
gg_teamwork_leader_messages = ServerVar('gg_teamwork_leader_messages')
gg_teamwork_winner_messages = ServerVar('gg_teamwork_winner_messages')


# =============================================================================
# >> EVENT CLASSES
# =============================================================================
class GG_Team_Win(ESEvent):
    '''Fires when a team wins the game'''

    winner = ShortField(
        min_value=2, max_value=3, comment='Team that won the match')

    loser = ShortField(
        min_value=2, max_value=3, comment='Team that lost the match')

# Get the ResourceFile instance to create the .res file
gg_teamwork_resource = ResourceFile(
    path(__file__).parent.joinpath('gg_teamwork.res'))

# Write the .res file
gg_teamwork_resource.write([GG_Team_Win], overwrite=True)


# =============================================================================
# >> TEAM CLASSES
# =============================================================================
class GGTeams(dict):
    '''Class to store the 2 teams'''

    def __new__(cls):
        '''Creates the new object and adds the teams to the dictionary'''

        # Make sure there is only one instance of the class
        if not '_the_instance' in cls.__dict__:

            # Get the new object
            cls._the_instance = dict.__new__(cls)

            # Loop through both teams
            for team in (2, 3):

                # Add the team to the dictionary
                cls._the_instance[team] = TeamManagement(team)

        # Return the dictionary
        return cls._the_instance

    def clear(self):
        '''Resets the team level value'''

        # Loop through both teams
        for team in self:

            # Reset the team's level and leader values
            gg_teams[team].reset_values()


class TeamManagement(object):
    '''Class used to store team values and perform actions on team members'''

    def __init__(self, team):
        '''Fired when the team's instance is initialized'''

        # Store the team
        self.team = team

        # Set the team's level and leader values
        self.reset_values()

    def reset_values(self):
        '''Resets the team's level and leader values'''

        # Set the values back to start
        self.level = 1
        self.leader = None

    def set_all_player_levels(self):
        '''Sets all players on the team to the highest level'''

        # Loop through all players on the team
        for userid in self.team_players:

            # Get the Player instance
            ggPlayer = Player(userid)

            # Does this player need to level up?
            if ggPlayer.level != self.level:

                # Level the player up to the highest level
                Player(userid).level = self.level

                # Set the player's multikill to 0
                ggPlayer.multikill = 0

    def set_player_level(self, userid):
        '''Sets a player that just joined the team's level'''

        # Get the player's Player() instance
        ggPlayer = Player(userid)

        # Does the player get set to level 1?
        if not int(gg_teamwork_jointeam_level):

            # Set the player to level 1
            ggPlayer.level = 1

        # Does the player need set to the teams start level for this round?
        else:

            # Set the player to the team's level
            ggPlayer.level = self.level

        # Either way, reset the player's multikill value
        ggPlayer.multikill = 0

    def check_old_leader(self, userid):
        '''Checks to see if the player was the team's leader'''

        # Was the player the team's leader?
        if userid != self.leader:

            # If not, return
            return

        # Get the team's highest level
        player, level = self.leader_level

        # Store the new player as the team's leader
        self.leader = player

        # Is there a leader?
        if self.leader is None:

            # If not, just return
            return

        # Is the new level the same as the previous?
        if level == self.level:

            # If they are the same, just return
            return

        # Store the new level
        self.level = level

        # Does a message need sent?
        if int(gg_teamwork_leader_messages):

            # Send a message to all players
            self.send_all_players_a_message(
                'TeamWork_LostLeader', {'level': self.level})

    def check_team_leader(self, userid, level):
        '''Checks to see if the player increased the team's level'''

        # Is the new level higher than the team's level?
        if level <= self.level:

            # If not, return
            return

        # Set the team's new level
        self.level = level

        # Set the team's new leader
        self.leader = userid

        # Does a leader message need printed?
        if int(gg_teamwork_leader_messages):

            # Send the message to all players
            self.send_all_players_a_message('TeamWork_NewLeader',
                {'player': getplayername(self.leader), 'level': self.level})

    def send_level_message(self):
        '''Sends a message to all players about the teams new level'''

        # Send the message to all players
        self.send_all_players_a_message('TeamWork_TeamLevel',
            {'level': self.level, 'weapon': get_level_weapon(self.level)})

    def send_winner_messages(self):
        '''Sends Winner Messages to all players'''

        # Store a team player's index
        index = self.index

        # Is there an index?
        if index is None:

            # If not, return
            return

        # Store the team's color
        color = self.color

        # Loop through all players on the server
        for userid in getUseridList():

            # Is the current player a bot?
            if isbot(userid):

                # Do not send messages to bots
                continue

            # Get the player's Player() instance
            ggPlayer = Player(userid)

            # Get the team's name
            teamname = langstring(self.teamname, userid=userid)

            # Send chat message for team winning the match
            ggPlayer.saytext2(
                index, 'TeamWork_Winner', {'teamname': teamname}, True)

            # We want to loop, so we send a message every second for 3 seconds
            for x in xrange(4):

                # Send centermsg about the winner
                delayed(x, ggPlayer.centermsg,
                    ('TeamWork_Winner_Center', {'teamname': teamname}))

            # Send toptext message about the winner
            ggPlayer.toptext(10, color,
                'TeamWork_Winner_Center', {'teamname': teamname})

    def send_all_players_a_message(self, message, tokens):
        '''Sends all players on the server a message'''

        # Store a team members index
        index = self.index

        # Is there an index?
        if index is None:

            # If not, don't send any messages
            return

        # Loop through all players on the server
        for userid in getUseridList():

            # Is the player a bot?
            if isbot(userid):

                # If so, don't send a message
                continue

            # Get the team's name
            teamname = langstring(self.teamname, userid=userid)

            # Update the tokens with the teamname
            tokens.update({'teamname': teamname})

            # Send the message to the player
            Player(userid).saytext2(index, message, tokens, True)

    @property
    def leader_level(self):
        '''Returns a list of all player levels on the team'''

        # Create a list to store player levels
        levels = {}

        # Loop through all players on the team
        for userid in self.team_players:

            # Add the player's level to the list
            levels[userid] = Player(userid).level

        # Are there any values?
        if not levels:

            # If not, return None values
            return None, None

        # Get a player on the highest level for the team
        player = max(levels, key=lambda userid: levels[userid])

        # Return the the player and the highest level
        return player, levels[player]

    @property
    def team_players(self):
        '''Returns all userid's on the team'''

        # Loop through all players on the server
        for userid in getUseridList():

            # Is the player on this team?
            if getplayerteam(userid) == self.team:

                # Yield the player's userid
                yield userid

    @property
    def index(self):
        '''Returns the index of a player on the team'''

        # Loop through all players on the server
        for userid in self.team_players:

            # Return the index of the first team player found
            return getindexfromhandle(getplayerhandle(userid))

        # If no team members, return None
        return None

    @property
    def teamname(self):
        return 'TeamWork_%s' % self.team

    @property
    def color(self):
        '''Returns the team's color'''

        # Is this the Terrorist team?
        if self.team == 2:

            # Return red for Terrorist color
            return '#red'

        # Return blue for Counter-Terrorist color
        return '#blue'

# Get the GGTeams instance
gg_teams = GGTeams()


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    '''Fired when the script is loaded'''

    # Register a callback for the gg_win event
    GG_Win().register_prefire_callback(pre_gg_win)

    # Declare and load the resource file
    gg_teamwork_resource.declare_and_load()


def unload():
    '''Fired when the script is unloaded'''

    # Unregister the gg_win event callback
    GG_Win().unregister_prefire_callback(pre_gg_win)


# =============================================================================
# >> REGISTERED CALLBACKS
# =============================================================================
def pre_gg_win(**event_var):
    '''Fired prior to gg_win event being fired'''

    # Get the team the winner is one
    winning_team = getplayerteam(event_var['winner'])

    # Fire the gg_teamwin event instead with the
    # winning team and losing team event variables
    GG_Team_Win(winner=winning_team, loser=5 - winning_team).fire()

    # Always return False so that gg_win never fires
    return False


# =============================================================================
# >> GAME EVENTS
# =============================================================================
def es_map_start(event_var):
    '''Fired when a new map starts'''

    # Reset the team's level and leader values
    gg_teams.clear()

    # Load the resource file
    gg_teamwork_resource.load()


def round_end(event_var):
    '''Fired at the end of each round'''

    # Loop through both teams
    for team in gg_teams:

        # Delay 1 tick so that the level is set properly
        delayed(0.1, gg_teams[team].set_all_player_levels)


def round_start(event_var):
    '''Fired when the round starts'''

    # Do messages need sent for what level each team is on?
    if not int(gg_teamwork_round_messages):

        # If not, return
        return

    # Loop through both teams
    for team in gg_teams:

        # Send chat messages about teams new level
        gg_teams[team].send_level_message()


def player_team(event_var):
    '''Fired any time a player changes teams'''

    # Store the userid
    userid = int(event_var['userid'])

    # Get the old team
    old_team = int(event_var['oldteam'])

    # Was the player on a "living" team?
    if old_team in gg_teams:

        # Check to see if the player was leading on their team
        gg_teams[old_team].check_old_leader(userid)

    # Get the team the player switched to
    team = int(event_var['team'])

    # Did the player switch to a "living" team?
    if team in gg_teams:

        # Set the player's level
        gg_teams[team].set_player_level(userid)


def gg_levelup(event_var):
    '''Fired when a player levels up'''

    # Get the leveler's team
    team = int(event_var['es_attackerteam'])

    # Check to see if the player increased the team's level
    gg_teams[team].check_team_leader(
        int(event_var['leveler']), int(event_var['new_level']))


def gg_start(event_var):
    '''Fired when the match is about to start'''

    # Reset the team's level and leader values
    gg_teams.clear()


def gg_team_win(event_var):
    '''Fired when a team wins the match'''

    # Reset the team's level and leader values
    gg_teams.clear()

    # Send Winner Messages?
    if int(gg_teamwork_winner_messages):

        # Send Winner Messages
        gg_teams[int(event_var['winner'])].send_winner_messages()

    # Get a random player from the server
    userid = getuserid()

    # End the match
    ServerCommand('es_xgive %s game_end' % userid)
    ServerCommand('es_xfire %s game_end EndGame' % userid)

    # Loop through all players on the server
    for userid in getUseridList():

        # Is the player a bot?
        if isbot(userid):

            # If so, don't play the sound
            continue

        # Play the winner sound to the player
        Player(userid).playsound('winner')
