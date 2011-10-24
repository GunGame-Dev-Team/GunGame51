# ../scripts/included/gg_turbo/gg_turbo_config.py

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

        # Create the gg_turbo instance
        with config.cfg_cvar('gg_turbo') as cvar:

            cvar.name = 'TURBO MODE'
            cvar.description.append('Gives the player their ' +
                'next weapon immediately when they level up.')
            cvar.options.append('0 = (Disabled) Do not load gg_turbo.')
            cvar.options.append('1 = (Enabled) Load gg_turbo.')
            cvar.default = 0
            cvar.text = 'Enables/Disables gg_turbo.'
