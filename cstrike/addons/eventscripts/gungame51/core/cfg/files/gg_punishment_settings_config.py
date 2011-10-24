# ../core/cfg/files/gg_punishment_settings_config.py

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
        config.name = 'Punishments Configuration'
        config.description = 'This file controls GunGame51 punishment settings'

        # Create the gg_afk_rounds instance
        with config.cfg_cvar('gg_afk_rounds') as cvar:

            cvar.name = 'AFK ROUNDS'
            cvar.options.append('0  = Disabled')
            cvar.options.append('# = The number of rounds ' +
                'the player can be AFK before punishment occurs.')
            cvar.default = 0
            cvar.text = ('The number of rounds a player ' +
                'can be AFK before punishment occurs.')

        # Create the gg_afk_punish instance
        with config.cfg_cvar('gg_afk_punish') as cvar:

            cvar.name = 'AFK PUNISHMENT'
            cvar.notes.append('Requires "gg_afk_rounds 1" or higher')
            cvar.options.append('0 = No punishment.')
            cvar.options.append('1 = Kick the player.')
            cvar.options.append('2 = Move the player to spectator.')
            cvar.default = 0
            cvar.text = ('The punishment for players ' +
                'who are AFK longer than "gg_afk_rounds".')
            cvar.notify = True

        # Create the gg_suicide_punish instance
        with config.cfg_cvar('gg_suicide_punish') as cvar:

            cvar.name = 'SUICIDE PUNISHMENT'
            cvar.options.append('0 = No punishment.')
            cvar.options.append('# = The number of levels a ' +
                'player will lose if they commit suicide.')
            cvar.default = 0
            cvar.text = ('The number of levels a ' +
                'player will lose if they commit suicide.')
            cvar.notify = True

        # Create the gg_tk_punish instance
        with config.cfg_cvar('gg_tk_punish') as cvar:

            cvar.name = 'TEAM KILL PUNISHMENT'
            cvar.options.append('0 = No punishment.')
            cvar.options.append('# = The number of levels ' +
                'a player will lose if they kill a teammate.')
            cvar.default = 0
            cvar.text = ('The number of levels a player ' +
                'will lose if they kill a teammate.')
            cvar.notify = True

        # Create the gg_retry_punish instance
        with config.cfg_cvar('gg_retry_punish') as cvar:

            cvar.name = 'RETRY/RECONNECT PUNISHMENT'
            cvar.options.append('0 = No punishment.')
            cvar.options.append('# = The number of levels a ' +
                'player will lose if they reconnect in the same round.')
            cvar.default = 0
            cvar.text = ('The number of levels a player will ' +
                'lose if they reconnect in the same round.')
            cvar.notify = True

        # Create the gg_hostage_killed_punish instance
        with config.cfg_cvar('gg_hostage_killed_punish') as cvar:

            cvar.name = 'HOSTAGE KILLED PUNISHMENT'
            cvar.options.append('0 = No punishment.')
            cvar.options.append('# = The number of levels ' +
                'a player will lose if they kill hostages.')
            cvar.default = 0
            cvar.text = ('The number of levels a ' +
                'player will lose if they kill hostages.')
            cvar.notify = True

        # Create the gg_hostage_killed_kills instance
        with config.cfg_cvar('gg_hostage_killed_kills') as cvar:

            cvar.name = 'HOSTAGE KILLED REQUIRED KILLS'
            cvar.options.append('# = The number of hostages ' +
                'killed required to level the player down')
            cvar.default = 0
            cvar.text = ('The number of hostages ' +
                'killed required to level the player down')
