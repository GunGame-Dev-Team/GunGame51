# ../scripts/included/gg_handicap/gg_handicap_config.py

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

        # Create the gg_handicap instance
        with config.cfg_cvar('gg_handicap') as cvar:

            cvar.name = 'HANDICAP'
            cvar.description.append(
                'Helps newly connected players by adjusting their level.')
            cvar.description.append('Basically "catching them up".')
            cvar.options.append('0 = (Disabled) Do not load gg_handicap.')
            cvar.options.append('1 = Set player to the ' +
                'lowest level of all the other players.')
            cvar.options.append('2 = Set player to the ' +
                'average level of all the other players.')
            cvar.default = 0
            cvar.text = ('Helps newly connected ' +
                'players by adjusting their level.')

        # Create the gg_handicap_max instance
        with config.cfg_cvar('gg_handicap_max') as cvar:

            cvar.name = 'HANDICAP MAXIMUM FIRST LEVEL'
            cvar.description.append('The highest level a player ' +
                'may receive when first joining the server.')
            cvar.notes.append('If you are running ' +
                'handicap update, this setting is pointless.')
            cvar.options.append('0 = (Disabled)')
            cvar.options.append('# = Max. level a player may join in on.')
            cvar.default = 0
            cvar.text = ('Helps newly connected ' +
                'players by adjusting their level. (max)')
            cvar.notify = True

        # Create the gg_handicap_no_reconnect instance
        with config.cfg_cvar('gg_handicap_no_reconnect') as cvar:

            cvar.name = 'HANDICAP NO RECONNECT'
            cvar.description.append([
                'gg_handicap will only process a handicap ' +
                    'level for the first time',
                'a player joins a team.  This prevents ' +
                    'players from abusing the',
                'handicap system. (reconnecting to level up)',
                ])
            cvar.notes.append('If you are running ' +
                'handicap update, this setting is pointless.')
            cvar.options.append('0 = (Disabled)')
            cvar.options.append('1 = (Enabled)')
            cvar.default = 0
            cvar.text = 'Prevents abuse from reconnecting'
            cvar.notify = True

        # Create the gg_handicap_update instance
        with config.cfg_cvar('gg_handicap_update') as cvar:

            cvar.name = 'HANDICAP UPDATE'
            cvar.description.append([
                'A timer (in seconds) that updates ' +
                    'players with the lowest level to the',
                'lowest level of the other players. ' +
                    'Basically "catching them up".',
                ])
            cvar.options.append(
                '0 = (Disabled) Do not load gg_handicap_update.')
            cvar.options.append('180 = (Enabled) Update the ' +
                'lowest level players every 180 seconds (3 minutes).')
            cvar.default = 0
            cvar.text = ('The time (in seconds) to update ' +
                "players' levels using handicap.")

        # Create the gg_handicap_legacy_mode instance
        with config.cfg_cvar('gg_handicap_legacy_mode') as cvar:

            cvar.name = 'LEGACY MODE'
            cvar.description.append([
                'This enables the old method of ' +
                    'handicap adjustment, which is',
                'based on when a player joins the ' +
                    'server. Instead of the new method,',
                'which is when the player joins a team for the first time.',
                ])
            cvar.options.append('0 = (Disabled)')
            cvar.options.append('1 = (Enabled)')
            cvar.default = 0
            cvar.text = 'Legacy mode'
            cvar.notify = True
