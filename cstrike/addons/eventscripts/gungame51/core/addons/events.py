# ../core/addons/events.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# EventScripts Imports
import es

# GunGame Imports
#   Addons
from priority import PriorityAddon


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# These events should always fire, even if there are Priority Addons
_priority_events = ['es_map_start', 'player_activate', 'es_player_validated',
    'player_disconnect', 'gg_addon_loaded', 'gg_addon_unloaded']


# =============================================================================
# >> CLASSES
# =============================================================================
class EventRegistry(dict):
    '''Class that holds all _EventManager instances to call events'''

    def __new__(cls):
        '''Method that makes sure the class is a singleton'''

        if not '_the_instance' in cls.__dict__:
            cls._the_instance = dict.__new__(cls)
        return cls._the_instance

    def register_for_event(self, event, callback):
        '''Method that registers events to be fired for addons'''

        # Is the event already in the dictionary?
        if not event in self:

            # Add the event to the dictionary as an _EventManager instance
            self[event] = _EventManager(event)

        # Add the callback to the list of callbacks for the event
        self[event].append(callback)

    def unregister_for_event(self, event, callback):
        '''Method that unregisters events'''

        # Is the event in the dictionary?
        if event in self:

            # Remove the callback from the event
            self[event].remove(callback)

            # Are there any remaining callbacks for the event?
            if not self[event].callbacks:

                # Unregister the event
                self[event]._unregister()

                # Remove the event from the dictionary
                del self[event]


class _EventManager(object):
    '''Class that registers an event and stores callbacks for the event'''

    def __init__(self, event):
        '''Registers the event'''

        # Store the event name
        self.event = event

        # Store a list to add callbacks to
        self.callbacks = []

        # Register the event
        es.addons.registerForEvent(self, self.event, self._call_event)

    def append(self, callback):
        '''Overrides the append method to make
            sure each callback is only added once'''

        # Get the callback instance
        callback = self._get_callback(callback)

        # Is the callback already in the list?
        if not callback in self.callbacks:

            # Append the callback instance for the given callback
            self.callbacks.append(callback)

    def remove(self, callback):
        '''Overrides the remove method to make sure the
            callback is in the list before removing'''

        # Get the callback instance
        callback = self._get_callback(callback)

        # Is the callback in the list?
        if callback in self.callbacks:

            # Remove the callback
            self.callbacks.remove(callback)

    def _call_event(self, event_var):
        '''Calls the event if there are no Priority Addons'''

        # Loop through all callbacks for the event
        for callback in self.callbacks:

            # Are there Priority Addons?
            if PriorityAddon():

                # Is the callback in a Priority Addon?
                if not callback['addon'] in PriorityAddon():

                    # Is the event supposed to fire anyway?
                    if not self.event in _priority_events:

                        # Do not fire this callback
                        continue

            # Call the callback with the SourceEventVariable argument
            callback['callback'](event_var)

    def _unregister(self):
        '''Unregisters the event'''

        # Unregister the event
        es.addons.unregisterForEvent(self, self.event)

    @staticmethod
    def _get_callback(callback):
        return {'callback': callback,
            'addon': callback.__module__.rsplit('.')[~0]}
