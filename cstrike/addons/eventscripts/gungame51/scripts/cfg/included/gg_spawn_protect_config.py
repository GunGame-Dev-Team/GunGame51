# ../addons/eventscripts/gungame/scripts/cfg/included/gg_spawn_protect.py

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
    'gungame51/included_addon_configs/gg_spawn_protect.cfg')
        
# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    generate_header(config)

    # Spawn Protection
    config.text('')
    config.text('='*76)
    config.text('>> SPAWN PROTECTION')
    config.text('='*76)
    config.text('Description:')
    config.text('   The number of seconds to allow spawn protection, in ' +
                'which they will be')
    config.text('   immune to other players fire but cannot levelup if they ' +
                'kill a player.')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not load gg_spawn_protect.')
    config.text('   # = Time (in seconds) for players to be spawn protected.')
    config.text('Default Value: 0')
    config.cvar('gg_spawn_protect', 0, 'Enables/Disables spawn ' +
                'protection.')
    config.text('')

    # Spawn Protection Colors
    config.text('')
    config.text('='*76)
    config.text('>> SPAWN PROTECTION COLORS')
    config.text('='*76)
    config.text('Description:')
    config.text('   The player\'s color while under spawn protection.')
    config.text('Notes:')
    config.text('   * Colors are set via the RGB (red/green/blue) model. ' +
                'For more information ')
    config.text('     on how to get the color you want, visit:')
    config.text('        http://www.tayloredmktg.com/rgb/')
    config.text('   * Alpha is the transparency of the player. The lower ' +
                'the number, the more')
    config.text('     transparent the player becomes.')
    config.text('Options:')
    config.text('   0-255')
    config.text('Default Values:')
    config.text('   * Red: 255')
    config.text('   * Green: 255')
    config.text('   * Blue: 255')
    config.text('   * Alpha: 150')
    config.cvar('gg_spawn_protect_red', 255, 'The red shade of the spawn ' +
                'protected player.')
    config.cvar('gg_spawn_protect_green', 255, 'The green shade of the spawn' +
                ' protected player.')
    config.cvar('gg_spawn_protect_blue', 255, 'The blue shade of the spawn ' +
                'protected player.')
    config.cvar('gg_spawn_protect_alpha', 150, 'The alpha of the spawn ' +
                'protected player.')
    config.text('')

    # Spawn Protection "Cancel On Fire"
    config.text('')
    config.text('='*76)
    config.text('>> SPAWN PROTECTION "CANCEL-ON-FIRE"')
    config.text('='*76)
    config.text('Description:')
    config.text('   Cancels the spawn protection timer when the player ' +
                'fires their weapon and')
    config.text('   allows the player to level up.')
    config.text('Note:')
    config.text('   * Uses "eventscripts_noisy", which "may" cause lag.')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not load gg_spawn_protect_cancelonfire.')
    config.text('   1 = (Enabled) Load gg_spawn_protect_cancelonfire.')
    config.text('Default Value: 0')
    config.cvar('gg_spawn_protect_cancelonfire', 0, 'Cancels spawn ' +
                'protection when the weapon is fired.')
    config.text('')

    # Allow Leveling Whilst Protected
    config.text('')
    config.text('='*76)
    config.text('>> ALLOW LEVELING WHILST PROTECTED')
    config.text('='*76)
    config.text('Description:')
    config.text('   Players can level up while spawn protected.')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not allow players to level up while ' +
                'spawn protected.')
    config.text('   1 = (Enabled) Allow players to level up while spawn ' +
                'protected.')
    config.text('Default Value: 0')
    config.cvar('gg_spawn_protect_can_level_up', 1, 'Allow players ' +
                'to level up while spawn protected')
    
    config.write()
    es.dbgmsg(0, '\tgg_spawn_protect.cfg')

def unload():
    global config

    # Remove the "notify" flags as set by addFlag('notify')
    for cvar in config.getCvars().keys():
        es.flags('remove', 'notify', cvar)
    
    # Delete the cfglib.AddonCFG instance
    del config