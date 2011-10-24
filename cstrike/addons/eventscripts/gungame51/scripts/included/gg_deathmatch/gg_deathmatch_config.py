# ../scripts/included/gg_deathmatch/gg_deathmatch_config.py

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

        # Create the gg_deathmatch instance
        with config.cfg_cvar('gg_deathmatch') as cvar:

            cvar.name = 'DEATHMATCH'
            cvar.description.append('Emulates a team-deathmatch mode, ' +
                'and players will respawn when they die.')
            cvar.notes.requires.append('gg_dead_strip')
            cvar.notes.requires.append('gg_dissolver')
            cvar.notes.conflict.append('gg_elimination')
            cvar.options.append('0 = (Disabled) Do not load gg_deathmatch.')
            cvar.options.append('1 = (Enabled) Load gg_deathmatch.')
            cvar.default = 0
            cvar.text = 'Enables/Disables gg_deathmatch.'

        # Create the gg_dm_respawn_delay instance
        with config.cfg_cvar('gg_dm_respawn_delay') as cvar:

            cvar.name = 'DEATHMATCH RESPAWN DELAY'
            cvar.description.append('The amount of time (in seconds)' +
                ' to wait before respawning a player after they die')
            cvar.notes.append('The respawn delay must be greater than 0.')
            cvar.notes.append(
                'You can use 0.1 for a nearly immediate respawn time')
            cvar.notes.append(
                'If set to 0 or less, the delay will be set to 0.1.')
            cvar.options.append(
                '# = Time (in seconds) to wait before respawning a player.')
            cvar.default = 2
            cvar.text = (
                'Seconds to wait before respawning a player after death.')
