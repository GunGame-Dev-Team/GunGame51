# ../scripts/included/gg_random_spawn/gg_random_spawn_config.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# EventScripts Imports
import es
import cfglib

# GunGame Imports
from gungame51.core.cfg import generate_header

# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
config = cfglib.AddonCFG('%s/cfg/' % es.ServerVar('eventscripts_gamedir') +
    'gungame51/included_addon_configs/gg_random_spawn.cfg')


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    generate_header(config)

    # Random Spawnpoints
    config.text('')
    config.text('=' * 76)
    config.text('>> RANDOM SPAWNPOINTS')
    config.text('=' * 76)
    config.text('Description:')
    config.text('   Loads random spawnpoints if a spawnpoint file for the ' +
                'current map has')
    config.text('    been created.')
    config.text('Note:')
    config.text('   Create spawnpoint files with the gg_spawnpoints ' +
                'included addon.')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not load gg_random_spawn.')
    config.text('   1 = (Enabled) Load gg_random_spawn.')
    config.text('Default Value: 0')
    config.cvar('gg_random_spawn', 0, 'Enables/Disables random spawn ' +
        'points').addFlag('notify')

    config.write()
    es.dbgmsg(0, '\tgg_random_spawn.cfg')


def unload():
    global config

    # Remove the "notify" flags as set by addFlag('notify')
    for cvar in config.getCvars().keys():
        es.flags('remove', 'notify', cvar)

    # Delete the cfglib.AddonCFG instance
    del config
