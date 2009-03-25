# ../cstrike/addons/eventscripts/gungame51/core/addons/__init__.py

class AddonInfo(dict):
    '''
    This will hold the sub-addon info similar to es.AddonInfo().
    It will be initialized in sub-addons that wish to use it.
    '''
    
    def __init__(self):
        '''
        Initialize the dictionary and populate it with mandatory
        information.
        
        NOTE:
            This class is intended for internal use only.
        
        USAGE:
            from gungame.core.addons import AddonInfo
        
            info = AddonInfo()
        
            # The addon's name, as if you were unsing es_load
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
        
        self.name = ''
        self.title = ''
        self.author = ''
        self.version = '0.0'
        self.requires = []
        self.conflicts = []
        
    def __setattr__(self, name, value):
        '''
        Setting an attribute is equivalent to setting an item
        '''
        self[name] = value
        
    def __getattr__(self, name):
        '''
        Getting an attribute is equivalent to getting an item
        '''
        return self[name]
        
    def __setitem__(self, name, value):
        if name not in self._getKeyList():
            raise KeyError('AddonInfo instance has no key: "%s". \
                            Use only "%s".' 
                                %(name, '", "'.join(self._getKeyList())))
                                
        # Capitalize the first letter of each word
        if name == 'title':
            value = str(value).title()
            
        dict.__setitem__(self, name, value)
        
    def __getitem__(self, name):
        if name not in self._getKeyList():
            raise KeyError('AddonInfo instance has no key: "%s". \
                            Use only "%s".' 
                                %(name, '", "'.join(self._getKeyList())))
            
        return dict.__getitem__(self, name)
        
    @staticmethod
    def _getKeyList():
        '''
        Return a list of valid attributes.
        '''
        return ['name', 'title', 'author', 'version', 'requires', 'conflicts']
        
    
class AddonStorage(dict):
    '''
    This will contain all instances of AddonInfo() for each addon.
    
    NOTE:
        This class is intended for internal use only.
        
    USAGE:
        from gungame.core.addons import AddonStorage
        
        storage = AddonStorage()
        storage['example_addon'] = AddonInfo()
        storage['example_addon']['name'] = 'example_addon'
        storage['example_addon']['title'] = 'Example Addon'
        storage['example_addon']['author'] = 'yournamehere'
        storage['example_addon']['version'] = '1.0'
        storage['example_addon']['requires'] = ['gg_addon1', 'gg_addon2']
        storage['example_addon']['conflicts'] = ['gg_addon3', 'gg_addon4']
    '''
    
    def __setattr__(self, addon, instance):
        '''
        Store the addon as an instance of AddonInfo()
        '''
        self[addon] = instance
        
    def __getattr__(self, addon):
        '''
        Return the named addon's instance of AddonInfo()
        '''
        return self[addon]
        
# Create a dictionary to contain the instance of AddonStorage()
addonStorage = AddonStorage()