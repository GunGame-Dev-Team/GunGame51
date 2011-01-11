# ../core/cfg/files/gg_default_addons_config.py

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

# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
config = cfglib.AddonCFG('%s/cfg/gungame51/gg_default_addons.cfg'
    % es.ServerVar('eventscripts_gamedir'))


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    config.text('*' * 76)
    config.text('*' + ' ' * 11 + 'gg_default_addons.cfg -- Default Addon ' +
                'Configuration' + ' ' * 11 + '*')
    config.text('*' + ' ' * 74 + '*')
    config.text('*' + ' ' * 17 + 'This file defines GunGame Addon settings.' +
                ' ' * 16 + '*')
    config.text('*' + ' ' * 74 + '*')
    config.text('*  Note: Any alteration of this file requires a server ' +
                'restart or a' + ' ' * 8 + '*')
    config.text('*' + ' ' * 11 + 'reload of GunGame.' + ' ' * 45 + '*')
    config.text('*' * 76)
    config.text('')
    config.text('')

    # Stats Database Prune
    config.text('')
    config.text('=' * 76)
    config.text('>> STATS DATABASE PRUNE')
    config.text('=' * 76)
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

    config.write()
    es.dbgmsg(0, '\tgg_default_addons.cfg')


def unload():
    global config

    # Remove the "notify" flags as set by addFlag('notify')
    for cvar in config.getCvars().keys():
        es.flags('remove', 'notify', cvar)

    # Delete the cfglib.AddonCFG instance
    del config
