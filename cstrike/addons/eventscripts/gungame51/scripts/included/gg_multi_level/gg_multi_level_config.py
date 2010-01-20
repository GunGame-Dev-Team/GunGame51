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
    'gungame51/included_addon_configs/gg_multi_level.cfg')
        
# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    generate_header(config)
    
    # Multi-Level
    config.text('')
    config.text('='*76)
    config.text('>> MULTI-LEVEL')
    config.text('='*76)
    config.text('Description:')
    config.text('   The number of times a player has to level up without ' +
                'dying prior to')
    config.text('   recieving the multi-level bonus:')
    config.text('      * The attacker will be given a speed boost.')
    config.text('      * The attacker will have sparks fly from their feet.')
    config.text('      * The attacker will have music emitted from their ' +
                'location.')
    config.text('Note:')
    config.text('   * Formally knows as Triple Level Bonus.')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not load gg_multi_level.')
    config.text('   # = (Enabled) The number of levels a player must get ' +
                'before achieving the')
    config.text('                 multi-level bonus.')
    config.text('Default Value: 0')
    config.cvar('gg_multi_level', 0, 'The # of levels it takes to get the ' +
                'multi-level bonus.')

    # Multi-Level Gravity
    config.text('')
    config.text('='*76)
    config.text('>> MULTI-LEVEL GRAVITY')
    config.text('='*76)
    config.text('Description:')
    config.text('   The percentage of gravity that players receieving the ' +
                'multi-level bonus')
    config.text('   will have.')
    config.text('Options:')
    config.text('   100 = (Disabled) Keep the player\'s gravity unchanged.')
    config.text('   # = (Enabled) The percentage of normal gravity the ' +
                'player')
    config.text('                 will have.')
    config.text('Default Value: 100')
    config.cvar('gg_multi_level_gravity', 100, 'The percentage of gravity ' +
                'included with the multi-level bonus.')

    # Multi-Level TK Victim Reset
    config.text('')
    config.text('='*76)
    config.text('>> MULTI-LEVEL TK VICTIM RESET')
    config.text('='*76)
    config.text('Description:')
    config.text('   Victims of team killings will not have their level-up ' +
                'count reset.')
    config.text('Options:')
    config.text('   0 = (Disabled) All players will have their level-up ' +
                'count reset')
    config.text('                  when they die.')
    config.text('   1 = (Enabled) Team kill victims not have their level-up ' +
                'count reset')
    config.text('when they die.')
    config.text('Default Value: 0')
    config.cvar('gg_multi_level_tk_reset', 0, 'Continue multi level count ' +
                'for TK victims.')   
    
    config.write()
    es.dbgmsg(0, '\tgg_multi_level.cfg')

def unload():
    global config

    # Remove the "notify" flags as set by addFlag('notify')
    for cvar in config.getCvars().keys():
        es.flags('remove', 'notify', cvar)
    
    # Delete the cfglib.AddonCFG instance
    del config