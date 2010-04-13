# ../addons/eventscripts/gungame51/scripts/cfg/included/gg_warmup_round.py

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
    'gungame51/included_addon_configs/gg_stats_logging.cfg')
        
# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    generate_header(config)
    
    # Stats Logging
    config.text('')
    config.text('='*76)
    config.text('>> STATS LOGGING')
    config.text('='*76)
    config.text('Description:')
    config.text('   When enabled, this addon will log game events for stats ' +
                'tracking for')
    config.text('   HLstatsX, Psychostats, and etc.')
    config.text('Notes:')
    # Not quite sure what this is, but I don't think I like it...
    config.text('   * Other options available in "gg_stats_logging.txt".')
    config.text('   * This should be used with third-party stats programs.')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not load gg_stats_logging.')
    config.text('   1 = (Enabled) Load gg_stats_logging.')
    config.text('Default Value: 0')
    config.cvar('gg_stats_logging', 0, 'Enables/Disables ' +
                'stats logging for third-party programs.').addFlag('notify')
    
    config.write()
    es.dbgmsg(0, '\tgg_stats_logging.cfg')

def unload():
    global config

    # Remove the "notify" flags as set by addFlag('notify')
    for cvar in config.getCvars().keys():
        es.flags('remove', 'notify', cvar)
    
    # Delete the cfglib.AddonCFG instance
    del config