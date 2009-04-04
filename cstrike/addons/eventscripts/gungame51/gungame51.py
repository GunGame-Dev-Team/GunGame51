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
from core.cfg.files import *

# ============================================================================
# >> TEST CODE
# ============================================================================
def load():
    # Load our test addons
    es.dbgmsg(0, '')
    es.dbgmsg(0, 'LOADING ADDONS:')
    es.dbgmsg(0, '-'*30)
    loadAddon('gg_deathmatch')
    loadAddon('gg_assist')
    loadAddon('gg_multi_level')
    
    # Oops! We can't unload turbo...it is a requirement of gg_deathmatch...
    unloadAddon('gg_turbo')
    es.dbgmsg(0, '-'*30)
    es.dbgmsg(0, '')
    
def unload():
    from core.addons import __addons__
    es.dbgmsg(0, '')
    es.dbgmsg(0, 'UNLOADING ADDONS:')
    es.dbgmsg(0, '-'*30)
    es.dbgmsg(0, '# of addons loaded: %i' %len(getAddonInfo()))
    # Create a copy of the list of addons
    list_addons = __addons__.__order__[:]
    # We need to unload in reverse due to DependencyErrors
    list_addons.reverse()
    for name in list_addons:
        unloadAddon(name)
        es.dbgmsg(0, '# of addons remaining: %i' %len(getAddonInfo()))
    es.dbgmsg(0, '-'*30)
    es.dbgmsg(0, '')