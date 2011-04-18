# ../scripts/included/gg_level_info/gg_level_info_config.py

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
    'gungame51/included_addon_configs/gg_level_info.cfg')


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    generate_header(config)

    # Level Info Hudhints
    config.text('')
    config.text('=' * 76)
    config.text('>> LEVEL INFO')
    config.text('=' * 76)
    config.text('Description:')
    config.text('   Sends hudhints to players for level info.')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not load gg_level_info.')
    config.text('   1 = (Enabled) Load gg_level_info.')
    config.text('Default Value: 0')
    config.cvar('gg_level_info', 0,
        'Enables/Disables gg_level_info.').addFlag('notify')

    config.write()
    es.dbgmsg(0, '\tgg_level_info.cfg')


def unload():
    global config

    # Remove the "notify" flags as set by addFlag('notify')
    for cvar in config.getCvars().keys():
        es.flags('remove', 'notify', cvar)

    # Delete the cfglib.AddonCFG instance
    del config
