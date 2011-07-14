# =============================================================================
# IMPORTS
# =============================================================================
# Python Imports
from __future__ import with_statement

# EventScripts Imports
import es

# Eventlib Imports
from fields import EventField
from exceptions import ESEventError


# =============================================================================
#   LIBRARY INFORMATION
# =============================================================================
info = es.AddonInfo()
info.name = "Eventlib - EventScripts python library"
info.version = "Eventlib Draft 8"
info.url = "http://www.eventscripts.com/pages/Eventlib/"
info.basename = "eventlib"
info.author = "XE_ManUp"


# =============================================================================
# GLOBAL VARIABLES/CONSTANTS
# =============================================================================
DATATYPES = {float: 'setfloat', int: 'setint', str: 'setstring'}


# =============================================================================
# CLASSES
# =============================================================================
class EventContextManager(object):
    """Inspired from http://forums.eventscripts.com/viewtopic.php?p=367772"""
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        """Utilized when the EventContextManager is entered. Used to initialize
        the event.

        """
        #print "es.event('initialize', '%s')" % self.name
        es.event('initialize', self.name)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Utilized when the EventContextManager is exited. Used to fire the
        event if there were no errors while setting the values. If any
        tracebacks were generated between the entering of the
        EventContextManager and the exit, the event will be cancelled.

        """
        # Check if there is a traceback, then fire or cancel the event
        if not traceback:
            # Fire the event
            #print "es.event('fire', '%s')" % self.name
            es.event('fire', self.name)
            return True
        else:
            # Cancel the event
            #print "es.event('cancel', '%s')" % self.name
            es.event('cancel', self.name)
            return False

    def set(self, field, value):
        """Sets the event variable values dynamically for es.event()."""
        if type(value) in DATATYPES:
            #print "es.event('%s', '%s', '%s', %s)" % (DATATYPES[type(value)],
            #    self.name, field, value)
            es.event(DATATYPES[type(value)], self.name, field, value)
        else:
            raise TypeError('Unsupported type: %s. Expected'
                % type(value).__name__ + ' float, int, or str type.')


class EventManager(object):
    def __init__(self):
        # Create a list to store callbacks
        self._callbacks = []

    def fire(self):
        """Handles the firing of ESEvent instances by initializing the
        EventContextManager, setting the int, float, or string values, then
        firing the event if no errors are raised. If errors are raised during
        the process, the event firing will be cancelled.

        Note:
            * Returns True if the event was successfully fired.
            * Returns False if the event was cancelled.

        """
        # Retrieve the event name
        event_name = self.get_event_name()

        # Prepare the values
        field_dict = {}
        
        # Loop through each event variable and set the types
        for field, ev in self._fields.items():
            try:
                value = ev.to_python(self.__dict__[field])
            except KeyError:
                raise ESEventError('Instance variable "%s" must be' % field +
                                   'set/declared prior to using the fire() ' +
                                   'method.')
            # Store the field and value to the dictionary
            field_dict[field] = value

        # Handle callbacks        
        for callback in self._callbacks:
            try:
                continue_event = callback(**field_dict)
                if continue_event is None:
                    continue
                elif bool(continue_event) is False:
                    return False
            except:
                pass

        # Fire the event using the EventContextManager
        with EventContextManager(event_name) as event:
            for field, value in field_dict.items():
                # Set the event variable value
                event.set(field, value)

    def register_callback(self, callback):
        """Registers a callback to be performed just before the event fires.

        Notes:
            * Requires the callback to accept keyword arguments (**kwargs).
            * Requires the callback to return a boolean return value.
            * If the callback returns False, it will cancel the event.
            * If the callback returns True, the event will fire.
            * If no return value is specified in the callback, the event will
              still fire.

        """
        if callable(callback):
            self._callbacks.append(callback)
        else:
            raise ESEventError('Callback registration failed: %s ' % callback +
                               'is not callable.')

    def unregister_callback(self, callback):
        """Unregisters a callback."""
        if callback in self._callbacks:
            self._callbacks.remove(callback)


class ESEventMeta(type):
    def __init__(cls, name, bases, contents):
        # Store the field definitions in the ESEvent class as a dictionary
        cls._fields = {}

        # Loop through the contents looking for ESEventField instances
        for key, value in contents.items():
            if isinstance(value, EventField):
                cls._fields[key] = value


class ESEvent(EventManager):
    __metaclass__ = ESEventMeta

    def __init__(self, **kw):
        # Allow the user to pass in keyword arguments to easily set the values
        for key, value in kw.items():
            if key in self._fields:
                setattr(self, key, value)

        super(ESEvent, self).__init__()

    def __setattr__(self, key, value):
        # Loop through each field and verify the values
        if key in self._fields:
            evField = self._fields[key]
            value = evField.to_python(value)

        super(ESEvent, self).__setattr__(key, value)

    def __setitem__(self, key, value):
        # Forward to __setattr__
        object.__setattr__(self, key, value)

    def __getitem__(self, key):
        # Forward to __getattribute__
        return object.__getattribute__(self, key)

    def get_event_name(self):
        """Returns the event name."""
        return self.__class__.__name__.lower()
