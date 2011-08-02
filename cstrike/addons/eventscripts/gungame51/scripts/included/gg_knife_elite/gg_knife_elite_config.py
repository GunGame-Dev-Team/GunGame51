# ../scripts/included/gg_knife_elite/gg_knife_elite_config.py

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

        # Create the gg_knife_elite instance
        with config.cfg_cvar('gg_knife_elite') as cvar:

            cvar.name = 'KNIFE ELITE'
            cvar.description.append('Once a player levels up, ' +
                'they only get a knife until the next round.')
            cvar.notes.requires.append('gg_dead_strip')
            cvar.notes.conflict.append('gg_turbo')
            cvar.options.append('0 = (Disabled) Do not load gg_knife_elite.')
            cvar.options.append('1 = (Enabled) Load gg_knife_elite.')
            cvar.default = 0
            cvar.text = 'Enables/Disables gg_knife_elite.'
