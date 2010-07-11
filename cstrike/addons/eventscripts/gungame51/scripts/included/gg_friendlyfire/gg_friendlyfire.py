# ../addons/eventscripts/gungame51/scripts/included/gg_friendlyfire/gg_friendlyfire.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
# Eventscripts Imports
import es
from playerlib import getPlayerList

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.leaders.shortcuts import get_leader_level
from gungame51.core.weapons.shortcuts import get_total_levels
from gungame51.core.messaging.shortcuts import msg
from gungame51.core.players.shortcuts import Player

# ============================================================================
# >> ADDON REGISTRATION/INFORMATION
# ============================================================================
info = AddonInfo()
info.name = 'gg_friendlyfire'
info.title = 'GG Friendly Fire' 
info.author = 'GG Dev Team' 
info.version = '0.2'
info.translations = ['gg_friendlyfire']

# ============================================================================
# >> GLOBAL VARIABLES
# ============================================================================
# Get the es.ServerVar() instance of "gg_friendlyfire"
gg_friendlyfire = es.ServerVar('gg_friendlyfire')
# Get the es.ServerVar() instance of "mp_friendlyfire"
mp_friendlyfire = es.ServerVar('mp_friendlyfire')

# Backup the value of "mp_friendlyfire"
oldFriendlyFire = int(mp_friendlyfire)

# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    es.dbgmsg(0, 'Loaded: %s' % info.name)

def unload():
    es.dbgmsg(0, 'Unloaded: %s' % info.name)
    
    # Set friendlyfire back to what it was before gg_friendlyfire loaded
    mp_friendlyfire.set(oldFriendlyFire)
    
# ============================================================================
# >> GAME EVENTS
# ============================================================================
def es_map_start(event_var):
    # Set mp_friendlyfire to 0
    mp_friendlyfire.set(0)

def gg_start(event_var):
    # Set mp_friendlyfire to 0
    mp_friendlyfire.set(0)

def gg_levelup(event_var):
    # Get activation level
    activateLevel = (get_total_levels() + 1) - int(gg_friendlyfire)

    # If the Leader is on the friendlyfire level?
    if get_leader_level() >= activateLevel:
        # Check whether mp_friendlyfire is enabled
        if int(mp_friendlyfire) == 0:
            # Set mp_friendlyfire to 1
            mp_friendlyfire.set(1)

            # Send the message
            msg('#human', 'WatchYourFire', prefix=True)

            # Playing sound
            for userid in getPlayerList('#human'):
                Player(userid).playsound('friendlyfire')