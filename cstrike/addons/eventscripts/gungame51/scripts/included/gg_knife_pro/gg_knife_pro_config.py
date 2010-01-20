# ../addons/eventscripts/gungame/scripts/cfg/included/gg_knife_pro_config.py

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
    'gungame51/included_addon_configs/gg_knife_pro.cfg')
        
# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    generate_header(config)
    
    # =========================================================================
    # GG_KNIFE_PRO CVARS
    # =========================================================================
    # Knife Pro
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
    config.cvar('gg_knife_pro', 0, 'Enables/Disables gg_knife_pro')
    
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
                'levels below the attacker.')
    
    # Knife Rookie
    config.text('')
    config.text('='*76)
    config.text('>> KNIFE PRO ROOKIE')
    config.text('='*76)
    config.text('Description:')
    config.text('      * The attacker will level up even when the victim is ' +
                'on level 1.')
    config.text('      * The attacker will level up even though the victim ' +
                'cannot leveldown.')
    config.text('      * The victim will level down even though the attacker' +
                ' cannot levelup.')
    config.text('Notes:')
    config.text('   * Allows attackers to level up even if the victim is on' +
                ' level 1.')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not allow attackers to level up if the' +
                ' victim is on')
    config.text('                  level 1.')
    config.text('   1 = (Enabled) Allow attackers to level up if the victim ' +
                'is on level 1.')
    config.text('Default Value: 0')
    config.cvar('gg_knife_pro_rookie', 0, 'Enables/Disables stealing levels ' +
                'from victims on level 1.')

    config.write()
    es.dbgmsg(0, '\tgg_knife_pro.cfg')

def unload():
    global config

    # Remove the "notify" flags as set by addFlag('notify')
    for cvar in config.getCvars().keys():
        es.flags('remove', 'notify', cvar)
    
    # Delete the cfglib.AddonCFG instance
    del config
