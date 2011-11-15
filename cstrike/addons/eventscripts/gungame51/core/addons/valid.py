# ../core/addons/valid.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame Imports
from gungame51.core import get_game_dir


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Store the path to the scripts directory
_main_addon_path = get_game_dir('addons/eventscripts/gungame51/scripts')


# =============================================================================
# >> CLASSES
# =============================================================================
class ValidAddons(dict):
    '''Class used to get/store all valid addons and their type'''

    def __new__(cls):
        '''Method used to make sure class is a singleton'''

        if not '_the_instance' in cls.__dict__:
            cls._the_instance = dict.__new__(cls)
        return cls._the_instance

    def __init__(self):
        '''Gets all addons if the class has not already be initialized'''

        # Are there any values in the dictionary?
        if self:

            # If so, no need to get the addons again
            return

        # Store the included addons
        self.included = self._get_addons_by_type('included')

        # Store the custom addons
        # Make sure that each addon is only listed once
        self.custom = self._get_addons_by_type(
            'custom').difference(self.included)

    def __getattr__(self, attr):
        '''Redirects to __getitem__ since this is a dictionary'''

        # Redirect to __getitem__
        return self.__getitem__(attr)

    def __setattr__(self, attr, value):
        '''Redirects to __setitem__ since this is a dictionary'''

        # Redirect to __setitem__
        self.__setitem__(attr, value)

    def __setitem__(self, item, value):
        '''
            Makes sure that only included and custom are keys to the dictionary
        '''

        # Is the item a proper addon type?
        if not item in ('included', 'custom'):

            # If not, raise an error
            raise KeyError('Key must be either "included" or "custom"')

        # Use super to finish setting the item
        super(ValidAddons, self).__setitem__(item, value)

    def get_addon_type(self, addon):
        '''Returns the "type" of addon (included or custom)'''

        # Loop through the addon types
        for addon_type in self:

            # Is the given addon a member of the current addon type?
            if addon in self[addon_type]:

                # Return the addon type
                return addon_type

        # If no addon type is found, raise an error
        raise ValueError('"%s" is not a valid addon' % addon)

    @property
    def all(self):
        '''Returns a set of all valid addons'''

        # Return all valid addons
        return self.included.union(self.custom)

    @staticmethod
    def _get_addons_by_type(addon_type):
        '''Returns a set of all valid addons for the given type'''

        # Return the set of addons
        return set([addon.namebase for addon in
            _main_addon_path.joinpath(addon_type).dirs()])
