# ../addons/eventscripts/gungame51/scripts/cfg/included/gg_welcome_msg_config.py

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
    'gungame51/included_addon_configs/gg_welcome_msg.cfg')
        
# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    generate_header(config)
    
    # gg_welcome_msg
    config.text('')
    config.text('='*76)
    config.text('>> GUNGAME WELCOME MESSAGE')
    config.text('='*76)
    config.text('Description:')
    config.text('   A menu displayed to newly connected players displaying ' +
                'server and addon')
    config.text('information.')
    config.text('   Players can type !welcome to bring this menu back up.')
    config.text('Note:')
    config.text('   The configureable message is available in' +
                '"gg_stats_logging.txt".')
    config.text('Options:')
    config.text('   0 = (Disabled)')
    config.text('   1 = (Enabled)')
    config.text('Default Value: 0')
    config.cvar('gg_welcome_msg', 0, 'Enables/Disables ' +
                'gg_welcome_msg.').addFlag('notify')
    config.text('')

    # gg_welcome_msg_timeout
    config.text('')
    config.text('='*76)
    config.text('>> GUNGAME WELCOME MESSAGE TIMEOUT')
    config.text('='*76)
    config.text('Description:')
    config.text('   The number (in seconds) it takes for the welcome message' +
                ' to dissappear.')
    config.text('Options:')
    config.text('   (#) = (#) seconds')
    config.text('   10 = 10 seconds')
    config.text('Default Value: 10')
    config.cvar('gg_welcome_msg_timeout', 10, 'Sets the number of seconds ' +
                'for gg_welcome_msg_timeout.')
    config.text('')

    config.write()
    es.dbgmsg(0, '\tgg_welcome_msg.cfg')

def unload():
    global config

    # Remove the "notify" flags as set by addFlag('notify')
    for cvar in config.getCvars().keys():
        es.flags('remove', 'notify', cvar)
    
    # Delete the cfglib.AddonCFG instance
    del config