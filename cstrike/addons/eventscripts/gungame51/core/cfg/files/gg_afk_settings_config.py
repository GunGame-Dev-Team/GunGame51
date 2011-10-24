# ../core/cfg/files/gg_afk_settings_config.py

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

    # Create the .cfg file
    with ConfigContextManager(
      path(__file__).namebase.replace('_config', '')) as config:

        # Add the config file base attributes
        config.name = 'AFK Configuration'
        config.description = 'This file controls GunGame AFK settings.'

        # Create the gg_allow_afk_levels instance
        with config.cfg_cvar('gg_allow_afk_levels') as cvar:

            cvar.name = 'AFK LEVELING'
            cvar.options.append(
                '0 = Do not allow attackers to level up with AFK kills.')
            cvar.options.append(
                '1 = Allow attackers to level up with AFK kills.')
            cvar.default = 0
            cvar.text = 'Allow attackers to level up with AFK kills.'

        # Create the gg_allow_afk_levels_knife instance
        with config.cfg_cvar('gg_allow_afk_levels_knife') as cvar:

            cvar.name = 'AFK LEVELING (KNIFE LEVEL)'
            cvar.notes.append('Requires "gg_allow_afk_levels 1"')
            cvar.options.append('0 = Do not allow attackers ' +
                'to level up with AFK kills when on knife level.')
            cvar.options.append('1 = Allow attackers ' +
                'to level up with AFK kills when on knife level.')
            cvar.default = 0
            cvar.text = ('Allow attackers to ' +
                'level up with AFK kills when on knife level.')

        # Create the gg_allow_afk_levels_nade instance
        with config.cfg_cvar('gg_allow_afk_levels_nade') as cvar:

            cvar.name = 'AFK LEVELING (HEGRENADE LEVEL)'
            cvar.notes.append('Requires "gg_allow_afk_levels 1"')
            cvar.options.append('0 = Do not allow attackers ' +
                'to level up with AFK kills when on HeGrenade level.')
            cvar.options.append('1 = Allow attackers to ' +
                'level up with AFK kills when on HeGrenade level.')
            cvar.default = 0
            cvar.text = ('Allow attackers to level ' +
                'up with AFK kills when on HEGrenade level.')
