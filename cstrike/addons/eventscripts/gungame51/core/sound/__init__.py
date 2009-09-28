# ../addons/eventscripts/gungame/core/sound/__init__.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
# Python Imports
from configobj import ConfigObj

# EventScripts Imports
import es

# GunGame Imports
from gungame51.core import getGameDir

# ============================================================================
# >> GLOBALS
# ============================================================================

# ============================================================================
# >> CLASSES
# ============================================================================
class SoundPack(object):    
    def __init__(self, name):
        self.__pack__ = ConfigObj(getGameDir('cfg/gungame51/sound_packs/%s.ini' %name))

    def __getitem__(self, name):
        if self.__pack__.has_key(name):
            return self.__pack__[name]
        else:
            return None

    def __getattr__(self, name):
        if self.__pack__.has_key(name):
            return self.__pack__[name]
        else:
            return None