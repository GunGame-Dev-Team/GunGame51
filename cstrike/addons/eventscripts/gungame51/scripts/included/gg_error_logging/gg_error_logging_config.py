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
    'gungame51/included_addon_configs/gg_error_logging.cfg')
        
# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    generate_header(config)
    
    # Error Logging
    config.text('='*76)
    config.text('>> ERROR LOGGING')
    config.text('='*76)
    config.text('Description:')
    config.text('   Logs all GunGame-related errors to a log file located in:')
    config.text('      "../<MOD>/addons/eventscripts/gungame51/logs/"')
    config.text('Notes:')
    config.text('   * If something in GunGame is not working and you are ' +
                'going to post a bug,')
    config.text('     make sure you enable this addon then post the ' +
                'error log when you are')
    config.text('     filling your bug report.')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not log errors.')
    config.text('   1 = (Enabled) Log errors.')
    config.text('Default Value: 1')
    config.cvar('gg_error_logging', 1, 'Logs all GunGame-related ' +
                'errors.').addFlag('notify')
    
    config.write()
    es.dbgmsg(0, '\tgg_error_logging.cfg')

def unload():
    global config

    # Remove the "notify" flags as set by addFlag('notify')
    for cvar in config.getCvars().keys():
        es.flags('remove', 'notify', cvar)
    
    # Delete the cfglib.AddonCFG instance
    del config