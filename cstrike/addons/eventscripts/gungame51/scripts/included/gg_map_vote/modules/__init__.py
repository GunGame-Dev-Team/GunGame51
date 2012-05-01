# ../scripts/included/gg_map_vote/modules/__init__.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# EventScripts Imports
#   ES
from es import ServerVar
#   Cmdlib
from cmdlib import registerSayCommand
from cmdlib import unregisterSayCommand

# Script Imports
from mapvote import mapvote
from nominate import nominate
from rtv import rtv


# =============================================================================
# >> CLASSES
# =============================================================================
class _VotingManagement(object):
    '''Class that registers, stores, and unregisters say commands'''

    # Set the base attributes
    vote_command = ''
    nominate_command = ''
    rtv_command = ''

    def register_say_commands(self):
        '''
            Method used to register say commands (if necessary) and store them
        '''

        # Get the player vote command
        vote_command = str(ServerVar('gg_map_vote_player_command'))

        # Is there a command?
        if vote_command:

            # Register the command
            registerSayCommand(vote_command,
                mapvote.player_vote_command, 'Send a player the MapVote')

            # Store the vote command
            self.vote_command = vote_command

        # Should the other commands be registered?
        if int(ServerVar('gg_map_vote')) != 1:

            # Do not register the other commands
            return

        # Should the nominate command be registered?
        if int(ServerVar('gg_map_vote_nominate')):

            # Get the nominate command
            nominate_command = str(ServerVar('gg_map_vote_nominate_command'))

            # Is there a nominate command?
            if nominate_command:

                # Register the nominate command
                registerSayCommand(nominate_command,
                    nominate.player_nominate_command,
                    'Send a player the Nomination Menu')

                # Store the nominate command
                self.nominate_command = nominate_command

        # Should the rtv command be registered?
        if int(ServerVar('gg_map_vote_rtv')):

            # Get the rtv vote command
            rtv_command = str(ServerVar('gg_map_vote_rtv_command'))

            # Is there an rtv command?
            if rtv_command:

                # Register the rtv command
                registerSayCommand(rtv_command,
                    rtv.player_rtv_command,
                    'Command players use to Rock the Vote.')

                # Store the rtv command
                self.rtv_command = rtv_command

    def unregister_say_commands(self):
        '''Method used to unregister say commands (if necessary)'''

        # Is there a player vote command?
        if self.vote_command:

            # Unregister the player vote command
            unregisterSayCommand(self.vote_command)

            # Reset the player vote command
            self.vote_command = ''

        # Is there a nominate command?
        if self.nominate_command:

            # Unregister the nominate command
            unregisterSayCommand(self.nominate_command)

            # Reset the nominate command
            self.vote_command = ''

        # Is there a rtv command?
        if self.rtv_command:

            # Unregister the rtv command
            unregisterSayCommand(self.rtv_command)

            # Reset the rtv command
            self.vote_command = ''

    @staticmethod
    def reset():
        '''Method used to reset MapVote, Nominate, and RockTheVote'''

        # Reset the MapVote
        mapvote.reset()

        # Reset Nominate
        nominate.reset()

        # Reset RockTheVote
        rtv.reset()

# Get the _VotingManagement instance
voting_management = _VotingManagement()
