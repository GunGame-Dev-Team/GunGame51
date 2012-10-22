# ../core/addons/loaded.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame Imports
#   Addons
from events import EventRegistry
from instance import AddonInstances
#   Events
from gungame51.core.events import GG_Addon_Loaded
from gungame51.core.events import GG_Addon_Unloaded
#   Messaging
from gungame51.core.messaging import MessageManager


# =============================================================================
# >> CLASSES
# =============================================================================
class _LoadedAddons(dict):
    '''Class to store all loaded addons'''

    def __getitem__(self, addon):
        '''Method used to get the instance for the given addon'''

        # Does the addon already exist in the dictionary?
        if addon in self:

            # Return the addon's instance
            return super(_LoadedAddons, self).__getitem__(addon)

        # Store the addon in the dictionary and get its instance
        value = self[addon] = _LoadedAddonInstance(addon)

        # Return the addon's instance
        return value

    def __delitem__(self, addon):
        '''Method used to unload an addon'''

        # Is the addon loaded?
        if not addon in self:

            # If not, raise an error
            raise NameError('Addon "%s" ' % addon +
                'cannot be unloaded. It is not currently loaded')

        # Unload the addon
        self[addon]._unload_addon()

        # Remove the addon from the dictionary
        super(_LoadedAddons, self).__delitem__(addon)

# Get the LoadedAddons instance
LoadedAddons = _LoadedAddons()


class _LoadedAddonInstance(object):
    '''Class that stores the instance of an included/custom addon'''

    def __init__(self, addon):
        '''Called when the addon is first imported'''

        # Get the Addons main instance
        instance = AddonInstances[addon]

        # Loop through all class attributes in the instance
        for attribute in instance.__dict__:

            # Store the same values for this class
            self.__setattr__(attribute, instance.__dict__[attribute])

        # Load the addon
        self._load_addon()

    def _load_addon(self):
        '''Method that loads the addon'''

        # Register events for the addon
        self._register_events()

        # Loop through all translation files for the addon
        for translation in self.info.translations:

            # Load the translations
            MessageManager().load(translation, self.basename)

        # Call the addon's load function
        self.call_block('load')

        # Create the Addon Loaded event instance
        gg_addon_loaded = GG_Addon_Loaded(
            addon=self.basename, type=self.addon_type)

        # Fire the gg_addon_loaded event
        gg_addon_loaded.fire()

    def _unload_addon(self):
        '''Method used to unload the addon and clean up'''

        # Unregister all events
        self._unregister_events()

        # Loop through all translation files for the addon
        for translation in self.info.translations:

            # Unload the translations
            MessageManager().unload(translation, self.basename)

        # Call the addon's unload function
        self.call_block('unload')

        # Create the Addon Unloaded event instance
        gg_addon_unloaded = GG_Addon_Unloaded(
            addon=self.basename, type=self.addon_type)

        # Fire the gg_addon_unloaded event
        gg_addon_unloaded.fire()

    def _register_events(self):
        '''Registers all functions as events'''

        # Loop through all global functions in the addon
        for event in self._possible_events:

            # Register the event
            EventRegistry.register_for_event(event, self.globals[event])

    def _unregister_events(self):
        '''Unregisters all functions as events'''

        # Loop through all global functions in the addon
        for event in self._possible_events:

            # Unregister the event
            EventRegistry.unregister_for_event(event, self.globals[event])

    def call_block(self, blockname, *a, **kw):
        '''Calls a function for the addon with arguments and keywords'''

        # Does the block exist as a function in the addon?
        if blockname in self.globals and callable(self.globals[blockname]):

            # Call the function with the given arguments and keywords
            self.globals[blockname](*a, **kw)

    @property
    def _possible_events(self):
        '''Generator used to get all possible events within an addon'''

        # Loop through all of the globals
        for event in self.globals:

            # Is the current global a function?
            if type(self.globals[event]).__name__ != 'function':

                # If not, do not register
                continue

            # Is the global private?
            if event.startswith('_'):

                # If private, do not register
                continue

            # Is the global native to the script?
            if self.globals[event].__module__ != self.module:

                # If not, do not register
                continue

            # Yield the global and its instance
            yield event
