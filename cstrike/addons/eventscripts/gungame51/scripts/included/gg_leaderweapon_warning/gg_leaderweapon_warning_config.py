# ../scripts/included/gg_leaderweapon_warning/gg_leaderweapon_warning_config.py

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

        # Create the gg_leaderweapon_warning instance
        with config.cfg_cvar('gg_leaderweapon_warning') as cvar:

            cvar.name = 'GUNGAME LEADER WEAPON WARNING'
            cvar.description.append(
                'Announces via sound at the beginning of each round when ' +
                'a player has reached either "hegrenade" or "knife" level.')
            cvar.options.append('0 = (Disabled)')
            cvar.options.append('1 = (Enabled)')
            cvar.default = 0
            cvar.text = ('Play a sound when a player ' +
                'reaches "hegrenade" or "knife" level.')

        # Create the gg_leaderweapon_warning_only_last instance
        with config.cfg_cvar('gg_leaderweapon_warning_only_last') as cvar:

            cvar.name = 'WARN ONLY ON LAST LEVELS'
            cvar.description.append(
                'Only play warnings on the last level of each weapon')
            cvar.options.append('0 = (Disabled)')
            cvar.options.append('1 = (Enabled)')
            cvar.default = 0
            cvar.text = ('Only play a sound when a player ' +
                'reaches the "last" hegrenade or knife level.')
