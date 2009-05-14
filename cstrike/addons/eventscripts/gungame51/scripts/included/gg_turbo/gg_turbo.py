# gungame/scripts/included/gg_turbo.py

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
import gamethread

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.players.shortcuts import Player
from gungame51.core.players.shortcuts import isDead

# ============================================================================
# >> ADDON REGISTRATION/INFORMATION
# ============================================================================
info = AddonInfo()
info.name = 'gg_turbo'
info.title = 'GG Turbo' 
info.author = 'GG Dev Team' 
info.version = '0.1'

# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    es.dbgmsg(0, 'Loaded: %s' % info.name)
    
def unload():
    es.dbgmsg(0, 'Unloaded: %s' % info.name)
    
# ============================================================================
# >> GUNGAME EVENTS
# ============================================================================
def gg_levelup(event_var):

    userid = int(event_var['leveler'])
    
    # Strip and give weapon
    giveWeapon(userid)

def gg_leveldown(event_var):

    userid = int(event_var['leveler'])

    # Strip and give weapon
    giveWeapon(userid)

# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
def giveWeapon(userid):
    
    # Do player checks first
    if not playerChecks(userid):
        return
    
    # Get player
    player = Player(userid)

    # Give them their next weapon
    player.giveWeapon()
    
    # Make them use it
    es.sexec(userid, "use weapon_%s" % player.weapon)
    
def playerChecks(userid):

    # Get player
    player = Player(userid)

    # Is player dead?
    if isDead(userid):
        # Return
        return False
        
    # TODO: Add more checks here
    # ...
    return True















