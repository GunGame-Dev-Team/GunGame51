import es
from gungame51.core.addons import getValidAddons
from gungame51.core.addons import __addons__
from gungame51.core.addons import load
from gungame51.core.addons import unload

class ConfigManager(object):
    def __init__(self):
        self.__loaded__ = {}
        es.addons.registerForEvent(self, 'server_cvar', self.server_cvar)
        
    def load(self, name):
        # Retrieve the config module
        config = self.getConfigByName(name)
        
        # Load the config
        config.load()
    
    def getConfigByName(self, name):
        '''
        Returns the module of an addon by name
        '''
        # If the addon is loaded we have stored the module
        if name in self.__loaded__:
            return self.__loaded__[name]
      
        mod = __import__('gungame51.core.cfg.files.%s' %name, globals(), locals(), [''])
        return mod
        
    def server_cvar(self, event_var):
        if not event_var['cvarname'].startswith('gg_'):
            return
            
        if event_var['cvarname'] not in getValidAddons():
            return
            
        # Load addons if the value is greater than 0
        if int(event_var['cvarvalue']) > 0:
            # Make sure the addon is not already loaded
            if event_var['cvarname'] not in __addons__.__loaded__:
                load(event_var['cvarname'])
        # Unload addons with the value of 0
        elif int(event_var['cvarvalue']) == 0:
            # Make sure that the addon is loaded
            if event_var['cvarname'] in __addons__.__loaded__:
                unload(event_var['cvarname'])
        
__configs__ = ConfigManager()