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
    'gungame51/included_addon_configs/gg_dead_strip.cfg')
        
# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    generate_header(config)
    
    # Dead Strip
    config.text('')
    config.text('='*76)
    config.text('>> DEAD STRIP')
    config.text('='*76)
    config.text('Description:')
    config.text('   Removes a player\'s weapons when they die.')
    config.text('Note:')
    config.text('   * Prevents players from picking up the wrong weapon.')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not load gg_dead_strip.')
    config.text('   1 = (Enabled) Load gg_dead_strip.')
    config.text('Default Value: 0')
    config.cvar('gg_dead_strip', 0, 'Enables/Disables ' +
                'gg_dead_strip.')
    
    config.write()
    es.dbgmsg(0, '\tgg_dead_strip.cfg')

def unload():
    global config

    # Remove the "notify" flags as set by addFlag('notify')
    for cvar in config.getCvars().keys():
        es.flags('remove', 'notify', cvar)
    
    # Delete the cfglib.AddonCFG instance
    del config