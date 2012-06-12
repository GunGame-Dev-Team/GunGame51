# ../core/menus/level_menu.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# Eventscripts Imports
#   ES
from es import exists
from es import getplayername
from es import getuserid
#   Cmdlib
from cmdlib import registerSayCommand
from cmdlib import unregisterSayCommand
#   Playerlib
from playerlib import getUseridList
#   Popuplib
from popuplib import create
from popuplib import delete
from popuplib import exists as pexists
from popuplib import find
from popuplib import send
from popuplib import unsendname

# GunGame Imports
from gungame51.core.menus.leader_menu import leader_menu_cmd
from gungame51.core.players.shortcuts import Player
from gungame51.core.leaders.shortcuts import get_leader_count
from gungame51.core.leaders.shortcuts import get_leader_level
from gungame51.core.leaders.shortcuts import is_leader
from gungame51.core.weapons.shortcuts import get_level_multikill
from gungame51.core.messaging.shortcuts import saytext2
from gungame51.core.messaging.shortcuts import msg


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    # Delete the popup if it exists
    if pexists('ggLevelMenu'):
        unsendname('ggLevelMenu', getUseridList('#human'))
        delete('ggLevelMenu')

    # Let's create the "gungameLevelMenu" popup
    ggLevelMenu = create('ggLevelMenu')

    # Create empty instance of the popup
    ggLevelMenu.addline('->1. LEVEL')
    ggLevelMenu.addline('   * ')
    ggLevelMenu.addline('   * ')
    ggLevelMenu.addline('   * ')
    ggLevelMenu.addline('->2. WINS')
    ggLevelMenu.addline('   * ')
    ggLevelMenu.addline('->   9. View Leaders Menu')
    ggLevelMenu.select(9, send_leader_menu)
    ggLevelMenu.prepuser = prep_level_menu
    ggLevelMenu.timeout('send', 10)
    ggLevelMenu.timeout('view', 10)

    # Register command
    registerSayCommand('!level', level_menu_cmd, 'Displays a !level menu.')


def unload():
    # Delete the popup if it exists
    if pexists('ggLevelMenu'):
        unsendname('ggLevelMenu', getUseridList('#human'))
        delete('ggLevelMenu')

    # Unregister commands
    unregisterSayCommand('!level')


# =============================================================================
# >> MENU FUNCTIONS
# =============================================================================
def level_menu_cmd(userid, args):
    # Make sure player exists
    if not exists('userid', userid) and userid != 0:
        return

    if len(args):
        # Send user level search
        searchInput = str(args)
        checkUserid = getuserid(searchInput)

        # If the search failed, tell them and return
        if not checkUserid:
            msg(userid, 'LevelInfo_PlayerSearchFailed',
                {'player': searchInput})
            return

        # Get the player instance
        ggPlayer = Player(checkUserid)

        # Send the results
        saytext2(userid, ggPlayer.index, 'LevelInfo_PlayerSearch',
                            {'player': getplayername(checkUserid),
                            'level': ggPlayer.level,
                            'weapon': ggPlayer.weapon})
    else:
        # Send menu
        send('ggLevelMenu', userid)


def prep_level_menu(userid, popupid):
    # Make sure the popup exists
    if not pexists('ggLevelMenu'):
        return

    ggLevelMenu = find('ggLevelMenu')
    ggPlayer = Player(userid)

    # Get multikill count for the player's level
    multiKill = get_level_multikill(ggPlayer.level)

    # Use multikill style menu ?
    if multiKill > 1:
        ggLevelMenu.modline(2,
           '   * You are on level %s (%s)' % (ggPlayer.level, ggPlayer.weapon))
        ggLevelMenu.modline(3, '   * You have made %s' % ggPlayer.multikill +
        '/%s of your required kills' % multiKill)

    # Normal style menu
    else:
        ggLevelMenu.modline(2, '   * You are on level %s' % ggPlayer.level)
        ggLevelMenu.modline(3,
                        '   * You need a %s kill to advance' % ggPlayer.weapon)

    # Get leader's level
    leaderLevel = get_leader_level()

    # See if the leader is higher than level 1
    if leaderLevel > 1:

        # See if the player is a leader:
        if is_leader(userid):

            # See if there is more than 1 leader
            if get_leader_count() > 1:
                ggLevelMenu.modline(4,
                        '   * You are currently tied for the leader position')

            # Player is the only leader
            else:
                ggLevelMenu.modline(4, '   * You are currently the leader')

        # This player is not a leader
        else:
            ggLevelMenu.modline(4,
                '   * You are %s level(s)' % (leaderLevel - ggPlayer.level) +
                'behind the leader')

    # There are no leaders
    else:
        ggLevelMenu.modline(4, '   * There currently is no leader')

    # Wins information
    ggLevelMenu.modline(6, '   * You have won %s time(s)' % ggPlayer.wins)


def send_leader_menu(userid, choice, popupname):
    # Send the leader menu
    leader_menu_cmd(userid, '')
