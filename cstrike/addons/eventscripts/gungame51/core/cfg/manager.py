# ../core/cfg/manager.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
from path import path
# EventScripts Imports
#   ES
import es
#   Cfglib
from cfglib import AddonCFG
#   Gamethread
from gamethread import delayed

# GunGame Imports
#   Addons
from gungame51.core.addons.valid import ValidAddons
#   Cfg
from dictionary import ConfigTypeDictionary
#   Messaging
from gungame51.core.messaging.shortcuts import langstring


# =============================================================================
# >> CLASSES
# =============================================================================
class ConfigManager(object):
    '''
    Class designed to handle the loading, unloading, and executing of python
    configs coded using cfglib.AddonCFG().
    '''

    def __new__(cls):
        '''Create a new instance of ConfigManager()
            and make sure there is only "one" instance'''

        # Is there already an instance
        if not '_the_instance' in cls.__dict__:

            # Create the instance
            cls._the_instance = object.__new__(cls)

            # Initialize the class instance variables
            cls._the_instance._loaded_configs = {}
            cls._the_instance._cvar_defaults = {}
            cls._the_instance._config_files = {}
            cls._the_instance._files_have_been_executed = False

        # Return the class instance
        return cls._the_instance

    def _load_configs(self):
        '''Loads all "main", "included", and "custom" addon config files'''

        # Print a message that the base cfg files
        # and the Included Addon cfg files are being loaded
        es.dbgmsg(0, langstring('Load_Configs'))

        # Loop through all base _config.py files
        for cfgfile in ConfigTypeDictionary().main:

            # Load the file
            self._load_config(cfgfile, 'main')

        # Loop through all Included Addon _config.py files
        for cfgfile in ConfigTypeDictionary().included:

            # Load the file
            self._load_config(cfgfile, 'included')

        # Print a message that the Custom Addon cfg files are being loaded
        es.dbgmsg(0, langstring('Load_CustomConfigs'))

        # Loop through all Custom Addon _config.py files
        for cfgfile in ConfigTypeDictionary().custom:

            # Load the file
            self._load_config(cfgfile, 'custom')

        # Execute all cfg files in one tick
        delayed(0, self._execute_cfg_files)

    def _load_config(self, cfgfile, cfg_type):
        '''Loads the _config.py file and stores its location to be executed'''

        # Get the _config.py file
        config = self._import_config(cfgfile.namebase, cfg_type)

        # Does the file have a load() function?
        if 'load' in config.__dict__:

            # Load all cvars and write the cfg file
            config.load()

        # Is the current file one of the base cfg files?
        if cfg_type == 'main':

            # If so, return
            return

        # Get the path of the _config.py file
        basepath = path(config.__dict__['__file__']).namebase[:~6]

        # Does the basepath need added to the stored paths?
        if not basepath in self._config_files:

            # Loop through all objects in the _config.py file
            for item in config.__dict__:

                # Is the object a cfglib.AddonCFG object?
                if not isinstance(config.__dict__[item], AddonCFG):

                    # If not, continue
                    continue

                # Get the AddonCFG instance
                cfg = config.__dict__[item]

                # Store the addon file's path with it's AddonCFG instance
                self._config_files[basepath] = cfg

                # Loop through all cvars in the AddonCFG instance
                for cvar, value, description in cfg.getCvars().values():

                    # Add the cvar by default value to _cvar_defaults
                    self._cvar_defaults[cvar] = value

                # Stop looping
                return

    def _execute_cfg_files(self):
        '''Executes all .cfg files on load'''

        # Loop through all config files
        for cfg in self._config_files.values():

            # Execute the configs
            es.mexec('gungame51' + cfg.cfgpath.rsplit('gungame51', 1)[1])

        # Delay 1 tick to allow all cfg files to be executed
        delayed(0, self._reload_addons)

    def _reload_addons(self):
        '''Reloads addons on GunGame load'''

        # Allow server_cvar to be called
        self._files_have_been_executed = True

        # Get a list of all valid addons
        valid_addons = ValidAddons().all

        # Loop through all valid addons
        for cvar in valid_addons:

            # Get the current value
            value = str(es.ServerVar(cvar))

            # Does the cvar need reloaded?
            if value != '0':

                # Force the value back to 0 without calling server_cvar
                es.forcevalue(cvar, 0)

                # Set the value back to the current setting
                es.set(cvar, value)

    def _import_config(self, name, cfg_type):
        '''Imports a *_config.py and returns its instance'''

        # Has the file already been imported?
        if name in self._loaded_configs:

            # Return the file's instance
            return self._loaded_configs[name]

        # Is the current file one of the base *_config.py files?
        if cfg_type == 'main':

            # Import the file
            self._loaded_configs[name] = __import__(
                'gungame51.core.cfg.files.%s' % name,
                globals(), locals(), [''])

        # Is the current file an included/custom addon *_config.py file?
        else:

            # Remove the trailing _config from the path to get the addon name
            addon = name.replace('_config', '')

            # Import the addon's *_config.py file
            self._loaded_configs[name] = __import__(
                'gungame51.scripts.%s.%s.%s' % (cfg_type, addon, name),
                globals(), locals(), [''])

        # Reload the file to make sure the correct instance is returned
        reload(self._loaded_configs[name])

        # Return the instance
        return self._loaded_configs[name]

    def _unload_configs(self):
        '''Unloads all cfg instances when unloading gungame51'''

        # Loop through all stored cfg file instances
        for cfg in self._config_files.values():

            # Loop through all cvars in the AddonCFG instance
            for cvar, value, description in cfg.getCvars().values():

                # Set the cvar back to it's default value
                es.ServerVar(cvar).set(self._cvar_defaults[cvar])

                # Remove the notify flag from the cvar
                es.ServerVar(cvar).removeFlag('notify')

                # Remove the cvar from the default value dictionary
                del self._cvar_defaults[cvar]

        # Loop through all *_config.py instances
        for name in self._loaded_configs.keys():

            # Does the instance have an unload() function?
            if 'unload' in self._loaded_configs[name].__dict__:

                # Run the instance's unload function
                self._loaded_configs[name].unload()

            # Remove the instance from the storage dictionary
            del self._loaded_configs[name]

        self._config_files.clear()
