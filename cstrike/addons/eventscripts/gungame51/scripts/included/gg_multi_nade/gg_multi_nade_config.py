# ../scripts/included/gg_multi_nade/gg_multi_nade_config.py

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

        # Create the gg_multi_nade instance
        with config.cfg_cvar('gg_multi_nade') as cvar:

            cvar.name = 'MULTIPLE GRENADES'
            cvar.description.append([
                'When a player reaches grenade level, ' +
                    'they are given another grenade',
                'when their thrown grenade detonates.',
                ])
            cvar.options.append('0 = (Disabled) Do not load gg_multi_nade.')
            cvar.options.append('1 = (Enabled) Load gg_multi_nade.')
            cvar.default = 0
            cvar.text = 'Enables/Disables gg_multi_nade.'

        # Create the gg_multi_nade_max_nades instance
        with config.cfg_cvar('gg_multi_nade_max_nades') as cvar:

            cvar.name = 'MAX GRENADES'
            cvar.description.append([
                'Defines the maximum number of grenades ' +
                    'that a player can be given during',
                'one life. (This includes the ' +
                    'hegrenade the player spawns with)'
                ])
            cvar.options.append(
                '0 = Unlimited - Always give the player another nade.')
            cvar.options.append(
                '# = Numerical limit - Only give up to # grenades.')
            cvar.default = 0
            cvar.text = ('The number of grenades a ' +
                'player on nade level gets per life.')
