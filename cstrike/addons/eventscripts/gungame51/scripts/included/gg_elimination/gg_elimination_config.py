# ../addons/eventscripts/gungame51/scripts/cfg/included/gg_elimination.py

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
    config.text('   * "gg_dissolver" will automatically be enabled.')
    config.text('   * Will not load if "gg_dissolver" can not be enabled.')
    config.text('   * Will not load with "gg_deathmatch" enabled.')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not load gg_elimination.')
    config.text('   1 = (Enabled) Load gg_elimination.')
    config.text('Default Value: 0')
    config.cvar('gg_elimination', 0, 'Enables/Disables ' +
                'gg_elimination.').addFlag('notify')

    # Elimination Spawn
    config.text('')
    config.text('='*76)
    config.text('>> ELIMINATION SPAWN')
    config.text('='*76)
    config.text('Description:')
    config.text('   Allow players to spawn when they join, if they didn\'t ')
    config.text('   spawn already that round.')
    config.text('Options:')
    config.text('   0 = (Disabled) Have players wait until the round ends ' +
                'to spawn.')
    config.text('   1 = (Enabled) Have players spawn when they join.')
    config.text('Default Value: 0')
    config.cvar('gg_elimination_spawn', 0, 'Have players spawn when they ' +
                'join if they haven\'t already for that round.')

    config.write()
    es.dbgmsg(0, '\tgg_elimination.cfg')

def unload():
    global config

    # Remove the "notify" flags as set by addFlag('notify')
    for cvar in config.getCvars().keys():
        es.flags('remove', 'notify', cvar)
    
    # Delete the cfglib.AddonCFG instance
    del config