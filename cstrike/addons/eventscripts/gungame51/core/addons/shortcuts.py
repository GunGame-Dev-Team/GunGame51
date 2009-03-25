# ../cstrike/addons/eventscripts/gungame51/core/addons/shortcuts.py

# GunGame Imports
from gungame51.core.addons import AddonInfo
from gungame51.core.addons import addonStorage


class Addon(object):
    '''
    This will be the class that each scripter should use within their addons.
    It should be initialized in all addons. It is a shortcut function that
    ties the AddonInfo() class into the AddonStorage() class, which allows
    the scripter as well as developers more control & information over the
    addons that are tied in with GunGame.
    
    USAGE:
        from gungame.core.addons.shortcuts import Addon
        
        info = Addon('example_addon')
        
        # The addon's name, as if you were es_load'ing it
        # This will be created for you already, but you can set it anyway
        info.name = 'example_addon'
        
        # The title of the addon, as it would be displayed in a menu
        # Each word will automatically be capitalized
        info.title = 'Example addon'
        
        # The author's name
        info.author = 'yournamehere'
        
        # The version number
        info.version = '1.0'
        
        # GunGame scripts that are required for your addon to run properly
        # This MUST be a list
        info.requires = ['gg_addon1', 'gg_addon2']
        
        # GunGame scripts that will conflict with your addon if loaded
        # This MUST be a list
        info.conflicts= ['gg_addon3', 'gg_addon4']
    '''
    
    def __init__(self, addon):
        self.addon = str(addon).lower()
        addonStorage[self.addon] = AddonInfo()
        addonStorage[self.addon]['name'] = self.addon
     
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
    '''
    Returns the stored AddonInfo() instance of the named addon from the
    AddonStorage() container class (returns a dictionary of the named addon's
    attributes).
    
    USAGE:
        from core.addons.shortcuts import getAddon
        
        myAddon = getAddon('example_addon')
        
        # Print the title of this addon
        es.msg(myAddon.title)
        
        # Set the title of this addon using the attribute method
        myAddon.title = 'Example Addon'
        
        # Set the title of this addon using the dictionary method
        myAddon['title'] = 'Example Addon'
        
        # Set the title of this addon in one line using the attribute method
        getAddon('example_addon').title = 'Example Addon'
        
        # Set the title of this addon in one line using the dictionary method
        getAddon('example_addon')['title'] = 'Example Addon'
    '''
    name = str(name).lower()
    if addonStorage.has_key(name):
        return addonStorage[str(name).lower()]
    raise KeyError('AddonStorage instance has no key: "%s".' %name)
    
def getAddons():
    '''
    Returns the stored AddonInfo() instances of all addons from the
    AddonStorage() container class (returns a nested dictionary of all addons'
    attributes). The key is the attribute "name", and the nested key/value
    pairs are the attributes.
    
    
    USAGE:
        from core.addons.shortcuts import getAddons
        
        dict_addons = getAddons()
        
        # Loop through the dictionary of addons
        for addon in dict_addons:
            # Print the addon
            es.msg(addon)
            
            # Loop through each addon individually
            for attribute in getAddons()[addon]:
                # Print the attribute name and value for each addon
                es.msg('%s = %s' %(attribute, getAddons()[addon][attribute]))
        
        # Change the title of example addon via dictionary style
        # (although better to use the getAddon() method)
        getAddons()['example_addon']['title'] = 'Example Addon'
        
        # Change the title of example addon via attribute style
        # (although better to use the getAddon() method)
        getAddons().example_addon.title = 'Example Addon'
    '''
    return addonStorage