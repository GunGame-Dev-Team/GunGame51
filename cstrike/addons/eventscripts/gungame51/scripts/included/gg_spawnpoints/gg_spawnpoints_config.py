# ../scripts/included/gg_spawnpoints/gg_spawnpoints_config.py

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

        # Create the gg_spawnpoints instance
        with config.cfg_cvar('gg_spawnpoints') as cvar:

            cvar.name = 'SPAWNPOINT MANAGER'
            cvar.description.append('This addon adds server (RCON) commands ' +
                'to allow admins to manage spawnpoints on the current map.')
            cvar.extra.append('Commands:')
            cvar.extra.append(' spawn_add <userid>')
            cvar.extra.append('   - Adds a spawnpoint at the users location.')
            cvar.extra.append(' spawn_remove <userid>')
            cvar.extra.append('   - Remove the spawnpoint ' +
                'closest to the userid passed after the command.')
            cvar.extra.append(' spawn_remove_all')
            cvar.extra.append('   - Removes all spawn points.')
            cvar.extra.append(' spawn_print')
            cvar.extra.append(
                '   - Prints spawnpoints into the server console.')
            cvar.extra.append(' spawn_show')
            cvar.extra.append('   - Toggles spawn point models on and off.')
            cvar.options.append('0 = (Disabled) Do not load gg_spawnpoints.')
            cvar.options.append('1 = (Enabled) Load gg_spawnpoints.')
            cvar.default = 0
            cvar.text = 'Spawn point management.'
