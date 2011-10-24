# ../core/cfg/addons.py

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

# GunGame Imports
#   Addons
from gungame51.core.addons.dependency import DependentAddons
from gungame51.core.addons.loaded import LoadedAddons
from gungame51.core.addons.queue import AddonQueue
from gungame51.core.addons.valid import ValidAddons
#   Cfg
from manager import ConfigManager


# =============================================================================
# >> CLASSES
# =============================================================================
class AddonCvars(object):
    def __new__(cls):
        if not '_the_instance' in cls.__dict__:
            cls._the_instance = object.__new__(cls)
        return cls._the_instance

    def _register_cvar_event(self):
        es.addons.registerForEvent(self, 'server_cvar', self.server_cvar)

    def _unregister_cvar_event(self):
        es.addons.unregisterForEvent(self, 'server_cvar')

    def server_cvar(self, event_var):

        # Is this being called when the cvars are being created?
        if not ConfigManager()._files_have_been_executed:

            # If so, return
            # The cvar should be called again once the .cfg files are executed
            return

        # Get the cvar and value
        cvarname = event_var['cvarname']
        cvarvalue = event_var['cvarvalue']

        # Is the cvar the cvar for an addon?
        if not cvarname in ValidAddons().all:

            # If not, simply return
            return

        # Is the value not equal to 0 (including floats) or ''?
        if self._is_enable_value(cvarvalue):

            # Is the addon already loaded?
            if cvarname in LoadedAddons():

                # Is the addon a dependent addon?
                if cvarname in DependentAddons():

                    # Was the addon recently set to be loaded by a depender?
                    if not cvarname in DependentAddons().recently_added:

                        # If not, set the addon to remain loaded
                        # when no other addons depend upon it
                        DependentAddons()[cvarname]._remain_loaded = True

                # The addon is already loaded, so return
                return

            # Load the addon
            AddonQueue().add_to_queue('load', cvarname)

        # Unload addons with the value of 0 (including floats) or ''
        else:

            # Is the addon loaded?
            if not cvarname in LoadedAddons():

                # If not, simply return
                return

            # Is the addon depended upon by other addons?
            if cvarname in DependentAddons():

                # Mark the addon as needing to be
                # unloaded when no addons depend upon it
                DependentAddons()[cvarname]._remain_loaded = False

                # Force the value back to 1
                es.forceval(cvarname, 1)

                # Return, since we do not want to unload the dependent addon
                return

            # Unload the addon
            AddonQueue().add_to_queue('unload', cvarname)

    @staticmethod
    def _is_enable_value(value):
        '''
            Method used to determine if the cvar is
            being set to an enable or disable value
        '''

        # Is the value an empty string?
        if not value:

            # If empty string, return False
            return False

        # Use try/except to get the float value of the cvar
        try:

            # Get the float value
            value = float(value)

            # Return True or False
            return bool(value)

        # Used in case an error occurs when floating the value
        except:

            # Return True in this instance
            return True

    @staticmethod
    def _is_default_value(name, value):
        return str(ConfigManager()._cvar_defaults[cvarname]) == cvarvalue
