# ../addons/eventscripts/gungame/scripts/included/gg_weapon_order_random/gg_weapon_order_random.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
# Python imports
import os.path
import random

# Eventscripts Imports
import es

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core import get_game_dir
from gungame51.core.weapons.shortcuts import getWeaponOrder
from gungame51.core.weapons.shortcuts import setWeaponOrder

# ============================================================================
# >> ADDON REGISTRATION/INFORMATION
# ============================================================================
info = AddonInfo()
info.name = 'gg_weapon_order_random'
info.title = 'GG Random Weapon Order File' 
info.author = 'GG Dev Team' 
info.version = '0.1'

# ============================================================================
# >> GLOBAL VARIABLES
# ============================================================================
# Get the es.ServerVar() instance of "gg_weapon_order_random"
gg_weapon_order_sort_type = es.ServerVar('gg_weapon_order_sort_type')

def es_map_start(event_var):
    # Get the weapon_orders directory
    baseDir = get_game_dir('cfg/gungame5/weapon_orders/')

    # Get a list of files in the weapon_orders directory
    files = filter(lambda x: os.path.splitext(x)[1] == '.txt',
                os.listdir(baseDir))

    # Get the current weapon order's file name
    currentFile = getWeaponOrder().file

    # Remove the current weapon order's file name
    files.remove('%s.txt' %currentFile)

    # If the current weapon order is the only weapon order, return
    if not len(files):
        return

    # Get a random weapon order file
    newFile = random.choice(files)

    # Set the new file
    currentOrder = setWeaponOrder(newFile, str(gg_weapon_order_sort_type))

    # Echo the new weapon order
    currentOrder.echo()