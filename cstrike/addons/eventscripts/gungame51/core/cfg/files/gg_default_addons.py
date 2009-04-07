# ../cstrike/addons/eventscripts/gungame/core/cfg/files/gg_default_addons.py

'''
$Rev: 15 $
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
config = cfglib.AddonCFG('%s/cfg/gungame51/gg_default_addons.cfg'
    %es.ServerVar('eventscripts_gamedir'))
        
# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    config.text('*'*76)
    config.text('*' + ' '*11 + 'gg_default_addons.cfg -- Default Addon ' +
                'Configuration' + ' '*11 + '*')
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
    
    # Error Logging
    config.text('='*76)
    config.text('>> ERROR LOGGING')
    config.text('='*76)
    config.text('Description:')
    config.text('   Logs all GunGame-related errors to a log file located in:')
    config.text('      "../<MOD>/addons/eventscripts/gungame/logs/"')
    config.text('Notes:')
    config.text('   * If something in GunGame is not working and you are ' +
                'going to post a bug,')
    config.text('     make sure you enable this addon then post the ' +
                'error log when you are')
    config.text('     filling your bug report.')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not log errors.')
    config.text('   1 = (Enabled) Log errors.')
    config.text('Default Value: 1')
    config.cvar('gg_error_logging', 1, 'Logs all GunGame-related ' +
                'errors.').addFlag('notify')
    
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
                'multi-level bonus.').addFlag('notify')
    
    # Turbo Mode
    config.text('')
    config.text('='*76)
    config.text('>> TURBO MODE')
    config.text('='*76)
    config.text('Description:')
    config.text('   Gives the player their next weapon immediately when they' +
                ' level up.')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not load gg_turbo.')
    config.text('   1 = (Enabled) Load gg_turbo.')
    config.text('Default Value: 0')
    config.cvar('gg_turbo', 0, 'Enables/Disables gg_turbo.').addFlag('notify')
    
    # No Block
    config.text('')
    config.text('='*76)
    config.text('>> NO BLOCK')
    config.text('='*76)
    config.text('Description:')
    config.text('   Makes it possible to pass through all players.')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not load gg_noblock.')
    config.text('   1 = (Enabled) Load gg_noblock.')
    config.text('Default Value: 0')
    config.cvar('gg_noblock', 0, 'Enables/Disables ' +
                'gg_noblock.').addFlag('notify')
    
    # Dead Strip
    config.text('')
    config.text('='*76)
    config.text('>> DEAD STRIP')
    config.text('='*76)
    config.text('Description:')
    config.text('   Removes a player\'s weapons when they die.')
    config.text('Note:')
    config.text('   * Prevents players from picking up the wrong weapon.')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not load gg_dead_strip.')
    config.text('   1 = (Enabled) Load gg_dead_strip.')
    config.text('Default Value: 0')
    config.cvar('gg_dead_strip', 0, 'Enables/Disables ' +
                'gg_dead_strip.').addFlag('notify')
    
    # =========================================================================
    # KNIFE-RELATED CVARS
    # =========================================================================
    # Knife Pro
    config.text('')
    config.text('='*76)
    config.text('>> KNIFE PRO')
    config.text('='*76)
    config.text('Description:')
    config.text('   When you kill a player with a knife, you will level up, ' +
                'and the victim')
    config.text('   will level down.')
    config.text('Notes:')
    config.text('   * Will not load with "gg_knife_rookie" enabled.')
    config.text('   * See the variable "gg_knife_pro_limit" for further ' +
                'enhancement of')
    config.text('     gg_knife_pro.')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not load gg_knife_pro.')
    config.text('   1 = (Enabled) Load gg_knife_pro.')
    config.text('Default Value: 0')
    config.cvar('gg_knife_pro', 0, 'Enables/Disables gg_knife_pro').addFlag('notify')
    
    # Knife Pro Limit
    config.text('')
    config.text('='*76)
    config.text('>> KNIFE PRO LIMIT')
    config.text('='*76)
    config.text('Description:')
    config.text('   Limits level stealing to players close to your own ' +
                'level.')
    config.text('Example:')
    config.text('   * If this is set to 3, you will not gain a level if you ' +
                'knife someone')
    config.text('     more than 3 levels below you.')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not enable the knife pro limit.')
    config.text('   # = (Enabled) Limit level stealing to this # of levels ' +
                'below the')
    config.text('                 attacker.')
    config.text('Default Value: 0')
    config.cvar('gg_knife_pro_limit', 0, 'Limit level stealing to this # of ' +
                'levels below the attacker.').addFlag('notify')
    
    # Knife Rookie
    config.text('')
    config.text('='*76)
    config.text('>> KNIFE ROOKIE')
    config.text('='*76)
    config.text('Description:')
    config.text('   Similar to gg_knife_pro, but not as strict:')
    config.text('      * The attacker will level up even when the victim is ' +
                'on level 1.')
    config.text('      * The attacker will level up even though the victim ' +
                'cannot leveldown.')
    config.text('      * The victim will level down even though the attacker' +
                ' cannot levelup.')
    config.text('Note:')
    config.text('   * Will not load with "gg_knife_pro" enabled.')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not load gg_knife_rookie.')
    config.text('   1 = (Enabled) Load gg_knife_rookie.')
    config.text('Default Value: 0')
    config.cvar('gg_knife_rookie', 0, 'Enables/Disables ' +
                'gg_knife_rookie.').addFlag('notify')
                
    # Knife Elite
    config.text('')
    config.text('='*76)
    config.text('>> KNIFE ELITE')
    config.text('='*76)
    config.text('Description:')
    config.text('   Once a player levels up, they only get a knife until ' +
                'the next round.')
    config.text('Notes:')
    config.text('   * Will not load with "gg_turbo" enabled.')
    config.text('   * "gg_dead_strip" will automatically be enabled.')
    config.text('   * Will not load if "gg_dead_strip" can not be enabled.')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not load gg_knife_elite.')
    config.text('   1 = (Enabled) Load gg_knife_elite.')
    config.text('Default Value: 0')
    config.cvar('gg_knife_elite', 0, 'Enables/Disables ' +
                'gg_knife_elite.').addFlag('notify')
    
    # =========================================================================
    # GRENADE-RELATED CVARS
    # =========================================================================
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
                'gg_earn_nade.').addFlag('notify')
    
    # Unlimited Grenades
    config.text('')
    config.text('='*76)
    config.text('>> UNLIMITED GRENADES')
    config.text('='*76)
    config.text('Description:')
    config.text('   When a player reaches grenade level, they are given ' +
                'another grenade when')
    config.text('   their thrown grenade detonates.')
    config.text('Note:')
    config.text('   * Will not load with "gg_earn_nades" enabled.')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not load gg_unl_grenade.')
    config.text('   1 = (Enabled) Load gg_unl_grenade.')
    config.text('Default Value: 0')
    config.cvar('gg_unl_grenade', 0, 'Enables/Disables ' +
                'gg_unl_grenade.').addFlag('notify')
    
    # Grenade Bonus
    config.text('')
    config.text('='*76)
    config.text('>> GRENADE BONUS')
    config.text('='*76)
    config.text('Description:')
    config.text('   Players on grenade level will receive this weapon along ' +
                'with the')
    config.text('   hegrenade.')
    config.text('Notes:')
    config.text('   * You can have multiple weapons by seperating them ' +
                'with commas.')
    config.text('   * If you choose to have multiple weapons, you can only ' +
                'have one primary')
    config.text('     weapon, one secondary weapon, and one grenade (not an ' +
                'hegrenade).')
    config.text('Examples:')
    config.text('   * gg_nade_bonus aug')
    config.text('   * gg_nade_bonus glock,aug')
    config.text('Options:')
    config.text('\tawp   \tscout\taug   \tmac10\ttmp   \tmp5navy\tump45\tp90')
    config.text('\tgalil\tfamas\tak47\tsg552\tsg550\tg3sg1\tm249\tm3')
    config.text('\txm1014\tm4a1\tglock\tusp   \tp228\tdeagle\telite\t' +
                'fiveseven')
    config.text('\tflashbang   \tsmokegrenade')
    config.text('\t0 = (Disabled) Do not load gg_nade_bonus.')
    config.text('Default Value: 0')
    config.cvar('gg_nade_bonus', 0, 'The weapon(s) to be given as a grenade ' +
                'level bonus weapon.').addFlag('notify')
    
    # Reload
    config.text('')
    config.text('='*76)
    config.text('>> RELOAD')
    config.text('='*76)
    config.text('Description:')
    config.text('   When a player gains a level, the ammo in their clip is ' +
                'replenished.')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not load gg_reload.')
    config.text('   1 = (Enabled) Load gg_reload.')
    config.text('Default Value: 0')
    config.cvar('gg_reload', 0, 'Enables/Disables ' +
                'gg_reload.').addFlag('notify')
    
    # Friendly Fire
    config.text('')
    config.text('='*76)
    config.text('>> FRIENDLY FIRE')
    config.text('='*76)
    config.text('Description:')
    config.text('   Automatically turn on friendly fire when a player reaches' +
                ' "x" levels')
    config.text('   below the last level (+1).')
    config.text('Examples:')
    config.text('   * gg_friendlyfire 1')
    config.text('       - The above will turn on friendly fire when a player' +
                ' reaches the last')
    config.text('         level.')
    config.text('   * gg_friendlyfire 2')
    config.text('        - The above will turn on friendly fire when a player' +
                ' reaches one')
    config.text('          level before the last.')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not load gg_friendlyfire.')
    config.text('   # = (Enabled) Turn on friendly fire when a player ' +
                'reaches "#" (+1) levels')
    config.text('                 below the last level.')
    config.text('Default Value: 0')
    config.cvar('gg_friendlyfire', 0, 'The number (+1) of levels below the ' +
                'last level to enable friendly fire.').addFlag('notify')
    
    # =========================================================================
    # STATS-RELATED CVARS
    # =========================================================================
    # Stats Database and Commands
    config.text('')
    config.text('='*76)
    config.text('>> STATS DATABASE AND COMMANDS')
    config.text('='*76)
    config.text('Description:')
    config.text('   Whether you want to keep track of winners on your ' +
                'server. This also')
    config.text('   enables the stat commands (!leader, !top, !rank, etc).')
    config.text('Note:')
    config.text('   * This will save a file to the server and requires ' +
                'appropiate read/write')
    config.text('     permissions.')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not load gg_stats.')
    config.text('   1 = (Enabled) Load gg_stats).')
    config.text('Default Value: 0')
    config.cvar('gg_stats', 0, 'Enables/Disables ' +
                'gg_stats.').addFlag('notify')
    
    # Stats Database Prune
    config.text('')
    config.text('='*76)
    config.text('>> STATS DATABASE PRUNE')
    config.text('='*76)
    config.text('Description:')
    config.text('   The number of days of inactivity for a winner that is ' +
                'tolerated until')
    config.text('   they are removed from the database.')
    config.text('Notes:')
    config.text('   * Pruning the database of old entries is STRONGLY ' +
                'RECOMMENDED for ')
    config.text('     high-volume servers.')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not load gg_prune_database.')
    config.text('   1 = (Enabled) Load gg_prune_database.')
    config.text('Default Value: 0')
    config.cvar('gg_prune_database', 0, 'The number inactive days before ' +
                'a winner is removed from the database.').addFlag('notify')
                
    # Stats Logging
    config.text('')
    config.text('='*76)
    config.text('>> STATS LOGGING')
    config.text('='*76)
    config.text('Description:')
    config.text('   When enabled, this addon will log game events for stats ' +
                'tracking for')
    config.text('   HLstatsX, Psychostats, and etc.')
    config.text('Notes:')
    # Not quite sure what this is, but I don't think I like it...
    config.text('   * Other options available in "stats_logging.txt".')
    config.text('   * This should be used with third-party stats programs.')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not load gg_stats_logging.')
    config.text('   1 = (Enabled) Load gg_stats_logging.')
    config.text('Default Value: 0')
    config.cvar('gg_stats_logging', 0, 'Enables/Disables ' +
                'stats logging for third-party programs.').addFlag('notify')
    
    # =========================================================================
    # SPAWN-RELATED CVARS
    # =========================================================================
    # Spawnpoint Manager
    config.text('')
    config.text('='*76)
    config.text('>> SPAWNPOINT MANAGER')
    config.text('='*76)
    config.text('Description:')
    config.text('   Loads random spawnpoints if a spawnpoint file for the ' +
                'current map has been')
    config.text('   created.  This addon also adds commands and a menu to ' +
                'allow admins to')
    config.text('   manage spawnpoints on the current map.')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not load gg_spawnpoints.')
    config.text('   1 = (Enabled) Load gg_spawnpoints.')
    config.text('Default Value: 0')
    config.cvar('gg_spawnpoints', 0, 'Enables/Disables random spawn points ' +
                'and spawn point management.').addFlag('notify')
    
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
    config.text('   1 = (Enabled) Load gg_spawn_protect.')
    config.text('Default Value: 0')
    config.cvar('gg_spawn_protect', 0, 'Enables/Disables spawn ' +
                'protection.').addFlag('notify')
                
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
                'protected player.').addFlag('notify')
    config.cvar('gg_spawn_protect_green', 255, 'The green shade of the spawn' +
                ' protected player.').addFlag('notify')
    config.cvar('gg_spawn_protect_blue', 255, 'The blue shade of the spawn ' +
                'protected player.').addFlag('notify')
    config.cvar('gg_spawn_protect_alpha', 150, 'The alpha of the spawn ' +
                'protected player.').addFlag('notify')
                
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
                'protection when the weapon is fired.').addFlag('notify')
                
    # Allow Leveling Whilst Protected
    config.text('')
    config.text('='*76)
    config.text('>> ALLOW LEVELING WHILST PROTECTED')
    config.text('='*76)
    config.text('Description:')
    config.text('   Players can level up while spawn protected.')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not load gg_spawn_protect_can_level_up.')
    config.text('   1 = (Enabled) Load gg_spawn_protect_can_level_up.')
    config.text('Default Value: 0')
    config.cvar('gg_spawn_protect_can_level_up', 0, 'Cancels spawn ' +
                'protection when the weapon is fired.').addFlag('notify')
    
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
                'gg_deathmatch.').addFlag('notify')
    
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
                ' a player after death.').addFlag('notify')
    
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
                'gg_elimination.').addFlag('notify')
    
    # Dissolver
    config.text('')
    config.text('='*76)
    config.text('>> DISSOLVER')
    config.text('='*76)
    config.text('Description:')
    config.text('   Removes ragdolls by dissolving them with various effects.')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not load gg_dissolver.')
    config.text('   1 = (Enabled) Load gg_dissolver.')
    config.text('Default Value: 0')
    config.cvar('gg_dissolver', 0, 'Enables/Disables ' +
                'gg_dissolver.').addFlag('notify')
    
    # Dissolver Effect
    config.text('')
    config.text('='*76)
    config.text('>> DISSOLVER EFFECT')
    config.text('='*76)
    config.text('Description:')
    config.text('   The type of effect that will happen upon the ragdoll.')
    config.text('Options:')
    config.text('   0 = No Effect')
    config.text('   1 = Energy')
    config.text('   2 = Heavy Electrical')
    config.text('   3 = Light Electrical')
    config.text('   4 = Core Effect')
    config.text('   5 = Random Effect')
    config.text('Default Value: 5')
    config.cvar('gg_dissolver_effect', 5, 'The type of effect that will ' +
                'happen upon the ragdoll.').addFlag('notify')
    
    # Handicap
    config.text('')
    config.text('='*76)
    config.text('>> HANDICAP')
    config.text('='*76)
    config.text('Description:')
    config.text('   Helps newly connected players by adjusting their level.')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not load gg_handicap.')
    config.text('   1 = Set player to the lowest level player other than ' +
                'themself.')
    config.text('       (Catch them up if they are behind)')
    config.text('   2 = Set player to median level.')
    config.text('   3 = Set player to average level.')
    config.text('Default Value: 0')
    config.cvar('gg_handicap', 0, 'Helps newly connected players by ' +
                'adjusting their level.').addFlag('notify')
    
    # Handicap Update
    config.text('')
    config.text('='*76)
    config.text('>> HANDICAP UPDATE')
    config.text('='*76)
    config.text('Description:')
    config.text('   A timer (in seconds) that updates players\' levels who ' +
                'are below the handicap.')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not load gg_handicap_update.')
    config.text('   1 = (Enabled) Load gg_handicap_update.')
    config.text('Default Value: 0')
    config.cvar('gg_handicap_update', 0, 'The time (in seconds) to update ' +
                'players\' levels using handicap.').addFlag('notify')
    
    config.write()
    config.execute()
    es.dbgmsg(0, '\tgg_default_addons.cfg')
'''
//=========================================================
// WELCOME MESSAGE
//=========================================================
// Show a welcome message to everyone that connects.
//
// Note: More options available in the "welcome_msg" folder.
//
// Options: 0 = Disabled
//          1 = Enabled

gg_welcome_msg 0

//=========================================================
// WELCOME MESSAGE TIMEOUT
//=========================================================
// How long until the welcome message dismisses itself.
//
// Default value: 5
//
// Options: 0 = Never dismiss
//          <seconds> = Stay up for <seconds>

gg_welcome_msg_timeout 5

//=========================================================
// CONVERTER
//=========================================================
// Allows you to upgrade your current winner database / spawnpoints from
// previous versions of GunGame (3/4) to GunGame 5 format.
//
// Options: 0 = Disabled
//          1 = Enabled

gg_convert 0
'''

def unload():
    # Remove the "notify" flags as set by addFlag('notify')
    for cvar in config.getCvars().keys():
        es.flags('remove', 'notify', cvar)
    
    # Delete the cfglib.AddonCFG instance
    global config
    del config