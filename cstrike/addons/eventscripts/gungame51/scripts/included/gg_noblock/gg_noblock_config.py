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
    'gungame51/included_addon_configs/gg_noblock.cfg')
        
# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    generate_header(config)
    
    # No Block
    config.text('')
    config.text('='*76)
    config.text('>> NO BLOCK')
    config.text('='*76)
    config.text('Description:')
    config.text('   Makes it possible to pass through all players.')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not load gg_noblock.')
    config.text('   1 = (Enabled) Load gg_noblock.')
    config.text('Default Value: 0')
    config.cvar('gg_noblock', 0, 'Enables/Disables ' +
                'gg_noblock.')
    
    config.write()
    es.dbgmsg(0, '\tgg_noblock.cfg')

def unload():
    global config

    # Remove the "notify" flags as set by addFlag('notify')
    for cvar in config.getCvars().keys():
        es.flags('remove', 'notify', cvar)
    
    # Delete the cfglib.AddonCFG instance
    del config