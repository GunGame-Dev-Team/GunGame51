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
from playerlib import getUseridList
from weaponlib import getWeaponList

# GunGame Imports

#    Weapon Function Imports
from core.weapons.shortcuts import getWeaponOrder
from core.weapons.shortcuts import setWeaponOrder
from core.weapons.shortcuts import getLevelMultiKill
from core.weapons.shortcuts import getTotalLevels

#    Config Function Imports
from core.cfg.shortcuts import loadConfig
from core.cfg.shortcuts import unloadConfig
from core.cfg.shortcuts import getConfigList

#    Addon Function Imports
from core.addons import AddonManager
from core.addons import PriorityAddon
from core.addons import gungame_info

#    Player Function Imports
from core.players.shortcuts import Player
from core.players.shortcuts import resetPlayers

#    Leaders Function Imports
from core.leaders.shortcuts import LeaderManager
from core.leaders.shortcuts import is_leader

#    Core Function Imports
from core import inMap
from core import get_game_dir

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

#   Database
from core.sql.shortcuts import prune_winners_db
from core.sql.shortcuts import Database

#   Menus
from core.menus import MenuManager

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
# >> ADDON REGISTRATION
# ============================================================================
info = es.AddonInfo()
del info['keylist'][:]
info.About = ('\n' +
             ' '*25 + '\tGunGame 5.1 (v%s)\n\n' % gungame_info('version') +
             ' '*25 + 'Authors:\n' +
             ' '*25 + '\tMichael Barr (XE_ManUp)\n' +
             ' '*25 + '\tLuke Robinson (Monday)\n' +
             ' '*25 + '\tWarren Alpert\n' +
             ' '*25 + '\tPaul Smith (RideGuy)\n' +
             ' '*25 + '\tDeniz Sezen (your-name-here)\n\n' +
             ' '*25 + 'Website: http://www.gungame5.com/\n')

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
        es.dbgmsg(0, '[GunGame] %s' % ('=' * 79))
        es.excepter(*sys.exc_info())
        es.dbgmsg(0, '[GunGame] %s' % ('=' * 79))
        es.unload('gungame')

def unload():
    # Unload translations
    unloadTranslation('gungame', 'gungame')

    from core.addons import dependencies
    # Create a copy of the dependencies dictionary
    dict_dependencies = dependencies.copy()

    # Loop through addons that have required dependencies
    for addon in list(set(map((lambda (x, y): y), [(x, y) for x in \
        dict_dependencies for y in dict_dependencies[x]]))):

        # Unload the addons that have required dependencies
        AddonManager().unload(addon, True)

    # Unload any remaining addons now that dependencies are handled
    for addon in AddonManager().__order__[:]:
        AddonManager().unload(addon, True)

    # Close the database
    Database().close()

    # Unload configs (removes flags from CVARs)
    unloadConfig(getConfigList())

    # Enable Buyzones
    es.server.queuecmd('es_xfire %d func_buyzone Enable' % es.getuserid())

    # Fire gg_unload event
    EventManager().gg_unload
    
def initialize():
    loadConfig(getConfigList())
    # Print load started
    es.dbgmsg(0, '[GunGame] %s' % ('=' * 79))
    
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
    
    # Clear out the GunGame system
    resetPlayers()
    
    # Restart map
    msg('#human', 'Loaded')
    
    # Fire gg_load event
    EventManager().gg_load()
    
    # Print load completed
    es.dbgmsg(0, '[GunGame] %s' % ('=' * 79))

    # Prune the DB
    prune_winners_db()

    # Set es.AddonInfo()
    gungame_info('addoninfo', info)
    
    # Load menus
    MenuManager().load('#all')

# ============================================================================
# >> GAME EVENTS
# ============================================================================
def es_map_start(event_var):
    # Check for priority addons
    if PriorityAddon():
        del PriorityAddon()[:]

    # Make the sounds downloadable
    make_downloadable()

    # Load custom GunGame events
    es.loadevents('addons/eventscripts/' + 
                  'gungame51/core/events/data/es_gungame_events.res')
    
    # Execute GunGame's autoexec.cfg
    es.delayed('1', 'exec gungame51/gg_server.cfg')
    
    # Reset the GunGame players
    resetPlayers()
    
    # Reset the GunGame leaders
    LeaderManager().reset()

    # Prune the DB
    prune_winners_db()
    
    # Update players in winner's database
    for userid in getUseridList('#human'):
        Player(userid).databaseUpdate()

