# ../addons/eventscripts/gungame/core/cfg/files/gg_afk_settings.py

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

# ============================================================================
# >> GLOBAL VARIABLES
# ============================================================================
config = cfglib.AddonCFG('%s/cfg/gungame51/gg_afk_settings.cfg'
        %es.ServerVar('eventscripts_gamedir'))
        
# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    config.text('*'*76)
    config.text('*' + ' '*28 + 'gg_afk_settings.cfg' + ' '*27 + '*')
    config.text('*' + ' '*74 + '*')
    config.text('*' + ' '*17 + 'This file controls GunGame AFK settings.' +
                ' '*17 + '*')
    config.text('*' + ' '*74 + '*')
    config.text('*  Note: Any alteration of this file requires a server ' +
                'restart or a' + ' '*8 + '*')
    config.text('*' + ' '*11 + 'reload of GunGame.' + ' '*45 + '*')
    config.text('*'*76)
    config.text('')
    config.text('')

    # AFK Leveling
    config.text('='*76)
    config.text('>> AFK LEVELING')
    config.text('='*76)
    config.text('Options:')
    config.text('   0 = Do not allow attackers to level up with AFK kills.')
    config.text('   1 = Allow attackers to level up with AFK kills.')
    config.text('Default Value: 0')
    config.cvar('gg_allow_afk_levels', 0, 'Allow attackers to level up with ' +
                'AFK kills.')
                
    # AFK Leveling Knife
    config.text('')
    config.text('')
    config.text('='*76)
    config.text('>> AFK LEVELING (KNIFE LEVEL)')
    config.text('='*76)
    config.text('Notes:')
    config.text('   * Requires "gg_allow_afk_levels 1"')
    config.text('Options:')
    config.text('   0 = Do not allow attackers to level up with AFK kills ' +
                'when on knife level.')
    config.text('   1 = Allow attackers to level up with AFK kills when on ' +
                'knife level.')
    config.text('Default Value: 0')
    config.cvar('gg_allow_afk_levels_knife', 0, 'Allow attackers to level ' +
                'up with AFK kills when on knife level.')
                
    # AFK Leveling HEGrenade
    config.text('')
    config.text('')
    config.text('='*76)
    config.text('>> AFK LEVELING (HEGRENADE LEVEL)')
    config.text('='*76)
    config.text('Notes:')
    config.text('   * Requires "gg_allow_afk_levels 1"')
    config.text('Options:')
    config.text('   0 = Do not allow attackers to level up with AFK kills ' +
                'when on HeGrenade level.')
    config.text('   1 = Allow attackers to level up with AFK kills when on ' +
                'HeGrenade level.')
    config.text('Default Value: 0')
    config.cvar('gg_allow_afk_levels_nade', 0, 'Allow attackers to level up ' +
                'with AFK kills when on HEGrenade level.')

    # This line creates/updates the .cfg file
    config.write()

    # Print to console to show successfule loading of the config
    es.dbgmsg(0, '\tgg_afk_settings.cfg')
    
def unload():
    global config
    
    # Remove the "notify" and "replicated" flags as set by makepublic()
    for cvar in config.getCvars().keys():
        es.flags('remove', 'notify', cvar)
    
    # Delete the cfglib.AddonCFG instance
    del config