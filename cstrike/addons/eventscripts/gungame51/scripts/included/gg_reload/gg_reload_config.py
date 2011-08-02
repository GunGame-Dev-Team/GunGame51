# ../scripts/included/gg_reload/gg_reload_config.py

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

        # Create the gg_reload instance
        with config.cfg_cvar('gg_reload') as cvar:

            cvar.name = 'RELOAD'
            cvar.description.append('When a player gains a ' +
                'level, the ammo in their clip is replenished.')
            cvar.options.append('0 = (Disabled) Do not load gg_reload.')
            cvar.options.append('1 = (Enabled) Load gg_reload.')
            cvar.default = 0
            cvar.text = 'Enables/Disables gg_reload.'
