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
    'gungame51/included_addon_configs/gg_unl_grenade.cfg')
        
# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    generate_header(config)
    
    # Unlimited Grenades
    config.text('')
    config.text('='*76)
    config.text('>> UNLIMITED GRENADES')
    config.text('='*76)
    config.text('Description:')
    config.text('   When a player reaches grenade level, they are given ' +
                'another grenade when')
    config.text('   their thrown grenade detonates.')
    config.text('Note:')
    config.text('   * Will not load with "gg_earn_nades" enabled.')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not load gg_unl_grenade.')
    config.text('   1 = (Enabled) Load gg_unl_grenade.')
    config.text('Default Value: 0')
    config.cvar('gg_unl_grenade', 0, 'Enables/Disables ' +
                'gg_unl_grenade.')
    
    config.write()
    es.dbgmsg(0, '\tgg_unl_grenade.cfg')

def unload():
    global config

    # Remove the "notify" flags as set by addFlag('notify')
    for cvar in config.getCvars().keys():
        es.flags('remove', 'notify', cvar)
    
    # Delete the cfglib.AddonCFG instance
    del config