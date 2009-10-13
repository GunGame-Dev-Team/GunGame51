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

# EventScripts Imports
import es
import gamethread
from playerlib import getPlayer
from playerlib import getPlayerList
from weaponlib import getWeaponList

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
from core.addons import __addons__
from core.addons import priority_addons

#    Player Function Imports
from core.players.shortcuts import Player
from core.players.shortcuts import resetPlayers

#    Leaders Function Imports
from core.leaders.shortcuts import leaders
from core.leaders.shortcuts import is_leader

#    Core Function Imports
from core import inMap
from core import getGameDir

#   Messaging Function Imports
from core.messaging.shortcuts import loadTranslation
from core.messaging.shortcuts import unloadTranslation
from core.messaging.shortcuts import saytext2
from core.messaging.shortcuts import centermsg
from core.messaging.shortcuts import toptext
from core.messaging.shortcuts import msg

#   Event Function Imports
from core.events.shortcuts import EventManager

#   Sound Function Imports
from core.sound import make_downloadable

# ============================================================================
# >> GLOBAL VARIABLES
# ============================================================================
gg_map_strip_exceptions = es.ServerVar('gg_map_strip_exceptions')
gg_weapon_order_file = es.ServerVar('gg_weapon_order_file')
gg_weapon_order_sort_type = es.ServerVar('gg_weapon_order_sort_type')
gg_multikill_override = es.ServerVar('gg_multikill_override')
gg_player_armor = es.ServerVar('gg_player_armor')
sv_alltalk = es.ServerVar('sv_alltalk')
gg_win_alltalk = es.ServerVar('gg_win_alltalk')
gg_allow_afk_levels = es.ServerVar('gg_allow_afk_levels')
gg_allow_afk_levels_knife = es.ServerVar('gg_allow_afk_levels_knife')
gg_allow_afk_levels_nade = es.ServerVar('gg_allow_afk_levels_nade')

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
    unloadTranslation('gungame', 'gungame')

    # Create a copy of the list of addons
    list_addons = __addons__.__order__[:]
    
    # We need to unload in reverse due to DependencyErrors
    list_addons.reverse()
    
    for name in list_addons:
        if name not in __addons__.__order__:
            continue
        __addons__.unload(name)

    # Unload configs (removes flags from CVARs)
    unloadConfig(getConfigList())
    
    # Grab a random userid for the below commands
    userid = es.getuserid()
    
    # Enable Buyzones
    es.server.queuecmd('es_xfire %d func_buyzone Enable' %userid)
    
    # Fire gg_unload event
    EventManager().gg_unload
    
    '''
    gungamelib.clearGunGame()
    '''

def initialize():
    loadConfig(getConfigList())
    # Print load started
    es.dbgmsg(0, '[GunGame] %s' % ('=' * 80))
    #gungamelib.echo('gungame', 0, 0, 'Load_Start', {'version': __version__})
    
    # Load custom events
    es.loadevents('declare', 
        'addons/eventscripts/gungame51/core/events/data/es_gungame_events.res')
    
    # Fire the gg_server.cfg
    es.server.cmd('exec gungame51/gg_server.cfg')
    
    # Get weapon order file
    # Set this as the weapon order and set the weapon order type
    currentOrder = setWeaponOrder(str(gg_weapon_order_file), 
                                  str(gg_weapon_order_sort_type))
    
    # Set multikill override
    if int(gg_multikill_override) > 1:
        currentOrder.setMultiKillOverride(int(gg_multikill_override))
        
    # Echo the weapon order to console
    es.dbgmsg(0, '[GunGame]')
    currentOrder.echo()
    es.dbgmsg(0, '[GunGame]')
    '''
    gungamelib.echo('gungame', 0, 0, 'Load_Commands')
    '''
    
    # Clear out the GunGame system
    resetPlayers()
    
    # Restart map
    msg('#human', 'Loaded')
    
    # Fire gg_load event
    EventManager().gg_load()
    
    # Print load completed
    #gungamelib.echo('gungame', 0, 0, 'Load_Completed')
    es.dbgmsg(0, '[GunGame] %s' % ('=' * 80))
    
# ============================================================================
# >> GAME EVENTS
# ============================================================================
def es_map_start(event_var):
    # Check for priority addons
    if priority_addons:
        del priority_addons[:]

    # Make the sounds downloadable
    make_downloadable()

    # Load custom GunGame events
    es.loadevents('addons/eventscripts/' + 
                  'gungame51/core/events/data/es_gungame_events.res')
    
    # Execute GunGame's autoexec.cfg
    es.delayed('1', 'exec gungame51/gg_server.cfg')
    
    '''
    =====================================================
    THERE HAS TO BE A BETTER WAY TO HANDLE THE FOLLOWING:
    =====================================================
    
    # Reset the "gungame_voting_started" variable
    dict_variables['gungame_voting_started'] = False
    
    # Reset the "rounds remaining" variable for multi-rounds
    dict_variables['roundsRemaining'] = \
        gungamelib.getVariableValue('gg_multi_round')
    '''
    
    '''
    # Check to see if the warmup round needs to be activated
    if int(es.ServerVar('gg_warmup_timer')):
        es.server.queuecmd('es_xload gungame/included_addons/gg_warmup_round')
    else:
        # Fire gg_start event
        EventManager().gg_start()
    '''
    
    # Reset the GunGame players
    resetPlayers()
    
    # Reset the GunGame leaders
    leaders.reset()
    
    '''
    # Make sounds downloadbale
    gungamelib.addDownloadableSounds()
    '''
    
    # =========================================================================
    # Equip players with a knife and possibly item_kevalr or item_assaultsuit
    # =========================================================================
    equipPlayer()    
    
