# ../scripts/included/gg_dissolver/gg_dissolver_config.py

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

        # Create the gg_dissolver instance
        with config.cfg_cvar('gg_dissolver') as cvar:

            cvar.name = 'DISSOLVER'
            cvar.description.append(
                'Removes ragdolls by dissolving them with various effects.')
            cvar.options.append('0 = Disabled')
            cvar.options.append('1 = No Effect')
            cvar.options.append('2 = Energy')
            cvar.options.append('3 = Heavy Electrical')
            cvar.options.append('4 = Light Electrical')
            cvar.options.append('5 = Core Effect')
            cvar.options.append('6 = Random Effect')
            cvar.default = 0
            cvar.text = 'Enables/Disables gg_dissolver.'
