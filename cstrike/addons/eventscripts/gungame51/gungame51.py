# ../<MOD>/addons/eventscripts/gungame/gungame.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
# Python imports
import sys

# EventScripts Imports
import es
import gamethread

# GunGame Imports
#    Weapon Function Imports
from core.weapons.shortcuts import setWeaponOrder
from core.weapons.shortcuts import getLevelMultiKill

#    Load, Execute and Reload GunGame Configs
import core.cfg.files
reload(core.cfg.files)
import scripts.cfg.included
reload(scripts.cfg.included)
import scripts.cfg.custom
reload(scripts.cfg.custom)

#    Config Function Imports
from core.cfg import __configs__

#    Addon Function Imports
from core.addons.shortcuts import unloadAddon

#    Core Function Imports
from core import isDead, isSpectator, inMap

#    Player Function Imports
from core.players.shortcuts import Player

# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    # Load translation file for gungame
    #gungamelib.loadTranslations('gungame')
    
    # Exec server.cfg before gungame loads.  If gungame is loaded from autoexec
    # this is needed so that the correct values are stored.
    es.server.cmd('exec server.cfg')
    
    try:
        initialize()
    except:
        #gungamelib.echo('gungame', 0, 0, 'Load_Exception')
        es.dbgmsg(0, '[GunGame] %s' % ('=' * 80))
        es.excepter(*sys.exc_info())
        es.dbgmsg(0, '[GunGame] %s' % ('=' * 80))
        es.unload('gungame')
        
def unload():
    # Unload all enabled addons
    from core.addons import __addons__

    # Create a copy of the list of addons
    list_addons = __addons__.__order__[:]
    
    # We need to unload in reverse due to DependencyErrors
    list_addons.reverse()
    
    for name in list_addons:
        if name not in __addons__.__order__:
            continue
        unloadAddon(name)
    
    # Unload configs (removes flags from CVARs)
    from core.cfg import getConfigList
    
    for name in getConfigList():
        __configs__.unload(name)
    
    # Grab a random userid for the below commands
    userid = es.getuserid()
    
    # Enable Buyzones
    es.server.queuecmd('es_xfire %d func_buyzone Enable' %userid)
    
    # Get map if
    try:
        mapObjectives = int(es.ServerVar('gg_map_obj'))
        
        # Re-enable objectives
        if mapObjectives < 3:
            # Re-enable all objectives
            if mapObjectives == 0:
                if len(es.createentitylist('func_bomb_target')):
                    es.server.queuecmd('es_xfire %d func_bomb_target Enable' %userid)
                elif len(es.createentitylist('func_hostage_rescue')):
                    es.server.queuecmd('es_xfire %d func_hostage_rescue Enable' %userid)
            
            # Enable bomb zone 
            elif mapObjectives == 1:
                if len(es.createentitylist('func_bomb_target')):
                    es.server.queuecmd('es_xfire %d func_bomb_target Enable' %userid)
            
            # Enable hostage objectives
            elif mapObjectives == 2:
                if len(es.createentitylist('func_hostage_rescue')):
                    es.server.queuecmd('es_xfire %d func_hostage_rescue Enable' %userid)
    except:
        pass
    
    # Fire gg_unload event
    '''
    We need to add this to the EventManager
    '''
    es.event('initialize', 'gg_unload')
    es.event('fire', 'gg_unload')
    
    '''
    gungamelib.clearGunGame()
    '''

def initialize():
    '''
    #global countBombDeathAsSuicide
    #global list_stripExceptions
    '''
    
    # Print load started
    es.dbgmsg(0, '[GunGame] %s' % ('=' * 80))
    #gungamelib.echo('gungame', 0, 0, 'Load_Start', {'version': __version__})
    
    # Load custom events
    es.loadevents('declare', 'addons/eventscripts/gungame51/core/events/data/es_gungame_events.res')
    
    # Fire the gg_server.cfg
    es.server.cmd('exec gungame51/gg_server.cfg')
    
    # Get strip exceptions
    if str(es.ServerVar('gg_map_strip_exceptions')) != '0':
        list_stripExceptions = str(es.ServerVar('gg_map_strip_exceptions')).split(',')
    
    # Get weapon order file
    # Set this as the weapon order and set the weapon order type
    currentOrder = setWeaponOrder(str(es.ServerVar('gg_weapon_order_file')), str(es.ServerVar('gg_weapon_order_sort_type')))
    
    # Set multikill override
    if int(es.ServerVar('gg_multikill_override')) > 1:
        currentOrder.setMultiKillOverride(int(es.ServerVar('gg_multikill_override')))
        
    # Echo the weapon order to console
    es.dbgmsg(0, '[GunGame]')
    currentOrder.echo()
    es.dbgmsg(0, '[GunGame]')
    '''
    gungamelib.echo('gungame', 0, 0, 'Load_Commands')
    '''
    
    # Clear out the GunGame system
    #gungamelib.resetGunGame()
    
    '''
    gungamelib.echo('gungame', 0, 0, 'Load_Warmup')
    '''

    # We will mess with this later...
    '''
    # Start warmup timer
    if inMap():
        # Check to see if the warmup round needs to be activated
        if int(es.ServerVar('gg_warmup_timer')) > 0:
        
            es.server.queuecmd('es_xload gungame/included_addons/gg_warmup_round')
        else:
            # Fire gg_start event
            es.event('initialize','gg_start')
            es.event('fire','gg_start')
    '''
    
    # Restart map
    #gungamelib.msg('gungame', '#all', 'Loaded')
    
    # Fire gg_load event
    '''
    Need to port this to the EventManager
    '''
    es.event('initialize', 'gg_load')
    es.event('fire', 'gg_load')
    
    # Print load completed
    #gungamelib.echo('gungame', 0, 0, 'Load_Completed')
    es.dbgmsg(0, '[GunGame] %s' % ('=' * 80))
    
# ============================================================================
# >> GAME EVENTS
# ============================================================================
def es_map_start(event_var):
    # Load custom GunGame events
    es.loadevents('declare', 'addons/eventscripts/gungame51/core/events/data/es_gungame_events.res')
    
    equipPlayer()
    
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
    #Shall we move this to an included addon?
    #    - Suicide check comment
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
    #Shall we move this to an included addon?
    #    - TeamKill check comment
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
    
# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
def equipPlayer():
    userid = es.getuserid()
    cmdFormat = 'es_xremove game_player_equip;' + \
                'es_xgive %s game_player_equip;' %userid + \
                'es_xfire %s game_player_equip AddOutput "weapon_knife 1"' \
                    %userid
    es.server.cmd(cmdFormat)
    
    # Retrieve the armor type
    armorType = int(es.ServerVar('gg_player_armor'))
    
    # Give the player full armor
    if armorType == 2:
        es.server.cmd('es_xfire %s game_player_equip AddOutput "item_assaultsuit 1"' % userid)
    
    # Give the player kevlar only
    elif armorType == 1:
        es.server.cmd('es_xfire %s game_player_equip AddOutput "item_kevlar 1"' % userid)

