# ../scripts/included/gg_random_spawn/gg_random_spawn.py

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
#   Random
from random import shuffle

# EventScripts Imports
#   ES
from es import entitysetvalue
from es import ServerVar

# SPE Imports
from spe import createEntity
from spe import getIndexOfEntity

# GunGame Imports
from gungame51.core import get_game_dir
from gungame51.core import get_version
#   Addons
from gungame51.core.addons.shortcuts import AddonInfo

# Script Imports
from modules.backups import backups

# =============================================================================
# >> ADDON REGISTRATION/INFORMATION
# =============================================================================
info = AddonInfo()
info.name = 'gg_random_spawn'
info.title = 'GG Random Spawn'
info.author = 'GG Dev Team'
info.version = get_version('gg_random_spawn')


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    '''Called when the script loads'''

    # Load the current map's spawnpoint file
    load_spawnpoints()


def unload():
    '''Called when the script unloads'''

    # Clear the backups dictionary
    backups.clear()


# =============================================================================
# >> GAME EVENTS
# =============================================================================
def es_map_start(event_var):
    '''Called when a new map has been loaded'''

    # Clear the backups dictionary
    backups.clear(True)

    # Load the current map's spawnpoint file
    load_spawnpoints()


# =============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# =============================================================================
def load_spawnpoints():
    '''Loads the spawnpoints for the current map'''

    # Get the location of the spawnpoint file for the current map
    spawnpoint_file = get_game_dir('cfg/gungame51/' +
        'spawnpoints/%s.txt' % ServerVar('eventscripts_currentmap'))

    # Is there a spawnpoint file for the current map?
    if not spawnpoint_file.isfile():

        # If not, simply return
        return

    # Open the spawnpoint file
    with spawnpoint_file.open() as open_file:

        # Store the lines in a list
        spawn_lines = [x.strip() for x in open_file.readlines() if x.strip()]

    # Split the spawnpoints into groups of 6 (3 for location, 3 for angle)
    spawnpoints = [x.split(' ', 6) for x in spawn_lines]

    # Shuffle the spawnpoints to randomize them
    shuffle(spawnpoints)

    # Store the backups
    already_created = backups.update()

    # Have the spawnpoints already been created?
    if already_created:

        # If they have return
        return

    # Loop through all of the spawnpoints
    for location in spawnpoints:

        # Loop through each team's spawnpoint entity
        for team in ('info_player_terrorist', 'info_player_counterterrorist'):

            # Create an entity of the current type
            entity = createEntity(team)

            # Get the entity's index
            index = getIndexOfEntity(entity)

            # Set the entity's origin
            entitysetvalue(index, 'origin', ' '.join(location[:3]))

            # Set the entity's angle
            entitysetvalue(index, 'angles', ' '.join(location[3:]))
