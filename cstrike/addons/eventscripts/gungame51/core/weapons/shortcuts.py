# ../cstrike/addons/eventscripts/gungame51/core/weapons/shortcuts.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
# GunGame Imports
from gungame51.core.weapons import weaponorders

# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
def getWeaponOrder(name=None):
    '''
    Returns the named weapon order instance if a name is provided as an
    argument. If no argument is provided, it will return the current GunGame
    weapon order instance that is in use. If no weapon order has been set for
    GunGame and no argument has been provided, "None" is returned.
    '''
    if name:
        return weaponorders.load(name)
    else:
        if weaponorders.gungameorder:
            return weaponorders.__weaponorders__[weaponorders.gungameorder]
        return None

def setWeaponOrder(name, type='#default'):
    '''
    Sets the weapon order to be used by GunGame.
    
    Notes:
        * name: (required)
            The name of the weapon order file as found in
                "../<MOD>/cfg/gungame/weapon_orders/"
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
        from gungame.core.weapons.shortcuts import setWeaponOrder
        
        # Use the default weapon order
        setWeaponOrder('default_weapon_order')
        
        # Use the default weapon order, but randomize the order
        setWeaponOrder('default_weapon_order', '#random')
        
        # Use the default weapon order, but reverse the order
        setWeaponOrder('default_weapon_order', '#reversed')
    '''
    weaponorders.load(name)
    weaponorders.setOrder(name)
    weaponorders.type = type
    return getWeaponOrder()
    
def getWeapon(level):
    '''
    Returns the name of the level's weapon set in GunGame's weapon order.
    '''
    return getWeaponOrder().getWeapon(level)
    
def getLevelMultiKill(level):
    '''
    Returns the multikill value of the level set in GunGame's weapon order.
    '''
    return getWeaponOrder().getMultiKill(level)