# gungame/scripts/included/gg_knife_rookie.py

'''
$Rev$
$LastChangedBy: micbarr $
$LastChangedDate: 2009-04-04 22:40:08 -0400 (Sat, 04 Apr 2009) $
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
info.name = 'gg_knife_rookie'
info.title = 'GG Knife Rookie' 
info.author = 'GG Dev Team' 
info.version = '0.1'
info.conflicts['gg_knife_pro']

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