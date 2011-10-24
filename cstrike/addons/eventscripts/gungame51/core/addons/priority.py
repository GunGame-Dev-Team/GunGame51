# ../core/addons/priority.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''


# =============================================================================
# >> CLASSES
# =============================================================================
class PriorityAddon(set):
    '''Class that holds all Priority Addons'''

    def __new__(cls, *elems):
        '''Method that makes sure the class is a singleton'''

        if not '_the_instance' in cls.__dict__:
            cls._the_instance = set.__new__(cls)
        return cls._the_instance

    def __init__(self, *elems):
        '''Adds any elements given on initialization'''

        # Update the set with the elements
        self.update(set(elems))

    def append(self, name):
        '''Added for backwards compatibility'''

        # Add the addon to the set
        self.add(name)

    def remove(self, name):
        '''Added for backwards compatibility'''

        # Remove the addon from the set
        self.discard(name)
