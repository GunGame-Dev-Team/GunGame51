# ../scripts/included/gg_stats_logging/gg_stats_logging_config.py

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

    # Create the cfg file
    with ConfigContextManager(
      path(__file__).parent.split('scripts')[~0][1:]) as config:

        # Create the gg_stats_logging instance
        with config.cfg_cvar('gg_stats_logging') as cvar:

            cvar.name = 'STATS LOGGING'
            cvar.description.append([
                ' When enabled, this addon will log ' +
                    'game events for stats tracking for',
                'HLstatsX, Psychostats, and etc.',
                ])
            cvar.notes.append(
                'Other options available in "gg_stats_logging.txt".')
            cvar.notes.append(
                'This should be used with third-party stats programs.')
            cvar.options.append('0 = (Disabled) Do not load gg_stats_logging.')
            cvar.options.append('1 = (Enabled) Load gg_stats_logging.')
            cvar.default = 0
            cvar.text = ('Enables/Disables stats ' +
                'logging for third-party programs.')
