# ../scripts/included/gg_warmup_round/gg_warmup_round_config.py

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

# EventScripts Imports
#   Cfglib
from cfglib import AddonCFG

# GunGame Imports
from gungame51.core import get_game_dir
#   Cfg
from gungame51.core.cfg.configs import ConfigContextManager


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():

    # Create the cfg file
    with ConfigContextManager(
      path(__file__).parent.split('scripts')[~0][1:]) as config:

        # Create the gg_warmup_round instance
        with config.cfg_cvar('gg_warmup_round') as cvar:

            cvar.name = 'WARMUP ROUND'
            cvar.notes.append('Players cannot ' +
                'level up during the warmup round.')
            cvar.notes.append('Warmup round is triggered ' +
                'at the start of each map change.')
            cvar.options.append('0 = Disabled.')
            cvar.options.append('1 = Enabled.')
            cvar.default = 0
            cvar.text = 'Enables or disables warmupround.'

        # Create the gg_warmup_timer instance
        with config.cfg_cvar('gg_warmup_timer') as cvar:

            cvar.name = 'WARMUP ROUND TIMER'
            cvar.options.append('The amount of time (in ' +
                'seconds) that the warmup round will last.')
            cvar.default = 30
            cvar.text = ('The amount of time (in ' +
                'seconds) that the the warmup round will last.')

        # Create the gg_warmup_weapon instance
        with config.cfg_cvar('gg_warmup_weapon') as cvar:

            cvar.name = 'WARMUP ROUND WEAPON'
            cvar.notes.append('Only supports "weapon_*" entities.')
            cvar.notes.append('Warmup round is triggered at ' +
                'the start of each map change.')
            cvar.options.append(' awp   \tscout\taug   \tmac10' +
                '\ttmp   \tmp5navy\tump45\tp90')
            cvar.options.append(' galil\tfamas\tak47\tsg552\t' +
                'sg550\tg3sg1\tm249\tm3')
            cvar.options.append(' xm1014\tm4a1\tglock\tusp   ' +
                '\tp228\tdeagle\telite\tfiveseven')
            cvar.options.append(' hegrenade\tknife')
            cvar.options.append('')
            cvar.options.append(' 0 = The first level weapon')
            cvar.options.append(' weapon1,weapon2,weapon3 = For ' +
                'each warmup, one of these weapons is chosen')
            cvar.options.append(' #random = For ' +
                'each warmup, a random weapon is chosen.')
            cvar.default = 'hegrenade'
            cvar.text = ('The weapon that players ' +
                'will use during the warmup round.')

        # Create the cfg section
        config.cfg_section('WARMUP START AND END CFG SETTINGS')

        # Create the gg_warmup_start_file instance
        with config.cfg_cvar('gg_warmup_start_file') as cvar:

            cvar.name = 'WARMUP ROUND START CFG FILE'
            cvar.description.append('Set to the .cfg ' +
                'file to be executed when Warmup Round starts.')
            cvar.notes.append('The cfg file should contain the ' +
                'GunGame values you wish to use for the current map.')
            cvar.notes.append('Make sure to turn off addons that should ' +
                'not be used during Warmup Round "prior" to turning on ' +
                'any addons that should be used during Warmup Round.')
            cvar.notes.append('The path to the file "must" ' +
                'be relative to the "../cfg/gungame51/" folder')
            cvar.default = (
                'included_addon_configs/warmup_round_start_default')
            cvar.text = 'CFG file to be executed when Warmup Round starts.'

        # Create the gg_warmup_end_file instance
        with config.cfg_cvar('gg_warmup_end_file') as cvar:

            cvar.name = 'WARMUP ROUND END CFG FILE'
            cvar.description.append('Set to the .cfg ' +
                'file to be executed when Warmup Round ends.')
            cvar.notes.append('The cfg file should contain the ' +
                'GunGame values you wish to use for the current map.')
            cvar.notes.append('Make sure to turn off any addons that ' +
                'were used during Warmup Round and are not needed for ' +
                'the current match, "prior" to turning on any addons ' +
                'that are needed for the current match.')
            cvar.notes.append('The path to the file "must" ' +
                'be relative to the "../cfg/gungame51/" folder')
            cvar.default = (
                'included_addon_configs/warmup_round_end_default')
            cvar.text = 'CFG file to be executed when Warmup Round ends.'

        # Create the extension section
        config.cfg_section('WARMUP ROUND EXTENSION SETTINGS')

        with config.cfg_cvar('gg_warmup_round_min_players') as cvar:

            cvar.name = 'MINUMUM HUMAN PLAYERS'
            cvar.description.append('Set to the minimum ' +
                'number of players needed for Warmup Round to end.')
            cvar.default = 0
            cvar.text = (
                'Number of human players needed for Warmup Round to end.')

        with config.cfg_cvar('gg_warmup_round_max_extensions') as cvar:

            cvar.name = 'MAX EXTENSIONS'
            cvar.description.append('Number of extensions '
                'allowed before Warmup Round automatically ends.')
            cvar.default = 1
            cvar.text = ('Maximum number of '
                'extensions allowed before Warmup Round ends.')

        with config.cfg_cvar('gg_warmup_round_players_reached') as cvar:

            cvar.name = 'MIN HUMAN PLAYERS REACHED'
            cvar.description.append(
                'Determines whether or not to end Warmup Round ' +
                'when the minimum number of players has been reached.')
            cvar.options.append(
                '0 = Never end Warmup as soon as min players is reached.')
            cvar.options.append('1 = Only end Warmup ' +
                'if in "extended" time when min players is reached.')
            cvar.options.append(
                '2 = End Warmup Round as soon as min players is reached.')
            cvar.default = 0
            cvar.text = (
                'Allows Warmup Round to end when min players is reached.')

    # Get the path to the default Warmup Round Start cfg file
    start_path = path(get_game_dir(
        'cfg/gungame51/included_addon_configs/warmup_round_start_default.cfg'))

    # Does the file exist?
    if not start_path.isfile():

        # Create the AddonCFG instance
        start = AddonCFG(start_path)

        # Add basic description of how to use the file
        start.text('-' * 74 + '//')
        start.text('//'.rjust(76))
        start.text('warmup_round_start_default.cfg'.center(74) + '//')
        start.text('//'.rjust(76))
        start.text(('This is the default file (using the ' +
            'value of gg_warmup_start_file)').center(74) + '//')
        start.text(('used to determine the gameplay ' +
            '"during" Warmup Round').center(74) + '//')
        start.text('//'.rjust(76))
        start.text(('As an example, if the server should ' +
            'have gg_deathmatch during Warmup').center(74) + '//')
        start.text(('and gg_elimination, gg_turbo, and ' +
            'gg_teamwork for the actual match,').center(74) + '//')
        start.text(
            'the contents could look like the following'.center(74) + '//')
        start.text('//'.rjust(76))
        start.text((' // Turn off any addons that ' +
            'should not be ran during warmup').ljust(74) + '//')
        start.text(' gg_elimination 0'.ljust(74) + '//')
        start.text(' gg_turbo 0'.ljust(74) + '//')
        start.text(' gg_teamwork 0'.ljust(74) + '//')
        start.text('//'.rjust(76))
        start.text((' // Turn on any addons that ' +
            'should be ran during warmup').ljust(74) + '//')
        start.text(' gg_deathmatch 1'.ljust(74) + '//')
        start.text('//'.rjust(76))
        start.text('-' * 74 + '//')

        # Write the file
        start.write()

    # Get the path to the default Warmup Round End cfg file
    end_path = path(get_game_dir(
        'cfg/gungame51/included_addon_configs/warmup_round_end_default.cfg'))

    # Does the file exist?
    if not end_path.isfile():

        # Create the AddonCFG instance
        end = AddonCFG(end_path)

        # Add basic description of how to use the file
        end.text('-' * 74 + '//')
        end.text('//'.rjust(76))
        end.text('warmup_round_end_default.cfg'.center(74) + '//')
        end.text('//'.rjust(76))
        end.text(('This is the default file (using the ' +
            'value of gg_warmup_end_file)').center(74) + '//')
        end.text(('used to change the gameplay from ' +
            'Warmup to the actual match').center(74) + '//')
        end.text('//'.rjust(76))
        end.text(('As an example, if the server should ' +
            'have gg_deathmatch during Warmup').center(74) + '//')
        end.text(('and gg_elimination, gg_turbo, and ' +
            'gg_teamwork for the actual match,').center(74) + '//')
        end.text(
            'the contents could look like the following'.center(74) + '//')
        end.text('//'.rjust(76))
        end.text((' // Turn off any addons that ' +
            'were ran during warmup,').ljust(74) + '//')
        end.text(' //   but need to be off during the match'.ljust(74) + '//')
        end.text(' gg_deathmatch 0'.ljust(74) + '//')
        end.text('//'.rjust(76))
        end.text((' // Turn on any addons that ' +
            'should be ran for the match').ljust(74) + '//')
        end.text(' gg_elimination 1'.ljust(74) + '//')
        end.text(' gg_turbo 1'.ljust(74) + '//')
        end.text(' gg_teamwork 1'.ljust(74) + '//')
        end.text('//'.rjust(76))
        end.text('-' * 74 + '//')

        # Write the file
        end.write()
