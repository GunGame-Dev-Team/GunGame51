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
    'gungame51/included_addon_configs/gg_dissolver.cfg')
        
# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    generate_header(config)
    
    # Dissolver
    config.text('')
    config.text('='*76)
    config.text('>> DISSOLVER')
    config.text('='*76)
    config.text('Description:')
    config.text('   Removes ragdolls by dissolving them with various effects.')
    config.text('Options:')
    config.text('   0 = Disabled')
    config.text('   1 = No Effect')
    config.text('   2 = Energy')
    config.text('   3 = Heavy Electrical')
    config.text('   4 = Light Electrical')
    config.text('   5 = Core Effect')
    config.text('   6 = Random Effect')
    config.text('Default Value: 0')
    config.cvar('gg_dissolver', 0, 'Enables/Disables ' +
                'gg_dissolver.')
    
    config.write()
    es.dbgmsg(0, '\tgg_dissolver.cfg')

def unload():
    global config

    # Remove the "notify" flags as set by addFlag('notify')
    for cvar in config.getCvars().keys():
        es.flags('remove', 'notify', cvar)
    
    # Delete the cfglib.AddonCFG instance
    del config