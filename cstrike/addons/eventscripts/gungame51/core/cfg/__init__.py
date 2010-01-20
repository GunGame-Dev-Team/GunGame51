# ../addons/eventscripts/gungame/core/cfg/__init__.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
# Python Imports
import os.path
from path import path

# EventScripts Imports
import es
import gamethread
from cfglib import AddonCFG

# GunGame Imports
from gungame51.core.addons import get_valid_addons
from gungame51.core.addons import AddonManager
from gungame51.core.addons import load
from gungame51.core.addons import unload
from gungame51.core.addons import dependencies
from gungame51.core.addons import conflicts
from gungame51.core import get_game_dir

# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
cfgExecuting = False

# =============================================================================
# >> CLASSES
# =============================================================================
class ConfigManager(object):
    '''
    Class designed to handle the loading, unloading, and executing of python
    configs coded using cfglib.AddonCFG().
    '''
    def __new__(cls, *p, **k):
        if not '_the_instance' in cls.__dict__:
            cls._the_instance = object.__new__(cls)
            # Initialize the class instance variables
            cls._the_instance.__loaded__ = {}
            cls._the_instance.__cvardefaults__ = {}
        return cls._the_instance

    # =========================================================================
    # >> ConfigManager() CUSTOM CLASS METHODS
    # =========================================================================
    def load(self, name):
        '''
        Loads the config's python file.

        Notes:
            * Attempts to execute the python file's "load" function if it
              exists.
            * Adds the "notify" flag to all CVARs declared in the config's
              python file.
            * Executes the config.
            * The scripter is responsible for the cfglib.AddonCFG().write()
              method.
        '''
        # Retrieve the config module
        config = self.get_config_by_name(name)

        # Load the config if it has a load function
        if config.__dict__.has_key('load'):
            config.load()

        # Make sure that no DependencyErrors are raised by GunGame itself due
        # to the order in which the configs are executed
        for item in config.__dict__:
            if isinstance(config.__dict__[item], AddonCFG):
                cfg = config.__dict__[item]
                # Loop through the CVARs in the configlib.AddonCFG instance
                for cvar, value, description in cfg.getCvars().values():
                    # Add the CVAR and default value to the dictionary
                    self.__cvardefaults__[cvar] = value
                    # Add the "notify" flag to the CVAR
                    es.ServerVar(cvar).addFlag('notify')
                global cfgExecuting
                cfgExecuting = True
                gamethread.delayed(0, self._reset_config_execution, ())
                cfg.execute()

    def unload(self, name):
        '''
        Unloads the config's python file.

        Notes:
            * Attempts to execute the python file's "unload" function if it
              exists.
            * Removes the "notify" flag from all CVARs declared in the config's
              python file.
        '''
        # Retrieve the config module
        config = self.get_config_by_name(name)

        for item in config.__dict__:
            if isinstance(config.__dict__[item], AddonCFG):
                cfg = config.__dict__[item]
                # Loop through the CVARs in the configlib.AddonCFG instance
                for cvar, value, description in cfg.getCvars().values():
                    # Remove the CVAR and default value from the dictionary
                    del self.__cvardefaults__[cvar]
                    # Remove the "notify" flag for the CVAR
                    es.ServerVar(cvar).removeFlag('notify')

        # Unload the config if it has an unload function
        if config.__dict__.has_key('unload'):
            config.unload()

        # Remove the stored config module
        del self.__loaded__[name]

    def _reset_config_execution(self):
        '''
        Resets the global veriable cfgExecuting for when configs are being
        executed via cfglib.AddonCFG().execute().
        '''
        global cfgExecuting
        cfgExecuting = False

    def get_config_by_name(self, name):
        '''
        Returns the module of a config by name.
        '''
        # If the config is loaded we have stored the module
        if name in self.__loaded__:
            return self.__loaded__[name]

        # Get the config type
        cfgType = ConfigManager.get_config_type(name)

        # Get the name of the addon the config belongs to
        addon = name.replace("_config", "")

        # Import the config and store the module
        if cfgType == 'main':
            self.__loaded__[name] = __import__('gungame51.core.cfg.files.%s'
                %name, globals(), locals(), [''])
        else:
            self.__loaded__[name] = __import__('gungame51.scripts' + \
                '.%s.%s.%s' %(cfgType, addon, name), globals(), locals(), [''])

        # We have to reload the module to re-instantiate the globals
        reload(self.__loaded__[name])

        return self.__loaded__[name]

    # =========================================================================
    # ConfigManager() STATIC CLASS METHODS
    # =========================================================================
    @staticmethod
    def server_cvar(event_var):
        '''
        Handles CVARs that are loaded via GunGame/'s ConfigManager.
        '''
        cvarName = event_var['cvarname']
        cvarValue = event_var['cvarvalue']

        if cvarName not in get_valid_addons():
            return

        # Load addons if the value is not 0, '', or a float equal to 0 
        if bool(str(cvarValue)) and False in \
        [x == '0' for x in str(cvarValue).split('.')]:
        
            # Make sure the addon is not already loaded
            if cvarName in AddonManager().__loaded__:
                return

            # Check to see if the user has tried to disable the addon, or if it
            # was executed by a config
            if cfgExecuting and cvarName in conflicts.keys():
                if str(ConfigManager().__cvardefaults__[cvarName]) == \
                    str(cvarValue):
                    
                    return

            gamethread.delayed(0, load, (cvarName))
            
        # Unload addons with the value of 0 (including floats) or ''
        else:
            # Make sure that the addon is loaded
            if cvarName not in AddonManager().__loaded__:
                return

            # Check to see if the user has tried to disable the addon, or if it
            # was executed by a config
            if cfgExecuting and cvarName in dependencies.keys():
                if str(ConfigManager().__cvardefaults__[cvarName]) == str(cvarValue):
                    return

            gamethread.delayed(0, unload, (cvarName))

    @staticmethod
    def config_exists(name):
        '''
        Returns an int (bool) value depending on a GunGame addon's existance.
        '''
        return get_game_dir('addons/eventscripts/gungame51/' +
            'core/cfg/files/%s.py' %name).isfile() or \
            get_game_dir('addons/eventscripts/gungame51/' +
            'scripts/included/%s/%s.py' \
                %(name.replace("_config", ""), name)).isfile() or \
            get_game_dir('addons/eventscripts/gungame51/' +
            'scripts/custom/%s/%s.py' \
                %(name.replace("_config", ""), name)).isfile()

    @staticmethod
    def get_config_type(name):
        '''
        Returns a string value of the config type:
            "custom"
            "included"
            "main"
        '''
        # Check to see if the config exists
        if not ConfigManager().config_exists(name):
            raise ValueError('Cannot get config type (%s): doesn\'t exist.'
                % name)

        # Get config type
        if get_game_dir('addons/eventscripts/gungame51/core/cfg' +
            '/files/%s.py' %name).isfile():
                return 'main'
        elif get_game_dir('addons/eventscripts/gungame51/scripts/' +
            'included/%s/%s.py' %(name.replace("_config", ""), name)).isfile():
                return 'included'
        elif get_game_dir('addons/eventscripts/gungame51/scripts/' +
            'custom/%s/%s.py' %(name.replace("_config", ""), name)).isfile():
                return 'custom'


