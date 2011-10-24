# ../core/events/__init__.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# EventScripts Imports
import es

# GunGame imports
from events import *
from eventlib.resource import ResourceFile
# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
gg_resource_file = ResourceFile('%s/core/events/data/gungame_events.res' % (
                         es.getAddonPath('gungame51')))


# =============================================================================
# Resource File Creation
# =============================================================================
# Create a list of the above events
events = [GG_LevelUp, GG_LevelDown, GG_Knife_Steal, GG_Multi_Level,
          GG_New_Leader, GG_Tied_Leader, GG_Leader_LostLevel,
          GG_Leader_Disconnect, GG_Vote, GG_Win, GG_Start, GG_Map_End, GG_Load,
          GG_Unload, GG_Addon_Loaded, GG_Addon_Unloaded]

# Write the events to the resource file
gg_resource_file.write(events, overwrite=True)