def round_start(event_var):

    # Retrieve a random userid
    userid = es.getuserid()

    # Disable Buyzones
    es.server.queuecmd('es_xfire %d func_buyzone Disable' % userid)

    # Remove weapons from the map
    list_noStrip = [(x.strip() if x.strip().startswith('weapon_') else \
                    'weapon_%s' % x.strip()) for x in \
                    str(gg_map_strip_exceptions).split(',') if x.strip() != \
                    ''] + ['weapon_knife']

    for weapon in getWeaponList('#all'):
        # Make sure that the admin doesn't want the weapon left on the map
        if weapon in list_noStrip:
            continue

        # Remove the weapon from the map
        es.server.queuecmd('es_xfire %i %s kill' % (userid, weapon))

    # Equip players with a knife and possibly item_kevlar or item_assaultsuit
    equip_player()

def player_spawn(event_var):
    # Check for priority addons
    if PriorityAddon():
        return

    userid = event_var['userid']
    
    # Is a spectator ?
    if getPlayer(userid).isobserver:
        return
    
    # Is dead ?
    if getPlayer(userid).isdead:
        return
    
    # Give the player their weapon
    gamethread.delayed(0.05, Player(userid).giveWeapon, ())
    
    # Reset the player's AFK calculation
    if not es.isbot(userid):
        gamethread.delayed(0.6, Player(userid).afk.reset, ())

    ggPlayer = Player(userid)
    
    # Send the level information hudhint
    ggPlayer.hudhint('LevelInfo_CurrentLevel', {'level': ggPlayer.level, 
                                                    'total': getTotalLevels()})

def player_death(event_var):
    # Check for priority addons
    if PriorityAddon():
        return

    # Set player ids
    userid = int(event_var['userid'])
    attacker = int(event_var['attacker'])

    # Is the attacker on the server?
    if not es.exists('userid', attacker):
        return

    # Suicide check
    if (attacker == 0 or attacker == userid):
        return

    # TEAM-KILL CHECK
    if (event_var['es_userteam'] == event_var['es_attackerteam']):
        return
    
    # Get victim object
    ggVictim = Player(userid)
    
    # Get attacker object
    ggAttacker = Player(attacker)           

    # Check the weapon was correct (Normal Kill)
    if event_var['weapon'] != ggAttacker.weapon:
        return
    
    # Don't continue if the victim is AFK
    if not int(gg_allow_afk_levels):
        
        # Make sure the victim is not a bot
        if not es.isbot(userid):
            
            # Is AFK ?
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
    
    # Check to see if player was the leader
    LeaderManager().disconnected_leader(userid)
    
def gg_levelup(event_var):
    # Check for priority addons
    if PriorityAddon():
        return
    
    userid = int(event_var['userid'])
    
    # Is a bot?
    if es.isbot(userid):
        return

    ggPlayer = Player(userid)
        
    # Send hudhint (level information)
    ggPlayer.hudhint('LevelInfo_CurrentLevel', {'level': ggPlayer.level, 
                                                    'total': getTotalLevels()})
    
def gg_win(event_var):
    # Get player info
    userid = int(event_var['winner'])
    index = getPlayer(userid).index
    playerName = es.getplayername(userid)
    if not es.isbot(userid):
        Player(userid).wins += 1

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
        for userid in getUseridList('#human'):
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
        saytext2('#human', index, 'PlayerWonRound', {'player': playerName})
        
        # Play the winner sound
        for userid in getUseridList('#human'):
            Player(userid).playsound('winner')
    
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

    # Update DB
    gamethread.delayed(1.5, Database().commit)
        
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

def player_changename(event_var):
    # Update the Player() instance's name attr (used for the db)
    userid = int(event_var['userid'])
    Player(userid).name = getPlayer(userid).name

def player_activate(event_var):
    # Update the player in the database
    userid = int(event_var['userid'])
    Player(userid).databaseUpdate()

# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
def equip_player():
    userid = es.getuserid()
    cmd = 'es_xremove game_player_equip;' + \
          'es_xgive %s game_player_equip;' % userid + \
          'es_xfire %s game_player_equip AddOutput "weapon_knife 1";' % userid

    # Retrieve the armor type
    armorType = int(gg_player_armor)

    # Give the player full armor
    if armorType == 2:
        cmd = cmd + \
            'es_xfire %s game_player_equip AddOutput "item_assaultsuit 1";' \
                % userid

    # Give the player kevlar only
    elif armorType == 1:
        cmd = cmd + \
            'es_xfire %s game_player_equip AddOutput "item_kevlar 1";' % userid

    es.server.queuecmd(cmd)