# ../scripts/included/gg_leaderweapon_warning/gg_leaderweapon_warning_config.py

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
    'gungame51/included_addon_configs/gg_leaderweapon_warning.cfg')


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    generate_header(config)

    # Leader Weapon Warning
    config.text('')
    config.text('=' * 76)
    config.text('>> GUNGAME LEADER WEAPON WARNING')
    config.text('=' * 76)
    config.text('Description:')
    config.text('   Announces via sound at the beginning of each round ' +
                'when a player')
    config.text('information.')
    config.text('     has reached either "hegrenade" or "knife" level.')
    config.text('Options:')
    config.text('   0 = (Disabled)')
    config.text('   1 = (Enabled)')
    config.text('Default Value: 0')
    config.cvar('gg_leaderweapon_warning', 0, 'Play a sound when a player ' +
                'reaches "hegrenade" or "knife" level.').addFlag('notify')

    # Play Warning only on last leves
    config.text('')
    config.text('=' * 76)
    config.text('>> WARN ONLY ON LAST LEVELS')
    config.text('=' * 76)
    config.text('Description:')
    config.text('   Only play warnings on the last level of each weapon')
    config.text('Options:')
    config.text('   0 = (Disabled)')
    config.text('   1 = (Enabled)')
    config.text('Default Value: 0')
    config.cvar('gg_leaderweapon_warning_only_last', 0,
                'Only play a sound when a player reaches ' +
                'the "last" hegrenade or knife level.').addFlag('notify')

    config.write()
    es.dbgmsg(0, '\tgg_leaderweapon_warning.cfg')


def unload():
    global config

    # Remove the "notify" flags as set by addFlag('notify')
    for cvar in config.getCvars().keys():
        es.flags('remove', 'notify', cvar)

    # Delete the cfglib.AddonCFG instance
    del config
