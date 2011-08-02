# ../core/cfg/files/gg_objectives_settings_config.py

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

    # Create the .cfg file
    with ConfigContextManager(path(__file__).namebase) as config:

        # Add the config file base attributes
        config.name = 'Objectives Configuration'
        config.description = 'This file controls GunGame51 objectives settings'

        # Create the gg_map_obj instance
        with config.cfg_cvar('gg_map_obj') as cvar:

            cvar.name = 'MAP OBJECTIVES'
            cvar.options.append('0 = No objectives disabled.')
            cvar.options.append('1 = All objectives disabled.')
            cvar.options.append('2 = Bomb objective disabled.')
            cvar.options.append('3 = Hostage objective disabled.')
            cvar.default = 0
            cvar.text = 'Controls which objectives will be disabled.'
            cvar.notify = True

        # Create the Bomb Defusal section
        config.cfg_section('BOMB DEFUSAL OBJECTIVE')

        # Create the gg_bomb_defused_levels instance
        with config.cfg_cvar('gg_bomb_defused_levels') as cvar:

            cvar.name = 'BOMB DEFUSED LEVELS'
            cvar.notes.append('Requires "gg_map_obj 0" or "gg_map_obj 3"')
            cvar.options.append('0 = Disabled.')
            cvar.options.append('# = The number of levels ' +
                'to reward a player for bomb defusal')
            cvar.default = 0
            cvar.text = 'Levels to reward a player for bomb defusal.'
            cvar.notify = True

        # Create the gg_bomb_defused_skip_knife instance
        with config.cfg_cvar('gg_bomb_defused_skip_knife') as cvar:

            cvar.name = 'BOMB DEFUSED LEVELING (KNIFE LEVEL)'
            cvar.notes.append('Requires "gg_map_obj 0" or "gg_map_obj 3"')
            cvar.notes.append('Requires "gg_bomb_defused_levels 1" or higher')
            cvar.options.append('0 = Do not allow players to ' +
                'level up if they defuse the bomb while on knife level.')
            cvar.options.append('1 = Allow players to level ' +
                'up if they defuse the bomb while on knife level.')
            cvar.default = 0
            cvar.text = ('Allow players to level ' +
                'up when they are on knife level.')

        # Create the gg_bomb_defused_skip_nade instance
        with config.cfg_cvar('gg_bomb_defused_skip_nade') as cvar:

            cvar.name = 'BOMB DEFUSED LEVELING (HEGRENADE LEVEL)'
            cvar.notes.append('Requires "gg_map_obj 0" or "gg_map_obj 3"')
            cvar.notes.append('Requires "gg_bomb_defused_levels 1" or higher')
            cvar.options.append('0 = Do not allow players to ' +
                'level up if they defuse the bomb while on hegrenade level.')
            cvar.options.append('1 = Allow players to level ' +
                'up if they defuse the bomb while on hegrenade level.')
            cvar.default = 0
            cvar.text = ('Allow players to level ' +
                'up when they are on HEGrenade level.')

        # Create the Bomb Explode section
        config.cfg_section('BOMB EXPLODE OBJECTIVE')

        # Create the gg_bomb_exploded_levels instance
        with config.cfg_cvar('gg_bomb_exploded_levels') as cvar:

            cvar.name = 'BOMB EXPLODED LEVELS'
            cvar.notes.append('Requires "gg_map_obj 0" or "gg_map_obj 3"')
            cvar.options.append('0 = Disabled.')
            cvar.options.append('# = The number of levels ' +
                'to reward a player for the bomb exploding')
            cvar.default = 0
            cvar.text = 'Levels to reward a player for bomb exploding.'
            cvar.notify = True

        # Create the gg_bomb_exploded_skip_knife instance
        with config.cfg_cvar('gg_bomb_exploded_skip_knife') as cvar:

            cvar.name = 'BOMB EXPLODED LEVELING (KNIFE LEVEL)'
            cvar.notes.append('Requires "gg_map_obj 0" or "gg_map_obj 3"')
            cvar.notes.append('Requires "gg_bomb_exploded_levels 1" or higher')
            cvar.options.append('0 = Do not allow players to ' +
                'level up if the bomb explodes while on knife level.')
            cvar.options.append('1 = Allow players to level ' +
                'up if the bomb explodes while on knife level.')
            cvar.default = 0
            cvar.text = ('Allow players to level ' +
                'up when they are on knife level.')

        # Create the gg_bomb_exploded_skip_nade instance
        with config.cfg_cvar('gg_bomb_exploded_skip_nade') as cvar:

            cvar.name = 'BOMB EXPLODED LEVELING (HEGRENADE LEVEL)'
            cvar.notes.append('Requires "gg_map_obj 0" or "gg_map_obj 3"')
            cvar.notes.append('Requires "gg_bomb_exploded_levels 1" or higher')
            cvar.options.append('0 = Do not allow players to ' +
                'level up if the bomb explodes while on hegrenade level.')
            cvar.options.append('1 = Allow players to level ' +
                'up if the bomb explodes while on hegrenade level.')
            cvar.default = 0
            cvar.text = ('Allow players to level ' +
                'up when they are on hegrenade level.')

        # Create the Hostage Rescue section
        config.cfg_section('HOSTAGE RESCUE OBJECTIVE')

        # Create the gg_hostage_rescued_levels instance
        with config.cfg_cvar('gg_hostage_rescued_levels') as cvar:

            cvar.name = 'HOSTAGE RESCUED LEVELS'
            cvar.notes.append('Requires "gg_map_obj 0" or "gg_map_obj 2"')
            cvar.options.append('0 = Disabled.')
            cvar.options.append('# = The number of levels ' +
                'to reward a player for rescuing hostages')
            cvar.default = 0
            cvar.text = 'Levels to reward a player for rescuing hostages.'
            cvar.notify = True

        # Create the gg_hostage_rescued_rescues instance
        with config.cfg_cvar('gg_hostage_rescued_rescues') as cvar:

            cvar.name = 'HOSTAGE RESCUED REQUIRED RESCUES'
            cvar.notes.append('Requires "gg_map_obj 0" or "gg_map_obj 2"')
            cvar.notes.append('Requires ' +
                '"gg_hostage_rescued_levels 1" or higher')
            cvar.options.append('# = The number of ' +
                'hostages a player must rescue to level up.')
            cvar.default = 0
            cvar.text = 'Number of hostages rescued required to level up.'

        # Create the gg_hostage_rescued_skip_knife instance
        with config.cfg_cvar('gg_hostage_rescued_skip_knife') as cvar:

            cvar.name = 'HOSTAGE RESCUED LEVELING (KNIFE LEVEL)'
            cvar.notes.append('Requires "gg_map_obj 0" or "gg_map_obj 2"')
            cvar.notes.append('Requires ' +
                '"gg_hostage_rescued_levels 1" or higher')
            cvar.options.append('0 = Do not allow players to level ' +
                'up when they rescue hostages while on knife level.')
            cvar.options.append('1 = Allow players to level ' +
                'up when they rescue hostages while on knife level.')
            cvar.default = 0
            cvar.text = ('Allow players to level ' +
                'up when they are on knife level.')

        # Create the gg_hostage_rescued_skip_nade instance
        with config.cfg_cvar('gg_hostage_rescued_skip_nade') as cvar:

            cvar.name = 'HOSTAGE RESCUED LEVELING (HEGRENADE LEVEL)'
            cvar.notes.append('Requires "gg_map_obj 0" or "gg_map_obj 2"')
            cvar.notes.append('Requires ' +
                '"gg_hostage_rescued_levels 1" or higher')
            cvar.options.append('0 = Do not allow players to level ' +
                'up when they rescue hostages while on hegrenade level.')
            cvar.options.append('1 = Allow players to level ' +
                'up when they rescue hostages while on hegrenade level.')
            cvar.default = 0
            cvar.text = ('Allow players to level ' +
                'up when they are on hegrenade level.')

        # Create the Hostage Stop section
        config.cfg_section('HOSTAGE STOP OBJECTIVE')

        # Create the gg_hostage_stopped_levels instance
        with config.cfg_cvar('gg_hostage_stopped_levels') as cvar:

            cvar.name = 'HOSTAGE STOPPED LEVELS'
            cvar.notes.append('Requires "gg_map_obj 0" or "gg_map_obj 2"')
            cvar.options.append('0 = Disabled.')
            cvar.options.append('# = The number of levels to reward ' +
                'a player for stopping others from rescuing hostages')
            cvar.default = 0
            cvar.text = ('Levels to reward a player for ' +
                'stopping other players from rescuing hostages.')
            cvar.notify = True

        # Create the gg_hostage_stopped_stops instance
        with config.cfg_cvar('gg_hostage_stopped_stops') as cvar:

            cvar.name = 'HOSTAGE STOPPED REQUIRED STOPS'
            cvar.notes.append('Requires "gg_map_obj 0" or "gg_map_obj 2"')
            cvar.notes.append('Requires ' +
                '"gg_hostage_stopped_levels 1" or higher')
            cvar.options.append('# = The number of hostages ' +
                'a player must stop from being rescued to level up.')
            cvar.default = 0
            cvar.text = 'Number of hostages stopped required to level up.'

        # Create the gg_hostage_stopped_skip_knife instance
        with config.cfg_cvar('gg_hostage_stopped_skip_knife') as cvar:

            cvar.name = 'HOSTAGE STOPPED LEVELING (KNIFE LEVEL)'
            cvar.notes.append('Requires "gg_map_obj 0" or "gg_map_obj 2"')
            cvar.notes.append('Requires ' +
                '"gg_hostage_stopped_levels 1" or higher')
            cvar.options.append('0 = Do not allow players to level up when ' +
                'they stop hostages from being rescued while on knife level.')
            cvar.options.append('1 = Allow players to level up when ' +
                'they stop hostages from being rescued while on knife level.')
            cvar.default = 0
            cvar.text = ('Allow players to level ' +
                'up when they are on knife level.')

        # Create the gg_hostage_stopped_skip_nade instance
        with config.cfg_cvar('gg_hostage_stopped_skip_nade') as cvar:

            cvar.name = 'HOSTAGE STOPPED LEVELING (HEGRENADE LEVEL)'
            cvar.notes.append('Requires "gg_map_obj 0" or "gg_map_obj 2"')
            cvar.notes.append('Requires ' +
                '"gg_hostage_stopped_levels 1" or higher')
            cvar.options.append([
                '0 = Do not allow players to level ' +
                'up when they stop hostages from ',
                'being rescued while on hegrenade level.',
                ])
            cvar.options.append([
                '1 = Allow players to level up when ' +
                'they stop hostages from being ',
                'rescued while on hegrenade level.',
                ])
            cvar.default = 0
            cvar.text = ('Allow players to level ' +
                'up when they are on hegrenade level.')
