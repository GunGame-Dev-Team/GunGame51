# ../addons/eventscripts/gungame/core/cfg/shortcuts.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
# GunGame Imports
from gungame51.core.cfg import ConfigManager
from gungame51.core.cfg import get_config_list

def loadConfig(names=[]):
    if not isinstance(names, list):
        names = [names,]

    for config in names:
        ConfigManager().load(config)

def unloadConfig(names=[]):
    if not isinstance(names, list):
        names = [names,]

    for config in names:
        ConfigManager().unload(config)

def getConfig(name):
    return ConfigManager().get_config_by_name(name)

def config_exists(name):
    return ConfigManager.config_exists(name)

def get_config_type(name):
    return ConfigManager.get_config_type(name)

# ============================================================================
# >> DOCTSTRING REDIRECTS
# ============================================================================
# Declare the docstring for loadConfig
loadConfig.__doc__ = ConfigManager().load.__doc__

# Declare the docstring for unloadConfig
unloadConfig.__doc__ = ConfigManager().unload.__doc__

# Declare the docstring for getConfig
getConfig.__doc__ = ConfigManager().get_config_by_name.__doc__

# Declare the docstring for config_exists
config_exists.__doc__ = ConfigManager.config_exists.__doc__

# Declare the docstring for get_config_type
get_config_type.__doc__ = ConfigManager.get_config_type.__doc__