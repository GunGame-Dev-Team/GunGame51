# ../cstrike/addons/eventscripts/gungame/core/cfg/files/gg_en_config.py

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
config = cfglib.AddonCFG('%s/cfg/gungame51/gg_en_config.cfg'
        %es.ServerVar('eventscripts_gamedir'))
        
# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    config.text('*'*76)
    config.text('*' + ' '*13 + 'gg_en_config.cfg -- English Server' +
                ' Configuration' + ' '*13 + '*')
    config.text('*' + ' '*74 + '*')
    config.text('*' + ' '*19 + 'This file controls GunGame settings.' +
                ' '*19 + '*')
    config.text('*' + ' '*74 + '*')
    config.text('*  Note: Any alteration of this file requires a server ' +
                'restart or a' + ' '*8 + '*')
    config.text('*' + ' '*11 + 'reload of GunGame.' + ' '*45 + '*')
    config.text('*'*76)
    config.text('')
    config.text('')

    config.text('+'*76)
    config.text('|' + ' '*29 + 'WEAPON SETTINGS' + ' '*30 + '|')
    config.text('+'*76)

    # Weapon Order File
    config.text('')
    config.text('')
    config.text('='*76)
    config.text('>> WEAPON ORDER FILE')
    config.text('='*76)
    config.text('Notes:')
    config.text('   * The file must be located under ' +
                '"cfg/gungame5/weapon_orders/".')
    config.text('   * Changing this variable in-game will result in a' +
                'restart.')
    config.text('   * If gg_weapon_order_random = 1, this will be the ' +
                'starting weapon')
    config.text('     order.')
    config.text('Default Value: "default_weapon_order"')
    config.cvar('gg_weapon_order_file', 'default_weapon_order', 'The file ' +
                'that will be used for the weapon order.').addFlag('notify')

    # Random Weapon Order File
    config.text('')
    config.text('='*76)
    config.text('>> RANDOM WEAPON ORDER FILE')
    config.text('='*76)
    config.text('Options:')
    config.text('   0 = (Disabled) use gg_weapon_order for a static weapon ' +
                'order.')
    config.text('   1 = (Enabled) get a new weapon order each map change.')
    config.text('Default Value: 0')
    config.cvar('gg_weapon_order_random', 0, 'Randomly select a new weapon ' +
                'order file each map.').addFlag('notify')

    # Weapon Order Sort Type
    config.text('')
    config.text('='*76)
    config.text('>> WEAPON ORDER SORT TYPE')
    config.text('='*76)
    config.text('Options:')
    config.text('   #default  = Order will go Top -> Bottom.')
    config.text('   #reversed = Order will go Bottom -> Top.')
    config.text('   #random   = Order will be randomly shuffled.')
    config.text('Default Value: "#default"')
    config.cvar('gg_weapon_order_sort_type', '#default', 'The order in which' +
                ' the weapons and levels will be sorted.').addFlag('notify')

    # Multikill Override
    config.text('')
    config.text('='*76)
    config.text('>> MULTIKILL OVERRIDE')
    config.text('='*76)
    config.text('Notes:')
    config.text('   * Keep this variable set to 0 unless you want to ' +
                'override the')
    config.text('     values you have set in your weapon order file.')
    config.text('   * This will not override hegrenade and knife, these are ' +
                'always 1.')
    config.text('Default Value: 0')
    config.cvar('gg_multikill_override', 0, 'The amount of kills a player ' +
                'needs to level up per weapon.').addFlag('notify')

    # Weapon Removal
    config.text('')
    config.text('='*76)
    config.text('>> WEAPON REMOVAL')
    config.text('='*76)
    config.text('Note:')
    config.text('   * Only weapon_* entities are supported.')
    config.text('Default Value: "hegrenade,flashbang,smokegrenade"')
    config.cvar('gg_map_strip_exceptions', 'hegrenade,flashbang,smokegrenade',
                'The weapons that will not be removed from the ' +
                'map.').addFlag('notify')

    config.text('')
    config.text('')
    config.text('+'*76)
    config.text('|' + ' '*24 + 'PLAYER PUNISHMENT SETTINGS' + ' '*24 + '|')
    config.text('+'*76)

    # AFK Rounds
    config.text('')
    config.text('')
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
                'AFK before punishment occurs.').addFlag('notify')

    # AFK Rounds Punishment
    config.text('')
    config.text('='*76)
    config.text('>> AFK ROUNDS PUNISHMENT ACTION')
    config.text('='*76)
    config.text('Options:')
    config.text('   0 = No punishment.')
    config.text('   1 = Kick the player.')
    config.text('   2 = Move the player to spectator.')
    config.text('Default Value: 0')
    config.cvar('gg_afk_action', 0, 'The punishment for players who are AFK ' +
                'longer than "gg_afk_rounds".').addFlag('notify')

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
                'will lose if they commit suicide.').addFlag('notify')

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
                'if they kill a teammate.').addFlag('notify')

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
                'lose if they reconnect in the same round.').addFlag('notify')

    config.text('')
    config.text('')
    config.text('+'*76)
    config.text('|' + ' '*31 + 'MAP SETTINGS' + ' '*31 + '|')
    config.text('+'*76)

    # Map Objectives
    config.text('')
    config.text('')
    config.text('='*76)
    config.text('>> MAP OBJECTIVES')
    config.text('='*76)
    config.text('Options:')
    config.text('   0 = All objectives disabled.')
    config.text('   1 = Bomb objective disabled.')
    config.text('   2 = Hostage objectives disabled.')
    config.text('   3 = No objectives disabled.')
    config.text('Default Value: 0')
    config.cvar('gg_map_obj', 0, 'Controls which objectives will be' +
                'disabled.').addFlag('notify')

    # Multi-Round
    config.text('')
    config.text('='*76)
    config.text('>> MULTI-ROUND')
    config.text('='*76)
    config.text('Notes:')
    config.text('   * Only set this variable if you want more than one ' +
                'round per map')
    config.text('     change.')
    config.text('   * The map vote will only trigger on the final round.')
    config.text('Options:')
    config.text('   0 = Disabled.')
    config.text('   # = The number of rounds that need to be played before ' +
                'a map')
    config.text('       change.')
    config.text('Default Value: 0')
    config.cvar('gg_multi_round', 0, 'The number of rounds that need to be ' +
                'played before a map change.').addFlag('notify')

    # Multi-Round Intermission
    config.text('')
    config.text('='*76)
    config.text('>> MULTI-ROUND INTERMISSION')
    config.text('='*76)
    config.text('Notes:')
    config.text('   * This option is only valid if "gg_multi_round" is set ' +
                'to a value')
    config.text('     higher than "0".')
    config.text('   * This will start an intermission timer similar to the ' +
                'warmup timer')
    config.text('     between rounds.')
    config.text('Options:')
    config.text('   # = The amount of time (in seconds) that the ' +
                'intermission lasts')
    config.text('       between rounds.')
    config.text('Default Value: 20')
    config.cvar('gg_multi_round', 20, 'The amount of time (in seconds) that ' +
                'the intermission lasts between rounds.').addFlag('notify')

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
                'that the the warmup round will last.').addFlag('notify')

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
    config.text('\thegrenade')
    config.text('\t0 = The first level weapon')
    config.text('Default Value: "hegrenade"')
    config.cvar('gg_warmup_weapon', 'hegrenade', 'The weapon that players ' +
                'will use during the warmup round.').addFlag('notify')

    # Warmup Round Deathmatch Mode
    config.text('')
    config.text('='*76)
    config.text('>> WARMUP ROUND DEATHMATCH MODE')
    config.text('='*76)
    config.text('Notes:')
    config.text('   * Requires the usage of "gg_respawn_cmd" (found below).')
    config.text('   * Please check the gg_default_addons.cfg for information' +
                ' regarding')
    config.text('     what is required to be enabled and disabled when')
    config.text('     running gg_deathmatch.')
    config.text('   * It is not necessary to enable deathmatch mode for the ' +
                'warmup')
    config.text('     round if "gg_deathmatch" has been set to "1".')
    config.text('Options:')
    config.text('   0 = Disabled.')
    config.text('   1 = Enabled.')
    config.text('Default Value: 0')
    config.cvar('gg_warmup_deathmatch', 0, 'Enable deathmatch during warmup ' +
                'round only.').addFlag('notify')

    # Warmup Round Elimination Mode
    config.text('')
    config.text('='*76)
    config.text('>> WARMUP ROUND ELIMINATION MODE')
    config.text('='*76)
    config.text('Notes:')
    config.text('   * Requires the usage of "gg_respawn_cmd" (found below).')
    config.text('   * Please check the gg_default_addons.cfg for information' +
                ' regarding')
    config.text('     what is required to be enabled and disabled when')
    config.text('     running gg_elimination.')
    config.text('   * It is not necessary to enable elimination mode for the' +
                ' warmup')
    config.text('     round if "gg_elimination" has been set to "1".')
    config.text('Options:')
    config.text('   0 = Disabled.')
    config.text('   1 = Enabled.')
    config.text('Default Value: 0')
    config.cvar('gg_warmup_elimination', 0, 'Enable elimination during ' +
                'warmup round only.').addFlag('notify')

    # Dynamic End of Map Chat Time
    config.text('')
    config.text('='*76)
    config.text('>> DYNAMIC END OF MAP CHAT TIME')
    config.text('='*76)
    config.text('Notes:')
    config.text('   * Dynamic chat time is based on the end of round winner ' +
                'music.')
    config.text('   * When enabled, the players will be able to chat for the' +
                ' length')
    config.text('     of the winner music.')
    config.text('   * If disabled, the "mp_chattime" variable will be used.')
    config.text('Options:')
    config.text('   0 = (Disabled) Use the server\'s mp_chattime variable.')
    config.text('   1 = (Enabled) Use the length of the individual audio ' +
                'file.')
    config.text('Default Value: 0')
    config.cvar('gg_dynamic_chattime', 0, 'Enables dynamic end of round chat' +
                ' time based on the winner music.').addFlag('notify')
    config.text('')
    config.text('')


    config.text('+'*76)
    config.text('|' + ' '*29 + 'PLAYER SETTINGS' + ' '*30 + '|')
    config.text('+'*76)


    # Defusers
    config.text('')
    config.text('')
    config.text('='*76)
    config.text('>> DEFUSERS')
    config.text('='*76)
    config.text('Options:')
    config.text('   0 = Disabled')
    config.text('   1 = Enabled')
    config.text('Default Value: 0')
    config.cvar('gg_player_defuser', 0, 'Automatically equip Counter-' +
                'Terrorist players with defusal kits on bomb ' +
                'maps.').addFlag('notify')

    # Armor
    config.text('')
    config.text('='*76)
    config.text('>> ARMOR')
    config.text('='*76)
    config.text('Options:')
    config.text('   0 = No armor')
    config.text('   1 = Kevlar only')
    config.text('   2 = Assaultsuit (Kevlar + Helmet)')
    config.text('Default Value: 2')
    config.cvar('gg_player_defuser', 2, 'The type of armor players are ' +
                'equipped with when they spawn.').addFlag('notify')
    config.text('')
    config.text('')


    config.text('+'*76)
    config.text('|' + ' '*30 + 'SOUND SETTINGS' + ' '*30 + '|')
    config.text('+'*76)


    # Sound Pack
    config.text('')
    config.text('')
    config.text('='*76)
    config.text('>> SOUND PACK')
    config.text('='*76)
    config.text('Notes:')
    config.text('   * Sound packs are located in "../cstrike/cfg/gungame5/' +
                'sound_packs".')
    config.text('   * The INI file names located in the "sound_packs" ' +
                'directory minus')
    config.text('     the ".ini" extension are what you would use when ' +
                'declaring the')
    config.text('     default sound pack that players will hear when sounds' +
                ' are played.')
    config.text('Default Value: "default"')
    config.cvar('gg_soundpack', 'default', 'The controls which sound pack ' +
                'will be used by default.').addFlag('notify')
    config.text('')

    # Leader Weapon Warning
    config.text('')
    config.text('='*76)
    config.text('>> LEADER WEAPON WARNING')
    config.text('='*76)
    config.text('Note:')
    config.text('   * Announces via sound at the beginning of each round ' +
                'when a player')
    config.text('     has reached either "hegrenade" or "knife" level.')
    config.text('Options:')
    config.text('   0 = Disabled.')
    config.text('   1 = Enabled.')
    config.text('Default Value: 0')
    config.cvar('gg_leaderweapon_warning', 0, 'Play a sound when a player ' +
                'reaches "hegrenade" or "knife" level.').addFlag('notify')
    config.text('')
    config.text('')


    config.text('+'*76)
    config.text('|' + ' '*26 + 'MISCELLANEOUS SETTINGS' + ' '*26 + '|')
    config.text('+'*76)


    # Respawn Command
    config.text('')
    config.text('')
    config.text('='*76)
    config.text('>> RESPAWN COMMAND')
    config.text('='*76)
    config.text('Note:')
    config.text('   * This setting is required for "gg_deathmatch".')
    config.text('   * This setting is required for "gg_elimination".')
    config.text('   * This setting is required if you plan on respawning ' +
                'players')
    config.text('     using GunGame.')
    config.text('   * Options listed below are not "all-inclusive". Any ' +
                'command that')
    config.text('     can be issued via console to respawn a player via ' +
                'userid can')
    config.text('     be used for this setting.')
    config.text('   * All options to respawn players current require an ' +
                'external')
    config.text('     plugin (ES Tool, GunGame Utils, Sourcemod, etc.) to be' +
                ' able to')
    config.text('     respawn players. Be sure that you have installed the ' +
                'appropriate')
    config.text('     plugin prior to attempting to use this option. ' +
                'Otherwise, players')
    config.text('     will not respawn.')
    config.text('Options:')
    config.text('\t"est_spawn"\t"gg_spawn"\t"sm_respawn #"')
    config.text('Default Value: "est_spawn"')
    config.cvar('gg_respawn_cmd', 'est_spawn', 'The console command that is ' +
                'used to respawn a player.').addFlag('notify')

    # This line creates/updates the .cfg file
    config.write()
    
    # Execute the config
    config.execute()

    # Print to console to show successfule loading of the config
    es.dbgmsg(0, '\tgg_en_config.cfg')
    
def unload():
    global config
    
    # Remove the "notify" and "replicated" flags as set by makepublic()
    for cvar in config.getCvars().keys():
        es.flags('remove', 'notify', cvar)
    
    # Delete the cfglib.AddonCFG instance
    del config