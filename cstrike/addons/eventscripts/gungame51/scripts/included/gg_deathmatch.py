# EventScripts Imports
import es

# GunGame Imports
from gungame51.core.addons.shortcuts import Addon

# ============================================================================
# >> TEST CODE
# ============================================================================

# Create "example_addon1" and set attributes
info = Addon('gg_deathmatch')
info.name = 'gg_deathmatch'
info.title = 'GG Deathmatch' 
info.author = 'GG Dev Team' 
info.version = '0.1' 
info.requires = ['gg_turbo', 'gg_dead_strip', 'gg_dissolver'] 
info.conflicts= ['gg_map_obj', 'gg_knife_elite', 'gg_elimination']

def load():
    es.dbgmsg(0, 'GG Deathmatch Loaded.')
    
def unload():
    es.dbgmsg(0, 'GG Deathmatch Unloaded.')
    
def player_death(event_var):
    es.msg('(gg_deathmatch) %s died!' %event_var['es_username'])