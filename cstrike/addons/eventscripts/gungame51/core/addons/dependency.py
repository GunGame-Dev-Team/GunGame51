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
class DependentAddons(dict):
    '''Class to store all dependent addons and their dependees'''

    def __new__(cls):
        '''Method used to make sure the class is a singleton'''

        if not '_the_instance' in cls.__dict__:
            cls._the_instance = dict.__new__(cls)
            cls._the_instance.recently_added = set()
        return cls._the_instance

    def __getitem__(self, dependee):
        '''Gets the addon's instance and adds it if not in the dictionary'''

        # Is the addon already depended upon?
        if dependee in self:

            # Return the addon's instance
            return super(DependentAddons, self).__getitem__(dependee)

        # Add the dependee to the dictionary
        value = self[dependee] = _Dependency(dependee in LoadedAddons())

        # Add the addon to recently_added
        # Used to keep track of _Dependency()._remain_loaded values properly
        self.recently_added.add(dependee)

        # In 1 tick, remove the addon from recently_added
        delayed(0.01, self.recently_added.discard, dependee)

        # Return the dependee's instance
        return value

    def __setitem__(self, addon, value):
        '''Adds the addon's instance to the dictionary'''

        # Is the addon loaded?
        if not addon in LoadedAddons():

            # Set the addon's cvar to 1
            es.set(addon, 1)

        # Re-call __setitem__ to add the addon to the dictionary
        super(DependentAddons, self).__setitem__(addon, value)

    def __delitem__(self, addon):
        '''Removes the addon from the dictionary'''

        # Is the addon in the dictionary?
        if addon in self:

            # Does the addon need unloaded?
            if not self[addon]._remain_loaded:

                # Set the addon's cvar to 0
                es.set(addon, 0)

            # Remove the addon from the dictionary
            super(DependentAddons, self).__delitem__(addon)

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


class _Dependency(set):
    '''
    Class to hold a set of addons that are depended upon by the another addon
    '''

    def __init__(self, remain_loaded):
        '''Called when the class is initialized'''

        # Set the addon to be unloaded or left
        # loaded when no addons depend upon it
        self._remain_loaded = remain_loaded