# Register the ConfigManager instance for the "server_cvar" event
es.addons.registerForEvent(ConfigManager(), 'server_cvar', ConfigManager().server_cvar)

dict_config_types = {
    "main":get_game_dir("/addons/eventscripts/gungame51/core/cfg/files"),
    "included":get_game_dir("/addons/eventscripts/gungame51/scripts/included"),
    "custom":get_game_dir("/addons/eventscripts/gungame51/scripts/custom")
    }

# ============================================================================
# >> FUNCTIONS
# ============================================================================
def get_config_list(type=None):
    '''
    Retrieves a list of cfglib configs of the following types:
        * main (the primary GunGame configs)
        * included (included addon configs)
        * custom (custom addon configs)

    Note:
        If no argument is provided, all possible configs will be returned 
        in the list.
    '''
    # Initialize a blank list to store the config names
    list_configs = []

    # Did they supply us with a type?
    if type:
        # Make sure they provided us with a valid argument value
        if type not in dict_config_types.keys():
            raise ValueError('Invalid argument type: "%s". Use only: "%s"'
                %(type, '", "'.join(dict_config_types.keys())) + ', or None.')

        # Only search for the specific type
        searchList = [dict_config_types[type]]

    # No type argument
    else:
        # Search all possible configs
        searchList = [x for x in dict_config_types.values()]

        # Reverse the search list to execute "main" configs first
        searchList.reverse()

    # Loop through each config path
    for cfgpath in searchList:
        # Walk through all files in the path
        for file in cfgpath.walkfiles('*.py'):
            # We require the configs to end with "_config.py"
            if not file.name.endswith("_config.py"):
                continue

            # Append the config to our list of configs
            list_configs.append(file.namebase)

    # Return the list of config names (no ".py" extension)
    return list_configs
    
def generate_header(config):
    '''
    Generates a generic header based off of the addon name.
    '''
    config.text('*'*76)

    # Retrieve the config path
    cfgPath = config.cfgpath

    # Get the addon name from the config path
    addon = cfgPath.split('/')[len(cfgPath.split('/'))-1].replace('.cfg', '')

    # Split the name via underscores
    list_title = str(addon).split('_')

    # Format the addon title
    addonTitle = '%s.cfg --' %str(addon)
    for index in range(1, len(list_title)):
        addonTitle += ' %s' %list_title[index].title()
    addonTitle +=' Configuration'

    config.text('*' + addonTitle.center(74) + '*')
    config.text('*' + ' '*74 + '*')
    config.text('*' + 'This file defines GunGame Addon settings.'.center(74) +
                '*')
    config.text('*' + ' '*74 + '*')
    config.text('*' +
                'Note: Any alteration of this file requires a'.center(74) +
                '*')
    config.text('*' + 'server restart or a reload of GunGame.'.center(74) +
                '*')
    config.text('*'*76)
    config.text('')
    config.text('')