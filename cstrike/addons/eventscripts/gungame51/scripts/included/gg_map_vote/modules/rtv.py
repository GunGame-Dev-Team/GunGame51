# ../scripts/included/gg_map_vote/modules/rtv.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
#   Math
from math import ceil

# EventScripts Imports
#   ES
from es import getuserid
from es import InsertServerCommand
from es import ServerVar

# GunGame Imports
#   Messaging
from gungame51.core.messaging.shortcuts import msg
from gungame51.core.messaging.shortcuts import saytext2
#   Weapons
from gungame51.core.leaders.shortcuts import get_leader_level
from gungame51.core.weapons.shortcuts import get_total_levels

# Script Imports
from attributes import AttributeManagement
from mapvote import mapvote
from players.rockers import RockTheVotePlayers


# =============================================================================
# >> CLASSES
# =============================================================================
class _RockTheVoteManagement(object):
    '''Class used to manage the RockTheVote'''

    def __init__(self):
        '''Called when the class instance is initialized'''

        # Store the base attributes
        self.players = RockTheVotePlayers()
        AttributeManagement.rtv = False

    def reset(self):
        '''Resets the base attributes'''

        # Reset the base attributes
        self.players.clear()
        AttributeManagement.rtv = False

    def player_rtv_command(self, userid, args):
        '''Called when a player uses the rtv command'''

        # Has the vote been rocked already?
        if AttributeManagement.rtv:

            # Tell player rtv already occurred
            msg(userid, 'RTVInitiated', prefix=True)

            # No need to go further
            return

        # Is a third party MapVote being used?
        if AttributeManagement.active == 2:

            # Just return
            return

        # Is the MapVote active?
        if AttributeManagement.active:

            # Tell player that voting already in progress
            msg(userid, 'VoteAlreadyInProgress', prefix=True)

            # No need to go further
            return

        # Is there already a MapVote winner?
        if not AttributeManagement.winner is None:

            # Tell player MapVote winner already chosen
            msg(userid, 'Nextmap',
                {'map': AttributeManagement.winner}, prefix=True)

            # No need to go further
            return

        # Get the cutoff level
        disable_level = (get_total_levels() *
            ServerVar('gg_map_vote_rtv_levels_required') / 100)

        # Is the leader too high of a level?
        if get_leader_level() >= disable_level:

            # Tell player it is too late to RockTheVote
            msg(userid, 'RTVPastLevel', {'level': disable_level}, True)

            # No need to go further
            return

        # Get the number of votes required to RockTheVote
        required_votes = int(ceil(len(list(mapvote.all_players)) *
            float(ServerVar('gg_map_vote_rtv_percent')) / 100))

        # Add the player to the set
        self.players.add(userid)

        # Are there enough votes to RockTheVotes?
        if len(self.players) < required_votes:

            # Message all players about the new RockTheVoter
            saytext2('#human', Player(userid).index, 'RTVVote',
                {'name': getplayername(userid), 'votes': len(self.players),
                'required': required_votes}, True)

            # If not, no need to go further
            return

        # Message all players that the vote has been rocked
        msg('#human', 'RTVPassed', prefix=True)

        # Set occurred to True
        AttributeManagement.rtv = True

        # Start the MapVote
        mapvote.start_map_vote()

    @staticmethod
    def end_map():
        '''Method used to end the current map after the MapVote'''

        # Get a userid on the server
        userid = getuserid()

        # Was a userid found?
        if not userid:

            # If not, simply change the level
            InsertServerCommand('changelevel %s' % AttributeManagement.winner)

            # No need to go further
            return

        # Set chattime to 5
        ServerVar('mp_chattime').set(5)

        # End the current map
        InsertServerCommand('es_xgive %s game_end' % userid)
        InsertServerCommand('es_xfire %s game_end EndGame' % userid)

# Get the _RockTheVoteManagement instance
rtv = _RockTheVoteManagement()
