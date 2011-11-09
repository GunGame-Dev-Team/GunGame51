# ../core/addons/conflicts.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''


# =============================================================================
# >> CLASSES
# =============================================================================
class ConflictError(Exception):
    '''
        Error to be raised when there is a
        conflicting addon trying to be loaded
    '''


class AddonConflicts(dict):
    '''Class used to store any Conflicting Addons'''

    def __new__(cls):
        '''Method used to make sure the class is a singleton'''

        if not '_the_instance' in cls.__dict__:
            cls._the_instance = dict.__new__(cls)
        return cls._the_instance

    def __getitem__(self, addon):
        '''Returns an addon's set of conflicts'''

        # Is the addon in the dictionary?
        if addon in self:

            # If so, simply return the set
            return super(AddonConflicts, self).__getitem__(addon)

        # Add the addon to the dictionary
        value = self[addon] = set()

        # Return the set
        return value

    def _add_conflict(self, conflict, loading_addon):
        '''Adds a conflict between addons'''

        # Add the addon that is loading to the conflicting addon's set
        self[conflict].add(loading_addon)

    def _remove_conflict(self, unloading_addon, conflict):
        '''Removes a conflict between addons'''

        # Remove the unloading addon from the conflicting addon's set
        self[conflict].discard(unloading_addon)

        # Are there any more addon's in the conflicters set?
        if not self[conflict]:

            # Remove the conflicter from the dictionary
            del self[conflict]
