# =============================================================================
# IMPORTS
# =============================================================================
# Python Imports
from __future__ import with_statement

# EventScripts Imports
import es

# Eventlib Imports
from fields import *
from resource import *
from exceptions import ESEventError


# =============================================================================
#   LIBRARY INFORMATION
# =============================================================================
info = es.AddonInfo()
info.name = "Eventlib - EventScripts python library"
info.version = "Eventlib Draft 14"
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
    def __init__(self, event_name):
        event_name = str(event_name)

        # The maximum event name length according to VALVe is 32 characters
        if len(event_name) > 32:
            raise ESEventError('The event name "%s" exceeds ' % event_name +
                               'the maximum length of 32 characters.')

        # No spaces are allowed in event names
        elif event_name.count(' '):
            raise ESEventError('Event names are not allowed to contain ' +
                               'spaces: "%s".' % event_name)

        self._name = str(event_name)

    def __enter__(self):
        """Utilized when the EventContextManager is entered. Used to initialize
        the event.

        """
        es.dbgmsg(1, "es.event('initialize', '%s')" % self._name)
        es.event('initialize', self._name)
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
            es.dbgmsg(1, "es.event('fire', '%s')" % self._name)
            es.event('fire', self._name)
            return True

        # Cancel the event
        es.dbgmsg(1, "es.event('cancel', '%s')" % self._name)
        es.event('cancel', self._name)
        return False

    def set(self, field, value):
        """Sets the event variable values dynamically for es.event()."""
        if not type(value) in DATATYPES:
            raise ESEventError('Unsupported type: %s. Expected'
                               % type(value).__name__ + ' float, int, or str' +
                               ' type.')

        # Set the event variable
        es.dbgmsg(1, ("es.event('%s', '%s', '%s', %s)"
                      % (DATATYPES[type(value)], self._name, field, value)))
        es.event(DATATYPES[type(value)], self._name, field, value)


class QuickEvent(object):
    """Class that can be used to fire an event without any error-checking or
    restrictions. It can also be used as a context manager using the with
    statement.

    Args:
        name (str): The name of the event.

    Kwargs:
        event_var_name (str)=event_var_value (int, float, str)

    Example Usage:
        # Example 1 (using a context manager)
        with QuickEvent('player_say') as event:
            event.userid = 2
            event.text = 'This is a test.'

        # Example 2 (directly firing using keyword arguments and fire() method)
        QuickEvent('player_say', userid=2, text='This is a test.').fire()

        # Example 3 (creating an instance, then firing)
        event = QuickEvent('player_say', userid=2, text='This is a test.')
        event.fire() # Fire using the fire() method
        event() # Fire using the __call__ method

    """
    def __init__(self, name, **kw):
        # Set the event name attribute
        super(QuickEvent, self).__setattr__('name', name)

        # Initialize the event
        es.event('initialize', name)

        # Iterate through keyword arguments and set the event variable/value
        for name, value in kw.iteritems():
            self.set_event_var(name, value)

    def __call__(self):
        self.fire()

    def __enter__(self):
        """Utilized when the QuickEvent is entered."""
        return self

    def __exit__(self, *a):
        """Utilized when the QuickEvent is exited. Used to fire the event if
        there were no errors while setting the values. If any tracebacks were
        generated between the entering of the QuickEvent and the exit, the
        event will be cancelled.

        """
        # Check if there is a traceback, then fire or cancel the event
        if not any(a):
            # Fire the event
            self.fire()
            return True

        # Cancel the event
        self.cancel()
        return False

    def __setattr__(self, name, value):
        # Override to set the event variable, not the attribute
        self.set_event_var(name, value)

    def __setitem__(self, name, value):
        # Override to set the event variable, not the dictionary
        self.set_event_var(name, value)

    def set_event_var(self, item, value):
        """Sets the event variable by its type. If the type is not found, the
        type is assumed to be string.

        """
        if isinstance(value, int):
            es.event('setint', self.name, item, value)
        elif isinstance(value, float):
            es.event('setfloat', self.name, item, value)
        else:
            es.event('setstring', self.name, item, str(value))

    def cancel(self):
        """Cancels the event."""
        es.event('cancel', self.name)

    def fire(self):
        """Fires the event."""
        es.event('fire', self.name)


class EventManager(object):
    def __new__(cls, *a, **kw):
        if not '_the_instance' in cls.__dict__:
            cls._the_instance = object.__new__(cls, *a, **kw)
            cls._the_instance._callbacks = []
        return cls._the_instance

    def fire(self):
        """Handles the firing of ESEvent instances by initializing the
        EventContextManager, setting the int, float, or string values, then
        firing the event if no errors are raised. If errors are raised during
        the process, the event firing will be cancelled.

        Notes:
            * Returns True if the event was successfully fired.
            * Returns False if the event was cancelled via a callback.
            * Raises an exception if the event was not fired due to an error.

        """
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
            continue_event = callback(**field_dict)
            if continue_event is None:
                continue
            elif bool(continue_event) is False:
                return False

        # Fire the event using the EventContextManager
        with EventContextManager(self.get_event_name()) as event:
            for field, value in field_dict.items():
                # Set the event variable value
                event.set(field, value)

        return True

    def register_prefire_callback(self, callback):
        """Registers a callback to be performed just before the event fires.

        Notes:
            * Requires the callback to accept keyword arguments (**kwargs).
            * Requires the callback to return a boolean return value.
            * If the callback returns False, it will cancel the event.
            * If the callback returns True, the event will fire.
            * If no return value is specified in the callback, the event will
              still fire.

        """
        # Make sure the callback is callable
        if not callable(callback):
            raise ESEventError('Callback registration failed: %s ' % callback +
                               'is not callable.')

        # Make sure we do not register the same callback twice
        if callback in self._callbacks:
            return

        # Add the callback to the list
        self._callbacks.append(callback)

    def unregister_prefire_callback(self, callback):
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
