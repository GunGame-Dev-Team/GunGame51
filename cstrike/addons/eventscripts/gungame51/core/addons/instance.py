# ../core/addons/instance.py

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
from info import AddonInfo
from valid import ValidAddons


# =============================================================================
# >> CLASSES
# =============================================================================
class AddonInstances(dict):
    '''Class that stores all included/custom addon instances'''

    def __new__(cls):
        '''Method used to make sure class is a singleton'''

        if not '_the_instance' in cls.__dict__:
            cls._the_instance = dict.__new__(cls)
        return cls._the_instance

    def __getitem__(self, addon):
        '''Returns the given addon's instance'''

        # Is the addon already in the dictionary?
        if addon in self:

            # If so, simply return the instance
            return super(AddonInstances, self).__getitem__(addon)

        # Add the addon's instance to the dictionary
        value = self[addon] = _AddonInstance(addon)

        # Return the instance
        return value


class _AddonInstance(object):
    '''Class that stores the instance of an included/custom addon'''

    def __init__(self, addon):
        '''Called when the addon is first imported'''

        # Store the addon's name
        self.basename = addon

        # Get the type of addon (included or custom)
        self.addon_type = ValidAddons().get_addon_type(self.basename)

        # Store the __module__ path for the addon
        self.module = 'gungame51.scripts.%s.%s.%s' % (
            self.addon_type, self.basename, self.basename)

        # Get the imported instance of the addon
        instance = __import__(self.module, globals(), locals(), [''])

        # Reload the instance to make sure all data is correct
        reload(instance)

        # Store the Globals for the instance
        self.globals = instance.__dict__

        # Store the AddonInfo instance of the addon
        self.info = self._get_addon_info()

    def _get_addon_info(self):
        '''Returns the AddonInfo instance for the addon'''

        # Loop through all of the globals
        for name in self.globals:

            # Is the current global an AddonInfo instance?
            if isinstance(self.globals[name], AddonInfo):

                # Return the AddonInfo instance
                return self.globals[name]

        # If no AddonInfo instance is found, return an empty one
        return AddonInfo()
