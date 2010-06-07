# ../addons/eventscripts/gungame51/scripts/cfg/included/gg_warmup_round.py

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
    'gungame51/included_addon_configs/gg_warmup_round.cfg')
        
# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    generate_header(config)
    
    # Warmup Round
    config.text('')
    config.text('='*76)
    config.text('>> WARMUP ROUND')
    config.text('='*76)
    config.text('Notes:')
    config.text('   * Players cannot level up during the warmup round.')
    config.text('   * Warmup round is triggered at the start of each map ' +
                'change.')
    config.text('Options:')
    config.text('   0 = Disabled.')
    config.text('   1 = Enabled.')
    config.text('Default Value: 0')
    config.cvar('gg_warmup_round', 0, 'Enables or disables warmup' +
                'round.').addFlag('notify')

    # Warmup Round Timer
    config.text('')
    config.text('='*76)
    config.text('>> WARMUP ROUND TIMER')
    config.text('='*76)
    config.text('Options:')
    config.text('   # = The amount of time (in seconds) that the warmup ' +
                'round will last.')
    config.text('Default Value: 30')
    config.cvar('gg_warmup_timer', 30, 'The amount of time (in seconds) ' +
                'that the the warmup round will last.')

    # Warmup Round Weapon
    config.text('')
    config.text('='*76)
    config.text('>> WARMUP ROUND WEAPON')
    config.text('='*76)
    config.text('Notes:')
    config.text('   * Only supports "weapon_*" entities.')
    config.text('   * Warmup round is triggered at the start of each map ' +
                'change.')
    config.text('Options:')
    config.text('\tawp   \tscout\taug   \tmac10\ttmp   \tmp5navy\tump45\tp90')
    config.text('\tgalil\tfamas\tak47\tsg552\tsg550\tg3sg1\tm249\tm3')
    config.text('\txm1014\tm4a1\tglock\tusp   \tp228\tdeagle\telite\t' +
                'fiveseven')
    config.text('\thegrenade\tknife')
    config.text('')
    config.text('\t0 = The first level weapon')
    config.text('\tweapon1,weapon2,weapon3 = For each warmup, one of these ' +
                'weapons is chosen')
    config.text('\t#random = For each warmup, a random weapon is chosen.')
    config.text('Default Value: "hegrenade"')
    config.cvar('gg_warmup_weapon', 'hegrenade', 'The weapon that players ' +
                'will use during the warmup round.')

    # Warmup Round Deathmatch Mode
    config.text('')
    config.text('='*76)
    config.text('>> WARMUP ROUND DEATHMATCH MODE')
    config.text('='*76)
    config.text('Notes:')
    config.text('   * Please check the gg_deathmatch.cfg for information' +
                ' regarding')
    config.text('     what is required to be enabled and disabled when')
    config.text('     running gg_deathmatch.')
    config.text('Options:')
    config.text('   0 = Disabled.')
    config.text('   1 = Enabled.')
    config.text('Default Value: 0')
    config.cvar('gg_warmup_deathmatch', 0, 'Enable deathmatch during warmup ' +
                'round only.')

    # Warmup Round Elimination Mode
    config.text('')
    config.text('='*76)
    config.text('>> WARMUP ROUND ELIMINATION MODE')
    config.text('='*76)
    config.text('Notes:')
    config.text('   * Please check the gg_elimination.cfg for information' +
                ' regarding')
    config.text('     what is required to be enabled and disabled when')
    config.text('     running gg_elimination.')
    config.text('Options:')
    config.text('   0 = Disabled.')
    config.text('   1 = Enabled.')
    config.text('Default Value: 0')
    config.cvar('gg_warmup_elimination', 0, 'Enable elimination during ' +
                'warmup round only.')    
    
    config.write()
    es.dbgmsg(0, '\tgg_warmup_round.cfg')

def unload():
    global config

    # Remove the "notify" flags as set by addFlag('notify')
    for cvar in config.getCvars().keys():
        es.flags('remove', 'notify', cvar)
    
    # Delete the cfglib.AddonCFG instance
    del config