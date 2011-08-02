# ../scripts/included/gg_spawn_protect/gg_spawn_protect_config.py

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

        # Create the gg_spawn_protect instance
        with config.cfg_cvar('gg_spawn_protect') as cvar:

            cvar.name = 'SPAWN PROTECTION'
            cvar.description.append([
                'The number of seconds to allow spawn ' +
                    'protection, in which they will be',
                'immune to other players fire but ' +
                    'cannot levelup if they kill a player.',
                ])
            cvar.options.append('0 = (Disabled) Do not load gg_spawn_protect.')
            cvar.options.append('# = Time (in seconds) ' +
                'for players to be spawn protected.')
            cvar.default = 0
            cvar.text = 'Enables/Disables spawn protection.'

        # Create the gg_spawn_protect_red instance
        with config.cfg_cvar('gg_spawn_protect_red') as cvar:

            cvar.name = 'SPAWN PROTECTION COLORS'
            cvar.description.append(
                "The player's color while under spawn protection.")
            cvar.notes.append([
                'Colors are set via the RGB (red/green/blue) ' +
                    'model. For more information',
                'on how to get the color you want, visit:',
                '\thttp://www.tayloredmktg.com/rgb/',
                ])
            cvar.notes.append([
                'Alpha is the transparency of the player. ' +
                    'The lower the number, the more',
                'transparent the player becomes.',
                ])
            cvar.options.append('0-255')
            cvar.default = 255
            cvar.default_text = [
                'Default Values:',
                '   * Red: 255',
                '   * Green: 255',
                '   * Blue: 255',
                '   * Alpha: 255',
                ]
            cvar.text = 'The red shade of the spawn protected player.'

        # Create the gg_spawn_protect_green instance
        with config.cfg_cvar('gg_spawn_protect_green') as cvar:

            cvar.name = ''
            cvar.default = 255
            cvar.default_text = ''
            cvar.text = 'The green shade of the spawn protected player.'

        # Create the gg_spawn_protect_blue instance
        with config.cfg_cvar('gg_spawn_protect_blue') as cvar:

            cvar.name = ''
            cvar.default = 255
            cvar.default_text = ''
            cvar.text = 'The blue shade of the spawn protected player.'

        # Create the gg_spawn_protect_alpha instance
        with config.cfg_cvar('gg_spawn_protect_alpha') as cvar:

            cvar.name = ''
            cvar.default = 150
            cvar.default_text = ''
            cvar.text = 'The alpha of the spawn protected player.'

        # Create the gg_spawn_protect_cancelonfire instance
        with config.cfg_cvar('gg_spawn_protect_cancelonfire') as cvar:

            cvar.name = 'SPAWN PROTECTION "CANCEL-ON-FIRE"'
            cvar.description.append([
                'Cancels the spawn protection timer ' +
                    'when the player fires their weapon',
                'and allows the player to level up.',
                ])
            cvar.notes.append(
                'Uses "eventscripts_noisy", which "may" cause lag.')
            cvar.options.append(
                '0 = (Disabled) Do not load gg_spawn_protect_cancelonfire.')
            cvar.options.append(
                '1 = (Enabled) Load gg_spawn_protect_cancelonfire.')
            cvar.default = 0
            cvar.text = 'Cancels spawn protection when the weapon is fired.'

        # Create the gg_spawn_protect_can_level_up instance
        with config.cfg_cvar('gg_spawn_protect_can_level_up') as cvar:

            cvar.name = 'ALLOW LEVELING WHILST PROTECTED'
            cvar.description.append(
                'Players can level up while spawn protected.')
            cvar.options.append('0 = (Disabled) Do not allow ' +
                'players to level up while spawn protected.')
            cvar.options.append('1 = (Enabled) Allow players ' +
                'to level up while spawn protected.')
            cvar.default = 0
            cvar.text = 'Allow players to level up while spawn protected'
