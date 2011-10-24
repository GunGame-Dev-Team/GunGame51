# ../core/cfg/files/gg_default_addons_config.py

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

    # Create the .cfg file
    with ConfigContextManager(
      path(__file__).namebase.replace('_config', '')) as config:

        # Add the config file base attributes
        config.name = 'Default Addon Configuration'
        config.description = 'This file defines GunGame Addon settings.'

        # Create the gg_prune_database instance
        with config.cfg_cvar('gg_prune_database') as cvar:

            cvar.name = 'STATS DATABASE PRUNE'
            cvar.description.append('The number of days of ' +
                'inactivity for a winner that is tolerated until')
            cvar.description.append('they are removed from the database.')
            cvar.notes.append('Pruning the database of ' +
                'old entries is STRONGLY RECOMMENDED for ')
            cvar.notes.append('high-volume servers.')
            cvar.options.append(
                '0 = (Disabled) Do not load gg_prune_database.')
            cvar.options.append('1 = (Enabled) Load gg_prune_database.')
            cvar.default = 0
            cvar.text = ('The number inactive days ' +
                'before a winner is removed from the database.')
