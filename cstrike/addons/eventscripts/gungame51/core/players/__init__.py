# ../core/players/__init__.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> CLASSES
# =============================================================================
class _FieldMeta(type):
    def __new__(cls, name, bases, attr):
        for base in bases:
            if hasattr(base, '_fields'):
                inherited = getattr(base, '_fields')
                try:
                    attr['_fields'].update(inherited)
                except KeyError:
                    attr['_fields'] = inherited
                except ValueError:
                    pass
        return type.__new__(cls, name, bases, attr)


class _PlayerMeta(object):
    __metaclass__ = _FieldMeta

    def __setattr__(self, name, value):
        if name in self._fields:
            value = self._fields[name].to_python(value)

        # Execute the custom attribute callbacks
        if name in CALLBACKS:
            for function in CALLBACKS[name].values():
                function(name, value, self)

        super(_PlayerMeta, self).__setattr__(name, value)


class CustomAttributeCallbacks(dict):
    """Class designed to store callback functions for custom attributes added
    to GunGame via a subaddon.

    """
    def __new__(cls, *p, **k):
        if not '_the_instance' in cls.__dict__:
            cls._the_instance = dict.__new__(cls)
        return cls._the_instance

    def add(self, attribute, function, addon):
        """Adds a callback to execute when a previously created attribute is
        set via the _BasePlayer class __setitem__ or __setattr__ methods.

        Note:
            Do not raise errors for GunGame attributes.
        """
        # Make sure that the function is callable
        if not callable(function):
            raise AttributeError('Callback "%s" is not callable.' % function)

        if not attribute in self:
            self[attribute] = {}

        # Add or update the attribute callback
        self[attribute].update({addon: function})

    def remove(self, attribute, addon):
        """Removes a callback to execute when a previously created attribute is
        set via the BasePlayer class' __getitem__ or __getattr__ methods.

        Note:
            No exceptions are raised if you attempt to delete a non-existant
            callback.
        """
        # Make sure the attribute callback exists
        if not attribute in self:
            return

        # Make sure that the addon exists in the attribute
        if not addon in self[attribute]:
            return

        # Delete the attribtue callback
        del self[attribute][addon]

        # See if the attribute is now empty
        if not self[attribute]:
            del self[attribute]


CALLBACKS = CustomAttributeCallbacks()

# =============================================================================
# >> POST-CLASS IMPORTS
# =============================================================================
# GunGame Imports
from players import *