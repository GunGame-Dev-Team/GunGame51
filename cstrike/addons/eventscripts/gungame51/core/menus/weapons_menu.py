# ../addons/eventscripts/gungame/core/menu/weapons_menu.py

'''
$Rev: 264 $
$LastChangedBy: micbarr $
$LastChangedDate: 2009-11-30 23:19:08 -0500 (Mon, 30 Nov 2009) $
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
# Eventscripts Imports
import es
import popuplib
from playerlib import getUseridList
from cmdlib import registerSayCommand
from cmdlib import unregisterSayCommand

# GunGame Imports
from gungame51.core.weapons.shortcuts import get_level_weapon
from gungame51.core.weapons.shortcuts import get_level_multikill
from gungame51.core.weapons.shortcuts import get_total_levels

# ============================================================================
# >> GLOBALS
# ============================================================================
ggWeaponsMenu = None

# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    generate_weapons_menu()

    # Register for the "server_cvar" event
    es.addons.registerForEvent(__import__(__name__), 'server_cvar', server_cvar)

    # Register command
    registerSayCommand('!weapons', weapons_menu_cmd, 'Displays a !weapons menu.')

def unload():
    # Delete the popup if it exists
    if popuplib.exists('ggWeaponsMenu'):
        ggWeaponsMenu.delete()
    
    # Register for the "server_cvar" event
    es.addons.unregisterForEvent(__import__(__name__), 'server_cvar')

    # Unregister commands
    unregisterSayCommand('!weapons')

# ============================================================================
# >> MENU FUNCTIONS
# ============================================================================
def generate_weapons_menu():
    global ggWeaponsMenu

    # Does the popup exist ?
    if popuplib.exists('ggWeaponsMenu'):
        # Delete the old menu
        popuplib.unsendname('ggWeaponsMenu', getUseridList('#human'))
        popuplib.delete('ggWeaponsMenu')

    weaponOrder = []
    level = 1
    totalLevels = get_total_levels()

    while level <= totalLevels:
        weaponOrder.append("[%s] %s" % (get_level_multikill(level), get_level_weapon(level)))
        level += 1

    # Make new menu
    ggWeaponsMenu = popuplib.easylist('ggWeaponsMenu', weaponOrder)
    ggWeaponsMenu.settitle('GunGame: Weapons Menu')
    ggWeaponsMenu.timeout('view', 30)
    ggWeaponsMenu.timeout('send', 30)

def weapons_menu_cmd(userid, args):
    # Make sure player exists
    if not es.exists('userid', userid):
        return

    # Send the new menu
    ggWeaponsMenu.send(userid)

def server_cvar(event_var):
    if event_var['cvarname'] in ['gg_weapon_order_file',
                        'gg_weapon_order_sort_type', 'gg_multikill_override']:
        generate_weapons_menu()