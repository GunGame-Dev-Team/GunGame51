# ../core/cfg/files/gg_en_config.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
from __future__ import with_statement
from path import path

# GunGame Imports
from gungame51.core.cfg import ConfigContextManager


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    # Create the .cfg file
    with ConfigContextManager(path(__file__).namebase) as config:

        config.name = 'English Server Configuration'
        config.description = 'This file controls GunGame51 settings.'

        config.cfg_section('WEAPON SETTINGS')

        with config.cfg_cvar('gg_weapon_order_file') as cvar:

            cvar.name = 'WEAPON ORDER FILE'
            cvar.notes.append('The file must be ' +
                'located under "cfg/gungame51/weapon_orders/".')
            cvar.notes.append('Changing this variable ' +
                'in-game will result in a restart.')
            cvar.notes.append('If gg_weapon_order_random = 1' +
                ', this will be the starting weapon order.')
            cvar.default = 'default_weapon_order'
            cvar.text = 'The file that will be used for the weapon order.'
            cvar.notify = True

        with config.cfg_cvar('gg_weapon_order_random') as cvar:

            cvar.name = 'RANDOM WEAPON ORDER FILE'
            cvar.options.append('0 = (Disabled) use ' +
                'gg_weapon_order for a static weapon order.')
            cvar.options.append('1 = (Enabled) ' +
                'get a new weapon order each map change.')
            cvar.default = 0
            cvar.text = 'Randomly select a new weapon order file each map.'
            cvar.notify = True

        with config.cfg_cvar('gg_weapon_order_random_excluded') as cvar:

            cvar.name = 'RANDOM WEAPON ORDER EXCLUDED FILES'
            cvar.options.append('"" = (Disabled) No weapon ' +
                'orders are excluding when choosing a random')
            cvar.options.append([
                '"" = (Disabled) No weapon orders ' +
                    'are excluding when choosing a random',
                'weapon order with gg_weapon_order_random enabled above.',
                ])
            cvar.options.append([
                '"name1,name2" = (Enabled) Exclude ' +
                    'these orders when choosing a random',
                'weapon order with gg_weapon_order_random enabled above.',
                ])
            cvar.default = 'weapon_short,nade_bonus_order'
            cvar.text = ('Excluded orders when choosing ' +
                'a random order with gg_weapon_order_random.')
            cvar.notify = True

        with config.cfg_cvar('gg_weapon_order_sort_type') as cvar:

            cvar.name = 'WEAPON ORDER SORT TYPE'
            cvar.options.append('#default  = Order will go Top -> Bottom.')
            cvar.options.append('#reversed = Order will go Bottom -> Top.')
            cvar.options.append('#random   = Order will be randomly shuffled.')
            cvar.notes.append('#reversed and #random sort ' +
                'types will move hegrenade and knife levels')
            cvar.notes.append('to the end of the order.')
            cvar.default = '#default'
            cvar.text = ('The order in which ' +
                'the weapons and levels will be sorted.')
            cvar.notify = True

        with config.cfg_cvar('gg_multikill_override') as cvar:

            cvar.name = 'MULTIKILL OVERRIDE'
            cvar.notes.append([
                'Keep this variable set to 0 unless you want to override the',
                'values you have set in your weapon order file.',
                ])
            cvar.notes.append('This will not override ' +
                'hegrenade and knife, these are always 1.')
            cvar.default = 0
            cvar.text = ('The amount of kills a ' +
                'player needs to level up per weapon.')
            cvar.notify = True

        with config.cfg_cvar('gg_map_strip_exceptions') as cvar:

            cvar.name = 'WEAPON REMOVAL'
            cvar.notes.append('Only weapon_* entities are supported.')
            cvar.default = 'hegrenade,flashbang,smokegrenade'
            cvar.text = 'The weapons that will not be removed from the map.'

        config.cfg_section('MAP SETTINGS')

        with config.cfg_cvar('gg_multi_round') as cvar:

            cvar.name = 'MULTI-ROUND'
            cvar.notes.append('Only set this variable ' +
                'if you want more than one round per map change.')
            cvar.notes.append('The map vote ' +
                'will only trigger on the final round.')
            cvar.options.append('0 = Disabled.')
            cvar.options.append('# = The number of rounds ' +
                'that need to be played before a map change.')
            cvar.default = 0
            cvar.text = ('The number of rounds that ' +
                'need to be played before a map change.')

        with config.cfg_cvar('gg_multi_round_intermission') as cvar:

            cvar.name = 'MULTI-ROUND INTERMISSION'
            cvar.notes.append([
                'This option is only valid if ' +
                    '"gg_multi_round" is set to a value',
                'higher than "0".',
                ])
            cvar.notes.append([
                'This will load "gg_warmup_round" ' +
                    'based off of the "gg_warmup timer"',
                'between rounds.',
                ])
            cvar.notes.append('Without an intermission, the next ' +
                'GunGame round will start immediately after a win.')
            cvar.options.append('0 = Do not have an intermission.')
            cvar.options.append('1 = Enable the intermission.')
            cvar.default = 0
            cvar.text = ('The amount of time (in seconds) ' +
                'that the intermission lasts between rounds.')

        with config.cfg_cvar('gg_dynamic_chattime') as cvar:

            cvar.name = 'DYNAMIC END OF MAP CHAT TIME'
            cvar.notes.append('Dynamic chat time is ' +
                'based on the end of round winner music.')
            cvar.notes.append([
                'When enabled, the players will be able to chat for the',
                'length of the winner music.',
                ])
            cvar.notes.append('If disabled, the ' +
                '"mp_chattime" variable will be used.')
            cvar.options.append("0 = (Disabled) Use " +
                "the server\'s mp_chattime variable.")
            cvar.options.append('1 = (Enabled) Use the ' +
                'length of the individual audio file.')
            cvar.default = 0
            cvar.text = ('Enables dynamic end of round ' +
                'chat time based on the winner music.')

        config.cfg_section('PLAYER SETTINGS')

        with config.cfg_cvar('gg_player_defuser') as cvar:

            cvar.name = 'DEFUSERS'
            cvar.options.append('0 = Disabled')
            cvar.options.append('1 = Enabled')
            cvar.default = 0
            cvar.text = ('Automatically equip Counter-Terrorist ' +
                'players with defusal kits on bomb maps.')

        with config.cfg_cvar('gg_player_armor') as cvar:

            cvar.name = 'ARMOR'
            cvar.options.append('0 = No armor')
            cvar.options.append('1 = Kevlar only')
            cvar.options.append('2 = Assaultsuit (Kevlar + Helmet)')
            cvar.default = 2
            cvar.text = ('The type of armor players ' +
                'are equipped with when they spawn.')

        config.cfg_section('SOUND SETTINGS')

        with config.cfg_cvar('gg_soundpack') as cvar:

            cvar.name = 'SOUND PACK'
            cvar.notes.append('Sound packs are located in ' +
                '"../cstrike/cfg/gungame51/sound_packs".')
            cvar.notes.append([
                'The INI file names located in ' +
                    'the "sound_packs" directory minus',
                'the ".ini" extension are what you ' +
                    'would use when declaring the',
                'default sound pack that players will ' +
                    'hear when sounds are played.',
                ])
            cvar.default = 'default'
            cvar.text = 'Controls which sound pack will be used by default.'
