# ../scripts/included/gg_leader_messages/gg_leader_messages_config.py

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

        with config.cfg_cvar('gg_leader_messages') as cvar:

            cvar.name = 'LEADER MESSAGES'
            cvar.description.append('Sends messages to ' +
                'players when the current leaders change.')
            cvar.options.append(
                '0 = (Disabled) Do not load gg_leader_messages.')
            cvar.options.append('1 = (Enabled) Load gg_leader_messages.')
            cvar.default = 0
            cvar.text = 'Enables/Disables gg_leader_messages.'