def round_start(event_var):
    # Retrieve a random userid
    userid = es.getuserid()

    # =========================================================================
    # Disable Buyzones
    # =========================================================================
    es.server.queuecmd('es_xfire %d func_buyzone Disable' %userid)

    # =========================================================================
    # Remove weapons from the map
    # =========================================================================
    list_noStrip = [x.strip() for x in str(gg_map_strip_exceptions).split(',')]

    if list_noStrip:
        for weapon in getWeaponList('#all'):
            # Make sure that the admin doesn't want the weapon left on the map
            if weapon in list_noStrip:
                continue

            # Remove the weapon from the map
            es.server.queuecmd('es_xfire %d weapon_%s kill' % (userid, weapon))
    else:
        es.server.queuecmd('es_xfire %d weapon_* kill' %userid)

    # =========================================================================
    # Equip players with a knife and possibly item_kevalr or item_assaultsuit
    # =========================================================================
    equipPlayer()

def player_spawn(event_var):
    userid = event_var['userid']
    
    if getPlayer(userid).isobserver:
        return
    
    if getPlayer(userid).isdead:
        return
    
    # Warmup Round Check Would Go Here
    # ....
    
    # Give the player their weapon
    Player(userid).giveWeapon()
    
    # Reset the player's AFK calculation
    if not es.isbot(userid):
        gamethread.delayed(0.6, Player(userid).afk.reset, ())

    # Send the level information hudhint
    # ....

def player_death(event_var):
    # Check for priority addons
    if priority_addons:
        return

    # Set player ids
    userid = int(event_var['userid'])
    attacker = int(event_var['attacker'])

    # Is the attacker on the server?
    if not es.exists('userid', attacker):
        return

    # Get victim object
    ggVictim = Player(userid)

    # Suicide check
    if (attacker == 0 or attacker == userid):
        return
    
    # Get attacker object
    ggAttacker = Player(attacker)

    # =========================================================================
    # TEAM-KILL CHECK
    # =========================================================================
    if (event_var['es_userteam'] == event_var['es_attackerteam']):
        return

    # =========================================================================
    # >> NORMAL KILL
    # =========================================================================
    # Check the weapon was correct
    if event_var['weapon'] != ggAttacker.weapon:
        return

    # =========================================================================
    # AFK CHECK
    # =========================================================================
    # Don't continue if the victim is AFK
    if not int(gg_allow_afk_levels):
        # Make sure the victim is not a bot
        if not es.isbot(userid):
            if ggVictim.afk():
                # Is their weapon an hegrenade and do we allow AFK leveling?
                if ggAttacker.weapon == 'hegrenade' and \
                    int(gg_allow_afk_levels_nade):
                        # Pass if we are allowing AFK leveling on nade level
                        pass

                # Is their weapon a knife and do we allow AFK leveling?
                elif ggAttacker.weapon == 'knife' and \
                    int(gg_allow_afk_levels_knife):
                        # Pass if we are allowing AFK leveling on knife level
                        pass

                # None of the above checks apply --- continue with hudhint
                else:
                    # Make sure the attacker is not a bot
                    if es.isbot(attacker):
                        return

                    # Tell the attacker they victim was AFK
                    ggAttacker.hudhint('PlayerAFK', {'player':
                                                     event_var['es_username']})
                    return

    # =========================================================================
    # MULTIKILL CHECK
    # =========================================================================
    # Get the current level's multikill value
    multiKill = getLevelMultiKill(ggAttacker.level)
    
    # If set to 1, level the player up
    if multiKill == 1:
        # Level them up
        ggAttacker.levelup(1, userid, 'kill')
        
        # Play the levelup sound
        ggAttacker.playsound('levelup')
        
        return
    
    # Multikill value is > 1 ... add 1 to the multikill attribute
    ggAttacker.multikill += 1
    
    # Finished the multikill
    if ggAttacker.multikill >= multiKill:
        # Level them up
        ggAttacker.levelup(1, userid, 'kill')
            
        # Play the levelup sound
        ggAttacker.playsound('levelup')
        
    # Increment their current multikill value
    else:
        # Message the attacker
        multiKill = getLevelMultiKill(ggAttacker.level)
        ggAttacker.hudhint('MultikillNotification', 
                           {'kills': ggAttacker.multikill, 'total': multiKill})
            
        # Play the multikill sound
        ggAttacker.playsound('multikill')

def player_disconnect(event_var):
    userid = int(event_var['userid'])
    
    leaders.disconnected_leader(userid)

