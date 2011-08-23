# ../scripts/custom/gg_teamplay/gg_teamplay_config.py

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
from gungame51.core.cfg import ConfigContextManager


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():

    # Create the cfg file
    with ConfigContextManager(
      path(__file__).parent.split('scripts')[~0][1:]) as config:

        # Create the gg_teamplay instance
        with config.cfg_cvar('gg_teamplay') as cvar:

            cvar.name = 'TEAMPLAY'
            cvar.description.append('Level-up as a Team')
            cvar.description.append('The team that wins ' +
                'each round increases their multikill value')
            cvar.description.append('When a team reaches ' +
                "their current level's multikill, they level up")
            cvar.options.append('0 = (Disabled) Do not load gg_teamplay.')
            cvar.options.append('1 = (Enabled) Load gg_teamplay.')
            cvar.default = 0
            cvar.text = 'Enables/Disables gg_teamplay.'

        # Create the gg_teamplay_roundend_messages instance
        with config.cfg_cvar('gg_teamplay_roundend_messages') as cvar:

            cvar.name = 'TEAMPLAY ROUNDEND MESSAGES'
            cvar.description.append('Send messages on ' +
                'round_end when a team earns a multikill or level')
            cvar.options.append('0 = (Disabled) Do not show chat messages ' +
                'when a team levels up or earns a multikill on round_end')
            cvar.options.append('1 = (Enabled) Show chat messages ' +
                'when a team levels up or earns a multikill on round_end')
            cvar.default = 1
            cvar.text = ('Enables/Disables showing chat messages ' +
                'when a team levels up or earns a multikill on round_end')

        # Create the gg_teamplay_level_info instance
        with config.cfg_cvar('gg_teamplay_level_info') as cvar:

            cvar.name = 'TEAMPLAY LEVEL INFO'
            cvar.description.append('Show team level ' +
                'info in player hudhint on player_spawn')
            cvar.options.append(
                '0 = (Disabled) Do not show hudhint level info messages')
            cvar.options.append(
                '1 = (Enabled) Show hudhint level info messages')
            cvar.default = 1
            cvar.text = 'Enables/Disables showing hudhint level info messages'

        # Create the gg_teamplay_winner_messages instance
        with config.cfg_cvar('gg_teamplay_winner_messages') as cvar:

            cvar.name = 'TEAMPLAY WINNER MESSAGES'
            cvar.description.append('Send Winner Messages when a team wins')
            cvar.options.append('0 = (Disabled) Do not show Winner Messages')
            cvar.options.append('1 = (Enabled) Show Winner Messages')
            cvar.default = 1
            cvar.text = 'Enables/Disables showing Winner Messages'

        # Create the gg_teamplay_end_on_first_kill instance
        with config.cfg_cvar('gg_teamplay_end_on_first_kill') as cvar:

            cvar.name = 'TEAMPLAY END ON FIRST KILL'
            cvar.description.append('First kill by a team on the last ' +
                'multikill of the last level will win the match')
            cvar.options.append('0 = (Disabled) Only end match ' +
                'when a team wins the final round')
            cvar.options.append([
                '1 = (Enabled) First player to get a ' +
                    'kill with the last level weapon ',
                '(if the team is on the last multikill) will win the match',
                ])
            cvar.default = 0
            cvar.text = ('Enables/Disables team winning with ' +
                'the first kill on the last weapon')
