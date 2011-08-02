# ../scripts/included/gg_dead_strip/gg_dead_strip_config.py

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

        # Create the gg_dead_strip instance
        with config.cfg_cvar('gg_dead_strip') as cvar:

            cvar.name = 'DEAD STRIP'
            cvar.description.append(
                "Removes a player's weapons when they die.")
            cvar.notes.append(
                'Prevents players from picking up the wrong weapon.')
            cvar.options.append('0 = (Disabled) Do not load gg_dead_strip.')
            cvar.options.append('1 = (Enabled) Load gg_dead_strip.')
            cvar.default = 0
            cvar.text = 'Enables/Disables gg_dead_strip.'
