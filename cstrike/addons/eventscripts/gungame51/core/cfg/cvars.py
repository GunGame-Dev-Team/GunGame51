# ../core/cfg/cvars.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame Imports
#   Cfg
from attributes import *
from manager import ConfigManager


# =============================================================================
# >> CLASSES
# =============================================================================
class CvarContextManager(object):
    '''
    Context Management class used to create variables within config files
    '''

    def __init__(self, cvarname, notify, config):
        '''Called when the class is first initialized'''

        # Create the cvar's attributes as their base values
        self.cvarname = cvarname
        self.name = None
        self.description = ListDescription(config)
        self.instructions = ListInstructions(config)
        self.notes = ListNotes(config)
        self.extra = ListManagement(config)
        self.examples = ListExamples(config)
        self.options = ListOptions(config)
        self.default = None
        self.default_text = None
        self.text = None
        self.notify = notify

    def __enter__(self):
        '''Returns the class instance to use for Context Management'''

        # Return the class
        return self

    def __exit__(self, exc_type, exc_value, _traceback):
        '''Verifies that certain attributes have values on exit'''

        # Was an error encountered?
        if _traceback:

            # Print the traceback
            es.dbgmsg(0, _traceback)
            return False

        # Does the cvar have a name value?
        if self.name is None:

            # Raise an error
            raise ValueError('No "name" set for "' + self.cvarname + '"')

        # Does the cvar have a default value?
        if self.default is None:

            # Raise an error
            raise ValueError(
                'No default value set for "' + self.cvarname + '"')

        # Does the cvar have a text value?
        if self.text is None:

            # Raise an error
            raise ValueError('No "text" set for "' + self.cvarname + '"')

        # Add the cvar with it's default value to ConfigManager
        ConfigManager()._cvar_defaults[self.cvarname] = self.default

        # Return
        return True
