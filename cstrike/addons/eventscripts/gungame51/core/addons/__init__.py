# ../cstrike/addons/eventscripts/gungame51/core/addons/__init__.py

# ============================================================================
# >> IMPORTS
# ============================================================================
# Eventscripts Imports
import es

# GunGame Imports
from shortcuts import getAddon
from shortcuts import getAddonType

# ============================================================================
# >> CLASSES
# ============================================================================
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


class DependencyError(Exception):
   """
   We want a nice, descriptive error for dependency problems
   Due to the fact this error is unique it will need to be referenced by module
   If we want this error excepted we must except:
   gungame.DependencyError
   """
   pass

class AddonCompatibility(dict):
   """
   This class holds sub-addons that are depended on or will conflict with
   a sub-addon being loaded. The loaded sub-addon will be stored under each
   dependency or conflict so we know what addons rely or conflict with other
   addons.
   """

   def notAcceptable(self, name, namelist):
      """
      Returns a set object of sub-addons in "namelist" that intersect with
      this instance's stored dependencies or conflicts
      """
      return set(namelist).intersection(self)

   def add(self, addon_name, namelist):
      """
      Adds a list of dependencies or conflicts, storing the
      addon name under each entry so we know which addons depend on
      or conflict with other addons.
      """
      for name in namelist:
         self[name] = self.get(name, []) + [addon_name]

   def remove(self, addon_name):
      """ Removes every dependency or conflict for a sub-addon """
      for sub_addon in list(self):
         if addon_name in self[sub_addon]:
            self[sub_addon].remove(addon_name)
            if not self[sub_addon]:
               del self[sub_addon]


dependencies = AddonCompatibility()
conflicts = AddonCompatibility()

### Addon managing classes """

