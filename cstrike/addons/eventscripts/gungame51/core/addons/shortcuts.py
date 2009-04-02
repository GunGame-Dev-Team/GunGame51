# ../cstrike/addons/eventscripts/gungame51/core/addons/shortcuts.py

# ============================================================================
# >> IMPORTS
# ============================================================================
#Eventscripts Imports
import es

# ============================================================================
# >> GLOBALS
# ============================================================================
gamePath = str(es.ServerVar('eventscripts_gamedir')).replace('\\', '/')

# ============================================================================
# >> FUNCTIONS
# ============================================================================
def getAddonInfo(name=None):
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
    from gungame51.core.addons import AddonManager
    # Standardize the addon name to be a lower-case string
    if name:
        name = str(name).lower()
    
    
    return AddonManager.getAddonInfo(name)
    
def getGameDir(dir):
    '''!Gets an absolute path to a game directory.
    
    @remark Implicitly replaces \\ with / (linux support)
    
    @param dir Directory to append to the game directory.
    
    @return An absolute path to the game directory plus \p dir.'''
    # Linux path seperators
    dir = dir.replace('\\', '/')
    
    # Return
    return '%s/%s' % (gamePath, dir)
    
def getAddonType(name):
    '''
    Returns a string value of the addon type:
        "custom"
        "included"
    '''
    # Check addon exists
    if not addonExists(name):
        raise ValueError('Cannot get addon type (%s): doesn\'t exist.' % name)
    
    from os.path import isfile
    
    # Get addon type
    if isfile(getGameDir('addons/eventscripts/gungame51/scripts/included/%s.py'
        %name)):
        return 'included'
    elif isfile(getGameDir('addons/eventscripts/gungame51/scripts/custom/%s.py'
        %name)):
        return 'custom'

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
                                  
def loadAddon(name):
   """ Most likely this will be a server command block in the future """
   from gungame51.core.addons import load
   load(name)
   
def unloadAddon(name):
   """ Most likely this will be a server command block in the future """
   from gungame51.core.addons import unload
   unload(name)