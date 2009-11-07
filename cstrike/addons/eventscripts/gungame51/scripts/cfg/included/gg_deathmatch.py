# ../addons/eventscripts/gungame/scripts/cfg/included/gg_deathmatch.py

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

# ============================================================================
# >> GLOBAL VARIABLES
# ============================================================================
config = cfglib.AddonCFG('%s/cfg/' %es.ServerVar('eventscripts_gamedir') +
    'gungame51/included_addon_configs/gg_deathmatch.cfg')
        
# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    config.text('*'*76)
    config.text('*' + ' '*14 + 'gg_deathmatch.cfg -- Death Match ' +
                'Configuration' + ' '*14 + '*')
    config.text('*' + ' '*74 + '*')
    config.text('*' + ' '*17 + 'This file defines GunGame Addon settings.' +
                ' '*16 + '*')
    config.text('*' + ' '*74 + '*')
    config.text('*  Note: Any alteration of this file requires a server ' +
                'restart or a' + ' '*8 + '*')
    config.text('*' + ' '*11 + 'reload of GunGame.' + ' '*45 + '*')
    config.text('*'*76)
    config.text('')
    config.text('')
    
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
    es.dbgmsg(0, '\tgg_deathmatch.cfg')

def unload():
    global config

    # Remove the "notify" flags as set by addFlag('notify')
    for cvar in config.getCvars().keys():
        es.flags('remove', 'notify', cvar)
    
    # Delete the cfglib.AddonCFG instance
    del config