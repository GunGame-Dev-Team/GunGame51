# ../scripts/included/gg_teamplay/gg_teamplay.py

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
from gungame51.core.events.eventlib.fields import ByteField
from gungame51.core.events.eventlib.fields import ShortField
#   Messaging
from gungame51.core.messaging.shortcuts import langstring
#   Players
from gungame51.core.players import Player
#   Weapons
from gungame51.core.weapons.shortcuts import get_level_multikill
from gungame51.core.weapons.shortcuts import get_level_weapon
from gungame51.core.weapons.shortcuts import get_total_levels


# =============================================================================
# >> ADDON REGISTRATION/INFORMATION
# =============================================================================
info = AddonInfo()
info.name = 'gg_teamplay'
info.title = 'GG Teamplay'
info.author = 'GG Dev Team'
info.version = '5.1.%s' % '$Rev$'.split('$Rev: ')[1].split()[0]
info.conflicts = ['gg_deathmatch', 'gg_ffa', 'gg_handicap', 'gg_teamwork']
info.translations = ['gg_teamplay']


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
gg_teamplay_roundend_messages = ServerVar('gg_teamplay_roundend_messages')
gg_teamplay_level_info = ServerVar('gg_teamplay_level_info')
gg_teamplay_winner_messages = ServerVar('gg_teamplay_winner_messages')
gg_teamplay_end_on_first_kill = ServerVar('gg_teamplay_end_on_first_kill')


# =============================================================================
# >> EVENT CLASSES
# =============================================================================
class GG_Team_Win(ESEvent):
    '''Fires when a team wins the game'''

    winner = ShortField(
        min_value=2, max_value=3, comment='Team that won the match')

    loser = ShortField(
        min_value=2, max_value=3, comment='Team that lost the match')


class GG_Team_LevelUp(ESEvent):
    '''Fires when a team levels up'''

    team = ShortField(min_value=2, max_value=3, comment='Team that leveled up')

    old_level = ByteField(
        min_value=1, comment='The old level of the team that leveled up')

    new_level = ByteField(
        min_value=1, comment='The new level of the team that leveled up')

# Get the ResourceFile instance to create the .res file
gg_teamplay_resource = ResourceFile(
    path(__file__).parent.joinpath('gg_teamplay.res'))

# Write the .res file
gg_teamplay_resource.write([GG_Team_Win, GG_Team_LevelUp], overwrite=True)


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
        '''Resets the team level and multikill values'''

        # Loop through both teams
        for team in self:

            # Reset the level and multikill values
            self[team].reset_levels()


