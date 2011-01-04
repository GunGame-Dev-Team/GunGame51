# ../addons/eventscripts/gungame51/core/cfg/files/gg_objectives_settings_config.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# EventScripts Imports
import es
import cfglib

# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
config = cfglib.AddonCFG('%s/cfg/gungame51/gg_objectives_settings.cfg'
        %es.ServerVar('eventscripts_gamedir'))
        
# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    config.text('*'*76)
    config.text('*' + ' '*24 + 'gg_objectives_settings.cfg' + ' '*24 + '*')
    config.text('*' + ' '*74 + '*')
    config.text('*' + ' '*14 + 'This file controls GunGame objectives ' +
                'settings.' + ' '*13 + '*')
    config.text('*' + ' '*74 + '*')
    config.text('*  Note: Any alteration of this file requires a server ' +
                'restart or a' + ' '*8 + '*')
    config.text('*' + ' '*11 + 'reload of GunGame.' + ' '*45 + '*')
    config.text('*'*76)
    config.text('')
    config.text('')

    # Map Objectives
    config.text('='*76)
    config.text('>> MAP OBJECTIVES')
    config.text('='*76)
    config.text('Options:')
    config.text('   0 = No objectives disabled.')
    config.text('   1 = All objectives disabled.')
    config.text('   2 = Bomb objective disabled.')
    config.text('   3 = Hostage objective disabled.')
    config.text('Default Value: 0')
    config.cvar('gg_map_obj', 0, 'Controls which objectives will be ' +
        'disabled.').addFlag('notify')

    # Bomb Defused Leveling
    config.text('')
    config.text('='*76)
    config.text('>> BOMB DEFUSED LEVELS')
    config.text('='*76)
    config.text('Notes:')
    config.text('   * Requires "gg_map_obj 0" or "gg_map_obj 3"')
    config.text('Options:')
    config.text('   0 = Disabled.')
    config.text('   # = The number of levels to reward a player for bomb ' +
                'defusal')
    config.text('Default Value: 0')
    config.cvar('gg_bomb_defused_levels', 0, 'Levels to reward a player for ' +
                'bomb defusal.').addFlag('notify')

    # Bomb Defused Leveling Knife
    config.text('')
    config.text('='*76)
    config.text('>> BOMB DEFUSED LEVELING (KNIFE LEVEL)')
    config.text('='*76)
    config.text('Notes:')
    config.text('   * Requires "gg_map_obj 0" or "gg_map_obj 3"')
    config.text('   * Requires "gg_bomb_defused_levels 1" or higher')
    config.text('Options:')
    config.text('   0 = Do not allow players to level up if they defuse the ' +
                'bomb while on knife level.')
    config.text('   1 = Allow players to level up if they defuse the bomb ' +
                'while on knife level.')
    config.text('Default Value: 0')
    config.cvar('gg_bomb_defused_skip_knife', 0, 'Allow players to level up ' +
                'when they are on knife level.')

    # Bomb Defused Leveling HEGrenade
    config.text('')
    config.text('='*76)
    config.text('>> BOMB DEFUSED LEVELING (HEGRENADE LEVEL)')
    config.text('='*76)
    config.text('Notes:')
    config.text('   * Requires "gg_map_obj 0" or "gg_map_obj 3"')
    config.text('   * Requires "gg_bomb_defused_levels 1" or higher')
    config.text('Options:')
    config.text('   0 = Do not allow players to level up if they defuse the ' +
                'bomb while on HEGrenade level.')
    config.text('   1 = Allow players to level up if they defuse the bomb ' +
                'while on HEGrenade level.')
    config.text('Default Value: 0')
    config.cvar('gg_bomb_defused_skip_nade', 0, 'Allow players to level up ' +
                'when they are on HEGrenade level.')

    # Bomb Exploded Leveling
    config.text('')
    config.text('='*76)
    config.text('>> BOMB EXPLODED LEVELS')
    config.text('='*76)
    config.text('Notes:')
    config.text('   * Requires "gg_map_obj 0" or "gg_map_obj 3"')
    config.text('Options:')
    config.text('   0 = Disabled.')
    config.text('   # = The number of levels to reward a player for the ' +
                'bomb exploding')
    config.text('Default Value: 0')
    config.cvar('gg_bomb_exploded_levels', 0, 'Levels to reward a player ' +
                'for bomb exploding.').addFlag('notify')

    # Bomb Exploded Leveling Knife
    config.text('')
    config.text('='*76)
    config.text('>> BOMB EXPLODED LEVELING (KNIFE LEVEL)')
    config.text('='*76)
    config.text('Notes:')
    config.text('   * Requires "gg_map_obj 0" or "gg_map_obj 3"')
    config.text('   * Requires "gg_bomb_exploded_levels 1" or higher')
    config.text('Options:')
    config.text('   0 = Do not allow players to level up if the bomb ' +
                'explodes while on knife level.')
    config.text('   1 = Allow players to level up if the bomb explodes ' +
                'while on knife level.')
    config.text('Default Value: 0')
    config.cvar('gg_bomb_exploded_skip_knife', 0, 'Allow players to level ' +
                'up when they are on knife level.')

    # Bomb Exploded Leveling HEGrenade
    config.text('')
    config.text('='*76)
    config.text('>> BOMB EXPLODED LEVELING (HEGRENADE LEVEL)')
    config.text('='*76)
    config.text('Notes:')
    config.text('   * Requires "gg_map_obj 0" or "gg_map_obj 3"')
    config.text('   * Requires "gg_bomb_exploded_levels 1" or higher')
    config.text('Options:')
    config.text('   0 = Do not allow players to level up if the bomb ' +
                'explodes while on HEGrenade level.')
    config.text('   1 = Allow players to level up if the bomb explodes ' +
                'while on HEGrenade level.')
    config.text('Default Value: 0')
    config.cvar('gg_bomb_exploded_skip_nade', 0, 'Allow players to level up ' +
                'when they are on HEGrenade level.')

    # Hostage Rescued Leveling
    config.text('')
    config.text('='*76)
    config.text('>> HOSTAGE RESCUED LEVELS')
    config.text('='*76)
    config.text('Notes:')
    config.text('   * Requires "gg_map_obj 0" or "gg_map_obj 2"')
    config.text('Options:')
    config.text('   0 = Disabled.')
    config.text('   # = The number of levels to reward a player for ' +
                'rescuing hostages')
    config.text('Default Value: 0')
    config.cvar('gg_hostage_rescued_levels', 0, 'Levels to reward a player ' +
                'for rescuing hostages.').addFlag('notify')

    # Hostage Rescued Required Rescues
    config.text('')
    config.text('='*76)
    config.text('>> HOSTAGE RESCUED REQUIRED RESCUES')
    config.text('='*76)
    config.text('Notes:')
    config.text('   * Requires "gg_map_obj 0" or "gg_map_obj 2"')
    config.text('   * Requires "gg_hostage_rescued_levels 1" or higher')
    config.text('Options:')
    config.text('   # = The number of hostages a player must rescue ' +
                'to level up.')
    config.text('Default Value: 0')
    config.cvar('gg_hostage_rescued_rescues', 0, 'Number of hostages rescued ' +
                'required to level up.')

    # Hostage Rescued Leveling Knife
    config.text('')
    config.text('='*76)
    config.text('>> HOSTAGE RESCUED LEVELING (KNIFE LEVEL)')
    config.text('='*76)
    config.text('Notes:')
    config.text('   * Requires "gg_map_obj 0" or "gg_map_obj 2"')
    config.text('   * Requires "gg_hostage_rescued_levels 1" or higher')
    config.text('Options:')
    config.text('   0 = Do not allow players to level up when they ' +
                'rescue hostages while on knife level.')
    config.text('   1 = Allow players to level up when they rescue hostages ' +
                'while on knife level.')
    config.text('Default Value: 0')
    config.cvar('gg_hostage_rescued_skip_knife', 0, 'Allow players to level ' +
                'up when they are on knife level.')

    # Hostage Rescued Leveling HEGrenade
    config.text('')
    config.text('='*76)
    config.text('>> HOSTAGE RESCUED LEVELING (HEGRENADE LEVEL)')
    config.text('='*76)
    config.text('Notes:')
    config.text('   * Requires "gg_map_obj 0" or "gg_map_obj 2"')
    config.text('   * Requires "gg_hostage_rescued_levels 1" or higher')
    config.text('Options:')
    config.text('   0 = Do not allow players to level up when they ' +
                'rescue hostages while on HEGrenade level.')
    config.text('   1 = Allow players to level up when they rescue hostages ' +
                'while on HEGrenade level.')
    config.text('Default Value: 0')
    config.cvar('gg_hostage_rescued_skip_nade', 0, 'Allow players to level ' +
                'up when they are on HEGrenade level.')

    # Hostage Stopped Leveling
    config.text('')
    config.text('='*76)
    config.text('>> HOSTAGE STOPPED LEVELS')
    config.text('='*76)
    config.text('Notes:')
    config.text('   * Requires "gg_map_obj 0" or "gg_map_obj 2"')
    config.text('Options:')
    config.text('   0 = Disabled.')
    config.text('   # = The number of levels to reward a player for ' +
                'stopping others from rescuing hostages')
    config.text('Default Value: 0')
    config.cvar('gg_hostage_stopped_levels', 0, 'Levels to reward a player ' +
                'for stopping other players from rescuing hostages.').addFlag('notify')

    # Hostage Rescued Required Stops
    config.text('')
    config.text('='*76)
    config.text('>> HOSTAGE RESCUED REQUIRED STOPS')
    config.text('='*76)
    config.text('Notes:')
    config.text('   * Requires "gg_map_obj 0" or "gg_map_obj 2"')
    config.text('   * Requires "gg_hostage_stopped_levels 1" or higher')
    config.text('Options:')
    config.text('   # = The number of hostages a player must stop from ' +
                'being rescued to level up.')
    config.text('Default Value: 0')
    config.cvar('gg_hostage_stopped_stops', 0, 'Number of hostages stopped ' +
                'required to level up.')

    # Hostage Stopped Leveling Knife
    config.text('')
    config.text('='*76)
    config.text('>> HOSTAGE STOPPED LEVELING (KNIFE LEVEL)')
    config.text('='*76)
    config.text('Notes:')
    config.text('   * Requires "gg_map_obj 0" or "gg_map_obj 2"')
    config.text('   * Requires "gg_hostage_stopped_levels 1" or higher')
    config.text('Options:')
    config.text('   0 = Do not allow players to level up when they ' +
                'stop hostages from being rescued while on knife level.')
    config.text('   1 = Allow players to level up when they stop hostages ' +
                'from being rescued while on knife level.')
    config.text('Default Value: 0')
    config.cvar('gg_hostage_stopped_skip_knife', 0, 'Allow players to level ' +
                'up when they are on knife level.')

    # Hostage Stopped Leveling HEGrenade
    config.text('')
    config.text('='*76)
    config.text('>> HOSTAGE STOPPED LEVELING (HEGRENADE LEVEL)')
    config.text('='*76)
    config.text('Notes:')
    config.text('   * Requires "gg_map_obj 0" or "gg_map_obj 2"')
    config.text('   * Requires "gg_hostage_stopped_levels 1" or higher')
    config.text('Options:')
    config.text('   0 = Do not allow players to level up when they ' +
                'stop hostages from being rescued while on HEGrenade level.')
    config.text('   1 = Allow players to level up when they stop hostages ' +
                'from being rescued while on HEGrenade level.')
    config.text('Default Value: 0')
    config.cvar('gg_hostage_stopped_skip_nade', 0, 'Allow players to level ' +
                'up when they are on HEGrenade level.')

    # This line creates/updates the .cfg file
    config.write()

    # Print to console to show successfule loading of the config
    es.dbgmsg(0, '\tgg_objectives_settings.cfg')
    
def unload():
    global config
    
    # Remove the "notify" and "replicated" flags as set by makepublic()
    for cvar in config.getCvars().keys():
        es.flags('remove', 'notify', cvar)
    
    # Delete the cfglib.AddonCFG instance
    del config