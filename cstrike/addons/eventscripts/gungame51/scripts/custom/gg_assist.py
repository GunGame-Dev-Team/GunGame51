# EventScripts Imports
import es

# GunGame Imports
from gungame51.core.addons.shortcuts import Addon

# ============================================================================
# >> TEST CODE
# ============================================================================

# Create "example_addon1" and set attributes
info = Addon('gg_assist')
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