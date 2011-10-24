# ../core/addons/shortcuts.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame Imports
#   Addons
from info import AddonInfo
from instance import AddonInstances
from loaded import LoadedAddons
from manager import AddonManager
from valid import ValidAddons


# =============================================================================
# >> FUNCTIONS
# =============================================================================
def get_addon_info(name=None):
    '''
    Returns the stored AddonInfo() instance of the named addon from the
    AddonStorage() container class (returns a dictionary of the named addon's
    attributes).

    USAGE:
        from core.addons.shortcuts import get_addon_info

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

    # Was a specific addon wanted?
    if name:

        # Get the addon's instance
        addon = AddonInstances()[str(name).lower()]

        # Return the addon's info
        return addon.info

    # Get a list of all loaded addons
    addons = list(LoadedAddons())

    # Return a dictionary of loaded addons and their info
    return dict(zip((addon, LoadedAddons()[addon].info) for addon in addons))


def get_addon_type(name):
    '''
    Returns a string value of the addon type:
        "custom"
        "included"
    '''

    # Return the type of addon
    return ValidAddons().get_addon_type(str(name).lower())


def addon_exists(name):
    '''
    Returns an int (bool) value depending on a GunGame addon's existance.
        0 = False (addon does not exist)
        1 = True (addon does exist)

    NOTE:
        This function only searches for addons that are to be included
        with GunGame 5.1+. It searches for the "addon_name.py" in the
        directories:
            "../<MOD>/addons/eventscripts/gungame51/scripts/included"
            "../<MOD>/addons/eventscripts/gungame51/scripts/custom"

        If the "addon_name.py" of the script does not exist, 0 will be
        returned.

    USAGE:
        from core.addons.shortcuts import addon_exists
    '''

    # Is the given name a valid addon
    return str(name).lower() in ValidAddons().all


def get_loaded_addon_list(addon_type=None):
    '''Returns a list of loaded addons for the given type'''

    # Get all addons
    addons = LoadedAddons()

    # Was a specific type needed?
    if addon_type in ('custom', 'included'):

        # Return a list of loaded addons for the given type
        return [addon for addon in addons
            if addons[addon].addon_type == addon_type]

    # Return a list of all loaded addons
    return list(addons)
