# ../scripts/included/gg_nade_bonus/gg_nade_bonus_config.py

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

        # Create the gg_nade_bonus instance
        with config.cfg_cvar('gg_nade_bonus') as cvar:

            cvar.name = 'GRENADE BONUS'
            cvar.description.append('Players on grenade level ' +
                'will receive weapons along with the hegrenade.')
            cvar.notes.append('You can have multiple weapons ' +
                'by separating them with commas.')
            cvar.notes.append('If you choose to have multiple weapons, you ' +
                'can only have one primary weapon, one secondary ' +
                'weapon, and one grenade (not an hegrenade).')
            cvar.notes.append(
                'You can list a weapon order file that players will ' +
                'progress through while remaining on hegrenade level.')
            cvar.notes.append(
                '/cfg/gungame51/weapon_orders/nade_bonus_order.txt ' +
                'has examples and more information on this feature.')
            cvar.examples.append('gg_nade_bonus aug')
            cvar.examples.append('gg_nade_bonus glock,aug')
            cvar.examples.append('gg_nade_bonus nade_bonus_order')
            cvar.options.append('awp      scout   aug      ' +
                'mac10   tmp     mp5navy   ump45')
            cvar.options.append('galil    famas   ak47     ' +
                'sg552   sg550   g3sg1     m249')
            cvar.options.append('xm1014   m4a1    glock    ' +
                'usp     p228    deagle    elite')
            cvar.options.append('m3       p90     fiveseven')
            cvar.options.append('flashbang        smokegrenade')
            cvar.options.append('')
            cvar.options.append('0 = (Disabled) Do not load gg_nade_bonus.')
            cvar.default = 0
            cvar.text = ('The weapon(s) to be given as a ' +
                'grenade level bonus weapon.')

        # Create the gg_nade_bonus_mode instance
        with config.cfg_cvar('gg_nade_bonus_mode') as cvar:

            cvar.name = 'NADE BONUS MODE'
            cvar.description.append('Defines how gg_nade_bonus will ' +
                'function when a weapon order is given and ' +
                'the player makes it through the entire order.')
            cvar.notes.append('Not necessary to change unless ' +
                'you are using a weapon order above.')
            cvar.options.append('0 = (Enabled) Keep ' +
                'the player on the last gun.')
            cvar.options.append('1 = (Enabled) Go through ' +
                'the list again (start over).')
            cvar.options.append('2 = (Enabled) Levelup the ' +
                'player (same as nade kill).')
            cvar.default = 0
            cvar.text = 'Defines how the last weapon in the order is handled.'

        # Create the gg_nade_bonus_reset instance
        with config.cfg_cvar('gg_nade_bonus_reset') as cvar:

            cvar.name = 'NADE BONUS DEATH RESET'
            cvar.description.append(
                'When enabled, every time a player spawns on nade level ' +
                'they will start over on the first weapon in the order.')
            cvar.notes.append('Not necessary to change ' +
                'unless you are using a weapon order above.')
            cvar.options.append('0 = (Disabled) Players ' +
                'will resume where they left off.')
            cvar.options.append('1 = (Enabled) Players will ' +
                'go back to the first weapon every spawn.')
            cvar.default = 0
            cvar.text = 'Enables/Disables gg_nade_bonus_reset.'
