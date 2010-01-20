# ../addons/eventscripts/gungame/scripts/cfg/included/gg_warmup_round.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
# EventScripts Imports
import es
import cfglib

# GunGame Imports
from gungame51.core.cfg import generate_header

# ============================================================================
# >> GLOBAL VARIABLES
# ============================================================================
config = cfglib.AddonCFG('%s/cfg/' %es.ServerVar('eventscripts_gamedir') +
    'gungame51/included_addon_configs/gg_spawnpoints.cfg')
        
# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    generate_header(config)
    
    # Spawnpoint Manager
    config.text('')
    config.text('='*76)
    config.text('>> SPAWNPOINT MANAGER')
    config.text('='*76)
    config.text('Description:')
    config.text('   This addon adds commands and a menu to allow admins to')
    config.text('   manage spawnpoints on the current map.')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not load gg_spawnpoints.')
    config.text('   1 = (Enabled) Load gg_spawnpoints.')
    config.text('Default Value: 0')
    config.cvar('gg_spawnpoints', 0, 'Spawn point ' +
        'management.').addFlag('notify')
    
    config.write()
    es.dbgmsg(0, '\tgg_spawnpoints.cfg')

def unload():
    global config

    # Remove the "notify" flags as set by addFlag('notify')
    for cvar in config.getCvars().keys():
        es.flags('remove', 'notify', cvar)
    
    # Delete the cfglib.AddonCFG instance
    del config