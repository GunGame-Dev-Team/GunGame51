# ../addons/eventscripts/gungame51/core/weapons/shortcuts.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
# EventScripts Imports
import es
from weaponlib import getWeaponList

# GunGame Imports
from gungame51.core.weapons import WeaponManager

# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
def get_weapon_order(name=None):
    '''
    Returns the named weapon order instance if a name is provided as an
    argument. If no argument is provided, it will return the current GunGame
    weapon order instance that is in use. If no weapon order has been set for
    GunGame and no argument has been provided, "None" is returned.
    '''
    if name:
        return WeaponManager().load(name)
    else:
        if WeaponManager().gungameorder:
            return WeaponManager().__weaponorders__[WeaponManager().gungameorder]
        return None

def set_weapon_order(name, type='#default'):
    '''
    Sets the weapon order to be used by GunGame.
    
    Notes:
        * name: (required)
            The name of the weapon order file as found in
                "../<MOD>/cfg/gungame51/weapon_orders/"
            minus the ".txt" extension.
        * type: (optional)
            The weapon order type:
                - "#default"
                    The same order as it is listed in the weapon order's file.
                - "#reversed"
                    The reverse of the order as it is listed in the weapon
                    order's file.
                - "#random"
                    Uses the weapons as they are listed in the weapon order's
                    file, but randomizes the order of the weapons.
    Usage:
        from gungame.core.weapons.shortcuts import set_weapon_order
        
        # Use the default weapon order
        set_weapon_order('default_weapon_order')
        
        # Use the default weapon order, but randomize the order
        set_weapon_order('default_weapon_order', '#random')
        
        # Use the default weapon order, but reverse the order
        set_weapon_order('default_weapon_order', '#reversed')
    '''
    WeaponManager().load(name)
    WeaponManager().set_order(name)
    WeaponManager().type = type
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