# ../cstrike/addons/eventscripts/gungame/core/cfg/__init__.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
# EventScripts Imports
import es

# GunGame Imports
from gungame51.core.addons import getValidAddons
from gungame51.core.addons import __addons__
from gungame51.core.addons import load
from gungame51.core.addons import unload

# ============================================================================
# >> CLASSES
# ============================================================================
class ConfigManager(object):
    def __init__(self):
        self.__loaded__ = {}
        es.addons.registerForEvent(self, 'server_cvar', self.server_cvar)
        
    def load(self, name):
        # Retrieve the config module
        config = self.getConfigByName(name)
        
        # Load the config
        config.load()
        
    def unload(self, name):
        # Retrieve the config module
        config = self.getConfigByName(name)
        
        # Unload the config
        config.unload()
        
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
        
        return self.__loaded__[name]
        
    def server_cvar(self, event_var):
        cvarName = event_var['cvarname']
        cvarValue = event_var['cvarvalue']
        
        if cvarName not in getValidAddons():
            return
            
        # Load addons if the value is greater than 0
        if int(cvarValue) > 0:
            # Make sure the addon is not already loaded
            if cvarName not in __addons__.__loaded__:
                load(cvarName)
        # Unload addons with the value of 0
        elif int(cvarValue) == 0:
            # Make sure that the addon is loaded
            if cvarName in __addons__.__loaded__:
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