class AddonManager(object):
    def __init__(self):
        self.__loaded__ = {}
        self.__events__ = {}
        self.__order__ = []

    def load(self, name):
        """ Loads a GunGame sub-addon by name """
        # If the addon is loaded we cannot load it again
        if name in self.__loaded__:
            raise NameError, 'GunGame sub-addon "%s" is already loaded' % name
        
        # Retrieve the addon
        addon = self.getAddonByName(name)

        # Add dependencies or conflicts of the sub-addon being unloaded
        self.addDependenciesConflicts(addon, name)

        # Register the events in the addon
        self.registerEvents(addon, name)
        
        # Save the module by name so we know it is loaded
        self.__loaded__[name] = addon
        
        # Add the module to the order of called events
        self.__order__.append(name)
        
        # Call the load block as is normally done by ES
        # We do this last because if there is a load error we don't want to
        # stop loading the sub-addon
        self.callBlock(addon, 'load')

    def unload(self, name):
        ''' Unloads a GunGame sub-addon by name '''
        # If the addon is not loaded we cannot unload it
        if name not in self.__loaded__:
            raise NameError, "GunGame sub-addon '%s' is not loaded" % name
        
        # Retrieve the addon
        addon = self.getAddonByName(name)

        # Remove dependencies or conflicts of the sub-addon being unloaded
        self.removeDependenciesConflicts(name)

        # Unregister the events in the addon
        self.unregisterEvents(addon, name)
        
        # Remove the module from the loaded module dictionary
        del self.__loaded__[name]
        
        # Remove the module from the order of called events
        self.__order__.remove(name)
        
        # Call the unload block as is normally done by ES
        # Again, we do this last so it doesn't matter if the block errors
        self.callBlock(addon, 'unload')

    def registerEvents(self, addon, name):
        """ Register all functions in the module as events to ES """
        addon_globals = addon.__dict__
        for item in addon_globals:
            if not callable(addon_globals[item]) or type(addon_globals[item]).__name__ != 'function':
                continue
                
            if item not in self.__events__:
                self.__events__[item] = {}
                    
            # Add the addon to the list of addons to call when the event triggers
            self.__events__[item][name] = addon_globals[item]
                
            es.dbgmsg(0, 'self.__events__[%s][%s] = %s' %(item, name, addon_globals[item]))
                
            # Re-register the event to this instance passing the event name and the event variables passed by ES
            es.addons.registerForEvent(self, item, lambda event_var: self.callEvent(item, event_var))
            #es.addons.registerForEvent(addon, item, addon.__dict__[item])
                
    def unregisterEvents(self, addon, name):
        """ Unregister all functions in the module from being called by ES as events """
        addon_globals = addon.__dict__
        for item in addon_globals:
            if callable(addon_globals[item]) and item in self.__events__:
                # Delete the addon from the list of addons to call when the event triggers
                current_event = self.__events__[item]
                if name in current_event:
                    del current_event[name]
                # Unregister the event if no more sub-addons are using it
                if not self.__events__[item]:
                    es.addons.unregisterForEvent(self, item)
                    
    def callEvent(self, event_name, event_var):
        """ Calls the events in sub-addons in the order dictated by __order__ """
        current_event = self.__events__[event_name]
        es.dbgmsg(0, self.__events__)
        for name in self.__order__:
            es.msg(':::::::::::%s' %name)
            if name in current_event:
                es.msg(event_var)
                es.msg(event_name)
                es.msg(current_event)
                es.msg(current_event[name])
                current_event[name](event_var)

    def addDependenciesConflicts(self, addon, name):
        '''
        Raises an error if there is a dependency or conflict problem or adds
        the addon's dependencies and conflicts to the existing dictionaries
        '''
        # Gather a list of dependencies and conflicts
        addon_depend, addon_conflict = self.getDependenciesConflicts(name)
        
        # If an addon is depended on and also conflicts, wth?
        conflicting = set(addon_depend).intersection(addon_conflict)
        
        if conflicting:
            raise DependencyError, "Sub-addon '%s' depends on and also conflicts with sub-addon(s) '%s'" % (name,
            "', '".join(conflicting))

        # Ensure this addon does not conflict with a loaded addon
        if name in conflicts:
            raise DependencyError, "Loaded sub-addon(s) '%s' conflict with sub-addon '%s'" % ("', '".join(conflicts[name]), name)
            
        # Ensure loaded addons do not conflict with this addon
        conflicting = set(self.__loaded__).intersection(addon_conflict)
        if conflicting:
            raise DependencyError, "Sub-addon '%s' conflicts with loaded sub-addon(s) '%s'" % (name,
            "', '".join(conflicting))
            
        # Ensure addons depended on by this sub-addon are loaded
        conflicting = set(self.__loaded__).difference(addon_depend)
        if conflicting:
            raise DependencyError, "Sub-addon '%s' requires sub-addon(s) '%s' to be loaded" % (name,
            "', '".join(conflicting))

        # Add this sub-addon's dependencies and conflicts
        dependencies.add(name, addon_depend)
        conflicts.add(name, addon_conflict)

    def removeDependenciesConflicts(self, name):
        """ Removes the dependencies or conflicts associated with a sub-addon """
        # Remove the sub-addon's dependencies and conflicts
        dependencies.remove(name)
        conflicts.remove(name)

    def getDependenciesConflicts(self, addon):
        """ Returns the dependencies and conflicts of an addon """
        
        mod = self.getAddonByName(addon)
        
        es.dbgmsg(0, mod.__name__.split('.')[-1])
        
        # Grab the addon info
        info = getAddon(addon)
        # Gather a list of dependencies
        addon_depend = info.requires if 'requires' in info else []
        # Gather a list of conflicts
        addon_conflict = info.conflicts if 'conflicts' in info else []
        
        es.dbgmsg(0, 'Requires: %s' %addon_depend)
        es.dbgmsg(0, 'Conflicts: %s' %addon_conflict)

        return addon_depend, addon_conflict

    def getAddonByName(self, name):
        ''' Returns the module of a sub-addon by name '''
        # If the addon is loaded we have stored the module
        if name in self.__loaded__:
            return self.__loaded__[name]
      
        # If the addon is not loaded we need to import it
        addonType = getAddonType(name)
        modulePath = 'gungame51.scripts.%s.%s' %(addonType, name)
        mod = __import__(modulePath, globals(), locals(), [''])
        return mod
        
    @staticmethod
    def getAddonInfo(addon):
        """ Returns the AddonInfo instance in the module if present """
        # If the addon info exists we return it
        addon_globals = addon.__dict__
        for name in addon_globals:
            if isinstance(addon_globals[name], AddonInfo):
                return addon_globals[name]
        '''
        # If the addon info does not exist we create a temporary substitution
        info = AddonInfo()
        info.name = addon.__name__
        info.version = 'Unknown'
        '''
        return info

    @staticmethod
    def callBlock(addon, blockname, *a, **kw):
        """ Calls a block in a loaded sub-addon """
        addon_globals = addon.__dict__
        if blockname in addon_globals and callable(addon_globals[blockname]):
            addon_globals[blockname](*a, **kw)


__addons__ = AddonManager()


# ============================================================================
# >> FUNCTIONS
# ============================================================================
# These wrappers make it possible to use key addon functions
# without interacting with the AddonManager directly
def load(*a, **kw):
   __addons__.load(*a, **kw)
load.__doc__ = AddonManager.load.__doc__


def unload(*a, **kw):
   __addons__.unload(*a, **kw)
unload.__doc__ = AddonManager.unload.__doc__