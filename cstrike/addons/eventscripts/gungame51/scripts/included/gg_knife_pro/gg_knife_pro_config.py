# ../scripts/included/gg_knife_pro/gg_knife_pro_config.py

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

# GunGame Imports
from gungame51.core.cfg import generate_header

# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
config = cfglib.AddonCFG('%s/cfg/' % es.ServerVar('eventscripts_gamedir') +
    'gungame51/included_addon_configs/gg_knife_pro.cfg')


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    generate_header(config)

    # =========================================================================
    # GG_KNIFE_PRO CVARS
    # =========================================================================
    # Knife Pro
    config.text('=' * 76)
    config.text('>> KNIFE PRO')
    config.text('=' * 76)
    config.text('Description:')
    config.text('    When you kill a player with a knife, you will level up,' +
                ' and the victim')
    config.text('   will level down.')
    config.text('    The attacker will not steal a level if they are on ' +
                'hegrenade or knife')
    config.text('    level, or if the victim can\'t level down.')
    config.text('Options:')
    config.text('    0 = (Disabled) Do not load gg_knife_pro.')
    config.text('    1 = (Enabled) Load gg_knife_pro.')
    config.text('Default Value: 0')
    config.cvar('gg_knife_pro', 0, 'Enables/Disables ' +
        'gg_knife_pro').addFlag('notify')

    # Knife Pro Limit
    config.text('')
    config.text('=' * 76)
    config.text('>> KNIFE PRO LIMIT')
    config.text('=' * 76)
    config.text('Description:')
    config.text('    Limits level stealing to players close to your own ' +
                'level.')
    config.text('Example:')
    config.text('    If this is set to 3, you will not gain a level if you ' +
                'knife someone')
    config.text('    more than 3 levels below you.')
    config.text('Options:')
    config.text('    0 = (Disabled) Do not enable the knife pro limit.')
    config.text('    # = (Enabled) Limit level stealing to this # of levels ' +
                'below the')
    config.text('                 attacker.')
    config.text('Default Value: 0')
    config.cvar('gg_knife_pro_limit', 0, 'Limit level stealing to this # of ' +
                'levels below the attacker.')

    # Knife Pro Always Level
    config.text('')
    config.text('=' * 76)
    config.text('>> KNIFE PRO ALWAYS LEVEL')
    config.text('=' * 76)
    config.text('Description:')
    config.text('    The attacker will always level up unless they are on ' +
                'hegrenade level.')
    config.text('    The victim will always level down.')
    config.text('Note:')
    config.text('    gg_knife_pro_limit still prevents leveling if enabled.')
    config.text('Options:')
    config.text('    0 = (Disabled) Conform to logical gg_knife_pro ruling')
    config.text('    1 = (Enabled) Always affect levels with exception to ' +
                'the situations in')
    config.text('                   the description above.')
    config.text('Default Value: 0')
    config.cvar('gg_knife_pro_always_level', 0, 'Enables/Disables always ' +
                'stealing levels.')

    # Allow Skip Nade
    config.text('')
    config.text('=' * 76)
    config.text('>> KNIFE PRO ALLOW SKIP NADE')
    config.text('=' * 76)
    config.text('Description:')
    config.text('    The attacker may skip grenade level with a knife kill.')
    config.text('Note:')
    config.text('    gg_knife_pro_limit still prevents leveling if enabled.')
    config.text('Options:')
    config.text('    0 = (Disabled) Conform to logical gg_knife_pro ruling')
    config.text('    1 = (Enabled) Allow players to knife past nade level.')
    config.text('Default Value: 0')
    config.cvar('gg_knife_pro_skip_nade', 0, 'Enables/Disables always ' +
                'skipping nade.')
    config.write()

    es.dbgmsg(0, '\tgg_knife_pro.cfg')


def unload():
    global config

    # Remove the "notify" flags as set by addFlag('notify')
    for cvar in config.getCvars().keys():
        es.flags('remove', 'notify', cvar)

    # Delete the cfglib.AddonCFG instance
    del config
