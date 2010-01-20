# ../addons/eventscripts/gungame/scripts/cfg/included/gg_nade_bonus.py

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
    'gungame51/included_addon_configs/gg_nade_bonus.cfg')

# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================

def load():
    generate_header(config)

    # gg_nade_bonus
    config.text('')
    config.text('='*76)
    config.text('>> GRENADE BONUS')
    config.text('='*76)
    config.text('Description:')
    config.text('   Players on grenade level will receive weapons along ' +
                'with the')
    config.text('   hegrenade.')
    config.text('Notes:')
    config.text('   * You can have multiple weapons by separating them ' +
                'with commas.')
    config.text('   * If you choose to have multiple weapons, you can only ' +
                'have one primary')
    config.text('     weapon, one secondary weapon, and one grenade (not an ' +
                'hegrenade).')
    config.text('   * You can list a weapon order file that players will ' +
                'will')
    config.text('     progress through while remaining on hegrenade level.')
    config.text('   * /cfg/gungame/weapon_orders/nade_bonus_order.txt has ' +
                'examples') 
    config.text('       and more information on this feature.')    
    config.text('Examples:')
    config.text('   * gg_nade_bonus aug')
    config.text('   * gg_nade_bonus glock,aug')
    config.text('   * gg_nade_bonus "nade_bonus_order"')
    config.text('Options:')
    config.text('   awp      scout   aug      mac10   tmp     mp5navy   ump45')
    config.text('   galil    famas   ak47     sg552   sg550   g3sg1     m249')
    config.text('   xm1014   m4a1    glock    usp     p228    deagle    elite')
    config.text('   m3       p90     fiveseven')
    config.text('   flashbang        smokegrenade')
    config.text('')
    config.text('   0 = (Disabled) Do not load gg_nade_bonus.')
    config.text('Default Value: 0')
    config.cvar('gg_nade_bonus', 0, 'The weapon(s) to be given as a grenade ' +
                'level bonus weapon.').addFlag('notify')
    config.text('')
    config.text('')
    
    # gg_nade_bonus_mode
    config.text('')
    config.text('='*76)
    config.text('>> NADE BONUS MODE')
    config.text('='*76)
    config.text('Description:')
    config.text('   Defines how gg_nade_bonus will function when a weapon ' +
                'order is given and,')
    config.text('   the player makes it through the entire order.')               
    config.text('Note:')
    config.text('   * Not nessesary to change unless you are using a weapon' +
                'order above.')
    config.text('Options:')
    config.text('   0 = (Enabled) Keep the player on the last gun.')
    config.text('   1 = (Enabled) Go through the list again (start over).')
    config.text('   2 = (Enabled) Levelup the player (same as nade kill).')
    config.text('Default Value: 0')
    config.cvar('gg_nade_bonus_mode', 0, 'Defines how the last weapon in ' +
                'the order is handled.')
    config.text('')
    config.text('')
    
    # gg_nade_bonus_reset
    config.text('')
    config.text('='*76)
    config.text('>> NADE BONUS DEATH RESET')
    config.text('='*76)
    config.text('Description:')
    config.text('   When enabled, every time a player spawns on nade level ' +
                'they will')
    config.text('   start over on the first weapon in the order.')               
    config.text('Note:')
    config.text('   * Not nessesary to change unless you are using a weapon' +
                'order above.')
    config.text('Options:')
    config.text('   0 = (Disabled) Players will resume where they left off.')
    config.text('   1 = (Enabled) Players will go back to the first weapon' + 
                'every spawn.')
    config.text('Default Value: 0')
    config.cvar('gg_nade_bonus_reset', 0, 'Enables/Disables ' +
                'gg_nade_bonus_reset.')
                
    # Write
    config.write()
    es.dbgmsg(0, '\tgg_nade_bonus.cfg')
       
def unload():
    global config
    
    # Remove the "notify" flags as set by addFlag('notify')
    for cvar in config.getCvars().keys():
        es.flags('remove', 'notify', cvar)
    
    # Delete the cfglib.AddonCFG instance
    del config