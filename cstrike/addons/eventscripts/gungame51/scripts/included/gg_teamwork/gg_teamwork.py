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
from es import getplayerteam
from es import getUseridList
from es import isbot
from es import ServerVar

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
info.conflicts = ['gg_deathmatch', 'gg_ffa', 'gg_handicap', 'gg_teamplay']
info.translations = ['gg_teamwork']


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
gg_teamwork_jointeam_level = ServerVar('gg_teamwork_jointeam_level')
gg_teamwork_messages = ServerVar('gg_teamwork_messages')


# =============================================================================
# >> EVENT CLASSES
# =============================================================================
class GG_Team_Win(ESEvent):
    '''Fires when a team wins the game'''

    winner = ShortField(
        min_value=2, max_value=3, comment='Team that won the match')

    loser = ShortField(
        min_value=2, max_value=3, comment='Team that lost the match')

    round = BooleanField(comment='1 if the winner of the round, 0 if the ' +
                         'winner of the map')

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

        # Get the new object
        self = dict.__new__(cls)

        # Loop through both teams
        for team in (2, 3):

            # Add the team to the dictionary
            self[team] = TeamManagement(team)

        # Return the dictionary
        return self

    def clear(self):
        '''Resets the team level value'''

        # Loop through both teams
        for team in self:

            # Reset the level value
            self[team].level = 1


class TeamManagement(object):
    '''Class used to store team values and perform actions on team members'''

    def __init__(self, team):
        '''Fired when the team's instance is initialized'''

        # Store the team
        self.team = team

        # Set the team's level value
        self.level = 1

    def set_all_player_levels(self):
        '''Sets all players on the team to the highest level'''

        # Get the highest level on the team
        self.level = max(self.get_team_levels)

        # Loop through all players on the team
        for userid in self.team_players:

            # Get the Player() instance for the current player
            ggPlayer = Player(userid)

            # Get the number of levels to increase the player
            levels = self.level - ggPlayer.level

            # Does the player need leveled up?
            if levels > 0:

                # Level the player up to the highest level
                ggPlayer.levelup(levels, reason=info.name)

    def set_player_level(self, userid):
        '''Sets a player that just joined the team's level'''

        # Get the player's Player() instance
        ggPlayer = Player(userid)

        # Does the player get set to level 1?
        if not int(gg_teamwork_jointeam_level):

            # Does the player need leveled down to level 1?
            if ggPlayer.level <= 1:

                # The player is on level 1, so return
                return

            # Get the number of levels to level the player down
            levels = ggPlayer.level - 1

            # Level the player down to level 1
            ggPlayer.leveldown(levels, reason=info.name)

        # Does the player need set to the teams start level for this round?
        else:

            # Get the number of levels to change the player
            levels = self.level - ggPlayer.level

            # Does the player's level need changed?
            if not levels:

                # If not, return
                return

            # Does the player need leveled up?
            if levels > 0:

                # Level the player up to the team's level
                ggPlayer.levelup(levels, reason=info.name)

            # Does the player need leveled down?
            else:

                # Level the player down to the team's level
                ggPlayer.leveldown(-levels, reason=info.name)

    def send_level_message(self):
        '''Sends a message to all players about the teams new level'''

        # Store a team member's index
        index = self.index

        # Loop through all players on the server
        for userid in getUseridList():

            # Is the player a bot?
            if isbot(userid):

                # If so, don't send a message
                continue

            # Get the leveling team's name
            teamname = langstring(self.teamname, userid=userid)

            # Send the message to the player
            Player(userid).saytext2(index,
                'TeamWork_TeamLevel', {'team': teamname,
                'level': self.level, 'weapon': get_level_weapon(self.level)})

    @property
    def get_team_levels(self):
        '''Returns a list of all player levels on the team'''

        # Create a list to store player levels
        levels = []

        # Loop through all players on the team
        for userid in self.team_players:

            # Add the player's level to the list
            levels.append(Player(userid).level)

        # Return the list of levels
        return levels

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

    @property
    def teamname(self):
        return 'TeamWork_%s' % self.team

# Gett he GGTeams instance
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
def pre_gg_win(event_var):
    '''Fired prior to gg_win event being fired'''

    # Get the team the winner is one
    winning_team = getplayerteam(event_var['winner'])

    # Fire the gg_teamwin event instead with the
    # winning team, losing team, and round event variables
    GG_Team_Win(winner=winning_team,
        loser=5 - winning_team, round=int(event_var['round'])).fire()

    # Always return False so that gg_win never fires
    return False


# =============================================================================
# >> GAME EVENTS
# =============================================================================
def es_map_start(event_var):
    '''Fired when a new map starts'''

    # Load the resource file
    gg_teamwork_resource.load()


def round_end(event_var):
    '''Fired at the end of each round'''

    # Loop through both teams
    for team in gg_teams:

        # Set all players on the team to the highest level
        gg_teams[team].set_all_player_levels()


def round_start(event_var):
    '''Fired when the round starts'''

    # Do messages need sent for what level each team is on?
    if not int(gg_teamwork_messages):

        # If not, return
        return

    # Loop through both teams
    for team in gg_teams:

        # Send chat messages about teams new level
        gg_teams[team].send_level_message()


def player_team(event_var):
    '''Fired any time a player changes teams'''

    # Get the team the player switched to
    team = int(event_var['team'])

    # Did the player switch to a "living" team?
    if team in gg_teams:

        # Set the player's level
        gg_teams[team].set_player_level(event_var['userid'])


def gg_start(event_var):
    '''Fired when the match is about to start'''

    # Reset team level and multikill values
    gg_teams.clear()


def gg_teamwin(event_var):
    '''Fired when a team wins the match'''

    # Reset team level and multikill values
    gg_teams.clear()
