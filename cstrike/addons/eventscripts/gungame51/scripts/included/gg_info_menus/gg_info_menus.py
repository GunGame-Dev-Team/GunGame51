# ../addons/eventscripts/gungame/scripts/included/gg_info_menus/gg_info_menus.py

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
import popuplib
from playerlib import getUseridList
from cmdlib import registerSayCommand
from cmdlib import unregisterSayCommand

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.leaders.shortcuts import get_leader_count
from gungame51.core.leaders.shortcuts import get_leader_level
from gungame51.core.leaders.shortcuts import get_leader_names
from gungame51.core.players import Player
from gungame51.core.weapons.shortcuts import getLevelWeapon

# ============================================================================
# >> ADDON REGISTRATION/INFORMATION
# ============================================================================
info = AddonInfo()
info.name = 'gg_info_menus'
info.title = 'GG Info Menus' 
info.author = 'GG Dev Team' 
info.version = '0.1'

# ============================================================================
# >> GLOBAL VARIABLES
# ============================================================================
gg_multikill_override = es.ServerVar('gg_multikill_override')

# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    # Register commands
    registerSayCommand('!leader', leaders, 'A list of the current leaders.')
    registerSayCommand('!leaders', leaders, 'A list of the current leaders.')
    registerSayCommand('!level', level, 'Displays a level menu.')

    # Build menus
    buildLeaderMenu()
    buildLevelMenu()

    # Load
    es.dbgmsg(0, 'Loaded: %s' % info.name)
    
def unload():
    # Unregister commands
    unregisterSayCommand('!leader')
    unregisterSayCommand('!leaders')
    unregisterSayCommand('!level')

    # Unload
    es.dbgmsg(0, 'Unloaded: %s' % info.name)
    
# ============================================================================
# >> GAME EVENTS
# ============================================================================
def gg_new_leader(event_var):
    # Rebuild leader menu
    rebuildLeaderMenu()

def gg_tied_leader(event_var):
    # Rebuild leader menu
    rebuildLeaderMenu()

def gg_leader_lostlevel(event_var):
    # Rebuild leader menu
    rebuildLeaderMenu()

# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
def buildLeaderMenu():
    # Check if the popup exists
    if popuplib.exists('gungameLeadersMenu'):
        # Unsend and delete it
        popuplib.unsendname('gungameLeadersMenu', getUseridList('#human'))
        popuplib.delete('gungameLeadersMenu')
    
    # Create the menu
    gungameLeadersMenu = popuplib.create('gungameLeadersMenu')
    gungameLeadersMenu.addline('->1. Current Leaders:')
    gungameLeadersMenu.addline('--------------------------')
    gungameLeadersMenu.addline('   * There currently is no leader')
    gungameLeadersMenu.addline('--------------------------')
    gungameLeadersMenu.addline('0. Exit')
    gungameLeadersMenu.timeout('send', 5)
    gungameLeadersMenu.timeout('view', 5)

def rebuildLeaderMenu():
    # Check if the popup exists
    if popuplib.exists('gungameLeadersMenu'):
        # Unsend and delete it
        popuplib.unsendname('gungameLeadersMenu', getUseridList('#human'))
        popuplib.delete('gungameLeadersMenu')
    
    # Get leader info
    leaderLevel = get_leader_level()
    leaderNames = get_leader_names()
    
    # Let's create the 'gungameLeadersMenu' popup
    gungameLeadersMenu = popuplib.create('gungameLeadersMenu')
    gungameLeadersMenu.addline('->1. Current Leaders:')
    gungameLeadersMenu.addline('    Level %d (%s)' %(leaderLevel, \
        getLevelWeapon(leaderLevel)))
    gungameLeadersMenu.addline('--------------------------')

    # Add leaders
    for name in leaderNames:
        gungameLeadersMenu.addline('   * %s' % name)

    # Finish off the menu
    gungameLeadersMenu.addline('--------------------------')
    gungameLeadersMenu.addline('0. Exit')
    gungameLeadersMenu.timeout('send', 5)
    gungameLeadersMenu.timeout('view', 5)

def leaders(userid, args):
    # Send leaders menu
    popuplib.send('gungameLeadersMenu', userid)

def buildLevelMenu():
    # Delete the popup if exists
    if popuplib.exists('gungameLevelMenu'):
        popuplib.unsendname('gungameLevelMenu', getUseridList('#human'))
        popuplib.delete('gungameLevelMenu')

    # Let's create the 'gungameLevelMenu' popup
    gungameLevelMenu = popuplib.create('gungameLevelMenu')
    gungameLevelMenu.addline('->1. Level')
    # More than one kill required?
    if int(gg_multikill_override) == 0:
        gungameLevelMenu.addline('   * You are on level <level>')
        gungameLevelMenu.addline('   * You need a <weapon> kill to advance')
    else:
        gungameLevelMenu.addline('   * You are on level <level> (<weapon>)')
        gungameLevelMenu \
            .addline('   * You have made #/# of your reqiured kills')
    gungameLevelMenu.addline('   * There currently is no leader')
    gungameLevelMenu.addline('->2. Leaders')
    gungameLevelMenu.addline('   * Leader Level: There are no leaders')
    gungameLevelMenu.addline('->   9. View Leaders Menu')
    gungameLevelMenu.submenu(9, 'gungameLeadersMenu')
    gungameLevelMenu.prepuser = prepGunGameLevelMenu
    gungameLevelMenu.timeout('send', 5)
    gungameLevelMenu.timeout('view', 5)

def prepGunGameLevelMenu(userid, popupid):
    gungameLevelMenu = popuplib.find('gungameLevelMenu')
    ggPlayer = Player(userid)
    playerLevel = ggPlayer.level

    if int(gg_multikill_override) == 0:
        gungameLevelMenu.modline(2, '   * You are on level %d' % playerLevel)
        gungameLevelMenu.modline(3, '   * You need a %s kill to advance' \
            % ggPlayer.getWeapon())
    else:
        gungameLevelMenu.modline(2, '   * You are on level %d (%s)' \
            % (playerLevel, ggPlayer.getWeapon()))
        gungameLevelMenu \
            .modline(3, '   * You have made %d/%d of your required kills' \
            % (ggPlayer.multikill, int(gg_multikill_override)))

    leaderLevel = get_leader_level()

    if leaderLevel > 1:
        # See if the player is a leader:
        if playerLevel == leaderLevel:
            # See if there is more than 1 leader
            if get_leader_count() > 1:
                # This player is tied with other leaders
                gungameLevelMenu.modline(4, \
                    '   * You are currently tied for the leader position')
            else:
                # This player is the only leader
                gungameLevelMenu.modline(4, '   * You are currently the leader')
        # This player is not a leader
        else:
            levelsBehindLeader = leaderLevel - playerLevel
            if levelsBehindLeader == 1:
                gungameLevelMenu \
                    .modline(4, '   * You are 1 level behind the leader')
            else:
                gungameLevelMenu \
                    .modline(4, '   * You are %d levels behind the leader' \
                        % levelsBehindLeader)
    else:
        # There are no leaders
        gungameLevelMenu.modline(4, '   * There currently is no leader')

    if leaderLevel > 1:
        gungameLevelMenu.modline(6, '   * Leader Level %d (%s)' \
            % (leaderLevel, getLevelWeapon(leaderLevel)))
    else:
        gungameLevelMenu \
            .modline(6, '   * Leader Level: There are no leaders')

def level(userid, args):
    # Send the level menu
    popuplib.send('gungameLevelMenu', userid)