# ../core/addons/priority.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''


# =============================================================================
# >> CLASSES
# =============================================================================
class _PriorityAddon(set):
    '''Class that holds all Priority Addons'''

    def __init__(self, *elems):
        '''Adds any elements given on initialization'''

        # Update the set with the elements
        self.update(set(elems))

    def __call__(self, *elems):
        '''Adds any elements when class object is called and returns the class

           Added for backwards compat with custom addons '''

        # Update the set with the elements
        self.update(set(elems))

        # Return the class
        return self

    def append(self, name):
        '''Added for backwards compatibility'''

        # Add the addon to the set
        self.add(name)

    def remove(self, name):
        '''Added for backwards compatibility'''

        # Remove the addon from the set
        self.discard(name)

# Get the PriorityAddon instance
PriorityAddon = _PriorityAddon()
