# ../core/cfg/defaults.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# EventScripts Imports
from es import ServerVar


# =============================================================================
# >> CLASSES
# =============================================================================
class _CvarDefaults(dict):
    '''Class that stores cvars with their default value'''

    def clear(self):
        '''Resets all cvars in the dictionary and then clears itself'''

        # Loop through all cvars in the dictionary
        for cvar in self:

            # Set the cvar to its default value
            ServerVar(cvar).set(self[cvar])

            # Remove the notify flag from the cvar
            ServerVar(cvar).removeFlag('notify')

        # Clear the dictionary
        super(_CvarDefaults, self).clear()

# Get the CvarDefaults instance
CvarDefaults = _CvarDefaults()
