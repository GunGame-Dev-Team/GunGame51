# ../cstrike/addons/eventscripts/gungame51/core/addons/__init__.py

# ============================================================================
# >> IMPORTS
# ============================================================================
# Eventscripts Imports
import es

# GunGame Imports
from gungame51.core import getGameDir

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
            info.title = 'Example Addon'
        
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
        '''
        Loads a GunGame sub-addon by name
        '''
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
        '''
        Unloads a GunGame sub-addon by name
        '''
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
        '''
        Register all functions in the module as events to ES
        '''
        # Retrieve the module's dictionary
        addon_globals = addon.__dict__
        
        # Loop through all items in the module's dictionary
        for item in addon_globals:
            # Ensure that the item is callable as well as a function
            if not callable(addon_globals[item]) or \
                type(addon_globals[item]).__name__ != 'function':
                continue
                
            # See if this is an event that we have not previously registered  
            if item not in self.__events__.keys():
                # Add the event to our __events__ dictionary
                self.__events__[item] = {}
                
                # We only register the specific event once, and use
                #   self.callEvent() to handle ALL events
                es.addons.registerForEvent(self, item, self.callEvent)
                
            # Add the addon to the list of addons to call when the event triggers
            self.__events__[item][name] = addon_globals[item]
            
    def unregisterEvents(self, addon, name):
        '''
        Unregister all functions in the module from being called by ES as
        events
        '''
        # Retrieve the module's dictionary
        addon_globals = addon.__dict__
        
        # Loop through all items in the addon dictionary
        for item in addon_globals:
            # Ensure that the item is callable, as well as contained within
            #   the __events__ dictionary
            if callable(addon_globals[item]) and item in self.__events__:
                # Delete the addon from the list of addons to call when the
                #   event triggers
                current_event = self.__events__[item]
                if name in current_event:
                    del current_event[name]
                # Unregister the event if no more sub-addons are using it
                if not self.__events__[item]:
                    es.addons.unregisterForEvent(self, item)
                    
    
    def callEvent(self, event_var):
        '''
        Calls the events in sub-addons in the order dictated by __order__
        '''
        # Grab the current event's dictionary from our __events__ dictionary
        current_event = self.__events__[str(event_var['es_event'])]
        
        # Loop through each addon in the __order__ list
        for name in self.__order__:
            # If the addon name is in the current event, call the function
            if name in current_event:
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
            pass
            return
            raise DependencyError, "Sub-addon '%s' depends on and also conflicts with sub-addon(s) '%s'" % (name,
            "', '".join(conflicting))

        # Ensure this addon does not conflict with a loaded addon
        if name in conflicts:
            pass
            return
            raise DependencyError, "Loaded sub-addon(s) '%s' conflict with sub-addon '%s'" % ("', '".join(conflicts[name]), name)
            
        # Ensure loaded addons do not conflict with this addon
        conflicting = set(self.__loaded__).intersection(addon_conflict)
        if conflicting:
            pass
            return
            raise DependencyError, "Sub-addon '%s' conflicts with loaded sub-addon(s) '%s'" % (name,
            "', '".join(conflicting))
            
        # Ensure addons depended on by this sub-addon are loaded
        conflicting = set(self.__loaded__).difference(addon_depend)
        
        # WEIRD ERROR HERE!!!!!!!!!!!!!!!!!!!!!!!
        if not conflicting:
            pass
            return
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
        
        
        # Grab the addon info
        info = self.getAddonInfo(mod.__name__.split('.')[-1])
        # Gather a list of dependencies
        addon_depend = info.requires if 'requires' in info else []
        # Gather a list of conflicts
        addon_conflict = info.conflicts if 'conflicts' in info else []
        
        #es.dbgmsg(0, 'Requires: %s' %addon_depend)
        #es.dbgmsg(0, 'Conflicts: %s' %addon_conflict)

        return addon_depend, addon_conflict

    def getAddonByName(self, name):
        '''
        Returns the module of an addon by name
        '''
        # If the addon is loaded we have stored the module
        if name in self.__loaded__:
            return self.__loaded__[name]
      
        # If the addon is not loaded we need to import it
        addonType = AddonManager().getAddonType(name)
        modulePath = 'gungame51.scripts.%s.%s' %(addonType, name)
        mod = __import__(modulePath, globals(), locals(), [''])
        return mod
        
    # ========================================================================
    # AddonManager() Static Class Methods
    # ========================================================================
    @staticmethod
    def getAddonInfo(addon=None):
        '''
        Returns the AddonInfo instance in the module if present
        '''
        if not addon:
            # Return a dictionary of all addons
            dict_addon = {}
            for name in __addons__.__loaded__:
                addon = AddonManager().getAddonByName(name)
                addon_globals = addon.__dict__
                for item in addon_globals:
                    if isinstance(addon_globals[item], AddonInfo):
                        dict_addon[name] =  addon_globals[item]
                        break
            return dict_addon
                
        if type(addon).__name__ == 'str':
            addon = AddonManager().getAddonByName(addon)
            
        # If the addon info exists we return it
        addon_globals = addon.__dict__
        for name in addon_globals:
            if isinstance(addon_globals[name], AddonInfo):
                return addon_globals[name]
                
        return None
        
    @staticmethod
    def getAddonType(name):
        '''
        Returns a string value of the addon type:
            "custom"
            "included"
        '''
        # Check addon exists
        if not AddonManager().addonExists(name):
            raise ValueError('Cannot get addon type (%s): doesn\'t exist.'
                % name)
        
        from os.path import isfile
        
        # Get addon type
        if isfile(getGameDir('addons/eventscripts/gungame51/scripts/included/%s.py'
            %name)):
            return 'included'
        elif isfile(getGameDir('addons/eventscripts/gungame51/scripts/custom/%s.py'
            %name)):
            return 'custom'
            
    @staticmethod
    def addonExists(name):
        '''
        Returns an int (bool) value depending on a GunGame addon's existance.
            0 = False (addon does not exist)
            1 = True (addon does exist)
            
        NOTE:
            This function only searches for addons that are to be included
            with GunGame 5.1+. It searches for the "addon_name.py" in the
            directories:
                "../<MOD>/addons/eventscripts/gungame/scripts/included"
                "../<MOD>/addons/eventscripts/gungame/scripts/custom"
                
            If the "addon_name.py" of the script does not exist, 0 will be
            returned.
            
        USAGE:
            from core.addons.shortcuts import addonExists
        '''
        from os.path import isfile
        
        return int(isfile(getGameDir('addons/eventscripts/gungame51/scripts' +
                                      '/included/%s.py' %name))) or \
                                      int(isfile(getGameDir('addons' +
                                      '/eventscripts/gungame51/scripts/custom' +
                                      '/%s.py' %name)))

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