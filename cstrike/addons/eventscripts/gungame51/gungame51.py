# ../addons/eventscripts/gungame/gungame.py

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
import os.path #gg_weapon_order_random
import random # gg_weapon_order_random

# EventScripts Imports
import es
import gamethread
from playerlib import getPlayer

# GunGame Imports

#    Weapon Function Imports
from core.weapons.shortcuts import getWeaponOrder
from core.weapons.shortcuts import setWeaponOrder
from core.weapons.shortcuts import getLevelMultiKill

#    Config Function Imports
from core.cfg.shortcuts import loadConfig
from core.cfg.shortcuts import unloadConfig
from core.cfg.shortcuts import getConfigList

#    Addon Function Imports
from core.addons.shortcuts import unloadAddon

#    Player Function Imports
from core.players.shortcuts import Player
from core.players.shortcuts import resetPlayers
from core.players.shortcuts import isDead
from core.players.shortcuts import isSpectator

#    Leaders Function Imports
from core.leaders import leaders
from core.leaders.shortcuts import resetLeaders
from core.leaders.shortcuts import isLeader

#    Core Function Imports
from core import inMap
from core import getGameDir

# Messaging imports
from core.messaging.shortcuts import loadTranslation
from core.messaging.shortcuts import unloadTranslation
from core.messaging.shortcuts import saytext2
from core.messaging.shortcuts import centermsg
from core.messaging.shortcuts import toptext
from core.messaging.shortcuts import msg

# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    # Load translations
    loadTranslation('gungame', 'gungame')
    
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
    # Unload translations
    unloadTranslation('gungame')
    
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
    unloadConfig(getConfigList())
    
    # Grab a random userid for the below commands
    userid = es.getuserid()
    
    # Enable Buyzones
    es.server.queuecmd('es_xfire %d func_buyzone Enable' %userid)
    
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
    loadConfig(getConfigList())
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
    resetPlayers()
    
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
    msg('#all', 'Loaded')
    
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
    
    # Execute GunGame's autoexec.cfg
    es.delayed('1', 'exec gungame51/gg_server.cfg')
    
    '''
    =====================================================
    THERE HAS TO BE A BETTER WAY TO HANDLE THE FOLLOWING:
    =====================================================
    
    # Reset the "gungame_voting_started" variable
    dict_variables['gungame_voting_started'] = False
    
    # Reset the "rounds remaining" variable for multi-rounds
    dict_variables['roundsRemaining'] = gungamelib.getVariableValue('gg_multi_round')
    '''
    
    '''
    # Check to see if the warmup round needs to be activated
    if int(es.ServerVar('gg_warmup_timer')):
        es.server.queuecmd('es_xload gungame/included_addons/gg_warmup_round')
    else:
        # Fire gg_start event
        es.event('initialize','gg_start')
        es.event('fire','gg_start')
    '''
    
    # Reset the GunGame players
    resetPlayers()
    
    # Reset the GunGame leaders
    resetLeaders()
    
    '''
    # Make sounds downloadbale
    gungamelib.addDownloadableSounds()
    '''
    
    # Equip the players
    equipPlayer()    
    
def round_start(event_var):
    global list_stripExceptions
    
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
    
    '''
    if int(es.ServerVar('gg_leaderweapon_warning')):
        leaderWeapon = gungamelib.getLevelWeapon(gungamelib.leaders.getLeaderLevel())
        
        # Play knife sound
        if leaderWeapon == 'knife':
            gungamelib.playSound('#all', 'knifelevel')
        
        # Play nade sound
        if leaderWeapon == 'hegrenade':
            gungamelib.playSound('#all', 'nadelevel')
    '''