class TeamManagement(object):
    '''Class used to store team values and perform actions on team members'''

    def __init__(self, team):
        '''Fired when the team's instance is initialized'''

        # Store the team
        self.team = team

        # Set the team's level and multikill value
        self.reset_levels()

    def reset_levels(self):
        '''Resets the team's level and multikill values'''

        # Set the values back to start
        self.multikill = 0
        self.level = 1

    def increase_multikill(self):
        '''Increases the team's multikill value
            and checks to see if a levelup is needed'''

        # Increase the team's multikill value
        self.multikill += 1

        # Does the team need leveled up?
        if self.multikill >= get_level_multikill(self.level):

            # Increase the team's level
            self.increase_level()

        # Does a message need sent?
        elif int(gg_teamplay_roundend_messages):

            # Send the message
            self.send_increase_multikill_message()

    def increase_level(self):
        '''Increases the team's level and levels up all team memebers'''

        # Reset the team's multikill value
        self.multikill = 0

        # Increase the team's level
        self.level += 1

        # Fire GG_Team_LevelUp
        GG_Team_LevelUp(team=self.team,
            old_level=self.level - 1, new_level=self.level).fire()

        # Did the team just win?
        if self.level == get_total_levels():

            GG_Team_Win(winner=self.team, loser=5 - self.team).fire()

            # Do not send messages or increase player levels
            return

        # Loop through all team members
        for userid in self.team_players:

            # Set the player's level to the team level
            self.set_player_level(userid)

        # Does a message need sent?
        if int(gg_teamplay_roundend_messages):

            # Send the message
            self.send_increase_level_message()

    def set_player_level(self, userid):
        '''Sets the player's level to the team's level'''

        # Get the Player instance
        ggPlayer = Player(userid)

        # Is the player prevented from leveling?
        if info.name in ggPlayer.preventlevel.levelup:

            # Remove the prevention
            ggPlayer.preventlevel.levelup.remove(info.name)

        # Set the player's level to the team's level
        ggPlayer.level = self.level

        # Add the addon to the player's levelup preventlevel
        ggPlayer.preventlevel.levelup.append(info.name)

    def check_final_kill(self, userid, weapon):
        '''Checks to see if the kill should end the match'''

        # Is the team on the last level?
        if self.level != get_total_levels():

            # If not, return
            return

        # Is the team on the last multikill for the last level?
        if self.multikill + 1 < get_level_multikill(self.level):

            # If not, return
            return

        # Was the weapon used the last level's weapon?
        if get_level_weapon(self.level) != weapon:

            # If not, return
            return

        # Get the Player instance
        ggPlayer = Player(userid)

        # Is the attacker on the last level?
        if ggPlayer.level != get_total_levels():

            # If not, return
            return

        # End the match
        GG_Team_Win(winner=self.team, loser=5 - self.team).fire()

    def send_increase_multikill_message(self):
        '''Sends information to chat when a team's multikill increases'''

        # Get the other team's instance
        other = gg_teams[5 - self.team]

        # Is the current team leading?
        if self.level > other.level:

            # Set message name
            message = 'TeamPlay_MultiKill_Leading'

            # Get the level difference
            levels = self.level - other.level

        # Is the current team losing?
        elif self.level < other.level:

            # Set message name
            message = 'TeamPlay_MultiKill_Trailing'

            # Get the level difference
            levels = other.level - self.level

        # Are the teams tied?
        else:

            # Set the message name
            message = 'TeamPlay_MultiKill_Tied'

            # Set the level difference
            levels = 0

        # Send the message to all players
        self.send_all_players_a_message(message,
            {'multikill': self.multikill,
             'total': get_level_multikill(self.level), 'levels': levels,
             'level': self.level, 'other': other.level})

    def send_increase_level_message(self):
        '''Sends information to chat when a team increases their level'''

        # Get the other team's instance
        other = gg_teams[5 - self.team]

        # Did the team just take the lead?
        if self.level - 1 == other.level:

            # Set the message name
            message = 'TeamPlay_Level_TakeLead'

            # Set the level difference
            levels = 1

        # Did the team increase it's lead?
        elif self.level > other.level:

            # Set the message name
            message = 'TeamPlay_Level_Increase'

            # Get the level difference
            levels = self.level - other.level

        # Did the team just tie the game?
        elif self.level == other.level:

            # Set the message name
            message = 'TeamPlay_Level_Tied'

            # Set the level difference
            levels = 0

        # Is the team still losing?
        else:

            # Set the message name
            message = 'TeamPlay_Level_Trailing'

            # Get the level difference
            levels = other.level - self.level

        # Send all players the message
        self.send_all_players_a_message(message,
            {'levels': levels, 'level': self.level})

    def send_hudhint_info(self, userid):
        '''Sends level info on player_spawn'''

        # Get the total levels
        total_levels = get_total_levels()

        # Create text showing team's level
        text = langstring('TeamPlay_LevelInfo_TeamLevel',
            {'teamname': langstring(self.teamname, userid=userid),
            'level': self.level, 'total': total_levels}, userid)

        # Add the teams weapon to the text
        text += langstring('TeamPlay_LevelInfo_TeamWeapon',
            {'weapon': get_level_weapon(self.level)}, userid)

        # Get the team's current level's multikill
        multikill = get_level_multikill(self.level)

        # Is more than 1 round required for this level?
        if multikill > 1:

            # Add Required Rounds to the text
            text += langstring('TeamPlay_LevelInfo_RequiredRounds',
                {'rounds': self.multikill, 'total': multikill}, userid)

        # Add a new-line character
        text += '\n'

        # Get the other team's instance
        other = gg_teams[5 - self.team]

        # Add the other team's level information
        text += langstring('TeamPlay_LevelInfo_TeamLevel',
            {'teamname': langstring(other.teamname, userid=userid),
            'level': other.level, 'total': total_levels}, userid)

        # Get the other team's current level's multikill
        multikill = get_level_multikill(other.level)

        # Is more than 1 round required for this level?
        if multikill > 1:

            # Add Required Rounds to the text
            text += langstring('TeamPlay_LevelInfo_RequiredRounds',
                {'rounds': self.multikill, 'total': multikill}, userid)

        # Send the player the hudhint
        Player(userid).hudhint(text)

    def send_winner_messages(self):
        '''Sends Winner Messages to all players'''

        # Store a team player's index
        index = self.index

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
            ggPlayer.saytext2(index,
                'TeamPlay_Winner', {'teamname': teamname})

            # We want to loop, so we send a message every second for 3 seconds
            for x in xrange(4):

                # Send centermsg about the winner
                delayed(x, ggPlayer.centermsg,
                    ('TeamPlay_Winner_Center', {'teamname': teamname}))

            # Send toptext message about the winner
            ggPlayer.toptext(10, color,
                'TeamPlay_Winner_Center', {'teamname': teamname})

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
            Player(userid).saytext2(index, message, tokens)

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
        '''Returns the team's name for use with langstring'''

        # Return the team's langstring name
        return 'TeamPlay_%s' % self.team

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

    # Declare and load the resource file
    gg_teamplay_resource.declare_and_load()


