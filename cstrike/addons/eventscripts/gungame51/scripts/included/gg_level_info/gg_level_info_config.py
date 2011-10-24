# ../scripts/included/gg_level_info/gg_level_info_config.py

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

        # Create the gg_level_info instance
        with config.cfg_cvar('gg_level_info') as cvar:

            cvar.name = 'LEVEL INFO'
            cvar.description.append(
                'Sends hudhints to players for level info.')
            cvar.options.append('0 = (Disabled) Do not load gg_level_info.')
            cvar.options.append('1 = (Enabled) Load gg_level_info.')
            cvar.default = 0
            cvar.text = 'Enables/Disables gg_level_info.'
