# ../cstrike/addons/eventscripts/gungame/gungame.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
# EventScripts Imports
import es
import gamethread

# GunGame Imports
from core.weapons.shortcuts import setWeaponOrder
from core.weapons.shortcuts import getWeaponOrder
from core.weapons.shortcuts import getLevelMultiKill

from core.cfg.files import *
from core.cfg import __configs__
from core.cfg import getConfigList

from core.addons.shortcuts import loadAddon
from core.addons.shortcuts import unloadAddon
from core.addons.shortcuts import getAddonInfo
from core.addons.shortcuts import addonExists

from core import isDead, isSpectator
from core.players import Player
'''
import core.addons.unittest as addons

addons.testAddonInfo()
addons.testAddonExists()
addons.testGetAddonType()
'''

# ==================================
#      THIS WILL BE IMPORTANT LATER
# LOAD WEAPON ORDERS
# LOAD CONFIGS
# LOAD ADDONS
# LOAD PLAYER CLASS
# ==================================

# ============================================================================
# >> TEST CODE
# ============================================================================
def load():
    # Load custom events
    es.loadevents('declare', 'addons/eventscripts/gungame51/core/events/data/es_gungame_events.res')
    
    currentOrder = setWeaponOrder('default_weapon_order', '#reversed')
    currentOrder.echo()
    es.dbgmsg(0, '(current) The weapon for level 7 is: %s' %currentOrder.getWeapon(7))
    es.dbgmsg(0, '(current) The multikill for level 7 is: %s' %currentOrder.getMultiKill(7))
    
    myOrder = getWeaponOrder('weapon_short.txt.zomg.whatrudoing.u.bastard')
    myOrder.echo()
    es.dbgmsg(0, '(short) The weapon for level 3 is: %s' %myOrder.getWeapon(3))
    es.dbgmsg(0, '(short) The multikill for level 3 is: %s' %myOrder.getMultiKill(3))
    es.dbgmsg(0, '(current) The weapon for level 3 is: %s' %currentOrder.getWeapon(3))
    es.dbgmsg(0, '(current) The multikill for level 3 is: %s' %currentOrder.getMultiKill(3))
    '''
    # Load our test addons
    es.dbgmsg(0, '')
    es.dbgmsg(0, 'LOADING ADDONS:')
    es.dbgmsg(0, '-'*30)
    es.server.cmd('gg_deathmatch 1')
    
    # Wow! I have to use a delay to list the addons because they load so quickly!
    #gamethread.delayed(0, listAddons, ())
    #es.server.cmd('gg_assist 1')
    '''
    #loadAddon('gg_assist')
    '''
    #es.server.cmd('gg_multi_level 1')
    
    # Oops! We can't unload turbo...it is a requirement of gg_deathmatch...
    #es.server.cmd('gg_turbo 0')
    #es.server.cmd('gg_deathmatch 0')
    
    es.dbgmsg(0, '-'*30)
    es.dbgmsg(0, '')
    '''
    
def es_map_start(event_var):
    # Load custom GunGame events
    es.loadevents('declare', 'addons/eventscripts/gungame51/core/events/data/es_gungame_events.res')
    equipPlayer()
def listAddons():
    from core.addons import __addons__
    list_addons = __addons__.__order__[:]
    for addon in list_addons:
        es.dbgmsg(0, '\t%s' %addon)
    es.dbgmsg(0, '# of addons remaining: %i' %len(getAddonInfo()))
    
def unload():
    from core.addons import __addons__
    es.dbgmsg(0, '')
    es.dbgmsg(0, 'UNLOADING ADDONS:')
    es.dbgmsg(0, '-'*30)
    es.dbgmsg(0, '# of addons loaded: %i' %len(getAddonInfo()))
    # Create a copy of the list of addons
    list_addons = __addons__.__order__[:]
    # We need to unload in reverse due to DependencyErrors
    list_addons.reverse()
    for name in list_addons:
        if name not in __addons__.__order__:
            continue
        unloadAddon(name)
        es.dbgmsg(0, '# of addons remaining: %i' %len(getAddonInfo()))
    es.dbgmsg(0, '-'*30)
    es.dbgmsg(0, '')
    
    # Testing the unloading of configs and removal of flags
    __configs__.unload('gg_en_config')
    
