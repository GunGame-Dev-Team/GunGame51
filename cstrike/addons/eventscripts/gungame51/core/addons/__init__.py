# ../cstrike/addons/eventscripts/gungame51/core/addons/__init__.py

class AddonInfo(dict):
    '''
    This will hold the sub-addon info similar to es.AddonInfo().
    It will be initialized in sub-addons that wish to use it.
    '''
    
    def __init__(self):
        '''
        Initialize the dictionary and populate it with mandatory
        information
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
        return ['name', 'title', 'author', 'version', 'requires', 'conflicts']
        
    
class AddonStorage(dict):
    '''
    This will contain all instances of AddonInfo() for each addon
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
        
addonStorage = AddonStorage()