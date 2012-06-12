# ../core/cfg/manager.py

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
from es import dbgmsg
from es import forcevalue
from es import mexec
from es import ServerVar
#   Cfglib
from cfglib import AddonCFG
#   Gamethread
from gamethread import delayed

# GunGame Imports
#   Addons
from gungame51.core.addons.valid import ValidAddons
#   Cfg
from defaults import CvarDefaults
from dictionary import ConfigTypeDictionary
from instance import ConfigInstances
from loaded import LoadedConfigs
#   Messaging
from gungame51.core.messaging.shortcuts import langstring


# =============================================================================
# >> CLASSES
# =============================================================================
class _ConfigManager(object):
    '''
    Class designed to handle the loading, unloading, and executing of python
    configs coded using cfglib.AddonCFG().
    '''

    def __init__(self):
        '''Called when the instance is instanciated'''

        # Store a variable to know if the files have been executed
        self._files_have_been_executed = False

    def _load_configs(self):
        '''Loads all "main", "included", and "custom" addon config files'''

        # Print a message that the base cfg files
        # and the Included Addon cfg files are being loaded
        dbgmsg(0, langstring('Load_Configs'))

        # Loop through all base _config.py files
        for cfgfile in ConfigTypeDictionary.main:

            # Load the file
            self._load_config(cfgfile)

        # Loop through all Included Addon _config.py files
        for cfgfile in ConfigTypeDictionary.included:

            # Load the file
            self._load_config(cfgfile)

        # Print a message that the Custom Addon cfg files are being loaded
        dbgmsg(0, langstring('Load_CustomConfigs'))

        # Loop through all Custom Addon _config.py files
        for cfgfile in ConfigTypeDictionary.custom:

            # Load the file
            self._load_config(cfgfile)

        # Execute all cfg files in one tick
        delayed(0, self._execute_cfg_files)

    def _load_config(self, cfgfile):
        '''Loads the _config.py file and stores its location to be executed'''

        # Get the _config.py file
        config = LoadedConfigs[cfgfile.namebase]

        # Loop through all objects in the _config.py file
        for item in config.__dict__:

            # Is the object a cfglib.AddonCFG object?
            if not isinstance(config.__dict__[item], AddonCFG):

                # If not, continue
                continue

            # Add the instance to ConfigInstances
            ConfigInstances.add(config.__dict__[item])

    def _execute_cfg_files(self):
        '''Executes all .cfg files on load'''

        # Loop through all config files
        for cfg in ConfigInstances:

            # Execute the configs
            mexec('gungame51' + cfg.cfgpath.rsplit('gungame51', 1)[1])

        # Delay 1 tick to allow all cfg files to be executed
        delayed(0, self._reload_addons)

    def _reload_addons(self):
        '''Reloads addons on GunGame load'''

        # Allow server_cvar to be called
        self._files_have_been_executed = True

        # Loop through all valid addons
        for cvar in ValidAddons.all:

            # Get the current value
            value = str(ServerVar(cvar))

            # Does the cvar need reloaded?
            if value != '0':

                # Force the value back to 0 without calling server_cvar
                forcevalue(cvar, 0)

                # Set the value back to the current setting
                ServerVar(cvar).set(value)

    def _unload_configs(self):
        '''Unloads all cfg instances when unloading gungame51'''

        # Clear the CvarDefaults dictionary
        CvarDefaults.clear()

        # Unload all config files
        LoadedConfigs.clear()

        # Clear the ConfigInstances set
        ConfigInstances.clear()

# Get the ConfigManager instance
ConfigManager = _ConfigManager()