def equipPlayer():
    userid = es.getuserid()
    es.server.cmd('es_xremove game_player_equip')
    es.server.cmd('es_xgive %s game_player_equip' % userid)
    es.server.cmd('es_xfire %s game_player_equip AddOutput "weapon_knife 1"' % userid)
    
    # Retrieve the armor type
    armorType = int(es.ServerVar('gg_player_armor'))
    
    # Give the player full armor
    if armorType == 2:
        es.server.cmd('es_xfire %s game_player_equip AddOutput "item_assaultsuit 1"' % userid)
    
    # Give the player kevlar only
    elif armorType == 1:
        es.server.cmd('es_xfire %s game_player_equip AddOutput "item_kevlar 1"' % userid)

def round_start(event_var):
    #global list_stripExceptions
    #global countBombDeathAsSuicide
    
    # Set a global for round_active
    #gungamelib.setGlobal('round_active', 1)
    
    # Create a variable to prevent bomb explosion deaths from counting a suicides
    countBombDeathAsSuicide = False
    
    # Disable Buyzones
    userid = es.getuserid()
    es.server.cmd('es_xfire %d func_buyzone Disable' %userid)
    
    '''
    # Remove weapons
    for weapon in gungamelib.getWeaponList('all'):
        # Make sure that the admin doesn't want the weapon left on the map
        if weapon in list_stripExceptions:
            continue
    
            
        # Remove the weapon from the map
        es.server.cmd('es_xfire %d weapon_%s kill' % (userid, weapon))
    '''
    # Equip players
    equipPlayer()

    # Get map info
    mapObjectives = int(es.ServerVar('gg_map_obj'))
    
    # If both the BOMB and HOSTAGE objectives are enabled, we don't do anything else
    if mapObjectives < 3:
        # Remove all objectives
        if mapObjectives == 0:
            if len(es.createentitylist('func_bomb_target')):
                es.server.cmd('es_xfire %d func_bomb_target Disable' %userid)
                es.server.cmd('es_xfire %d weapon_c4 Kill' %userid)
            
            elif len(es.createentitylist('func_hostage_rescue')):
                es.server.cmd('es_xfire %d func_hostage_rescue Disable' %userid)
                es.server.cmd('es_xfire %d hostage_entity Kill' %userid)
        
        # Remove bomb objectives
        elif mapObjectives == 1:
            if len(es.createentitylist('func_bomb_target')):
                es.server.cmd('es_xfire %d func_bomb_target Disable' %userid)
                es.server.cmd('es_xfire %d weapon_c4 Kill' % userid)
        
        # Remove hostage objectives
        elif mapObjectives == 2:
            if len(es.createentitylist('func_hostage_rescue')):
                es.server.cmd('es_xfire %d func_hostage_rescue Disable' %userid)
                es.server.cmd('es_xfire %d hostage_entity Kill' % userid)
    '''
    if gungamelib.getVariableValue('gg_leaderweapon_warning'):
        leaderWeapon = gungamelib.getLevelWeapon(gungamelib.leaders.getLeaderLevel())
        
        # Play knife sound
        if leaderWeapon == 'knife':
            gungamelib.playSound('#all', 'knifelevel')
        
        # Play nade sound
        if leaderWeapon == 'hegrenade':
            gungamelib.playSound('#all', 'nadelevel')
    '''
    
def player_spawn(event_var):
    userid = event_var['userid']
    
    if isSpectator(userid):
        return
    
    if isDead(userid):
        return
    
    # Warmup Round Check Would Go Here
    # ....
    
    # Give the player their weapon
    es.dbgmsg(0, '%s should have a %s.' %(event_var['es_username'], Player(userid).weapon))
    Player(userid).giveWeapon()
    
    # Send the level information hudhint
    # ....
    
    # Check to see if this player is a CT
    if int(event_var['es_userteam']) == 3:
        # Check for map objectives
        if int(es.ServerVar('gg_map_obj')) > 1:
            # Are we in a de_ map and want to give defuser?
            if len(es.createentitylist('func_bomb_target')) and int(es.ServerVar('gg_player_defuser')) > 0:
                # Make sure the player doesn't already have a defuser
                if not playerlib.getPlayer(userid).get('defuser'):
                    es.server.queuecmd('es_xgive %d item_defuser' % userid)
                    
