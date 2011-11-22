# ../core/cfg/instance.py

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
from defaults import CvarDefaults


# =============================================================================
# >> CLASSES
# =============================================================================
class _ConfigInstances(set):
    '''Class that stores AddonCFG instances'''

    def add(self, config):
        '''Overrides the add method to also add cvars to CvarDefaults'''

        # Is the instance already in the set?
        if config in self:

            # No need to re-add it
            return

        # Loop through all cvars in the instance
        for cvar, value, description in config.getCvars().values():

            # Add the cvar with its default value to CvarDefaults
            CvarDefaults[cvar] = value

        # Add the item to the set
        super(_ConfigInstances, self).add(config)

# Get the ConfigInstances instance
ConfigInstances = _ConfigInstances()
