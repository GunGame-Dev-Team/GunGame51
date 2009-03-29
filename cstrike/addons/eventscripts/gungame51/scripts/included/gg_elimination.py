# EventScripts Imports
import es

# GunGame Imports
from gungame51.core.addons.shortcuts import Addon

# ============================================================================
# >> TEST CODE
# ============================================================================

# Create "example_addon1" and set attributes
info = Addon('gg_elimination')
info.name = 'gg_elimination'
info.title = 'GG Elimination' 
info.author = 'GG Dev Team' 
info.version = '0.1' 
info.requires = ['gg_turbo', 'gg_dead_strip', 'gg_dissolver'] 
info.conflicts= ['gg_knife_elite', 'gg_deathmatch']

def load():
    es.dbgmsg(0, 'GG Elimination Loaded.')
    
def unload():
    es.dbgmsg(0, 'GG Elimination Unloaded.')
    
def player_death(event_var):
    es.msg('(gg_elimination) %s died!' %event_var['es_username'])