def player_death(event_var):
    # Warmup Round Check
    # ....
    
    # Set player ids
    userid = int(event_var['userid'])
    attacker = (event_var['attacker'])
    
    # Is the attacker on the server?
    if not es.exists('userid', attacker):
        return
        
    # Get victim object
    gungameVictim = Player(userid)
    
    '''
    Shall we move this to an included addon?
        - Suicide check comment
    '''
    # =============
    # SUICIDE CHECK
    # =============
    if (attacker == 0 or attacker == userid): #and countBombDeathAsSuicide:
        if int(es.ServerVar('gg_suicide_punish')) == 0:
            return
            
        # Trigger level down
        gungameVictim.leveldown(int(es.ServerVar('gg_suicide_punish')), userid, 'suicide')
        
        # Message
        #gungamelib.msg('gungame', attacker, 'Suicide_LevelDown', {'newlevel':gungameVictim.level})
        
        # Play the leveldown sound
        #gungamelib.playSound(userid, 'leveldown')
        
        return
        
    # Get attacker object
    gungameAttacker = Player(attacker)
    '''
    Shall we move this to an included addon?
        - TeamKill check comment
    '''
    # ===============
    # TEAM-KILL CHECK
    # ===============
    if (event_var['es_userteam'] == event_var['es_attackerteam']):
        if int(es.ServerVar('gg_tk_punish')) == 0:
            return
            
        # Trigger level down
        gungameAttacker.leveldown(int(es.ServerVar('gg_tk_punish')), userid, 'tk')
        
        # Message
        #gungamelib.msg('gungame', attacker, 'TeamKill_LevelDown', {'newlevel':gungameAttacker.level})
        
        # Play the leveldown sound
        #gungamelib.playSound(attacker, 'leveldown')
        
        return
        
    # ===========
    # NORMAL KILL
    # ===========
    # Get weapon name
    weapon = event_var['weapon']
    
    # Check the weapon was correct
    if weapon != gungameAttacker.weapon:
        return
    
    '''
    # Don't continue if the victim is AFK
    if gungameVictim.isPlayerAFK():
        # Tell the attacker they were AFK
        gungamelib.hudhint('gungame', attacker, 'PlayerAFK', {'player': event_var['es_username']})
        
        # Check AFK punishment
        if not gungameVictim.isbot and gungamelib.getVariableValue('gg_afk_rounds') > 0:
            afkPunishCheck(userid)
        
        return
    '''
    
    # No multikill? Just level up...
    multiKill = getLevelMultiKill(gungameAttacker.level)
    if multiKill == 1:
        # Level them up
        gungameAttacker.levelup(1, userid, 'kill')
        
        # Play the levelup sound
        #gungamelib.playSound(attacker, 'levelup')
        
        return
    
    # Using multikill
    gungameAttacker.multikill += 1
    
    # Finished the multikill
    if gungameAttacker.multikill >= multiKill:
        # Level them up
        gungameAttacker.levelup(1, userid, 'kill')
            
        # Play the levelup sound
        #gungamelib.playSound(attacker, 'levelup')
        
    # Increment their current multikill value
    else:
        # Message the attacker
        #multiKill = gungamelib.getLevelMultiKill(gungameAttacker['level'])
        #gungamelib.hudhint('gungame', attacker, 'MultikillNotification', {'kills': gungameAttacker['multikill'], 'total': multiKill})
            
        # Play the multikill sound
        #gungamelib.playSound(attacker, 'multikill')
        es.tell(attacker, 'something')
        
def gg_levelup(event_var):
    es.msg('%s leveled up by killing %s!' %(event_var['es_attackername'], event_var['es_username']))