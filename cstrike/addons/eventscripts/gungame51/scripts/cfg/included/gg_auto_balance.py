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

# ============================================================================
# >> GLOBAL VARIABLES
# ============================================================================
config = cfglib.AddonCFG('%s/cfg/' % es.ServerVar('eventscripts_gamedir') +
    'gungame51/included_addon_configs/gg_auto_balance.cfg')
        
# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    config.text('*'*76)
    config.text('*' + ' '*12 + 'gg_auto_balance.cfg -- Auto Balancer ' +
                'Configuration' + ' '*12 + '*')
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
    
    # gg_auto_balance
    config.text('')
    config.text('='*76)
    config.text('>> AUTO BALANCE')
    config.text('='*76)
    config.text('Description:')
    config.text('   A team balancer based upon average level.')
    config.text('Notes:')
    config.text('   * "mp_limitteams" will automatically be set to 1.')
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
    config.text('Default Value: 3')
    config.cvar('gg_auto_balance_threshold', 3, 'Threshold for gg_auto_' +
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
    config.text('   * Useful for deathmatch.')
    config.text('   * Last player alive will not be forced')
    config.text('Options:')
    config.text('   0 = (Disabled)')
    config.text('   # = Time in seconds before a player is swaped teams.')
    config.text('Default Value: 0')
    config.cvar('gg_auto_balance_force', 0, 'Force threshold for gg_auto_' +
                'force')
    config.text('')
    
    # gg_auto_balance_notify
    config.text('')
    config.text('='*76)
    config.text('>> NOTIFICATION')
    config.text('='*76)
    config.text('Description:')
    config.text('   Notify players with a message and a flashing screen when' +
                ' they are moved.')
    config.text('Options:')
    config.text('   0 = (Disabled) No notification')
    config.text('   1 = (Enabled) Notification')
    config.text('Default Value: 1')
    config.cvar('gg_auto_balance_notify', 1, 'Notification for gg_auto_' +
                'balance')
    config.text('')
    
    # gg_auto_balance_immunity    
    config.text('')
    config.text('='*76)
    config.text('>> IMMUNITY LIST')
    config.text('='*76)
    config.text('Description:')
    config.text('   List of steamids that are allways immune from being ' +
                'swapped.')
    config.text('Notes:')
    config.text('   * Try to keep this list to a minimum.')
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
    config.text('>> BALANCE TIMER')
    config.text('='*76)
    config.text('Description:')
    config.text('   How often in minutes teams are checked for balance.')
    config.text('Notes:')
    config.text('   * Only used for deathmatch since rounds do not end.')
    config.text('Options:')
    config.text('# = Time in minutes')
    config.text('Default Value: 3')
    config.cvar('gg_auto_balance_timer', 3, 'Timer for gg_auto_' +
                'balance')

    # gg_auto_balance_knife
    config.text('')
    config.text('='*76)
    config.text('>> COUNT KNIFE AS LEVEL 1')
    config.text('='*76)
    config.text('Description:')
    config.text('   How often in minutes teams are checked for balance.')
    config.text('Notes:')
    config.text('   * Only used for deathmatch since rounds do not end.')
    config.text('Options:')
    config.text('   0 = (Disabled)')
    config.text('# = Time in minutes')
    config.text('Default Value: 3')
    config.cvar('gg_auto_balance_knife', 0, 'Timer for gg_auto_' +
                'balance')

    # gg_auto_balance_nade
    config.text('')
    config.text('='*76)
    config.text('>> COUNT NADE AS LEVEL 1')
    config.text('='*76)
    config.text('Description:')
    config.text('   How often in minutes teams are checked for balance.')
    config.text('Notes:')
    config.text('   * Only used for deathmatch since rounds do not end.')
    config.text('Options:')
    config.text('   0 = (Disabled)')
    config.text('# = Time in minutes')
    config.text('Default Value: 3')
    config.cvar('gg_auto_balance_nade', 0, 'Timer for gg_auto_' +
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