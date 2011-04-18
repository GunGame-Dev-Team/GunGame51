# ../scripts/included/gg_winner_messages/gg_winner_messages_config.py

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
    'gungame51/included_addon_configs/gg_winner_messages.cfg')


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    generate_header(config)

    # Winner Messages
    config.text('')
    config.text('=' * 76)
    config.text('>> WINNER MESSAGES')
    config.text('=' * 76)
    config.text('Description:')
    config.text('   Sends messages to player when someone wins a round/match.')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not load gg_winner_messages.')
    config.text('   1 = (Enabled) Load gg_winner_messages.')
    config.text('Default Value: 0')
    config.cvar('gg_winner_messages', 0,
        'Enables/Disables gg_winner_messages.').addFlag('notify')

    config.write()
    es.dbgmsg(0, '\tgg_winner_messages.cfg')


def unload():
    global config

    # Remove the "notify" flags as set by addFlag('notify')
    for cvar in config.getCvars().keys():
        es.flags('remove', 'notify', cvar)

    # Delete the cfglib.AddonCFG instance
    del config
