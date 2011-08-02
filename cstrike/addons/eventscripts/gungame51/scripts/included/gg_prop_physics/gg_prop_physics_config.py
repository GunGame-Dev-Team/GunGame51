# ../scripts/included/gg_prop_physics/gg_prop_physics_config.py

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

        # Create the gg_prop_physics instance
        with config.cfg_cvar('gg_prop_physics') as cvar:

            cvar.name = 'PROP PHYSICS'
            cvar.description.append(
                'Earn Levels/Multikills with prop_physics kills.')
            cvar.options.append('0 = (Disabled) Do not load gg_prop_physics.')
            cvar.options.append('1 = (Enabled) Load gg_prop_physics.')
            cvar.default = 0
            cvar.text = 'Enables/Disables gg_prop_physics.'

        # Create the gg_prop_physics_increment_nade instance
        with config.cfg_cvar('gg_prop_physics_increment_nade') as cvar:

            cvar.name = 'INCREMENT NADE'
            cvar.options.append(
                '0 = Do not increment or levelup on Nade level')
            cvar.options.append('1 = Increment or Levelup on Nade level')
            cvar.default = 0
            cvar.text = 'Increment or Levelup when on Nade level.'

        # Create the gg_prop_physics_increment_knife instance
        with config.cfg_cvar('gg_prop_physics_increment_knife') as cvar:

            cvar.name = 'INCREMENT KNIFE'
            cvar.options.append(
                '0 = Do not increment or levelup on Knife level')
            cvar.options.append('1 = Increment or Levelup on Knife level')
            cvar.default = 0
            cvar.text = 'Increment or Levelup when on Knife level.'
