# ../core/menus/score_menu.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# Eventscripts Imports
import es
from cmdlib import registerSayCommand
from cmdlib import unregisterSayCommand

# GunGame Imports
from gungame51.core.players.shortcuts import Player
from gungame51.core.menus import OrderedMenu
from gungame51.core.menus.shortcuts import get_index_page


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    # Register command
    registerSayCommand('!score', score_menu_cmd, 'Displays a !score menu.')


def unload():
    # Unregister commands
    unregisterSayCommand('!score')


# =============================================================================
# >> MENU FUNCTIONS
# =============================================================================
def score_menu_cmd(userid, args):
    # Make sure player exists
    if not es.exists('userid', userid) and userid != 0:
        return

    # Get list of levels
    scoreList = []
    for player in es.getUseridList():
        scoreList.append('[%s] %s' % (Player(player).level,
                                                    es.getplayername(player)))
    # Sort from highest to lowest
    scoreList.sort(lambda a, b: cmp(int(b[1:].split("]")[0]),
        int(a[1:].split("]")[0])))

    # Is the list empty ?
    if not scoreList:
        return

    # Get the list number the player is at
    listNumber = scoreList.index('[%s] %s' % (Player(userid).level,
                                                es.getplayername(userid))) + 1

    # Create a new OrderedMenu
    ggScoreMenu = OrderedMenu(userid, 'GunGame: Score Menu', scoreList,
                                                    highlightIndex=listNumber)

    # Send the OrderedMenu on the page the player is on
    ggScoreMenu.send_page(get_index_page(listNumber))
