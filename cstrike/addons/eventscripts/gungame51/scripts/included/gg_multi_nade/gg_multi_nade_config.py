# ../addons/eventscripts/gungame/scripts/cfg/included/gg_multi_nade_config.py

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
    'gungame51/included_addon_configs/gg_multi_nade.cfg')
        
# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    generate_header(config)
    
    # Multiple Grenades
    config.text('')
    config.text('='*76)
    config.text('>> MULTIPLE GRENADES')
    config.text('='*76)
    config.text('Description:')
    config.text('   When a player reaches grenade level, they are given ' +
                'another grenade when')
    config.text('   their thrown grenade detonates.')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not load gg_multi_nade.')
    config.text('   1 = (Enabled) Load gg_multi_nade.')
    config.text('Default Value: 0')
    config.cvar('gg_multi_nade', 0, 'Enables/Disables ' +
                'gg_multi_nade.').addFlag('notify')
    
    # Max Grenades
    config.text('')
    config.text('='*76)
    config.text('>> MAX GRENADES')
    config.text('='*76)
    config.text('Description:')
    config.text('   Defines the maximum number of grenades that a player ' +
                'can be given during')
    config.text('   one life. (This includes the hegrenade the player ' +
                'spawns with)')
    config.text('Options:')
    config.text('   0 = Unlimited - Always give the player another nade.')
    config.text('   # = Numerical limit - Only give up to # grenades.')
    config.text('Default Value: 0')
    config.cvar('gg_multi_nade_max_nades', 0, 'The number of ' +
                'grenades a player on nade level gets per life.')

    config.write()
    es.dbgmsg(0, '\tgg_multi_nade.cfg')

def unload():
    global config

    # Remove the "notify" flags as set by addFlag('notify')
    for cvar in config.getCvars().keys():
        es.flags('remove', 'notify', cvar)
    
    # Delete the cfglib.AddonCFG instance
    del config
