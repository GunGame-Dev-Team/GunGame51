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
    'gungame51/included_addon_configs/gg_reload.cfg')
        
# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    generate_header(config)
    
    # Reload
    config.text('')
    config.text('='*76)
    config.text('>> RELOAD')
    config.text('='*76)
    config.text('Description:')
    config.text('   When a player gains a level, the ammo in their clip is ' +
                'replenished.')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not load gg_reload.')
    config.text('   1 = (Enabled) Load gg_reload.')
    config.text('Default Value: 0')
    config.cvar('gg_reload', 0, 'Enables/Disables ' +
                'gg_reload.').addFlag('notify')
    
    config.write()
    es.dbgmsg(0, '\tgg_reload.cfg')

def unload():
    global config

    # Remove the "notify" flags as set by addFlag('notify')
    for cvar in config.getCvars().keys():
        es.flags('remove', 'notify', cvar)
    
    # Delete the cfglib.AddonCFG instance
    del config