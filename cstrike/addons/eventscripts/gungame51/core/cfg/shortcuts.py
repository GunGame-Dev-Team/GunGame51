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
from gungame51.core.cfg import getConfigList

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
    return ConfigManager().getConfigByName(name)

def configExists(name):
    return ConfigManager.configExists(name)

def getConfigType(name):
    return ConfigManager.getConfigType(name)

# ============================================================================
# >> DOCTSTRING REDIRECTS
# ============================================================================
# Declare the docstring for loadConfig
loadConfig.__doc__ = ConfigManager().load.__doc__

# Declare the docstring for unloadConfig
unloadConfig.__doc__ = ConfigManager().unload.__doc__

# Declare the docstring for getConfig
getConfig.__doc__ = ConfigManager().getConfigByName.__doc__

# Declare the docstring for configExists
configExists.__doc__ = ConfigManager.configExists.__doc__

# Declare the docstring for getConfigType
getConfigType.__doc__ = ConfigManager.getConfigType.__doc__