def round_end(event_var):
    '''
    MOVE THE BELOW CODE TO GG_AFK INCLUDED ADDON
    '''
    # Was a ROUND_DRAW or GAME_COMMENCING?
    if int(event_var['reason']) == 10 or int(event_var['reason']) == 16:
        return
    
    # Do we punish AFKers?
    if not int(es.ServerVar('gg_afk_rounds')):
        return
    
    # Now, we will loop through the userid list and run the AFK Punishment Checks on them
    for userid in playerlib.getUseridList('#alive,#human'):
        gungamePlayer = Player(userid)
        
        # Check to see if the player was AFK
        if gungamePlayer.isPlayerAFK():
            afkPunishCheck(userid)    
    '''
    END GG_AFK CODE
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
    ggVictim = Player(userid)
    
    # Suicide check
    if (attacker == 0 or attacker == userid): #and countBombDeathAsSuicide:
            return
    
    # Get attacker object
    ggAttacker = Player(attacker)
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
        ggAttacker.leveldown(int(es.ServerVar('gg_tk_punish')), userid, 'tk')
        
        # Message
        ggAttacker.msg('TeamKill_LevelDown', {'newlevel':ggAttacker.level})
        
        # Play the leveldown sound
        #gungamelib.playSound(attacker, 'leveldown')
        
        return
        
    # ===========
    # NORMAL KILL
    # ===========
    # Get weapon name
    weapon = event_var['weapon']
    
    # Check the weapon was correct
    if weapon != ggAttacker.weapon:
        return
    
    '''
    # Don't continue if the victim is AFK
    if ggVictim.isPlayerAFK():
        # Tell the attacker they were AFK
        gungamelib.hudhint('gungame', attacker, 'PlayerAFK', {'player': event_var['es_username']})
        
        # Check AFK punishment
        if not ggVictim.isbot and gungamelib.getVariableValue('gg_afk_rounds') > 0:
            afkPunishCheck(userid)
        
        return
    '''
    
    # No multikill? Just level up...
    multiKill = getLevelMultiKill(ggAttacker.level)
    if multiKill == 1:
        # Level them up
        ggAttacker.levelup(1, userid, 'kill')
        
        # Play the levelup sound
        #gungamelib.playSound(attacker, 'levelup')
        
        return
    
    # Using multikill
    ggAttacker.multikill += 1
    
    # Finished the multikill
    if ggAttacker.multikill >= multiKill:
        # Level them up
        ggAttacker.levelup(1, userid, 'kill')
            
        # Play the levelup sound
        #gungamelib.playSound(attacker, 'levelup')
        
    # Increment their current multikill value
    else:
        # Message the attacker
        multiKill = getLevelMultiKill(ggAttacker.level)
        ggAttacker.hudhint('MultikillNotification', {'kills': ggAttacker.multikill, 'total': multiKill})
            
        # Play the multikill sound
        #gungamelib.playSound(attacker, 'multikill')
        
def player_disconnect(event_var):
    userid = int(event_var['userid'])
    # Is leader?
    if isLeader(userid):
        leaders.remove(userid, False)

def bomb_defused(event_var):
    '''
    Maybe we could add a variable for this? It seems like a good idea:
    
    gg_bomb_defused_level #
    gg_bomb_defused_skip_knife 0|1
    gg_bomb_defused_skip_hegrenade 0|1
    '''
    # Set vars
    ggPlayer = Player(event_var['userid'])
    weapon = ggPlayer.weapon
    
    # Cant skip the last level
    if ggPlayer.level == getWeaponOrder().getTotalLevels() or weapon in ['knife', 'hegrenade']:
        ggPlayer.msg('CannotSkipLevel_ByDefusing', {'level':weapon})
        return
    
    # Level them up
    ggPlayer.levelup(1, 0, 'bomb_defused')

def bomb_exploded(event_var):
    '''
    Maybe we could add a variable for this? It seems like a good idea:
    
    gg_bomb_exploded_level #
    gg_bomb_exploded_skip_knife 0|1
    gg_bomb_exploded_skip_hegrenade 0|1
    '''
    # Set vars
    ggPlayer = Player(event_var['userid'])
    weapon = ggPlayer.weapon
    
    # Cant skip the last level
    if ggPlayer.level == getWeaponOrder().getTotalLevels() or weapon in ['knife', 'hegrenade']:
        ggPlayer.msg('CannotSkipLevel_ByPlanting', {'level':weapon})
        return
    
    # Level them up
    ggPlayer.levelup(1, 0, 'bomb_exploded')
    
'''
def player_team(event_var):
    # Was a disconnect?
    if int(event_var['disconnect']) == 1:
        return
        
    # Play welcome sound
    if int(event_var['oldteam']) < 2 and team > 1:
        gungamelib.playSound(userid, 'welcome')
