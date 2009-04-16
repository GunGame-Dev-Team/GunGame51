# ../cstrike/addons/eventscripts/gungame/core/cfg/__init__.py

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

# ============================================================================
# >> CLASSES
# ============================================================================
class ConfigManager(object):
    def __init__(self):
        self.__loaded__ = {}
        self.__cvardefaults__ = {}
        es.addons.registerForEvent(self, 'server_cvar', self.server_cvar)
        
    def load(self, name):
        # Retrieve the config module
        config = self.getConfigByName(name)
        
        # Load the config
        config.load()
        
        # Make sure that no DependencyErrors are raised by GunGame itself due
        # to the order in which the configs are executed
        for item in config.__dict__:
            if isinstance(config.__dict__[item], AddonCFG):
                cfg = config.__dict__[item]
                global cfgExecuting
                cfgExecuting = True
                gamethread.delayed(0, self.resetConfigExecution, ())
                cfg.execute()
                for cvar, value, description in cfg.getCvars().values():
                    self.__cvardefaults__[cvar] = value

    def unload(self, name):
        # Retrieve the config module
        config = self.getConfigByName(name)
        
        # Unload the config
        config.unload()
        
        # Remove the stored config module
        del self.__loaded__[name]
        
    def resetConfigExecution(self):
        global cfgExecuting
        cfgExecuting = False
        
    def getConfigByName(self, name):
        '''
        Returns the module of an addon by name
        '''
        # If the config is loaded we have stored the module
        if name in self.__loaded__:
            return self.__loaded__[name]
        else:
            self.__loaded__[name] = __import__('gungame51.core.cfg.files.%s'
                %name, globals(), locals(), [''])
                
            # We have to reload the module to re-instantiate the globals
            reload(self.__loaded__[name])
        
        return self.__loaded__[name]
        
    def server_cvar(self, event_var):
        cvarName = event_var['cvarname']
        cvarValue = event_var['cvarvalue']
        
        if cvarName not in getValidAddons():
            return
            
        # Load addons if the value is greater than 0
        if int(cvarValue) > 0:
            # Make sure the addon is not already loaded
            if cvarName in __addons__.__loaded__:
                return
            
            # Check to see if the user has tried to disable the addon, or if it
            # was executed by a config
            if cfgExecuting and cvarName in conflicts.keys():
                if int(self.__cvardefaults__[cvarName]) == int(cvarValue):
                    return

            load(cvarName)
            
        # Unload addons with the value of 0
        elif int(cvarValue) == 0:
            # Make sure that the addon is loaded
            if cvarName not in __addons__.__loaded__:
                return

            # Check to see if the user has tried to disable the addon, or if it
            # was executed by a config
            if cfgExecuting and cvarName in dependencies.keys():
                if int(self.__cvardefaults__[cvarName]) == int(cvarValue):
                    return

            unload(cvarName)

    @staticmethod
    def getConfigType(name):
        '''
        Returns a string value of the addon type:
            "custom"
            "included"
        '''
        # Check addon exists
        if not AddonManager().addonExists(name):
            raise ValueError('Cannot get addon type (%s): doesn\'t exist.'
                % name)
        
        # Get addon type
        if os.path.isfile(getGameDir('addons/eventscripts/gungame51/scripts/included' +
            '/%s.py' %name)):
            return 'included'
        elif os.path.isfile(getGameDir('addons/eventscripts/gungame51/scripts/custom' +
            '/%s.py' %name)):
            return 'custom'
        
__configs__ = ConfigManager()

def getConfigList(type=None):
    '''
    Retrieves a list of configlib configs of the following types:
        * main (the primary GunGame configs)
        * included (included addon configs)
        * custom (custom addon configs)
        
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