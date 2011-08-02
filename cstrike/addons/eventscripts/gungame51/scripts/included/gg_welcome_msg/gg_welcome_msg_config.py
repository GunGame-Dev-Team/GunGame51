# ../scripts/included/gg_welcome_msg/gg_welcome_msg_config.py

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

        # Create the gg_welcome_msg instance
        with config.cfg_cvar('gg_welcome_msg') as cvar:

            cvar.name = 'GUNGAME WELCOME MESSAGE'
            cvar.description.append([
                'A menu displayed to newly connected ' +
                    'players displaying',
                'server and addon information',
                ])
            cvar.description.append(
                'Players can type !welcome to bring this menu back up.')
            cvar.notes.append('The configureable message ' +
                'is available in "gg_welcome_msg.txt".')
            cvar.options.append('0 = (Disabled)')
            cvar.options.append('1 = (Enabled)')
            cvar.default = 0
            cvar.text = 'Enables/Disables gg_welcome_msg.'

        # Create the gg_welcome_msg_timeout instance
        with config.cfg_cvar('gg_welcome_msg_timeout') as cvar:

            cvar.name = 'GUNGAME WELCOME MESSAGE TIMEOUT'
            cvar.description.append('The number (in seconds) ' +
                'it takes for the welcome message to dissappear.')
            cvar.options.append('(#) = (#) seconds')
            cvar.options.append('10 = 10 seconds')
            cvar.default = 10
            cvar.text = ('Sets the number of ' +
                'seconds for gg_welcome_msg_timeout.')
