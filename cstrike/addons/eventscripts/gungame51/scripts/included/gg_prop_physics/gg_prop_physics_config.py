# ../scripts/included/gg_prop_physics/gg_prop_physics_config.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# EventScripts Imports
import es
import cfglib

# GunGame Imports
from gungame51.core.cfg import generate_header

# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
config = cfglib.AddonCFG('%s/cfg/' % es.ServerVar('eventscripts_gamedir') +
    'gungame51/included_addon_configs/gg_prop_physics.cfg')


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    generate_header(config)

    # Prop Physics
    config.text('')
    config.text('=' * 76)
    config.text('>> PROP PHYSICS')
    config.text('=' * 76)
    config.text('Description:')
    config.text('   Earn Levels/Multikills with prop_physics kills.')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not load gg_prop_physics.')
    config.text('   1 = (Enabled) Load gg_prop_physics.')
    config.text('Default Value: 0')
    config.cvar('gg_prop_physics', 0, 'Enables/Disables ' +
                'gg_prop_physics.').addFlag('notify')

    # Increment Nade
    config.text('')
    config.text('=' * 76)
    config.text('>> INCREMENT NADE')
    config.text('=' * 76)
    config.text('Options:')
    config.text('   0 = Do not increment or levelup on Nade level')
    config.text('   1 = Increment or Levelup on Nade level')
    config.text('Default Value: 0')
    config.cvar('gg_prop_physics_increment_nade', 0, 'Increment or Levelup ' +
                                                        'when on Nade level.')

    # Increment Knife
    config.text('')
    config.text('=' * 76)
    config.text('>> INCREMENT KNIFE')
    config.text('=' * 76)
    config.text('Options:')
    config.text('   0 = Do not increment or levelup on Knife level')
    config.text('   1 = Increment or Levelup on Knife level')
    config.text('Default Value: 0')
    config.cvar('gg_prop_physics_increment_knife', 0, 'Increment or Levelup ' +
                                                        'when on Knife level.')

    config.write()
    es.dbgmsg(0, '\tgg_prop_physics.cfg')


def unload():
    global config

    # Remove the "notify" flags as set by addFlag('notify')
    for cvar in config.getCvars().keys():
        es.flags('remove', 'notify', cvar)

    # Delete the cfglib.AddonCFG instance
    del config
