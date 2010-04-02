# ../addons/eventscripts/gungame/scripts/cfg/included/gg_handicap_config.py

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
    'gungame51/included_addon_configs/gg_handicap.cfg')
        
# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    generate_header(config)
    
    # Handicap
    config.text('')
    config.text('='*76)
    config.text('>> HANDICAP')
    config.text('='*76)
    config.text('Description:')
    config.text('   Helps newly connected players by adjusting their level.')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not load gg_handicap.')
    config.text('   1 = Set player to the lowest level of all the other ' +
                'players.')
    config.text('       Basically "catching them up".')
    config.text('Default Value: 0')
    config.cvar('gg_handicap', 0, 'Helps newly connected players by ' +
                'adjusting their level.').addFlag('notify')

    # Handicap Update
    config.text('')
    config.text('='*76)
    config.text('>> HANDICAP UPDATE')
    config.text('='*76)
    config.text('Description:')
    config.text('   A timer (in seconds) that updates players with the ' +
                'lowest level to the')
    config.text('   lowest level of the other players. Basically "catching ' +
                'them up".')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not load gg_handicap_update.')
    config.text('   180 = (Enabled) Update the lowest level players')
    config.text('                    every 180 seconds (3 minutes).')
    config.text('Default Value: 0')
    config.cvar('gg_handicap_update', 0, 'The time (in seconds) to update ' +
                'players\' levels using handicap.')
    
    config.write()
    es.dbgmsg(0, '\tgg_handicap.cfg')

def unload():
    global config

    # Remove the "notify" flags as set by addFlag('notify')
    for cvar in config.getCvars().keys():
        es.flags('remove', 'notify', cvar)
    
    # Delete the cfglib.AddonCFG instance
    del config