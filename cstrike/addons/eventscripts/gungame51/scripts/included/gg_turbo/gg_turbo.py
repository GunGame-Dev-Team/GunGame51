# gungame/scripts/included/gg_turbo.py

'''
$Rev: 13 $
$LastChangedBy: micbarr $
$LastChangedDate: 2009-04-06 20:23:27 -0400 (Mon, 06 Apr 2009) $
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
# Python Imports


# Eventscripts Imports
import es

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.players.shortcuts import Player

from gungame51.core.leaders.shortcuts import isLeader
from gungame51.core.leaders.shortcuts import getLeaderCount
from gungame51.core.leaders.shortcuts import getOldLeaderList
from gungame51.core.leaders.shortcuts import getLeaderList
from gungame51.core.leaders.shortcuts import getLeaderNames
from gungame51.core.leaders.shortcuts import getLeaderLevel
# ============================================================================
# >> ADDON REGISTRATION/INFORMATION
# ============================================================================
info = AddonInfo()
info.name = 'gg_turbo'
info.title = 'GG Turbo' 
info.author = 'GG Dev Team' 
info.version = '0.1'

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
    es.msg('(gg_turbo) %s died!' %event_var['es_username'])
    
def gg_levelup(event_var):
    userid = event_var['leveler']
    name = event_var['es_attackername']
    myPlayer = Player(userid)
    
    myPlayer.strip()
    myPlayer.giveWeapon()
    
    es.dbgmsg(0, '')
    es.dbgmsg(0, '='*40)
    es.dbgmsg(0, '%s (%s) is a leader: %s' %(name, userid, isLeader(userid)))
    es.dbgmsg(0, 'Leader count: %s' %getLeaderCount())
    es.dbgmsg(0, 'Leader level: %s' %getLeaderLevel())
    es.dbgmsg(0, 'Old leader list: %s' %getOldLeaderList())
    es.dbgmsg(0, 'Current leader list: %s' %getLeaderList())
    es.dbgmsg(0, 'Leader names: %s' %getLeaderNames())
    es.dbgmsg(0, '='*40)
    es.dbgmsg(0, '')
# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================