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

# GunGame Imports
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

        # Create the gg_warmup_deathmatch instance
        with config.cfg_cvar('gg_warmup_deathmatch') as cvar:

            cvar.name = 'WARMUP ROUND DEATHMATCH MODE'
            cvar.notes.append('Please check the gg_deathmatch.cfg ' +
                'for information regarding running gg_deathmatch.')
            cvar.options.append('0 = Disabled.')
            cvar.options.append('1 = Enabled.')
            cvar.default = 0
            cvar.text = 'Enable deathmatch during warmup round only.'

        # Create the gg_warmup_elimination instance
        with config.cfg_cvar('gg_warmup_elimination') as cvar:

            cvar.name = 'WARMUP ROUND ELIMINATION MODE'
            cvar.notes.append('Please check the gg_elimination.cfg for ' +
                'information regarding what is required to be ' +
                'enabled and disabled when running gg_elimination.')
            cvar.options.append('0 = Disabled.')
            cvar.options.append('1 = Enabled.')
            cvar.default = 0
            cvar.text = 'Enable elimination during warmup round only.'
