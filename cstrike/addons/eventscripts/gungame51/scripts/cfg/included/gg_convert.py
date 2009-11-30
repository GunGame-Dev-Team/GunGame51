# ../addons/eventscripts/gungame/scripts/cfg/included/gg_convert.py

'''
$Rev$
$LastChangedBy: Monday $
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
    'gungame51/included_addon_configs/gg_convert.cfg')
        
# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    config.text('*'*76)
    config.text('*' + ' ' + 'gg_convert.cfg -- Winners Database & ' +
                'Spawnpoints Converter Configuration' + ' ' + '*')
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
    
    # gg_convert
    config.text('')
    config.text('='*76)
    config.text('>> CONVERT')
    config.text('='*76)
    config.text('Description:')
    config.text('   A tool used to convert gungame 3, 4 and 5 (prior to 5.1' +
                ') winner databases & spawnpoint files.')
    config.text('Instructions:')
    config.text('   * Place a copy of your winners database or spawnpoint ' +
                'files in this folder:')
    config.text('       ../cfg/gungame51/gg_convert/')
    config.text('   * Database files include:')
    config.text('       GunGame3: es_gg_winners_db.txt')
    config.text('       GunGame4: es_gg_database.sqldb')
    config.text('       GunGame5: winnersdata.db')
    config.text('Options:')
    config.text('   0 = (Disabled)')
    config.text('   1 = (Enabled) Add together the current and converted ' +
                'wins for each player and combine spawnpoints.')
    config.text('   2 = (Enabled) Replace the current winners and ' +
                'spawnpoints with the converted ones.')
    config.text('Default Value: 0')
    config.cvar('gg_convert', 0, 'Enables/Disables ' +
                'gg_convert.')
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