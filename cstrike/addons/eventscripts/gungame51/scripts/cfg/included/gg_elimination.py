# ../addons/eventscripts/gungame/scripts/cfg/included/gg_elimination.py

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
    'gungame51/included_addon_configs/gg_elimination.cfg')
        
# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    generate_header(config)
    '''
    config.text('*'*76)
    config.text('*' +
                'gg_elimination.cfg -- Elimination Configuration'.center(74) +
                '*')
    config.text('*' + ' '*74 + '*')
    config.text('*' + 'This file defines GunGame Addon settings.'.center(74) +
                '*')
    config.text('*' + ' '*74 + '*')
    config.text('*' +
                'Note: Any alteration of this file requires a'.center(74) +
                '*')
    config.text('*' + 'server restart or a reload of GunGame.'.center(74) +
                '*')
    config.text('*'*76)
    config.text('')
    config.text('')
    '''
    # Elimination
    config.text('')
    config.text('='*76)
    config.text('>> ELIMINATION')
    config.text('='*76)
    config.text('Description:')
    config.text('   Respawn when your killer is killed.')
    config.text('Notes:')
    config.text('   * "gg_dead_strip" will automatically be enabled.')
    config.text('   * Will not load if "gg_dead_strip" can not be enabled.')
    config.text('   * "gg_turbo" will automatically be enabled.')
    config.text('   * Will not load if "gg_turbo" can not be enabled.')
    config.text('   * "gg_dissolver" will automatically be enabled.')
    config.text('   * Will not load if "gg_dissolver" can not be enabled.')
    config.text('   * Will not load with "gg_deathmatch" enabled.')
    config.text('   * Will not load with "gg_knife_elite" enabled.')
    config.text('   * Will not load with "gg_map_obj" enabled.')
    config.text('   * This addon requires usage of the "gg_respawn_cmd" ' +
                'found in the')
    config.text('     gg_en_config.cfg')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not load gg_elimination.')
    config.text('   1 = (Enabled) Load gg_elimination.')
    config.text('Default Value: 0')
    config.cvar('gg_elimination', 0, 'Enables/Disables ' +
                'gg_elimination.')

    config.write()
    es.dbgmsg(0, '\tgg_elimination.cfg')

def unload():
    global config

    # Remove the "notify" flags as set by addFlag('notify')
    for cvar in config.getCvars().keys():
        es.flags('remove', 'notify', cvar)
    
    # Delete the cfglib.AddonCFG instance
    del config