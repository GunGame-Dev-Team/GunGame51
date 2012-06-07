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

        # Create the gg_turbo_quick
        with config.cfg_cvar('gg_turbo_quick') as cvar:

            cvar.name = 'QUICK SWITCH'
            cvar.description.append('Allows players to use ' +
                'their new weapon immediately after receiving it.')
            cvar.description.append(
                'Without setting this, players will have to go ' +
                'through the animation before they can use the weapon.')
            cvar.options.append('0 = (Disabled) The animation will play.')
            cvar.options.append('1 = (Enabled) The animation will not play.')
            cvar.default = 0
            cvar.text = ('Allows players to use their new ' +
                'weapon immediately after receiving it.')