def unload():
    '''Fired when the script is unloaded'''

    # Loop through all players on the server
    for userid in getUseridList():

        # Get the Player() instance
        ggPlayer = Player(userid)

        # Does the player have gg_teamplay in preventlevel?
        if info.name in ggPlayer.preventlevel.levelup:

            # Remove the addon from the player's levelup preventlevel
            ggPlayer.preventlevel.levelup.remove(info.name)


# =============================================================================
# >> GAME EVENTS
# =============================================================================
def es_map_start(event_var):
    '''Fired when a new map starts'''

    # Reset team level and multikill values
    gg_teams.clear()

    # Load the resource file
    gg_teamplay_resource.load()


def round_end(event_var):
    '''Fired every time the round ends'''

    # Get the team that won the round
    winner = int(event_var['winner'])

    # Did a team win the round?
    if winner in gg_teams:

        # Increase the winning team's multikill
        gg_teams[winner].increase_multikill()


def player_spawn(event_var):
    '''Fired every time a player spawns'''

    # Get the player's team
    team = int(event_var['es_userteam'])

    # Is the player on a team?
    if not team in gg_teams:

        # If not, return
        return

    # Store the userid
    userid = int(event_var['userid'])

    # Set the player's level to the team's level
    gg_teams[team].set_player_level(userid)

    # Does the player need the level info sent?
    if int(gg_teamplay_level_info):

        # Send the player their team's level info
        gg_teams[team].send_hudhint_info(userid)


def player_death(event_var):
    '''Fired when a player dies'''

    # Check for last kill to end the match?
    if not int(gg_teamplay_end_on_first_kill):
        return

    # Get the attacker's team
    attackerteam = int(event_var['es_attackerteam'])

    # Was this a teamkill or suicide?
    if attackerteam == int(event_var['es_userteam']):
        return

    # Is the attacker on a team?
    if attackerteam in gg_teams:

        # Check to see if this kill ends the match
        gg_teams[attackerteam].check_final_kill(
            int(event_var['attacker']), event_var['weapon'])


def gg_start(event_var):
    '''Fired when the match is about to start'''

    # Reset team level and multikill values
    gg_teams.clear()


def gg_teamwin(event_var):
    '''Fired when a team wins the match'''

    # Reset team level and multikill values
    gg_teams.clear()

    # Send Winner Messages?
    if int(gg_teamplay_winner_messages):

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
