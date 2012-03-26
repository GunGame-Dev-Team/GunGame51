# ../modules/backups.py

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
from es import ServerVar


# =============================================================================
# >> CLASSES
# =============================================================================
class _VariableBackups(dict):
    '''Class used to store variables with their default value'''

    def __getitem__(self, variable):
        '''Gets the variable's instance and adds it if not in the dictionary'''

        # Is the variable already being stored?
        if variable in self:

            # Return the variable's instance
            return super(_VariableBackups, self).__getitem__(variable)

        # Get the variable's instance
        value = self[variable] = _RegisteredAddons(variable)

        # Return the variable's instance
        return value

    def __delitem__(self, variable):
        '''Removes the variable from the dictionary,
            and sets it back to the default value'''

        # Is the variable in the dictionary?
        if not variable in self:

            # If the variable is not in the dictionary, simply return
            return

        # Set the variable to its default value
        ServerVar(variable).set(self[variable].default)

        # Delete the variable from the dictionary
        super(_VariableBackups, self).__delitem__(variable)

# Get the _VariableBackups instance
VariableBackups = _VariableBackups()


class _RegisteredAddons(set):
    '''Class used to register addons to the
        variable and store its default value'''

    def __init__(self, variable):
        '''Stores the variable, its default value,
            and addons that register for the variable'''

        # Store the variable
        self.variable = variable

        # Get the default value
        value = str(ServerVar(variable))

        # Try to typecast the value to float
        try:
            value = float(value)
        except:
            pass

        # Store the default value
        self.default = value

    def remove(self, addon):
        '''Unregisters an addon for the variable and removes the
            variable from the dictionary if it is no longer registered'''

        # Is the addon registered for the variable?
        if not addon in self:

            # If not, simply return
            return

        # Unregister the addon for the variable
        super(_RegisteredAddons, self).remove(addon)

        # Are any addons registered for the variable?
        if not self:

            # If not, remove the variable from the dictionary
            del VariableBackups[self.variable]
