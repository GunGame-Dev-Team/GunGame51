# ../cstrike/addons/eventscripts/gungame/gungame.py

# ============================================================================
# >> IMPORTS
# ============================================================================
# EventScripts Imports
import es

# GunGame Imports
from core.addons.shortcuts import loadAddon
from core.addons.shortcuts import unloadAddon
from core.addons.shortcuts import getAddonInfo
from core.addons.shortcuts import addonExists

# ============================================================================
# >> TEST CODE
# ============================================================================
def load():
    # Load our 2 test addons
    es.dbgmsg(0, '')
    es.dbgmsg(0, 'LOADING ADDONS:')
    es.dbgmsg(0, '-'*30)
    loadAddon('gg_deathmatch')
    loadAddon('gg_assist')
    es.dbgmsg(0, '-'*30)
    es.dbgmsg(0, '')
    
def unload():
    from core.addons import __addons__
    es.dbgmsg(0, '')
    es.dbgmsg(0, 'UNLOADING ADDONS:')
    es.dbgmsg(0, '-'*30)
    es.dbgmsg(0, '# of addons loaded: %i' %len(getAddonInfo()))
    es.dbgmsg(0, '__loaded__ Addons: %s' %__addons__.__loaded__.keys())
    es.dbgmsg(0, '__order__ Addons: %s' %__addons__.__order__)
    for name in __addons__.__loaded__.copy():
        unloadAddon(name)
        # Test the count of addons via getAddonInfo()
        es.dbgmsg(0, '# of addons remaining: %i' %len(getAddonInfo()))
        es.dbgmsg(0, '__loaded__ Remaining: %s' %__addons__.__loaded__.keys())
        es.dbgmsg(0, '__order__ Remaining: %s' %__addons__.__order__)
    es.dbgmsg(0, '-'*30)
    es.dbgmsg(0, '')