'''
    
def gg_levelup(event_var):
    # Cache new level for later use
    newLevel = int(event_var['new_level'])
    
    # Temporary message
    es.msg('%s leveled up by killing %s!' %(event_var['es_attackername'], event_var['es_username']))
    '''
    THIS IS NOW HANDLED BY THE EVENT MANAGER. LEAVING THIS HERE FOR REFERENCE
    FOR RIGHT NOW.
    
    # ============
    # WINNER CHECK
    # ============
    if int(event_var['old_level']) == gungamelib.getTotalLevels() and newLevel > gungamelib.getTotalLevels():
        es.event('initialize', 'gg_win')
        es.event('setint', 'gg_win', 'attacker', event_var['attacker'])
        es.event('setint', 'gg_win', 'winner', event_var['attacker'])
        es.event('setint', 'gg_win', 'userid', event_var['userid'])
        es.event('setint', 'gg_win', 'loser', event_var['userid'])
        es.event('setint', 'gg_win', 'round', '1' if dict_variables['roundsRemaining'] > 1 else '0')
        es.event('fire', 'gg_win')
        
        return
    '''
    
    
    # ===============
    # REGULAR LEVELUP
    # ===============
    # Get attacker info
    ggPlayer = Player(event_var['attacker'])
    
    '''
    STILL HAVE TO FIGURE OUT HOW TO IMPLEMENT SOUNDS
    
    # Player on knife level?
    if ggPlayer.weapon == 'knife':
        gungamelib.playSound('#all', 'knifelevel')
    
    # Player on nade level?
    if ggPlayer.weapon == 'hegrenade':
        gungamelib.playSound('#all', 'nadelevel')
    '''
    
    '''
    WILL ADD THIS A LITTLE LATER -- I HAVE TO FIGURE OUT THE DEAL WITH THE
    "canShowHudHints()" FUNCTION. I BELIEVE THIS IS ONLY IF A MAP VOTE IS
    ACTIVE.
    
    # Show level info HUDHint
    if gungamelib.canShowHints():
        levelInfoHint(attacker)
    '''
    
    '''
    I BELIEVE THIS SHOULD BE HANDLED BY A GG_MAP_VOTE ADDON OF SOME SORT BASED
    ON WHATEVER VARIABLE TRIGGERS IT --- "gg_vote_trigger"?
    
    # ==================
    # VOTE TRIGGER CHECK
    # ==================
    
    # Get leader level
    leaderLevel = gungamelib.leaders.getLeaderLevel()
    
    if leaderLevel == (gungamelib.getTotalLevels() - gungamelib.getVariableValue('gg_vote_trigger')):
        # Nextmap already set?
        if es.ServerVar('eventscripts_nextmapoverride') != '':
            gungamelib.echo('gungame', 0, 0, 'MapSetBefore')
            return
        
        # Vote already started?
        if dict_variables['gungame_voting_started']:
            return
        
        if dict_variables['roundsRemaining'] < 2:
            es.event('initialize', 'gg_vote')
            es.event('fire', 'gg_vote')
    '''
    
'''
AGAIN, I FEEL THIS IS SOMETHING THAT DOES NOT BELONG IN THE CORE OF GUNGAME

def gg_vote(event_var):
    dict_variables['gungame_voting_started'] = True
    
    if gungamelib.getVariableValue('gg_map_vote') == 2:
        es.server.queuecmd(gungamelib.getVariableValue('gg_map_vote_command'))
