# ../scripts/included/gg_knife_pro/gg_knife_pro_config.py

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

        # Create the gg_knife_pro instance
        with config.cfg_cvar('gg_knife_pro') as cvar:

            cvar.name = 'KNIFE PRO'
            cvar.description.append('When you kill a player with a knife, ' +
                'you will level up, and the victim will level down.')
            cvar.description.append(
                'The attacker will not steal a level if they are on ' +
                "hegrenade or knife level, or if the victim can't level down.")
            cvar.options.append('0 = (Disabled) Do not load gg_knife_pro.')
            cvar.options.append('1 = (Enabled) Load gg_knife_pro.')
            cvar.default = 0
            cvar.text = 'Enables/Disables gg_knife_pro.'

        # Create the gg_knife_pro_limit instance
        with config.cfg_cvar('gg_knife_pro_limit') as cvar:

            cvar.name = 'KNIFE PRO LIMIT'
            cvar.description.append('Limits level stealing to ' +
                'players close to your own level.')
            cvar.examples.append('If this is set to 3, you will not gain a ' +
                'level if you knife someone more than 3 levels below you.')
            cvar.options.append(
                '0 = (Disabled) Do not enable the knife pro limit.')
            cvar.options.append('# = (Enabled) Limit level ' +
                'stealing to this # of levels below the attacker.')
            cvar.default = 0
            cvar.text = ('Limit level stealing ' +
                'to this # of levels below the attacker.')

        # Create the gg_knife_pro_always_level instance
        with config.cfg_cvar('gg_knife_pro_always_level') as cvar:

            cvar.name = 'KNIFE PRO ALWAYS LEVEL'
            cvar.description.append('The attacker will always ' +
                'level up unless they are on hegrenade level.')
            cvar.description.append('The victim will always level down.')
            cvar.notes.append(
                'gg_knife_pro_limit still prevents leveling if enabled.')
            cvar.options.append(
                '0 = (Disabled) Conform to logical gg_knife_pro ruling')
            cvar.options.append('1 = (Enabled) Always affect levels with ' +
                'exception to the situations in the description above.')
            cvar.default = 0
            cvar.text = 'Enables/Disables always stealing levels.'

        # Create the gg_knife_pro_skip_nade instance
        with config.cfg_cvar('gg_knife_pro_skip_nade') as cvar:

            cvar.name = 'KNIFE PRO ALLOW SKIP NADE'
            cvar.description.append(
                'The attacker may skip grenade level with a knife kill.')
            cvar.notes.append(
                'gg_knife_pro_limit still prevents leveling if enabled.')
            cvar.options.append(
                '0 = (Disabled) Conform to logical gg_knife_pro ruling')
            cvar.options.append(
                '1 = (Enabled) Allow players to knife past nade level.')
            cvar.default = 0
            cvar.text = 'Enables/Disables always skipping nade.'
