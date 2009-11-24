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
    'gungame51/included_addon_configs/gg_friendlyfire.cfg')
        
# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    generate_header(config)
    
    # Friendly Fire
    config.text('')
    config.text('='*76)
    config.text('>> FRIENDLY FIRE')
    config.text('='*76)
    config.text('Description:')
    config.text('   Automatically turn on friendly fire when a player ' +
                'reaches "x" levels')
    config.text('   below the last level (+1).')
    config.text('Examples:')
    config.text('   * gg_friendlyfire 1')
    config.text('       - The above will turn on friendly fire when a player' +
                ' reaches the last')
    config.text('         level.')
    config.text('   * gg_friendlyfire 2')
    config.text('        - The above will turn on friendly fire when a ' +
                'player reaches one')
    config.text('          level before the last.')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not load gg_friendlyfire.')
    config.text('   # = (Enabled) Turn on friendly fire when a player ' +
                'reaches "#" (+1) levels')
    config.text('                 below the last level.')
    config.text('Default Value: 0')
    config.cvar('gg_friendlyfire', 0, 'The number (+1) of levels below the ' +
                'last level to enable friendly fire.')
    
    config.write()
    es.dbgmsg(0, '\tgg_friendlyfire.cfg')

def unload():
    global config

    # Remove the "notify" flags as set by addFlag('notify')
    for cvar in config.getCvars().keys():
        es.flags('remove', 'notify', cvar)
    
    # Delete the cfglib.AddonCFG instance
    del config