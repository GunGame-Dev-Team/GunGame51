# ../core/cfg/__init__.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame Imports
#   Cfg
from addons import AddonCvars
from dictionary import ConfigTypeDictionary
from manager import ConfigManager


# =============================================================================
# >> FUNCTIONS
# =============================================================================
def load_configs():
    '''Loads all configs and registers the server_cvar event'''

    # Load all configs
    ConfigManager()._load_configs()

    # Register the server_cvar event
    AddonCvars()._register_cvar_event()


def unload_configs():
    '''Unloads and cleans up the configuration structure'''

    # Unregister the server cvar hooking
    AddonCvars()._unregister_cvar_event()

    # Unload configuration files
    ConfigManager()._unload_configs()


def generate_header(config):
    '''
    Generates a generic header based off of the addon name.
    '''
    config.text('*' * 76)

    # Retrieve the config path
    cfgPath = config.cfgpath

    # Get the addon name from the config path
    addon = cfgPath.split('/')[len(cfgPath.split('/')) - 1].replace('.cfg', '')

    # Split the name via underscores
    list_title = str(addon).split('_')

    # Format the addon title
    addonTitle = '%s.cfg --' % str(addon)
    for index in range(1, len(list_title)):
        addonTitle += ' %s' % list_title[index].title()
    addonTitle += ' Configuration'

    config.text('*' + addonTitle.center(74) + '*')
    config.text('*' + ' ' * 74 + '*')
    config.text('*' + 'This file defines GunGame Addon settings.'.center(74) +
                '*')
    config.text('*' + ' ' * 74 + '*')
    config.text('*' +
                'Note: Any alteration of this file requires a'.center(74) +
                '*')
    config.text('*' + 'server restart or a reload of GunGame.'.center(74) +
                '*')
    config.text('*' * 76)
    config.text('')
    config.text('')
