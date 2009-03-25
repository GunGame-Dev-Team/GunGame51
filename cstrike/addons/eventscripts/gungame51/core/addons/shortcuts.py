# ../cstrike/addons/eventscripts/gungame51/core/addons/shortcuts.py

# GunGame Imports
from gungame51.core.addons import AddonInfo
from gungame51.core.addons import addonStorage


class Addon(object):
    def __init__(self, addon):
        self.addon = str(addon).lower()
        addonStorage[self.addon] = AddonInfo()
     
    def __getattr__(self, item):
        return addonStorage[self.addon][item]
    
    def __setattr__(self, item, value):
        if item == 'addon':
            object.__setattr__(self, item, value)
            return

        addonStorage[self.addon][item] = value
        
    def __del__(self):
        del addonStorage[self.addon]
            
def getAddon(name):
    name = str(name).lower()
    if addonStorage.has_key(name):
        return addonStorage[str(name).lower()]
    raise KeyError('AddonInfo instance has no key: "%s". \
                            Use only "%s".' 
                                %(name, '", "'.join(AddonInfo()._getKeyList())))
    
def getAddons():
    return addonStorage