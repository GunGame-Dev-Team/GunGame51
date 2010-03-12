# ../addons/eventscripts/gungame/core/menu/weapons_menu.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
# Eventscripts Imports
import es
from cmdlib import registerSayCommand
from cmdlib import unregisterSayCommand

# GunGame Imports
from gungame51.core.players import Player
from gungame51.core.menus import OrderedMenu
from gungame51.core.menus.shortcuts import get_index_page
from gungame51.core.weapons.shortcuts import get_level_weapon
from gungame51.core.weapons.shortcuts import get_level_multikill
from gungame51.core.weapons.shortcuts import get_total_levels

# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    # Register command
    registerSayCommand('!weapons', weapons_menu_cmd, 'Displays a !weapons menu.')

def unload():
    # Unregister commands
    unregisterSayCommand('!weapons')

# ============================================================================
# >> MENU FUNCTIONS
# ============================================================================
def weapons_menu_cmd(userid, args):
    # Make sure player exists
    if not es.exists('userid', userid):
        return

    weaponOrder = []
    level = 1
    totalLevels = get_total_levels()

    while level <= totalLevels:
        weaponOrder.append("[%s] %s" % (get_level_multikill(level), get_level_weapon(level)))
        level += 1

    # Get the level the player is on
    ggLevel = Player(userid).level

    # Create a new OrderedMenu
    ggWeaponsMenu = OrderedMenu(userid, 'GunGame: Weapons Menu', weaponOrder,
                                                    highlightIndex=ggLevel)

    # Send the OrderedMenu on the page the player's weapon is on
    ggWeaponsMenu.send_page(get_index_page(ggLevel))