# ../scripts/included/gg_random_spawn/modules/backups.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# EventScripts Imports
#   ES
from es import entitygetvalue
from es import entitysetvalue
from es import getEntityIndexes

# SPE Imports
from spe import createEntity
from spe import getIndexOfEntity
from spe import removeEntityByIndex


# =============================================================================
# >> CLASSES
# =============================================================================
class _LocationBackups(dict):
    '''Class used to store backup locations for the given entity'''

    def __init__(self, entity):
        '''Called when the class is initialized'''

        # Store the given entity name
        self.entity = entity

    def __delitem__(self, location):
        '''
            Removes a location from the dictionary and recreates the spawnpoint
        '''

        # Get the angle to set
        angle = self[location]

        # Create an entity of the instance's type
        entity = createEntity(self.entity)

        # Get the entity's index
        index = getIndexOfEntity(entity)

        # Set the entity's origin
        entitysetvalue(index, 'origin', location)

        # Set the entity's angle
        entitysetvalue(index, 'angles', angle)

        # Remove the location from the dictionary
        super(_LocationBackups, self).__delitem__(location)

    def clear(self, clean=False):
        '''Clears the dictionary'''

        # Is this supposed to just clean the dictionary?
        if clean:

            # If so, simply clear the dictionary
            super(_LocationBackups, self).clear()

            # Go no further
            return

        # Remove all entity's of the instance's type from the server
        self.remove_all_entities()

        # Loop through all locations
        for location in list(self):

            # Remove the location from the dictionary
            del self[location]

    def remove_all_entities(self):
        '''Removes all entity's of the instance's type from the server'''

        # Loop through all indexes of the instance's type
        for index in getEntityIndexes(self.entity):

            # Remove the entity from the server
            removeEntityByIndex(index)


class _BackupManager(dict):
    '''Class that stores backups of both entity types for spawnpoints'''

    def __init__(self):
        '''Called when the class is first initialized'''

        # Loop through both types of entities
        for entity in ('info_player_terrorist',
          'info_player_counterterrorist'):

            # Add the entity to the dictionary
            self[entity] = _LocationBackups(entity)

    def clear(self, clean=False):
        '''Clears the dictionaries for both entity types'''

        # Loop through the entity types
        for entity in self:

            # Clear the dictionary
            self[entity].clear(clean)

    def update(self):
        '''Updates the dictionaries and removes the old indexes'''

        # Has the class already been updated this map?
        if any([self[entity] for entity in self]):

            # If so, return
            return True

        # Loop through the entity types
        for entity in self:

            # Loop through the indexes for the entity type
            for index in getEntityIndexes(entity):

                # Store the location
                location = entitygetvalue(index, 'origin')

                # Store the angle
                angle = entitygetvalue(index, 'angles')

                # Add the location to the dictionary
                self[entity][location] = angle

                # Remove the entity from the server
                removeEntityByIndex(index)

        # Return
        return False

# Get the _BackupManager instance
backups = _BackupManager()
