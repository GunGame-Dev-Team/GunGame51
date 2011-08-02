# ../scripts/included/gg_elimination/gg_elimination_config.py

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

        # Create the gg_elimination instance
        with config.cfg_cvar('gg_elimination') as cvar:

            cvar.name = 'ELIMINATION'
            cvar.description.append('Respawn when your killer is killed.')
            cvar.notes.requires.append('gg_dead_strip')
            cvar.notes.requires.append('gg_dissolver')
            cvar.notes.conflict.append('gg_deathmatch')
            cvar.options.append('0 = (Disabled) Do not load gg_elimination.')
            cvar.options.append('1 = (Enabled) Load gg_elimination.')
            cvar.default = 0
            cvar.text = 'Enables/Disables gg_elimination.'

        # Create the gg_elimination_spawn instance
        with config.cfg_cvar('gg_elimination_spawn') as cvar:

            cvar.name = 'ELIMINATION SPAWN'
            cvar.description.append([
                "Allow players to spawn when they join, if they didn't ",
                'spawn already that round.',
                ])
            cvar.options.append('0 = (Disabled) Have ' +
                'players wait until the round ends to spawn.')
            cvar.options.append(
                '1 = (Enabled) Have players spawn when they join.')
            cvar.default = 0
            cvar.text = ('Have players spawn when they join ' +
                "if they haven't already for that round.")
