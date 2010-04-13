# ../addons/eventscripts/gungame51/core/cfg/files/gg_en_config.py

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
    config.text('Note:')
    config.text('   #reversed and #random sort types will move hegrenade ' +
                'and knife levels')
    config.text('   to the end of the order.')
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
                'map.')

    config.text('')
    config.text('')
    config.text('+'*76)
    config.text('|' + ' '*31 + 'MAP SETTINGS' + ' '*31 + '|')
    config.text('+'*76)

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
                'played before a map change.')

    # Multi-Round Intermission
    config.text('')
    config.text('='*76)
    config.text('>> MULTI-ROUND INTERMISSION')
    config.text('='*76)
    config.text('Notes:')
    config.text('   * This option is only valid if "gg_multi_round" is set ' +
                'to a value')
    config.text('     higher than "0".')
    config.text('   * This will load "gg_warmup_round" based off of the ' +
                '"gg_warmup timer"')
    config.text('     between rounds.')
    config.text('   * Without an intermission, the next GunGame round will ' +
                'start immediately after a win.')
    config.text('Options:')
    config.text('   0 = Do not have an intermission.')
    config.text('   1 = Enable the intermission.')
    config.text('Default Value: 0')
    config.cvar('gg_multi_round_intermission', 0, 'The amount of time (in ' +
                'seconds) that the intermission lasts between rounds.')

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
                ' time based on the winner music.')
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
                'maps.')

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
    config.cvar('gg_player_armor', 2, 'The type of armor players are ' +
                'equipped with when they spawn.')
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
                'will be used by default.')

    # This line creates/updates the .cfg file
    config.write()

    # Print to console to show successfule loading of the config
    es.dbgmsg(0, '\tgg_en_config.cfg')
    
def unload():
    global config
    
    # Remove the "notify" and "replicated" flags as set by makepublic()
    for cvar in config.getCvars().keys():
        es.flags('remove', 'notify', cvar)
    
    # Delete the cfglib.AddonCFG instance
    del config