# ../core/addons/dependency.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# EventScripts Imports
#   ES
import es
#   Gamethread
from gamethread import delayed

# GunGame Imports
#   Addons
from loaded import LoadedAddons


# =============================================================================
# >> CLASSES
# =============================================================================
class _DependentAddons(dict):
    '''Class to store all dependent addons and their dependees'''

    def __init__(self):
        '''Called when the instance is created'''

        # Store a set of recently added dependencies
        self.recently_added = set()

    def __getitem__(self, dependee):
        '''Gets the addon's instance and adds it if not in the dictionary'''

        # Is the addon already depended upon?
        if dependee in self:

            # Return the addon's instance
            return super(_DependentAddons, self).__getitem__(dependee)

        # Add the dependee to the dictionary
        value = self[dependee] = _Dependency(dependee in LoadedAddons)

        # Add the addon to recently_added
        # Used to keep track of _Dependency().remain_loaded values properly
        self.recently_added.add(dependee)

        # In 1 tick, remove the addon from recently_added
        delayed(0.01, self.recently_added.discard, dependee)

        # Return the dependee's instance
        return value

    def __setitem__(self, addon, value):
        '''Adds the addon's instance to the dictionary'''

        # Is the addon loaded?
        if not addon in LoadedAddons:

            # Set the addon's cvar to 1
            es.set(addon, 1)

        # Re-call __setitem__ to add the addon to the dictionary
        super(_DependentAddons, self).__setitem__(addon, value)

    def __delitem__(self, addon):
        '''Removes the addon from the dictionary'''

        # Is the addon in the dictionary?
        if addon in self:

            # Does the addon need unloaded?
            if not self[addon].remain_loaded:

                # Set the addon's cvar to 0
                es.set(addon, 0)

            # Remove the addon from the dictionary
            super(_DependentAddons, self).__delitem__(addon)

    def _add_dependency(self, dependee, depender):
        '''Adds a dependent addon to an addon that it depends upon'''

        # Add the dependent addon to the depend
        self[dependee].add(depender)

    def _remove_dependency(self, dependee, depender):
        '''Removes a dependent addon from an addon that it depends upon'''

        # Is the depended upon addon in the dictionary?
        if not dependee in self:

            # If not, raise an error
            raise KeyError('"%s" is not a dependent' % dependee)

        # Is the dependent addon listed as a depender?
        if not depender in self[dependee]:

            # If not, raise an error
            raise ValueError('"%s" ' % depender +
                'is not listed a a depender for "%s"' % dependee)

        # Remove the dependent addon from the dependee
        self[dependee].discard(depender)

        # Are there any more addons that depend upon the given addon
        if not self[dependee]:

            # Remove the addon from the dictionary
            del self[dependee]

# Get the DependentAddons instance
DependentAddons = _DependentAddons()


class _Dependency(set):
    '''
    Class to hold a set of addons that are depended upon by the another addon
    '''

    def __init__(self, remain_loaded):
        '''Called when the class is initialized'''

        # Set the addon to be unloaded or left
        # loaded when no addons depend upon it
        self.remain_loaded = remain_loaded
