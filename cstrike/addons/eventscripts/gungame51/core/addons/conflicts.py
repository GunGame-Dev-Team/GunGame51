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


class _AddonConflicts(dict):
    '''Class used to store any Conflicting Addons'''

    def __getitem__(self, addon):
        '''Returns an addon's set of conflicts'''

        # Is the addon in the dictionary?
        if addon in self:

            # If so, simply return the set
            return super(_AddonConflicts, self).__getitem__(addon)

        # Add the addon to the dictionary
        value = self[addon] = set()

        # Return the set
        return value

    def _add_conflict(self, conflict, loading_addon):
        '''Adds a conflict between addons'''

        # Add the addon that is loading to the conflicting addon's set
        self[conflict].add(loading_addon)

    def _remove_conflict(self, conflict, unloading_addon):
        '''Removes a conflict between addons'''

        # Remove the unloading addon from the conflicting addon's set
        self[conflict].discard(unloading_addon)

        # Are there any more addon's in the conflicters set?
        if not self[conflict]:

            # Remove the conflicter from the dictionary
            del self[conflict]

# Get the AddonConflicts instance
AddonConflicts = _AddonConflicts()
