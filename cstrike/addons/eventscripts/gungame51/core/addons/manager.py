# ../core/addons/manager.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame Imports
from gungame51.core import gungame_info
#   Addons
from conflicts import AddonConflicts
from dependency import DependentAddons
from loaded import LoadedAddons


# =============================================================================
# >> CLASSES
# =============================================================================
class AddonManager(object):
    def __new__(cls):
        '''Method to make sure the class is a singleton'''

        if not '_the_instance' in cls.__dict__:
            cls._the_instance = object.__new__(cls)
        return cls._the_instance

    def _load_addon(self, addon):
        '''Method used to load a GunGame sub-addon'''

        # Is the addon already loaded?
        if addon in LoadedAddons():

            # If so, raise an error
            raise NameError('GunGame sub-addon "%s" is already loaded' % addon)

        # Load the addon and get it's instance
        instance = LoadedAddons()[addon]

        # Loop through all of the addon's dependencies
        for dependee in instance.info.requires:

            # Is the dependee in LoadedAddons?
            if not dependee in LoadedAddons():

                # Load the dependee
                self._load_addon(dependee)

            # Add the dependency
            DependentAddons()._add_dependency(dependee, instance.basename)

        # Loop through all of the addon's conflicts
        for conflict in instance.info.conflicts:

            # Add the conflict
            AddonConflicts()._add_conflict(conflict, instance.basename)

        # Update GunGame info
        gungame_info('update')

    def _unload_addon(self, addon, unloading_gg=False):
        '''Method used to unload a GunGame sub-addon'''

        # Is the addon not currently loaded?
        if not addon in LoadedAddons():

            # If not, raise an error
            raise NameError('GunGame sub-addon "%s" is not loaded' % addon)

        # Get the addon's instance
        instance = LoadedAddons()[addon]

        # Loop through all of the addon's dependencies
        for dependee in instance.info.requires:

            # Store whether the dependee needs unloaded
            keep_addon_loaded = DependentAddons()[dependee]._remain_loaded

            # Add the dependency
            DependentAddons()._remove_dependency(dependee, instance.basename)

            # Does the dependee still have dependers?
            if not dependee in DependentAddons():

                # Does the dependee need unloaded?
                if not keep_addon_loaded:

                    # Unload the dependee
                    self._unload_addon(dependee)

        # Loop through all of the addon's conflicts
        for conflict in instance.info.conflicts:

            # Add the conflict
            AddonConflicts()._remove_conflict(conflict, instance.basename)

        # Remove the addon from LoadedAddons
        del LoadedAddons()[addon]

        # Is GunGame unloading?
        if not unloading_gg:

            # If not, update GunGame info
            gungame_info('update')

    @staticmethod
    def call_block(instance, blockname, *a, **kw):
        '''
            Method kept for backwards compatibility.

            Allows scripters to call other addon's functions.
        '''

        # Call the function with the given arguments and keywords
        instance.call_block(blockname, *a, **kw)

    @property
    def __loaded__(self):
        '''
            Method kept for backwards compatibility.

            Allows scripters to use the AddonManager to get LoadedAddons
        '''

        # Return the LoadedAddons dictionary
        return LoadedAddons()