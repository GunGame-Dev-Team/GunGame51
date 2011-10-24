# ../scripts/custom/gg_teamwork/gg_teamwork_config.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
from __future__ import with_statement
from path import path

# GunGame Imports
from gungame51.core.cfg.configs import ConfigContextManager


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():

    # Create the cfg file
    with ConfigContextManager(
      path(__file__).parent.split('scripts')[~0][1:]) as config:

        # Create the gg_teamwork instance
        with config.cfg_cvar('gg_teamwork') as cvar:

            cvar.name = 'TEAMWORK'
            cvar.description.append('Level-up to the highest ' +
                '"team" level at the end of every round')
            cvar.notes.append('Work together to get 1 player to level up ' +
                'as much as possible during the round, so that your team ' +
                'achieves the highest level it can each round.')
            cvar.notes.append('To have even more fun with this mod, it is ' +
                'highly recommended you use gg_assist at the same ' +
                'time:\n\thttp://forums.gungame.net/viewtopic.php?f=74&t=1294')
            cvar.options.append('0 = (Disabled) Do not load gg_teamwork.')
            cvar.options.append('1 = (Enabled) Load gg_teamwork.')
            cvar.default = 0
            cvar.text = 'Enables/Disables gg_teamwork.'

        # Create the gg_teamwork_jointeam_level instance
        with config.cfg_cvar('gg_teamwork_jointeam_level') as cvar:

            cvar.name = 'TEAMWORK JOINTEAM LEVEL'
            cvar.description.append('What level to set a ' +
                'player that joins the team during the match')
            cvar.options.append(
                '0 = Set players to level 1 when joining a team.')
            cvar.options.append('1 = Set players to the level ' +
                'that the team started on for the current round.')
            cvar.default = 1
            cvar.text = ('Set players to level 1 or the level ' +
                'the team started the round when joining a team')

        # Create the gg_teamwork_messages instance
        with config.cfg_cvar('gg_teamwork_round_messages') as cvar:

            cvar.name = 'TEAMWORK ROUND MESSAGES'
            cvar.description.append('Send messages on ' +
                'round_end about what level each team was set to.')
            cvar.options.append(
                '0 = (Disabled) Do not send messages on round_end')
            cvar.options.append('1 = (Enabled) Send messages on round_end')
            cvar.default = 1
            cvar.text = ('Enable/Disable sending messages on ' +
                'round_end about what level each team is now on')

        # Create the gg_teamwork_leader_messages instance
        with config.cfg_cvar('gg_teamwork_leader_messages') as cvar:

            cvar.name = 'TEAMPLAY LEADER MESSAGES'
            cvar.description.append('Send messages when the ' +
                'leader on each team increases their level.')
            cvar.options.append('0 = (Disabled) Do not ' +
                "send messages when the team's level increases")
            cvar.options.append('1 = (Enabled) Send ' +
                "messages when the team's level increases")
            cvar.default = 1
            cvar.text = ('Enable/Disable sending messages ' +
                "when a player increases the team's level")

        # Create the gg_teamwork_winner_messages instance
        with config.cfg_cvar('gg_teamwork_winner_messages') as cvar:

            cvar.name = 'TEAMPLAY WINNER MESSAGES'
            cvar.description.append(
                'Send messages when a team wins the match.')
            cvar.options.append('0 = (Disabled) Do not ' +
                'send messages when a team wins the match')
            cvar.options.append('1 = (Enabled) Send ' +
                'messages when a team wins the match')
            cvar.default = 1
            cvar.text = ('Enable/Disable sending ' +
                'messages when a team wins the match')