'''
    
def gg_win(event_var):
    # Get player info
    userid = int(event_var['winner'])
    index = getPlayer(userid).index
    playerName = es.getplayername(userid)
    
    '''
    CURRENTLY, EVENT_VAR['ROUND'] WILL ALWAYS RETURN 0. I HAVE TO FIGURE OUT A
    GOOD WAY TO IMPLEMENT THIS.
    '''
    if event_var['round'] == '0':
        # ====================================================
        # MAP WIN
        # ====================================================
        # End game
        es.server.cmd('es_xgive %d game_end;es_xfire %d game_end EndGame'
            %(userid, userid))
        
        # Tell the world
        saytext2('#all', index, 'PlayerWon', {'player':playerName})
        
        '''
        # Play the winner sound
        gungamelib.playSound('#all', 'winner')
        '''
    else:
        # ====================================================
        # ROUND WIN
        # ====================================================
        '''
        # Calculate rounds remaining
        dict_variables['roundsRemaining'] -= 1
        '''
        
        # End the GunGame Round
        es.server.queuecmd('mp_restartgame 2')
        
        # Check to see if the warmup round needs to be activated
        if int(es.ServerVar('gg_round_intermission')):
            '''
            gungamelib.setGlobal('isIntermission', 1)
            
            es.server.queuecmd('es_xload gungame/included_addons/gg_warmup_round')
            '''
        # Tell the world
        saytext2('#all', index, 'PlayerWonRound', {'player':playerName})
        
        '''
        # Play the winner sound
        gungamelib.playSound('#all', 'roundwinner')
        '''
    
    # ====================================================
    # ALL WINS
    # ====================================================
    # Enable alltalk
    if not int(es.ServerVar('sv_alltalk')) and int(es.ServerVar('gg_win_alltalk')):
        es.server.cmd('sv_alltalk 1')
    
    # Tell the world (center message)
    centermsg('#all', 'PlayerWon_Center', {'player': playerName})
    gamethread.delayed(1, centermsg, ('#all', 'PlayerWon_Center', {'player': playerName}))
    gamethread.delayed(2, centermsg, ('#all', 'PlayerWon_Center', {'player': playerName}))
    gamethread.delayed(3, centermsg, ('#all', 'PlayerWon_Center', {'player': playerName}))
    
    # Toptext
    if int(event_var['es_attackerteam']) == 2:
        toptext('#all', 10, '#red', 'PlayerWon_Center', {'player': playerName})
    else:
        toptext('#all', 10, '#blue', 'PlayerWon_Center', {'player': playerName})
        
def gg_start(event_var):
    # Reset all the players
    resetPlayers()
    
def gg_addon_loaded(event_var):
    es.dbgmsg(0, 'gg_addon_loaded: "%s" of type "%s"' %(event_var['addon'], event_var['type']))
    
def gg_addon_unloaded(event_var):
    es.dbgmsg(0, 'gg_addon_unloaded: "%s" of type "%s"' %(event_var['addon'], event_var['type']))
    
# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
def equipPlayer():
    userid = es.getuserid()
    cmdFormat = 'es_xremove game_player_equip;' + \
                'es_xgive %s game_player_equip;' %userid + \
                'es_xfire %s game_player_equip AddOutput "weapon_knife 1;"' \
                    %userid
    
    # Retrieve the armor type
    armorType = int(es.ServerVar('gg_player_armor'))
    
    # Give the player full armor
    if armorType == 2:
        cmdFormat = cmdFormat + \
            'es_xfire %s game_player_equip AddOutput "item_assaultsuit 1;"' \
                %userid
    
    # Give the player kevlar only
    elif armorType == 1:
        cmdFormat = cmdFormat + \
            'es_xfire %s game_player_equip AddOutput "item_kevlar 1";' %userid
            
    es.server.queuecmd(cmdFormat)