def bomb_defused(event_var):
    # Check for priority addons
    if priority_addons:
        return

    # Set vars
    ggPlayer = Player(event_var['userid'])
    weapon = ggPlayer.weapon
    
    # Cant skip the last level
    if ggPlayer.level == getWeaponOrder().getTotalLevels() or \
                                weapon in ['knife', 'hegrenade']:
        ggPlayer.msg('CannotSkipLevel_ByDefusing', {'level':weapon})
        return
    
    # Level them up
    ggPlayer.levelup(1, 0, 'bomb_defused')

def bomb_exploded(event_var):
    # Check for priority addons
    if priority_addons:
        return

    # Set vars
    ggPlayer = Player(event_var['userid'])
    weapon = ggPlayer.weapon
    
    # Cant skip the last level
    if ggPlayer.level == getWeaponOrder().getTotalLevels() or \
                                weapon in ['knife', 'hegrenade']:
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
    # Check for priority addons
    if priority_addons:
        return

    # Cache new level for later use
    newLevel = int(event_var['new_level'])
    
    # Temporary message
    es.msg('%s leveled up by ' % event_var['es_attackername'] +
           'killing %s!' % event_var['es_username'])
    
    # ===============
    # REGULAR LEVELUP
    # ===============
    # Get attacker info
    ggPlayer = Player(event_var['attacker'])
    
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
    leaderLevel = gungamelib.leaders.get_leader_level()
    
    if leaderLevel == \
    (gungamelib.getTotalLevels() - \
    gungamelib.getVariableValue('gg_vote_trigger')):
        # Nextmap already set?
        if es.ServerVar('eventscripts_nextmapoverride') != '':
            gungamelib.echo('gungame', 0, 0, 'MapSetBefore')
            return
        
        # Vote already started?
        if dict_variables['gungame_voting_started']:
            return
        
        if dict_variables['roundsRemaining'] < 2:
            EventManager().gg_vote()
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
        saytext2('#human', index, 'PlayerWon', {'player':playerName})
        

        # Play the winner sound
        for userid in getPlayerList('#human'):
            Player(userid).playsound('winner')

    else:
        # =====================================================================
        # ROUND WIN
        # =====================================================================
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
            
            es.server.queuecmd('es_xload ' +
                               'gungame/included_addons/gg_warmup_round')
            '''
        # Tell the world
        saytext2('#human', index, 'PlayerWonRound', {'player':playerName})
        
        '''
        # Play the winner sound
        gungamelib.playSound('#human', 'roundwinner')
        '''
    
    # =========================================================================
    # ALL WINS
    # =========================================================================
    # Enable alltalk
    if not int(sv_alltalk) and int(gg_win_alltalk):
        es.server.queuecmd('sv_alltalk 1')
    
    # Tell the world (center message)
    centermsg('#human', 'PlayerWon_Center', {'player': playerName})
    gamethread.delayed(1, centermsg, ('#human', 'PlayerWon_Center', 
                                                    {'player': playerName}))
    gamethread.delayed(2, centermsg, ('#human', 'PlayerWon_Center', 
                                                    {'player': playerName}))
    gamethread.delayed(3, centermsg, ('#human', 'PlayerWon_Center', 
                                                    {'player': playerName}))
    
    # Toptext
    if int(event_var['es_attackerteam']) == 2:
        toptext('#human', 10, '#red', 'PlayerWon_Center', 
                                                    {'player': playerName})
    else:
        toptext('#human', 10, '#blue', 'PlayerWon_Center', 
                                                    {'player': playerName})
        
def gg_start(event_var):
    # Reset all the players
    resetPlayers()
    
def gg_addon_loaded(event_var):
    es.dbgmsg(0, 'gg_addon_loaded: "%s" ' % event_var['addon'] + 
                 'of type "%s"' % event_var['type'])
    
def gg_addon_unloaded(event_var):
    es.dbgmsg(0, 'gg_addon_unloaded: "%s" ' % event_var['addon'] + 
                 'of type "%s"' % event_var['type'])

def server_cvar(event_var):
    cvarName = event_var['cvarname']

    if cvarName in ['gg_weapon_order_file', 'gg_weapon_order_sort_type', 
                                                    'gg_multikill_override']:
        # Get weapon order file
        # Set this as the weapon order and set the weapon order type
        currentOrder = setWeaponOrder(str(gg_weapon_order_file), 
                                      str(gg_weapon_order_sort_type))

        # Set multikill override
        currentOrder.setMultiKillOverride(int(gg_multikill_override))


# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
def equipPlayer():
    userid = es.getuserid()
    cmd = 'es_xremove game_player_equip;' + \
          'es_xgive %s game_player_equip;' %userid + \
          'es_xfire %s game_player_equip AddOutput "weapon_knife 1";' %userid

    # Retrieve the armor type
    armorType = int(gg_player_armor)

    # Give the player full armor
    if armorType == 2:
        cmd = cmd + \
            'es_xfire %s game_player_equip AddOutput "item_assaultsuit 1";' \
                %userid

    # Give the player kevlar only
    elif armorType == 1:
        cmd = cmd + \
            'es_xfire %s game_player_equip AddOutput "item_kevlar 1";' %userid

    es.server.queuecmd(cmd)