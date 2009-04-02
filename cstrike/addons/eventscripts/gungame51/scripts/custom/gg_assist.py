# EventScripts Imports
import es

# GunGame Imports
from gungame51.core.addons import AddonInfo

# ============================================================================
# >> TEST CODE
# ============================================================================

# Create "example_addon1" and set attributes
info = AddonInfo()
info.name = 'gg_assist'
info.title = 'GG Assist' 
info.author = 'GG Dev Team' 
info.version = '0.1' 
info.requires = [] 
info.conflicts= []

def load():
    es.dbgmsg(0, 'GG Assist Loaded.')
    
def unload():
    es.dbgmsg(0, 'GG Assist Unloaded.')
    
def player_death(event_var):
    es.msg('(gg_assist) %s died!' %event_var['es_username'])