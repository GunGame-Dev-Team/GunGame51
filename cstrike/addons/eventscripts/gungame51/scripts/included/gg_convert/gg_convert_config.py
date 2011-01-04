# ../addons/eventscripts/gungame51/scripts/included/gg_convert/gg_convert_config.py

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
    'gungame51/included_addon_configs/gg_convert.cfg')
        
# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    generate_header(config)

    # gg_convert
    config.text('')
    config.text('='*76)
    config.text('>> CONVERT')
    config.text('='*76)
    config.text('Description:')
    config.text('   A tool used to convert gungame 3, 4 and 5 (prior to 5.1' +
                ') winner databases')
    config.text('& spawnpoint files.')
    config.text('Instructions:')
    config.text('   * Place a copy of your winners database or spawnpoint ' +
                'files in this')
    config.text('folder:')
    config.text('       ../cfg/gungame51/converter/')
    config.text('   * Database files include:')
    config.text('       GunGame3: es_gg_winners_db.txt')
    config.text('       GunGame4: es_gg_database.sqldb')
    config.text('       GunGame5: winnersdata.db')
    config.text('Note:')
    config.text('   GunGame5.0 SpawnPoint files have not been changed in ' +
                'GunGame5.1.')
    config.text('        (Simply drag them to ../cfg/gungame51/spawnpoints/)')
    config.text('Options:')
    config.text('   0 = (Disabled)')
    config.text('   1 = (Enabled) Add together the current and converted ' +
                'wins for each player')
    config.text('and combine spawnpoints.')
    config.text('   2 = (Enabled) Replace the current winners and ' +
                'spawnpoints with the')
    config.text('converted ones.')
    config.text('Default Value: 0')
    config.cvar('gg_convert', 0, 'Enables/Disables ' +
                'gg_convert.').addFlag('notify')
    config.text('')

    config.write()
    es.dbgmsg(0, '\tgg_convert.cfg')

def unload():
    global config

    # Remove the "notify" flags as set by addFlag('notify')
    for cvar in config.getCvars().keys():
        es.flags('remove', 'notify', cvar)
    
    # Delete the cfglib.AddonCFG instance
    del config