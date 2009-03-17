import es


class GunGameError(Exception):
    pass

    
class Dependencies(dict):
    def __init__(self):
        super(Dependencies, self).__init__(self)
        
    def __setattr__(self, addon, dependency, value):
        # Ensure Dependency Values do not conflict
        for key in self:
            for addonName, value in self[key].items():
                if addon == addonName and value != self[key][addonName]:
                    es.dbgmsg(0, 'No way, Jose!')
        self[addon][dependency] = value
            
    def __getattr__(self, addon, dependency):
        return self[addon][dependency]


dependencies = Dependencies()


class DependencyManager(object):
    def __init__(self, addon):
        self.addon = str(addon)
        if self.addon in dependencies:
            return
            
        for key in dependencies:
            for addon, value in dependencies[key].items():
                if self.addon == addon and value == 0:
                    es.dbgmsg(0, 'Unable to load "%s". "%s" must be unloaded first.' %(self.addon, key))
                    return
                    
        dependencies[self.addon] = {}
        
    def remove(self, dependency):
        if dependency in dependencies[self.addon]:
            del dependencies[self.addon][dependency]
        
    def __getattr__(self, dependency):
        if dependency in dependencies[self.addon]:
            return dependencies[self.addon][dependency]
        raise GunGameError('Addon "%s" has no dependency registered for "%s".'
                           %(self.addon, dependency))
        
        
class Addons(object):
    def __init__(self):
        self.addonList = []
        
    def isLoaded(self, addonName):
        return int(addonName in self.addonList)
        
        
addons = Addons()
        
        
class AddonManager(object):
    def __init__(self, addon, displayName=None, dependencyDict={}):
        # The actual addon name
        self.addon = str(addon)
        
        # Name to be displayed via menus
        self.displayName = str(displayName)
        
        # The dependencies to be passed to the DependencyManager() class
        self.dependencies = dependencyDict
        
        # Register the dependencies
        if self.dependencies:
            dependencies[addon] = {}
            for addon in self.dependencies:
                dependencies[self.addon][addon] = self.dependencies[addon]
                # Temporary Debug Message
                es.dbgmsg(0, 'Addon %s set dependency for "%s %s"' %(self.addon, addon, self.dependencies[addon]))