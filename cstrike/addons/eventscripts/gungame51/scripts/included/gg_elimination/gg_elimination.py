# ../addons/eventscripts/gungame/scripts/included/gg_elimination/gg_elimination.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
# Python Imports


# Eventscripts Imports
import es

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo

# ============================================================================
# >> ADDON REGISTRATION/INFORMATION
# ============================================================================
info = AddonInfo()
info.name = 'gg_elimination'
info.title = 'GG Elimination' 
info.author = 'GG Dev Team' 
info.version = '0.1'
info.requires = ['gg_turbo', 'gg_dead_strip', 'gg_dissolver']
info.conflicts = ['gg_deathmatch', 'gg_knife_elite']

# ============================================================================
# >> GLOBAL VARIABLES
# ============================================================================


# ============================================================================
# >> CLASSES
# ============================================================================


# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    es.dbgmsg(0, 'Loaded: %s' % info.name)
    
def unload():
    es.dbgmsg(0, 'Unloaded: %s' % info.name)
    
# ============================================================================
# >> GAME EVENTS
# ============================================================================


# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================