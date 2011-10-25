# ../core/weapons/shortcuts.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# EventScripts Imports
from weaponlib import getWeaponList

# GunGame Imports
from gungame51.core.weapons import WeaponOrderManager
from gungame51.core.weapons import weaponOrderStorage

import es
# =============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# =============================================================================
def get_weapon_order(name=None):
    """Returns the named weapon order instance if a name is provided as an
    argument. If no argument is provided, it will return the current GunGame
    weapon order instance that is in use.
    """
    if name:
        return weaponOrderStorage[name]

    return WeaponOrderManager().active


def set_weapon_order(name):
    """Sets the weapon order to be used by GunGame.

    Notes:
        * name: (required)
            The name of the weapon order file as found in
                "../<MOD>/cfg/gungame51/weapon_orders/"
            minus the ".txt" extension.

    Usage:
        from gungame.core.weapons.shortcuts import set_weapon_order

        # Use the default weapon order
        set_weapon_order('default_weapon_order')
    """
    WeaponOrderManager().activate(name)
    WeaponOrderManager().active._set_active_order_type()
    return get_weapon_order()


def get_level_weapon(level, weaponOrderName=None):
    '''
    Returns the name of the level's weapon set in GunGame's weapon order.
    '''
    return get_weapon_order(weaponOrderName).get_weapon(level)


def get_level_multikill(level, weaponOrderName=None):
    '''
    Returns the multikill value of the level set in GunGame's weapon order.
    '''
    return get_weapon_order(weaponOrderName).get_multikill(level)


def get_total_levels(weaponOrderName=None):
    return get_weapon_order(weaponOrderName).get_total_levels()
