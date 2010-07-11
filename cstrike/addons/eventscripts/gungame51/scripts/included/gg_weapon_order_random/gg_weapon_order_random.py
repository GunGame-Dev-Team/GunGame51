# ../addons/eventscripts/gungame51/scripts/included/gg_weapon_order_random/gg_weapon_order_random.py

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
from gungame51.core.weapons.shortcuts import get_weapon_order
from gungame51.core.weapons.shortcuts import set_weapon_order

# ============================================================================
# >> ADDON REGISTRATION/INFORMATION
# ============================================================================
info = AddonInfo()
info.name = 'gg_weapon_order_random'
info.title = 'GG Random Weapon Order File' 
info.author = 'GG Dev Team' 
info.version = "5.1.%s" %"$Rev$".split('$Rev: ')[1].split()[0]

# ============================================================================
# >> GLOBAL VARIABLES
# ============================================================================
# Get the es.ServerVar() instance of "gg_weapon_order_random"
gg_weapon_order_sort_type = es.ServerVar('gg_weapon_order_sort_type')
gg_weapon_order_random_excluded = \
                                es.ServerVar("gg_weapon_order_random_excluded")

# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    es.dbgmsg(0, 'Unloaded: %s' % info.name)

def unload():
    es.dbgmsg(0, 'Loaded: %s' % info.name)

# ============================================================================
# >> GAME EVENTS
# ============================================================================
def es_map_start(event_var):
    # Get a list of files names ([:-4] to remove .txt extensions) in the
    # weapon_orders directory
    files = [x.name[:-4] for x in get_game_dir('cfg/gungame51/weapon_orders') \
                                                            .files("*.txt")]

    # Get the current weapon order's file name
    currentFile = get_weapon_order().file

    # Remove the current weapon order's file name
    files.remove('%s' %currentFile)

    # Do not choose from excluded weapon orders
    for excluded_file in str(gg_weapon_order_random_excluded).split(","):
        excluded_file = excluded_file.strip()
        if excluded_file in files:
            files.remove(excluded_file)

    # If the current weapon order is the only weapon order, return
    if not len(files):
        return

    # Get a random weapon order file
    newFile = random.choice(files)

    # Set the new file
    currentOrder = set_weapon_order(newFile, str(gg_weapon_order_sort_type))

    # Echo the new weapon order
    currentOrder.echo()