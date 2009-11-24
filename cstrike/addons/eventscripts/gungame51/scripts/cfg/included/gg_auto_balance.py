# ../addons/eventscripts/gungame/scripts/cfg/included/gg_auto_balance.py

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
config = cfglib.AddonCFG('%s/cfg/' % es.ServerVar('eventscripts_gamedir') +
    'gungame51/included_addon_configs/gg_auto_balance.cfg')
        
# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    # Generate header
    generate_header(config)
    
    # gg_auto_balance
    config.text('')
    config.text('='*76)
    config.text('>> GUNGAME AUTO BALANCE')
    config.text('='*76)
    config.text('Description:')
    config.text('   When enabled, gg_auto_balancer will attempt to balance ' +
                'teams based upon')
    config.text('   GunGame level.  It will automatically correct team size' +
                ' as well as ')
    config.text('   prevent team stacking.')
    config.text('Notes:')
    config.text('   * "mp_limitteams" will automatically be set to "1"')
    config.text('   * "mp_autoteambalance" will automatically be set to "0"')
    config.text('Options:')
    config.text('   0 = (Disabled)')
    config.text('   1 = (Enabled)')
    config.text('Default Value: 0')
    config.cvar('gg_auto_balance', 0, 'Enables/Disables ' +
                'gg_auto_balance.')
    config.text('')
    
    # gg_auto_balance_threshold
    config.text('')
    config.text('='*76)
    config.text('>> THRESHOLD')
    config.text('='*76)
    config.text('Description:')
    config.text('   Min average level difference before the teams will be ' +
                'balanced.')
    config.text('Notes:')
    config.text('   * Setting this low will cause frequent balancing.')
    config.text('Options:')
    config.text('   # = Threshold')
    config.text('Default Value: 1.75')
    config.cvar('gg_auto_balance_threshold', 1.75, 'Threshold for gg_auto_' +
                'balance')
    config.text('')
    
    # gg_auto_balance_useimmune
    config.text('')
    config.text('='*76)
    config.text('>> IMMUNITY')
    config.text('='*76)
    config.text('Description:')
    config.text('   Max amount of times a player can be moved before ' +
                'becomming immune.')
    config.text('Notes:')
    config.text('   * If this is set too low the auto_balancer can run out')
    config.text('     possible players.')
    config.text('Options:')
    config.text('   # = Max team changes per player')
    config.text('Default Value: 3')
    config.cvar('gg_auto_balance_useimmune', 3, 'Max team swaps for gg_auto_' +
                'balance')
    config.text('')
    
    # gg_auto_balance_force
    config.text('')
    config.text('='*76)
    config.text('>> FORCE SWAP OF LIVE PLAYERS')
    config.text('='*76)
    config.text('Description:')
    config.text('   Instead of waiting for players to die, swap players on ' +
                'the fly')
    config.text('   if they live too long.')
    config.text('Notes:')
    config.text('   * Required for deathmatch.')
    config.text('   * Last player alive will not be forced to move, if')
    config.text('     deathmatch is disabled.')
    config.text('Options:')
    config.text('   # = Time in seconds before a player is swapped teams.')
    config.text('Default Value: 15')
    config.cvar('gg_auto_balance_force', 15, 'Force threshold for gg_auto_' +
                'force')
    config.text('')
    
    # gg_auto_balance_notify
    config.text('')
    config.text('='*76)
    config.text('>> NOTIFICATION')
    config.text('='*76)
    config.text('Description:')
    config.text('   Notify players with a message, screen flash, and ' +
                'a sound when they are')
    config.text('   moved.')
    config.text('Options:')
    config.text('   0 = (Disabled) No notification')
    config.text('   1 = (Enabled) Notification')
    config.text('   2 = (Enabled) Notification w/ sound')
    config.text('Default Value: 2')
    config.cvar('gg_auto_balance_notify', 2, 'Notification for gg_auto_' +
                'balance')
    config.text('')

    # gg_auto_balance_notify_all
    config.text('')
    config.text('='*76)
    config.text('>> NOTIFY SERVER OF BALANCE')
    config.text('='*76)
    config.text('Description:')
    config.text('   Notify players with a chat message when a team balance ' +
                'is preformed.')
    config.text('Options:')
    config.text('   0 = (Disabled) No notification')
    config.text('   1 = (Enabled) Notify the server')
    config.text('Default Value: 1')
    config.cvar('gg_auto_balance_notify_all', 1, 'Notification for gg_auto_' +
                'balance')
    config.text('')
    
    # gg_auto_balance_immunity    
    config.text('')
    config.text('='*76)
    config.text('>> IMMUNITY LIST')
    config.text('='*76)
    config.text('Description:')
    config.text('   List of steamids that are always immune from being ' +
                'swapped.')
    config.text('Notes:')
    config.text('   * Requires "gg_auto_balance_useimmune" to be enabled.')
    config.text('Options:')
    config.text('   0 = (Disabled)')
    config.text('Examples:')
    config.text('   gg_auto_balance_immunity "STEAM_0:0:0000000, ' +
                'STEAM_0:1:1111111"')
    config.text('Default Value: 0')
    config.cvar('gg_auto_balance_immunity', 0, 'Immunity list for gg_auto_' +
                'balance')    
    config.text('')
    
    # gg_auto_balance_timer
    config.text('')
    config.text('='*76)
    config.text('>> DEATHMATCH TIMER')
    config.text('='*76)
    config.text('Description:')
    config.text('   How often in minutes teams are checked for balance.')
    config.text('Notes:')
    config.text('   * Only used when deathmatch is enabled, since rounds ' +
                'do not end.')
    config.text('   * Required for gg_deathmatch.')
    config.text('Options:')
    config.text('# = Time in minutes')
    config.text('Default Value: 3')
    config.cvar('gg_auto_balance_timer', 3, 'Timer for gg_auto_' +
                'balance')

    # gg_auto_balance_knife
    config.text('')
    config.text('='*76)
    config.text('>> CHANGE KNIFE LEVEL')
    config.text('='*76)
    config.text('Description:')
    config.text('   Knife level will be considered as another level ' +
                ' for balancing purposes.')
    config.text('Options:')
    config.text('   0 = (Disabled)')
    config.text('# = Level')
    config.text('Example:')
    config.text('   gg_auto_balance_knife = 1')
    config.text('       (Knife level will be considered level 1)')
    config.text('Default Value: 0')
    config.cvar('gg_auto_balance_knife', 0, 'Knife lvl override for gg_auto_' +
                'balance')

    # gg_auto_balance_nade
    config.text('')
    config.text('='*76)
    config.text('>> CHANGE GRENADE LEVEL')
    config.text('='*76)
    config.text('Description:')
    config.text('   Grenade level will be considered as another level ' +
                'for balancing purposes.')
    config.text('Options:')
    config.text('   0 = (Disabled)')
    config.text('# = Level')
    config.text('Example:')
    config.text('   gg_auto_balance_nade = 5')
    config.text('       (Nade level will be considered level 5)')
    config.text('Default Value: 0')
    config.cvar('gg_auto_balance_nade', 0, 'Nade lvl override for gg_auto_' +
                'balance')

    config.write()
    es.dbgmsg(0, '\tgg_auto_balance.cfg')

def unload():
    global config

    # Remove the "notify" flags as set by addFlag('notify')
    for cvar in config.getCvars().keys():
        es.flags('remove', 'notify', cvar)
    
    # Delete the cfglib.AddonCFG instance
    del config