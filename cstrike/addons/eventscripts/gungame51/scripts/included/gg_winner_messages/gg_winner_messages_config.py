# ../scripts/included/gg_winner_messages/gg_winner_messages_config.py

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

        # Create the gg_winner_messages instance
        with config.cfg_cvar('gg_winner_messages') as cvar:

            cvar.name = 'WINNER MESSAGES'
            cvar.description.append('Sends messages to ' +
                'players when someone wins a round/match.')
            cvar.options.append(
                '0 = (Disabled) Do not load gg_winner_messages.')
            cvar.options.append('1 = (Enabled) Load gg_winner_messages.')
            cvar.default = 0
            cvar.text = 'Enables/Disables gg_winner_messages.'
