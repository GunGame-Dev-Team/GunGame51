# ../core/addons/manager.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
#   Addons
from conflicts import AddonConflicts
from dependency import DependentAddons
from loaded import LoadedAddons


# =============================================================================
# >> CLASSES
# =============================================================================
class AddonManager(object):
    '''Class that manages loading/unloading addons'''

    def _load_addon(self, addon):
        '''Method used to load a GunGame sub-addon'''

        # Is the addon already loaded?
        if addon in LoadedAddons:

            # If so, raise an error
            raise NameError('GunGame sub-addon "%s" is already loaded' % addon)

        # Load the addon and get it's instance
        instance = LoadedAddons[addon]

        # Loop through all of the addon's dependencies
        for dependee in instance.info.requires:

            # Add the dependency
            DependentAddons._add_dependency(dependee, instance.basename)

            # Is the dependee in LoadedAddons?
            if not dependee in LoadedAddons:

                # Load the dependee
                self._load_addon(dependee)

        # Loop through all of the addon's conflicts
        for conflict in instance.info.conflicts:

            # Add the conflict
            AddonConflicts._add_conflict(conflict, instance.basename)

    def _unload_addon(self, addon):
        '''Method used to unload a GunGame sub-addon'''

        # Is the addon not currently loaded?
        if not addon in LoadedAddons:

            # If not, raise an error
            raise NameError('GunGame sub-addon "%s" is not loaded' % addon)

        # Get the addon's instance
        instance = LoadedAddons[addon]

        # Loop through all of the addon's dependencies
        for dependee in instance.info.requires:

            # Store whether the dependee needs unloaded
            keep_addon_loaded = DependentAddons[dependee].remain_loaded

            # Add the dependency
            DependentAddons._remove_dependency(dependee, instance.basename)

            # Does the dependee still have dependers?
            if not dependee in DependentAddons:

                # Does the dependee need unloaded?
                if not keep_addon_loaded:

                    # Unload the dependee
                    self._unload_addon(dependee)

        # Loop through all of the addon's conflicts
        for conflict in instance.info.conflicts:

            # Add the conflict
            AddonConflicts._remove_conflict(conflict, instance.basename)

        # Remove the addon from LoadedAddons
        del LoadedAddons[addon]

    @staticmethod
    def unload_all_addons():
        '''Method used to remove all addons on unload'''

        # Remove all dependencies
        DependentAddons.clear()

        # Remove all conflicts
        AddonConflicts.clear()

        # Loop through all loaded addons
        for addon in LoadedAddons.keys():

            # Unload the addon
            del LoadedAddons[addon]

    @staticmethod
    def call_block(instance, blockname, *a, **kw):
        '''
            Method kept for backwards compatibility.

            Allows scripters to call other addon's functions.
        '''

        # Call the function with the given arguments and keywords
        instance._call_block(blockname, *a, **kw)

    @property
    def __loaded__(self):
        '''
            Method kept for backwards compatibility.

            Allows scripters to use the AddonManager to get LoadedAddons
        '''

        # Return the LoadedAddons dictionary
        return LoadedAddons
