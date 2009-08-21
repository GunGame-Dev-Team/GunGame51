# ../addons/eventscripts/gungame/scripts/included/gg_knife_pro/gg_knife_pro.py

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
from gungame51.core.weapons.shortcuts import getTotalLevels
from gungame51.core.messaging.shortcuts import msg
from gungame51.core.messaging.shortcuts import saytext2

# ============================================================================
# >> ADDON REGISTRATION/INFORMATION
# ============================================================================
info = AddonInfo()
info.name = 'gg_knife_pro'
info.title = 'GG Knife Pro' 
info.author = 'GG Dev Team' 
info.version = '0.1'
info.conflicts = ['gg_knife_rookie']
info.translations = ['gg_knife_pro']

# ============================================================================
# >> GLOBAL VARIABLES
# ============================================================================
gg_knife_pro_limit = es.ServerVar('gg_knife_pro_limit')
gg_allow_afk_levels = es.ServerVar('gg_allow_afk_levels')

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

    # ===================
    # Player Information
    # ===================
    attacker = int(event_var['attacker'])
    userid   = int(event_var['userid'])
    userteam = event_var['es_userteam']
    attackerteam = event_var['es_attackerteam']

    # ===================
    # Check for suicide
    # ===================
    if (attackerteam == userteam) or (userid == attacker) or (attacker == 0):
        return
    
    # ===================
    # Was weapon a knife
    # ===================
    if event_var['weapon'] != 'knife':
        return
        
    # ==================
    # Add warmup check
    # here.
    # ==================
    # .. 
   
    # ===================
    # Attacker Info
    # ===================
    ggAttacker = Player(attacker)
    
    # ===================
    # Attacker checks
    # ===================
    # Fix duplicate winning
    if ggAttacker.level >= getTotalLevels():
        return
    
    # ',,|,,' ?
    if ggAttacker.preventlevel:
        return
        
    # Is the attacker on knife or grenade level?
    if ggAttacker.weapon in ('knife', 'hegrenade'):
        msg(attacker, 'CannotSkipThisLevel', prefix=True)
        return
    
    # ===================
    # Victim info
    # ===================
    ggVictim = Player(userid)
    
    # ===================
    # Victim checks
    # ===================
    # Can the victim level down
    if ggVictim.preventlevel:
        msg(attacker, 'VictimPreventLevel', prefix=True)
        return
        
    # Is victim on level 1?
    es.msg(ggVictim.level)
    if ggVictim.level == 1:
        msg(attacker, 'VictimLevel1', prefix=True)
        return
        
    # Is the victim AFK?
    if ggVictim.afk():
        msg(attacker, 'VictimAFK', prefix=True)
        return
        
    # Is the level difference higher than the limit?
    if (ggAttacker.level - ggVictim.level) >= int(gg_knife_pro_limit) and int(gg_knife_pro_limit) != 0:
        msg(attacker, 'LevelDifferenceLimit', {'limit': int(gg_knife_pro_limit)}, prefix=True)
        return
        
    # ===================
    # Level changes
    # ===================
    ggVictim.leveldown(1, attacker, 'steal')
    ggAttacker.levelup(1, userid, 'steal')
    
    # Prevent player from leveling twice from the same knife kill
    ggAttacker.preventlevel.append('gg_knife_pro')
    gamethread.delayed(0, ggAttacker.preventlevel.remove, ('gg_knife_pro'))
     
    # ===================
    # Sounds go hurr
    # ===================
    # ...

    # ===================
    # Fire the event
    # ===================
    es.event('initialize', 'gg_knife_steal')
    es.event('setint', 'gg_knife_steal', 'attacker', attacker)
    es.event('setint', 'gg_knife_steal', 'attacker_level', ggAttacker.level)
    es.event('setint', 'gg_knife_steal', 'userid_level', ggVictim.level)
    es.event('setint', 'gg_knife_steal', 'userid', userid)
    es.event('fire', 'gg_knife_steal')
    
    # Announce the level steal
    saytext2('#human', ggAttacker.index, 'StoleLevel', {'attacker': event_var['es_attackername'], 'victim': event_var['es_username']})
    
# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================










