# ../addons/eventscripts/gungame/core/addons/shortcuts.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
# Eventscripts Imports
import es

# GunGame Imports
from gungame51.core.addons import AddonInfo
from gungame51.core.addons import AddonManager
from gungame51.core.addons import load
from gungame51.core.addons import unload

# ============================================================================
# >> FUNCTIONS
# ============================================================================
def getAddonInfo(name=None):
    '''
    Returns the stored AddonInfo() instance of the named addon from the
    AddonStorage() container class (returns a dictionary of the named addon's
    attributes).
    
    USAGE:
        from core.addons.shortcuts import getAddonInfo
        
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
    # Standardize the addon name to be a lower-case string
    if name:
        name = str(name).lower()
    
    return AddonManager.getAddonInfo(name)
    
def getAddonType(name):
    '''
    Returns a string value of the addon type:
        "custom"
        "included"
    '''
    return AddonManager.getAddonType(name)

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
    return AddonManager.addonExists(name)

# These are only here temporarily. Do not use them in scripts.
def loadAddon(name):
   '''
   Loads GunGame Addons
   '''
   load(name)
   
def unloadAddon(name):
   '''
   Unloads GunGame Addons
   '''
   unload(name)