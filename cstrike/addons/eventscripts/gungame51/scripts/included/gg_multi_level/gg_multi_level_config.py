# ../scripts/included/gg_multi_level/gg_multi_level_config.py

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

        # Create the gg_multi_level instance
        with config.cfg_cvar('gg_multi_level') as cvar:

            cvar.name = 'MULTI-LEVEL'
            cvar.description.append([
                'The number of times a player has ' +
                    'to level up without dying prior to',
                'recieving the multi-level bonus:',
                ])
            cvar.extra.append('      * The attacker will be ' +
                'given a speed boost.')
            cvar.extra.append('      * The attacker will have ' +
                'sparks fly from their feet.')
            cvar.extra.append('      * The attacker will have ' +
                'music emitted from their location.')
            cvar.notes.append('Formally knows as Triple Level Bonus.')
            cvar.options.append('0 = (Disabled) Do not load gg_multi_level.')
            cvar.options.append([
                '# = (Enabled) The number of levels ' +
                    'a player must get before',
                'achieving the multi-level bonus.',
                ])
            cvar.default = 0
            cvar.text = ('The # of levels it takes ' +
                'to get the multi-level bonus.')

        # Create the gg_multi_level_speed instance
        with config.cfg_cvar('gg_multi_level_speed') as cvar:

            cvar.name = 'MULTI-LEVEL SPEED'
            cvar.description.append('The percentage of speed that ' +
                'players receieving the multi-level bonus will have.')
            cvar.options.append(
                "100 = (Disabled) Keep the player's speed unchanged.")
            cvar.options.append('# = (Enabled) The percentage ' +
                'of normal speed the player will have.')
            cvar.default = 150
            cvar.text = ('The percentage of gravity ' +
                'included with the multi-level bonus.')

        # Create the gg_multi_level_gravity instance
        with config.cfg_cvar('gg_multi_level_gravity') as cvar:

            cvar.name = 'MULTI-LEVEL GRAVITY'
            cvar.description.append('The percentage of gravity that ' +
                'players receieving the multi-level bonus will have.')
            cvar.options.append(
                "100 = (Disabled) Keep the player's gravity unchanged.")
            cvar.options.append('# = (Enabled) The percentage ' +
                'of normal gravity the player will have.')
            cvar.default = 100
            cvar.text = ('The percentage of gravity ' +
                'included with the multi-level bonus.')

        # Create the gg_multi_level_tk_reset instance
        with config.cfg_cvar('gg_multi_level_tk_reset') as cvar:

            cvar.name = 'MULTI-LEVEL TK VICTIM RESET'
            cvar.description.append('Victims of team killings ' +
                'will not have their level-up count reset.')
            cvar.options.append('0 = (Disabled) All players ' +
                'will have their level-up count reset when they die.')
            cvar.options.append('1 = (Enabled) Team kill victims ' +
                'not have their level-up count reset when they die.')
            cvar.default = 0
            cvar.text = 'Continue multi level count for TK victims.'
