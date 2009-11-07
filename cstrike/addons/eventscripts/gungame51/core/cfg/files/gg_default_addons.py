# ../addons/eventscripts/gungame/core/cfg/files/gg_default_addons.py

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
                'errors.')

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
    config.cvar('gg_turbo', 0, 'Enables/Disables gg_turbo.')

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
                'gg_noblock.')

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
                'gg_dead_strip.')

    # =========================================================================
    # KNIFE-RELATED CVARS
    # =========================================================================
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
                'gg_knife_elite.')

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
                'gg_earn_nade.')

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
                'gg_unl_grenade.')

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
                'gg_reload.')

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
                'gg_stats.')

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
                'a winner is removed from the database.')

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
                'stats logging for third-party programs.')

    # =========================================================================
    # SPAWN-RELATED CVARS
    # =========================================================================

    # Random Spawnpoints
    config.text('')
    config.text('='*76)
    config.text('>> RANDOM SPAWNPOINTS')
    config.text('='*76)
    config.text('Description:')
    config.text('   Loads random spawnpoints if a spawnpoint file for the ' +
                'current map has')
    config.text('    been created.')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not load gg_random_spawn.')
    config.text('   1 = (Enabled) Load gg_random_spawn.')
    config.text('Default Value: 0')
    config.cvar('gg_random_spawn', 0, 'Enables/Disables random spawn points')

    # Spawnpoint Manager
    config.text('')
    config.text('='*76)
    config.text('>> SPAWNPOINT MANAGER')
    config.text('='*76)
    config.text('Description:')
    config.text('   This addon adds commands and a menu to allow admins to')
    config.text('   manage spawnpoints on the current map.')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not load gg_spawnpoints.')
    config.text('   1 = (Enabled) Load gg_spawnpoints.')
    config.text('Default Value: 0')
    config.cvar('gg_spawnpoints', 0, 'Spawn point management.')

    # Dissolver
    config.text('')
    config.text('='*76)
    config.text('>> DISSOLVER')
    config.text('='*76)
    config.text('Description:')
    config.text('   Removes ragdolls by dissolving them with various effects.')
    config.text('Options:')
    config.text('   0 = Disabled')
    config.text('   1 = No Effect')
    config.text('   2 = Energy')
    config.text('   3 = Heavy Electrical')
    config.text('   4 = Light Electrical')
    config.text('   5 = Core Effect')
    config.text('   6 = Random Effect')
    config.text('Default Value: 0')
    config.cvar('gg_dissolver', 0, 'Enables/Disables ' +
                'gg_dissolver.')

    # Handicap
    config.text('')
    config.text('='*76)
    config.text('>> HANDICAP')
    config.text('='*76)
    config.text('Description:')
    config.text('   Helps newly connected players by adjusting their level.')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not load gg_handicap.')
    config.text('   1 = Set player to the level of the lowest level of all ' +
                'the other players.')
    config.text('       Basically "catching them up".')
    config.text('Default Value: 0')
    config.cvar('gg_handicap', 0, 'Helps newly connected players by ' +
                'adjusting their level.')

    # Handicap Update
    config.text('')
    config.text('='*76)
    config.text('>> HANDICAP UPDATE')
    config.text('='*76)
    config.text('Description:')
    config.text('   A timer (in seconds) that updates players with the ' +
                'lowest level to the')
    config.text('   lowest level of the other players. Basically "catching ' +
                'them up".')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not load gg_handicap_update.')
    config.text('   180 = (Enabled) Update the lowest level players every ' +
                '180 seconds (3 minutes).')
    config.text('Default Value: 0')
    config.cvar('gg_handicap_update', 0, 'The time (in seconds) to update ' +
                'players\' levels using handicap.')

    # Thanks
    config.text('')
    config.text('='*76)
    config.text('>> THANKS')
    config.text('='*76)
    config.text('Description:')
    config.text('   Allows players to type !thanks to display a list of ' +
                'those involved with')
    config.text('   development and testing of GunGame.')
    config.text('Options:')
    config.text('   0 = Disabled')
    config.text('   1 = Enabled')
    config.text('Default Value: 1')
    config.cvar('gg_thanks', 1, 'Displays a list of those involved with ' +
                'development and testing of GunGame.')

    config.write()
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
    global config

    # Remove the "notify" flags as set by addFlag('notify')
    for cvar in config.getCvars().keys():
        es.flags('remove', 'notify', cvar)

    # Delete the cfglib.AddonCFG instance
    del config