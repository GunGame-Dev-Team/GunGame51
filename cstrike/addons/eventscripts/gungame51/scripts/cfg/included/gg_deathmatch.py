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

# GunGame Imports
from gungame51.core.cfg import generate_header

# ============================================================================
# >> GLOBAL VARIABLES
# ============================================================================
config = cfglib.AddonCFG('%s/cfg/' %es.ServerVar('eventscripts_gamedir') +
    'gungame51/included_addon_configs/gg_deathmatch.cfg')
        
# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    generate_header(config)
    
    # Deathmatch
    config.text('')
    config.text('='*76)
    config.text('>> DEATHMATCH')
    config.text('='*76)
    config.text('Description:')
    config.text('   Emulates a team-deathmatch mode, and players will ' +
                'respawn when they die.')
    config.text('Notes:')
    config.text('   * "gg_dead_strip" will automatically be enabled.')
    config.text('   * Will not load if "gg_dead_strip" can not be enabled.')
    config.text('   * "gg_turbo" will automatically be enabled.')
    config.text('   * Will not load if "gg_turbo" can not be enabled.')
    config.text('   * "gg_dissolver" will automatically be enabled.')
    config.text('   * Will not load if "gg_dissolver" can not be enabled.')
    config.text('   * Will not load with "gg_map_obj" enabled.')
    config.text('   * Will not load with "gg_knife_elite" enabled.')
    config.text('   * Will not load with "gg_elimination" enabled.')
    config.text('   * This addon requires usage of the "gg_respawn_cmd" ' +
                'found in the')
    config.text('     gg_en_config.cfg')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not load gg_deathmatch.')
    config.text('   1 = (Enabled) Load gg_deathmatch.')
    config.text('Default Value: 0')
    config.cvar('gg_deathmatch', 0, 'Enables/Disables ' +
                'gg_deathmatch.')

    # Deathmatch Respawn Delay
    config.text('')
    config.text('='*76)
    config.text('>> DEATHMATCH RESPAWN DELAY')
    config.text('='*76)
    config.text('Description:')
    config.text('   The amount of time (in seconds) to wait before ' +
                'respawning a player after')
    config.text('   they die.')
    config.text('Notes:')
    config.text('   * The respawn delay must be greater than 0.')
    config.text('   * You can use 0.1 for a nearly immediate respawn time.')
    config.text('   * If set to 0 or less, the delay will be set to 0.1.')
    config.text('Options:')
    config.text('   # = Time (in seconds) to wait before respawning a player.')
    config.text('Default Value: 2')
    config.cvar('gg_dm_respawn_delay', 2, 'Seconds to wait before respawning' +
                ' a player after death.')

    config.write()
    es.dbgmsg(0, '\tgg_deathmatch.cfg')

def unload():
    global config

    # Remove the "notify" flags as set by addFlag('notify')
    for cvar in config.getCvars().keys():
        es.flags('remove', 'notify', cvar)
    
    # Delete the cfglib.AddonCFG instance
    del config