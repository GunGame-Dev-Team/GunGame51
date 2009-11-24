# ../addons/eventscripts/gungame/scripts/cfg/included/gg_warmup_round.py

'''
$Rev: 233 $
$LastChangedBy: micbarr $
$LastChangedDate: 2009-11-24 04:29:41 -0500 (Tue, 24 Nov 2009) $
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
    'gungame51/included_addon_configs/gg_earn_nade.cfg')
        
# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    generate_header(config)
    
    # Earn Grenade
    config.text('')
    config.text('='*76)
    config.text('>> EARN GRENADES')
    config.text('='*76)
    config.text('Description:')
    config.text('   When a player reaches grenade level, they can earn extra' +
                ' grenades by')
    config.text('   killing enemies with another weapon.')
    config.text('Note:')
    config.text('   * Players can only carry one hegrenade at a time.')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not load gg_earn_nade.')
    config.text('   1 = (Enabled) Load gg_earn_nade.')
    config.text('Default Value: 0')
    config.cvar('gg_earn_nade', 0, 'Enables/Disables ' +
                'gg_earn_nade.')
    
    config.write()
    es.dbgmsg(0, '\tgg_earn_nade.cfg')

def unload():
    global config

    # Remove the "notify" flags as set by addFlag('notify')
    for cvar in config.getCvars().keys():
        es.flags('remove', 'notify', cvar)
    
    # Delete the cfglib.AddonCFG instance
    del config