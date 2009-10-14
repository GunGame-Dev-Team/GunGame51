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

# EventScripts Imports
import es
import gamethread
from cfglib import AddonCFG

# GunGame Imports
from gungame51.core.addons import getValidAddons
from gungame51.core.addons import __addons__
from gungame51.core.addons import load
from gungame51.core.addons import unload
from gungame51.core.addons import dependencies
from gungame51.core.addons import conflicts
from gungame51.core import getGameDir

configExecuting = False

# =============================================================================
# >> CLASSES
# =============================================================================
class ConfigManager(object):
    '''
    Class designed to handle the loading, unloading, and executing of python
    configs coded using cfglib.AddonCFG().
    '''
    # =========================================================================
    # >> ConfigManager() CLASS INITIALIZATION
    # =========================================================================
    def __init__(self):
        self.__loaded__ = {}
        self.__cvardefaults__ = {}

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
        config = self.getConfigByName(name)

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
                gamethread.delayed(0, self.resetConfigExecution, ())
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
        config = self.getConfigByName(name)

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

    def resetConfigExecution(self):
        '''
        Resets the global veriable cfgExecuting for when configs are being
        executed via cfglib.AddonCFG().execute().
        '''
        global cfgExecuting
        cfgExecuting = False

    def getConfigByName(self, name):
        '''
        Returns the module of a config by name.
        '''
        # If the config is loaded we have stored the module
        if name in self.__loaded__:
            return self.__loaded__[name]

        # Get the config type
        cfgType = ConfigManager.getConfigType(name)

        # Import the config and store the module
        if cfgType == 'main':
            self.__loaded__[name] = __import__('gungame51.core.cfg.files.%s'
                %name, globals(), locals(), [''])
        else:
            self.__loaded__[name] = __import__('gungame51.scripts.cfg' + \
                '.%s.%s' %(cfgType, name), globals(), locals(), [''])

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

        if cvarName not in getValidAddons():
            return

        # Load addons if the value is not 0, '', or a float equal to 0 
        if bool(str(cvarValue)) and False in \
        [x == '0' for x in str(cvarValue).split('.')]:
        
            # Make sure the addon is not already loaded
            if cvarName in __addons__.__loaded__:
                return

            # Check to see if the user has tried to disable the addon, or if it
            # was executed by a config
            if cfgExecuting and cvarName in conflicts.keys():
                if str(__configs__.__cvardefaults__[cvarName]) == \
                    str(cvarValue):
                    
                    return

            gamethread.delayed(0, load, (cvarName))
            
        # Unload addons with the value of 0 (including floats) or ''
        else:
            # Make sure that the addon is loaded
            if cvarName not in __addons__.__loaded__:
                return

            # Check to see if the user has tried to disable the addon, or if it
            # was executed by a config
            if cfgExecuting and cvarName in dependencies.keys():
                if str(__configs__.__cvardefaults__[cvarName]) == str(cvarValue):
                    return

            gamethread.delayed(0, unload, (cvarName))

    @staticmethod
    def configExists(name):
        '''
        Returns an int (bool) value depending on a GunGame addon's existance.
        '''
        return int(os.path.isfile(getGameDir('addons/eventscripts/gungame51/' +
            'core/cfg/files/%s.py' %name))) or \
            int(os.path.isfile(getGameDir('addons/eventscripts/gungame51/' +
            'scripts/cfg/included/%s.py' %name))) or \
            int(os.path.isfile(getGameDir('addons/eventscripts/gungame51/' +
            'scripts/cfg/custom/%s.py' %name)))

    @staticmethod
    def getConfigType(name):
        '''
        Returns a string value of the config type:
            "custom"
            "included"
            "main"
        '''
        # Check to see if the config exists
        if not ConfigManager().configExists(name):
            raise ValueError('Cannot get config type (%s): doesn\'t exist.'
                % name)

        # Get config type
        if os.path.isfile(getGameDir('addons/eventscripts/gungame51/core/cfg' +
            '/files/%s.py' %name)):
            return 'main'
        elif os.path.isfile(getGameDir('addons/eventscripts/gungame51/' +
            'scripts/cfg/included/%s.py' %name)):
            return 'included'
        elif os.path.isfile(getGameDir('addons/eventscripts/gungame51/' +
            'scripts/cfg/custom/%s.py' %name)):
            return 'custom'

__configs__ = ConfigManager()
# Register the ConfigManager instance for the "server_cvar" event
es.addons.registerForEvent(__configs__, 'server_cvar', __configs__.server_cvar)

# ============================================================================
# >> FUNCTIONS
# ============================================================================
def getConfigList(type=None):
    '''
    Retrieves a list of configlib configs of the following types:
        * main (the primary GunGame configs)
        * included (included addon configs)
        * custom (custom addon configs)a
        
    Note:
        If no argument is provided, all possible configs will be returned in the list.
    '''
    dict_types = {'main':getGameDir('addons/eventscripts/gungame51/core/cfg/' +
                  'files'),
                  'included':getGameDir('addons/eventscripts/gungame51/' +
                  'scripts/cfg/included'),
                  'custom':getGameDir('addons/eventscripts/gungame51/scripts' +
                  '/cfg/custom')}

    list_configs = []

    if type:
        if type not in ['main', 'included', 'custom']:
            raise TypeError('Invalid argument type: "%s". Use only: "%s"'
                %(type, '", "'.join(dict_types.keys())) + ', or None.')

        searchList = [dict_types[type]]
    else:
        searchList = [dict_types['main'], dict_types['included'],
                      dict_types['custom']]

    for path in searchList:
        for item in os.listdir(path):
            # Ignore subfolders
            if os.path.isdir(os.path.join(path, item)):
                continue

            # Split the filename and extension
            filename, extension = item.split('.')

            # Ignore .pyc files
            if extension == 'pyc':
                continue

            # Ignore __init__ files
            if filename == '__init__':
                continue

            # Append the filename (without the extension)
            list_configs.append(filename)

    return list_configs