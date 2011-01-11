# ../scripts/included/gg_turbo/gg_turbo_config.py

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
    'gungame51/included_addon_configs/gg_turbo.cfg')


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    generate_header(config)

    # Turbo Mode
    config.text('')
    config.text('=' * 76)
    config.text('>> TURBO MODE')
    config.text('=' * 76)
    config.text('Description:')
    config.text('   Gives the player their next weapon immediately when they' +
                ' level up.')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not load gg_turbo.')
    config.text('   1 = (Enabled) Load gg_turbo.')
    config.text('Default Value: 0')
    config.cvar('gg_turbo', 0, 'Enables/Disables gg_turbo.').addFlag('notify')

    config.write()
    es.dbgmsg(0, '\tgg_turbo.cfg')


def unload():
    global config

    # Remove the "notify" flags as set by addFlag('notify')
    for cvar in config.getCvars().keys():
        es.flags('remove', 'notify', cvar)

    # Delete the cfglib.AddonCFG instance
    del config
