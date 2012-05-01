# ../scripts/included/gg_map_vote/modules/mapvote.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
#   Random
from random import choice as rchoice

# EventScripts Imports
#   ES
from es import getUseridList
from es import isbot
from es import ServerCommand
from es import ServerVar
#   Popuplib
from popuplib import easymenu
from popuplib import isqueued

# GunGame Imports
#   Messaging
from gungame51.core.messaging.shortcuts import hudhint
from gungame51.core.messaging.shortcuts import langstring
#   Players
from gungame51.core.players.shortcuts import Player
#   Repeat
from gungame51.core.repeat import Repeat

# Script Imports
from attributes import AttributeManagement
from events import GG_Map_Vote_Ended
from events import GG_Map_Vote_Started
from events import GG_Map_Vote_Submit
from votemaps import VoteMapList
from players.voters import DictionaryOfPlayers


# =============================================================================
# >> CLASSES
# =============================================================================
class _MapVoteManagement(object):
    '''Class used to manage the MapVote'''

    def __init__(self):
        '''Called when the class instance is initialized'''

        # Store the base attributes
        AttributeManagement.active = False
        AttributeManagement.winner = None
        self.repeat = Repeat('gg_map_vote', self.count_down)
        self.votes = DictionaryOfPlayers()

    def reset(self):
        '''Resets the base attributes'''

        # Reset the base attributes
        AttributeManagement.active = False
        AttributeManagement.winner = None
        self.votes.clear()

    def player_vote_command(self, userid, args):
        '''Called when a player uses the vote command'''

        # Send the menu to the player
        self.send_map_vote_to_player(userid)

    def send_map_vote_to_player(self, userid):
        '''Sends the MapVote to the given player if needed'''

        # Should the player be sent the MapVote menu?
        if self.check_send_vote(userid):

            # Start the player's menu loop
            self.votes[userid].start_menu_loop()

    def check_send_vote(self, userid):
        '''Checks to see if the given player should receive the MapVote menu'''

        # Is the MapVote active?
        if not AttributeManagement.active:

            # If the MapVote is not active, do not send
            return False

        # Has the player already voted?
        if userid in self.votes and not self.votes[userid].choice is None:

            # If the player already voted, do not send
            return False

        # Does the player already have the MapVote in their queue?
        if isqueued('gg_map_vote', userid):

            # If the player has the MapVote queued, do not send
            return False

        # Send the menu to the player
        return True

    def start_map_vote(self):
        '''Starts the MapVote'''

        # Is a 3rd party MapVote system being used?
        if int(ServerVar('gg_map_vote')) == 2:

            # Execute the 3rd party's command
            ServerCommand(str(ServerVar('gg_map_vote_command')))

            # Don't go any further
            return

        # Get the list of maps to vote on
        self.maps = VoteMapList()

        # Set the MapVote to be active
        AttributeManagement.active = True

        # Create the MapVote menu
        self.menu = easymenu('gg_map_vote', 'choice', self.chosen_map)

        # Set the title for the MapVote menu
        self.menu.settitle(langstring('PlaceYourVotes'))

        # Make sure the MapVote timesout every 4 seconds
        self.menu.timeout('view', 4)

        # Loop through all maps that are to be voted on
        for map_name in self.maps:

            # Add the map to the MapVote menu
            self.menu.addoption(map_name, map_name)

        # Get the duration of the MapVote
        duration = int(ServerVar('gg_map_vote_time'))

        # Setup the gg_map_vote_started event
        gg_map_vote_started = GG_Map_Vote_Started(
            maps=','.join(self.maps), duration=duration)

        # Fire the gg_map_vote_started event
        gg_map_vote_started.fire()

        # Start the MapVote repeat
        self.repeat.start(1, duration)

        # Should the MapVote only be sent to dead players?
        if int(ServerVar('gg_map_vote_after_death')):

            # Loop through all dead human players
            for userid in self.dead_players:

                # Send the MapVote menu to the player
                self.send_map_vote_to_player(userid)

            # Do not go any further
            return

        # Loop through all player human players
        for userid in self.all_players:

            # Send the MapVote menu to the player
            self.send_map_vote_to_player(userid)

    def count_down(self):
        '''Counts down the MapVote and displays the current leaders'''

        # Did the MapVote just end?
        if self.repeat.remaining == 0:

            # End the MapVote
            self.end_map_vote()

            # Do not go further
            return

        # Are there 5 or fewer seconds remaining to vote?
        if self.repeat.remaining <= 5:

            # Loop through all human players
            for userid in self.all_players:

                # Play a countdown beep for the player
                Player(userid).playsound('countDownBeep')

        # Get all the current votes
        all_votes = [self.votes[userid].choice for userid in
            self.votes if not self.votes[userid].choice is None]

        # Have any votes been cast?
        if not all_votes:

            # If not, simply return
            return

        # Find how many votes each map has currently received
        votes_per_map = dict((map_name,
            all_votes.count(map_name))
            for map_name in set(all_votes))

        # Sort the maps by how many votes each has currently received
        sorted_votes = sorted(votes_per_map,
            key=lambda map_name: votes_per_map[map_name],
            reverse=True)

        # Create an empty string to add text to
        text = ''

        # Loop through the three maps with the most current votes
        for x in xrange(min(3, len(sorted_votes))):

            # Get the map's name
            map_name = sorted_votes[x]

            # Add to the text showing the map
            # and how many votes it has received
            text += langstring('MapVotes',
                tokens={'map': map_name, 'votes': votes_per_map[map_name]})

        # Get the type of message to send
        message = ('Countdown_Singular' if
            self.repeat.remaining == 1 else 'Countdown_Plural')

        # Send a hudhint message to all players about the current vote totals
        hudhint('#human', message,
            {'time': self.repeat.remaining,
            'voteInfo': text,
            'votes': len(all_votes),
            'totalVotes': len(list(self.all_players))})

    def chosen_map(self, userid, choice, popupid):
        '''Stores the map that the player voted for'''

        # Stop the player's loop
        self.votes[userid].stop_loop()

        # Store the player's vote
        self.votes[userid].choice = choice

        # Setup the gg_map_vote_submit event
        gg_map_vote_submit = GG_Map_Vote_Submit(userid=userid, choice=choice)

        # Fire the gg_map_vote_submit event
        gg_map_vote_submit.fire()

        # Has everyone on the server voted?
        if len(list(self.all_players)) != len(self.votes):

            # If not, simply return
            return

        # Stop the countdown
        self.repeat.stop()

        # End the MapVote
        self.end_map_vote()

    def end_map_vote(self):
        '''Ends the MapVote and gets the winning map'''

        # Remove the menu
        self.menu.delete()

        # Get all of the maps that were chosen
        all_votes = [self.votes[userid].choice for userid in
            self.votes if not self.votes[userid].choice is None]

        # Were there no votes?
        if not all_votes:

            # Select a random map from the maplist as the winner
            AttributeManagement.winner = rchoice(self.maps)

        # Were there some votes?
        else:

            # Find how many votes each map received
            votes_per_map = dict((map_name,
                all_votes.count(map_name))
                for map_name in set(all_votes))

            # Sort the maps by how many votes each had
            sorted_votes = sorted(votes_per_map,
                key=lambda map_name: votes_per_map[map_name],
                reverse=True)

            # Get the winning number of votes
            winning_votes = votes_per_map[sorted_votes[0]]

            # Get all maps that received the winning number of votes
            winners = [map_name for map_name in votes_per_map 
                if votes_per_map[map_name] == winning_votes]

            # Choose a winner out of the maps that
            # received the winning number of votes
            AttributeManagement.winner = rchoice(winners)

        # Setup the gg_map_vote_ended event
        gg_map_vote_ended = GG_Map_Vote_Ended(winner=AttributeManagement.winner,
            votes=votes_per_map[AttributeManagement.winner], total_votes=len(all_votes))

        # Fire the gg_map_vote_ended event
        gg_map_vote_ended.fire()

    @property
    def all_players(self):
        '''Yields all human players'''

        # Loop through all userids on the server
        for userid in getUseridList():

            # Is the player a Bot?
            if not isbot(userid):

                # If the player is human, yield their userid
                yield userid

    @property
    def dead_players(self):
        '''Yields all dead human players'''

        # Loop through all human players
        for userid in self.all_players:

            # Is the player dead?
            if getplayerprop(userid, 'CBasePlayer.pl.deadflag'):

                # If so, yield their userid
                yield userid

# Get the _MapVoteManagement instance
mapvote = _MapVoteManagement()
