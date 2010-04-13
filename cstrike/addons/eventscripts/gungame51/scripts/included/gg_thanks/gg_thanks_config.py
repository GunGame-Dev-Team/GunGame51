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
    'gungame51/included_addon_configs/gg_thanks.cfg')
        
# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    generate_header(config)
    
    # Thanks
    config.text('')
    config.text('='*76)
    config.text('>> THANKS')
    config.text('='*76)
    config.text('Description:')
    config.text('   Allows players to type !thanks to display a list of ' +
                'those involved with')
    config.text('   development and testing of GunGame.')
    config.text('Options:')
    config.text('   0 = Disabled')
    config.text('   1 = Enabled')
    config.text('Default Value: 1')
    config.cvar('gg_thanks', 1, 'Displays a list of those involved with ' +
                'development and testing of GunGame.').addFlag('notify')
    
    config.write()
    es.dbgmsg(0, '\tgg_thanks.cfg')

def unload():
    global config

    # Remove the "notify" flags as set by addFlag('notify')
    for cvar in config.getCvars().keys():
        es.flags('remove', 'notify', cvar)
    
    # Delete the cfglib.AddonCFG instance
    del config