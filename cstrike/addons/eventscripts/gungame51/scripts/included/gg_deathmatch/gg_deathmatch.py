# ../addons/eventscripts/gungame/scripts/included/gg_deathmatch/gg_deathmatch.py

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
info.name = 'gg_deathmatch'
info.title = 'GG Deathmatch' 
info.author = 'GG Dev Team' 
info.version = '0.1' 
info.requires = ['gg_turbo', 'gg_dead_strip', 'gg_dissolver'] 
info.conflicts= ['gg_map_obj', 'gg_knife_elite', 'gg_elimination']

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
def player_death(event_var):
    es.msg('(gg_deathmatch) %s died!' %event_var['es_username'])

# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================