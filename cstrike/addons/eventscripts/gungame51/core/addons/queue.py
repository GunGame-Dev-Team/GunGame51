# ../core/addons/queue.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# EventScripts Imports
#   Gamethread
from gamethread import delayed

# GunGame Imports
#   Addons
from conflicts import AddonConflicts
from conflicts import ConflictError
from dependency import DependentAddons
from instance import AddonInstances
from loaded import LoadedAddons
from manager import AddonManager


# =============================================================================
# >> CLASSES
# =============================================================================
class AddonQueue(dict):
    def __new__(cls):
        '''Make sure the class is a singleton'''

        if not '_the_instance' in cls.__dict__:
            cls._the_instance = dict.__new__(cls)
        return cls._the_instance

    def __getattr__(self, attr):
        '''Redirects to __getitem__ since this is a dictionary'''

        # Redirect to __getitem__
        return self.__getitem__(attr)

    def __getitem__(self, queue_type):
        '''Returns a set of addons in the wanted queue'''

        # Is the queue type already in the dictionary?
        if queue_type in self:

            # Return the item
            return super(AddonQueue, self).__getitem__(queue_type)

        # Is the wanted queue type a valid value?
        if not queue_type in ('load', 'unload'):

            # Raise an error
            raise KeyError('"%s" ' % queue_type +
                'is not a valid key for AddonQueue')

        # Set the queue type to a set to add addons in
        value = self[queue_type] = set()

        # Return the set
        return value

    def add_to_queue(self, queue_type, addon):
        '''Adds an addon to the load or unload queue'''

        # Are there any values in the dictionary?
        if not self:

            # If not, create the delay
            delayed(0, self._loop_through_queue)

        # Add the given addon to the given type's set
        self[queue_type].add(addon)

    def _loop_through_queue(self):
        '''Unload and load addons from the queues'''

        # Do any addons need unloaded?
        if 'unload' in self:

            # Unload all queued addons
            self._unload_addons()

        # Do any addons need loaded?
        if 'load' in self:

            # Load all queued addons
            self._load_addons()

        # Clear the dictionary for further use
        self.clear()

    def _unload_addons(self):
        '''Unloads all addons in the unload queue'''

        # Loop through all addons in the unload queue
        for addon in self.unload:

            # Unload the addon
            AddonManager()._unload_addon(addon)

    def _load_addons(self):
        '''Attempts to load all addons in the load queue'''

        # Create an empty dictionary to store addon instances
        self._current_instances = {}

        # Loop through all addons in the load queue
        for addon in self.load:

            # Add the addons instance to the dictionary
            self._add_addon_instance(addon)

        # Loop through all addon instances
        for addon in self._current_instances:

            # Is the addon listed as a conflict?
            if addon in AddonConflicts():

                # If so, raise an error about the conflict
                raise ConflictError('"%s" can not be loaded.' % addon +
                    '  Sub-addon is listed as a conflict with ' +
                    '"%s"' % '", "'.join(list(AddonConflicts()[addon])))

            # Loop through all conflicts for the current addon
            for conflict in self._current_instances[addon].info.conflicts:

                # Is the conflict already loaded?
                if conflict in LoadedAddons():

                    # If so, raise an error
                    raise ConflictError('Sub-addon "%s" is ' % conflict +
                        'already loaded and is a conflict with "%s"' % addon)

                # Is the conflict going to be loaded?
                if conflict in self._current_instances:

                    # If so, raise an error
                    raise ConflictError('Sub-addon "%s" is set ' % conflict +
                        'to be loaded and is a conflict with "%s"' % addon)

        # Everything went well if getting to this point
        # Loop through all addons in the load queue
        for addon in self.load:

            # Has the addon been loaded as a dependency?
            if addon in DependentAddons():

                # If so, do not re-attempt to load the addon
                continue

            # Load the addon
            AddonManager()._load_addon(addon)

    def _add_addon_instance(self, addon):
        '''Method used to store all addon instances that will be loaded'''

        # Is the addon already in the dictionary?
        if addon in self._current_instances:

            # If so, simply return
            return

        # Add the addons instance to the dictionary
        self._current_instances[addon] = AddonInstances()[addon]

        # Loop through all dependencies for the current addon
        for required_addon in self._current_instances[addon].info.requires:

            # Add the dependency to the dictionary
            self._add_addon_instance(required_addon)
