# ../cstrike/addons/eventscripts/gungame/core/cfg/shortcuts.py

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
from gungame51.core.cfg import __configs__
from gungame51.core.cfg import getConfigList

def loadConfig(names=[]):
    if not isinstance(names, list):
        names = [names,]

    for config in names:
        __configs__.load(config)

def unloadConfig(names=[]):
    if not isinstance(names, list):
        names = [names,]

    for config in names:
        __configs__.unload(config)

def getConfig(name):
    return __configs__.getConfigByName(name)

def configExists(name):
    return ConfigManager.configExists(name)

def getConfigType(name):
    return ConfigManager.getConfigType(name)

# ============================================================================
# >> DOCTSTRING REDIRECTS
# ============================================================================
# Declare the docstring for loadConfig
loadConfig.__doc__ = __configs__.load.__doc__

# Declare the docstring for unloadConfig
unloadConfig.__doc__ = __configs__.unload.__doc__

# Declare the docstring for getConfig
getConfig.__doc__ = __configs__.getConfigByName.__doc__

# Declare the docstring for configExists
configExists.__doc__ = ConfigManager.configExists.__doc__

# Declare the docstring for getConfigType
getConfigType.__doc__ = ConfigManager.getConfigType.__doc__