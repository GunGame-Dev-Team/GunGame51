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
    'gungame51/included_addon_configs/gg_knife_elite.cfg')
        
# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    generate_header(config)
    
    # Knife Elite
    config.text('')
    config.text('='*76)
    config.text('>> KNIFE ELITE')
    config.text('='*76)
    config.text('Description:')
    config.text('   Once a player levels up, they only get a knife until ' +
                'the next round.')
    config.text('Notes:')
    config.text('   * Will not load with "gg_turbo" enabled.')
    config.text('   * "gg_dead_strip" will automatically be enabled.')
    config.text('   * Will not load if "gg_dead_strip" can not be enabled.')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not load gg_knife_elite.')
    config.text('   1 = (Enabled) Load gg_knife_elite.')
    config.text('Default Value: 0')
    config.cvar('gg_knife_elite', 0, 'Enables/Disables ' +
                'gg_knife_elite.')
    
    config.write()
    es.dbgmsg(0, '\tgg_knife_elite.cfg')

def unload():
    global config

    # Remove the "notify" flags as set by addFlag('notify')
    for cvar in config.getCvars().keys():
        es.flags('remove', 'notify', cvar)
    
    # Delete the cfglib.AddonCFG instance
    del config