# ../addons/eventscripts/gungame/core/cfg/files/gg_punishment_settings.py

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
config = cfglib.AddonCFG('%s/cfg/gungame51/gg_punishment_settings.cfg'
        %es.ServerVar('eventscripts_gamedir'))
        
# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    config.text('*'*76)
    config.text('*' + ' '*24 + 'gg_punishment_settings.cfg' + ' '*24 + '*')
    config.text('*' + ' '*74 + '*')
    config.text('*' + ' '*14 + 'This file controls GunGame punishment ' +
                'settings.' + ' '*13 + '*')
    config.text('*' + ' '*74 + '*')
    config.text('*  Note: Any alteration of this file requires a server ' +
                'restart or a' + ' '*8 + '*')
    config.text('*' + ' '*11 + 'reload of GunGame.' + ' '*45 + '*')
    config.text('*'*76)
    config.text('')
    config.text('')
    
    
    # AFK Rounds
    config.text('='*76)
    config.text('>> AFK ROUNDS')
    config.text('='*76)
    config.text('Options:')
    config.text('   0  = Disabled')
    config.text('   # = The number of rounds the player can be AFK before ' +
                'punishment')
    config.text('       occurs.')
    config.text('Default Value: 0')
    config.cvar('gg_afk_rounds', 0, 'The number of rounds a player can be ' +
                'AFK before punishment occurs.')

    # AFK Rounds Punishment
    config.text('')
    config.text('='*76)
    config.text('>> AFK PUNISHMENT')
    config.text('='*76)
    config.text('Notes:')
    config.text('  * Requires "gg_afk_rounds 1" or higher')
    config.text('Options:')
    config.text('   0 = No punishment.')
    config.text('   1 = Kick the player.')
    config.text('   2 = Move the player to spectator.')
    config.text('Default Value: 0')
    config.cvar('gg_afk_punish', 0, 'The punishment for players who are AFK ' +
                'longer than "gg_afk_rounds".')

    # Suicide Punishment
    config.text('')
    config.text('='*76)
    config.text('>> SUICIDE PUNISHMENT')
    config.text('='*76)
    config.text('Options:')
    config.text('   0 = No punishment.')
    config.text('   # = The number of levels a player will lose if they ' +
                'commit suicide.')
    config.text('Default Value: 0')
    config.cvar('gg_suicide_punish', 0, 'The number of levels a player ' +
                'will lose if they commit suicide.')

    # Team Kill Punishment
    config.text('')
    config.text('='*76)
    config.text('>> TEAM KILL PUNISHMENT')
    config.text('='*76)
    config.text('Options:')
    config.text('   0 = No punishment.')
    config.text('   # = The number of levels a player will lose if they kill' +
                ' a')
    config.text('       teammate.')
    config.text('Default Value: 0')
    config.cvar('gg_tk_punish', 0, 'The number of levels a player will lose ' +
                'if they kill a teammate.')

    # Retry Punishment
    config.text('')
    config.text('='*76)
    config.text('>> RETRY/RECONNECT PUNISHMENT')
    config.text('='*76)
    config.text('Options:')
    config.text('   0 = No punishment.')
    config.text('   # = The number of levels a player will lose if they ' +
                'reconnect')
    config.text('       in the same round.')
    config.text('Default Value: 0')
    config.cvar('gg_retry_punish', 0, 'The number of levels a player will ' +
                'lose if they reconnect in the same round.')

    # This line creates/updates the .cfg file
    config.write()

    # Print to console to show successfule loading of the config
    es.dbgmsg(0, '\tgg_punishment_settings.cfg')
    
def unload():
    global config
    
    # Remove the "notify" and "replicated" flags as set by makepublic()
    for cvar in config.getCvars().keys():
        es.flags('remove', 'notify', cvar)
    
    # Delete the cfglib.AddonCFG instance
    del config