# ../core/players/callbacks.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame Imports
from . import CALLBACKS


# =============================================================================
# >> CLASSES
# =============================================================================
class PlayerCallbacks(object):
    """Class that handles custom attribute callbacks."""
    @staticmethod
    def add_attribute_callback(attribute, function, addon):
        """Adds a callback function when an attribute is set using the class-
        based dictionary CustomAttributeCallbacks. The callback function must
        have 2 arguments declared. The first argument will be the actual name
        of the attribute. The second argument will be the value that it was set
        to.

        Notes:
            * If an error is raised in your callback, the value will not be
              set.
            * You can set callbacks before you set the custom attribute on the
              player instances.
            * The intention of this method is to be able to check the value of
              custom attributes, and raise errors if they are not within
              certain ranges/specifications.

        Usage:
            Player.add_attribute_callback('attribute_name', callback_function,
                                        'gg_addon_name')

            def callback_function(name_of_the_attribute, value_to_be_checked):
                if name_of_the_attribute == 'attribute_name':
                    if value_to_be_checked > 0 and value_to_be_checked < 10:
                        pass
                    else:
                        raise ValueError('Value must be between 1 and 10!')

        """
        # Add the attribute callback to the CustomAttributeCallbacks instance
        CALLBACKS.add(attribute, function, addon)

    @staticmethod
    def remove_attribute_callback(attribute):
        """Removes a callback function that is called when a named attribute is
        set using the class-based dictionary CustomAttributeCallbacks.

        Note:
            Attempting to remove a non-existant attribute callback will not
            raise an exception.

        Usage:
            Player.remove_attribute_callback('attribute_name')

        """
        # Remove the callback from the CustomAttributeCallbacks instance
        CALLBACKS.remove(attribute)

    @staticmethod
    def remove_callbacks_for_addon(addon):
        """Removes all attribute callbacks from the class-based dictionary
        CustomAttributeCallBacks that have been associated with the named
        addon.

        Usage:
            Player.remove_callbacks_for_addon('gg_addon_name')

        Note:
            Attempting to remove attributes from an addon that does not exist
            or if no attributes exist that are associated with the addon will
            not raise an exception.

        """
        # Loop through each attribute in the CustomAttributeCallBacks instance
        for attribute in CALLBACKS.keys():
            # Continue to the next attribute if the addon name is not found
            if not addon in CALLBACKS[attribute]:
                continue

            # Remove the custom attribute callback
            CALLBACKS.remove(attribute, addon)
