# ../cstrike/addons/eventscripts/gungame51/scripts/custom/gg_assist.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate: 2009-04-13 01:35:15 -0400 (Mon, 13 Apr 2009) $
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
# Python Imports


# Eventscripts Imports
import es

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.players import Player

# ============================================================================
# >> ADDON REGISTRATION/INFORMATION
# ============================================================================
info = AddonInfo()
info.name = 'gg_assist'
info.title = 'GG Assist' 
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
    
    for userid in es.getUseridList():
        Player(userid).assistpoints = 0
    Player.addAttributeCallBack('assistpoints', callback, 'gg_assist')
    
def unload():
    es.dbgmsg(0, 'Unloaded: %s' % info.name)
    
    for userid in es.getUseridList():
        del Player(userid).assistpoints
        
    Player.removeAttributeCallBack('assistpoints')
    
# ============================================================================
# >> GAME EVENTS
# ============================================================================

def player_death(event_var):
    attacker = int(event_var['attacker'])
    victim = int(event_var['userid'])
    Player(attacker).levelup(1, victim, 'levelup')
    es.dbgmsg(0, 'Attacker\'s level : %s' %Player(attacker).level)
    #Player(attacker).leveldown(1, victim, 'leveldown')
    Player(attacker).msg()
    
def gg_levelup(event_var):
    es.dbgmsg(0, '%s just leveled up: %s' %(event_var['es_attackername'], event_var['new_level']))
    es.dbgmsg(0, '%s is on level: %s' %(event_var['es_attackername'], Player(event_var['leveler']).level))
    es.dbgmsg(0, '%s now has the weapon: %s' %(event_var['es_attackername'], Player(event_var['leveler']).weapon))
    
def gg_leveldown(event_var):
    es.dbgmsg(0, '%s just leveled down: %s' %(event_var['es_username'], event_var['new_level']))
    es.dbgmsg(0, '%s now has the weapon: %s' %(event_var['es_username'], Player(event_var['leveler']).weapon))
'''
def player_death(event_var):
    es.msg('(gg_assist) %s died!' %event_var['es_username'])
    # Only for testing sakes...
    Player(event_var['attacker']).assistpoints += 1
    
    es.dbgmsg(0, '%s\'s assist points: %s' %(event_var['es_attackername'], Player(event_var['attacker']).assistpoints))
'''

# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
def callback(name, value):
    if name == 'assistpoints':
        if value not in range(0, 100):
            raise ValueError('Value must be 0-100. Tried setting "%s" to "%s"' %(name, value))
        es.dbgmsg(0, 'Valid value for %s: %s'%(name, value))