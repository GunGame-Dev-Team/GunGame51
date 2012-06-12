# ../core/menus/rank_menu.py

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
from es import getplayersteamid
#   Cmdlib
from cmdlib import registerSayCommand
from cmdlib import unregisterSayCommand

# GunGame Imports
#   Menus
from gungame51.core.menus import OrderedMenu
from gungame51.core.menus.shortcuts import get_index_page
#   SQL
from gungame51.core.sql.shortcuts import get_winners_list


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    # Register command
    registerSayCommand('!rank', rank_menu_cmd, 'Displays a !rank menu.')


def unload():
    # Unregister commands
    unregisterSayCommand('!rank')


# =============================================================================
# >> MENU FUNCTIONS
# =============================================================================
def rank_menu_cmd(userid, args):
    # Make sure player exists
    if not exists('userid', userid) and userid != 0:
        return

    # Get the winners list with a limit of 0 (unlimited)
    currentWinners = get_winners_list(0)
    rankings = []
    rank = 0

    # Empty database ?
    if currentWinners == []:
        rankings = ['Nobody has won yet!']

    # 1 Winner ?
    elif isinstance(currentWinners, dict):
        # Check to see if the player requesting the menu is the player being
        # listed
        if currentWinners["uniqueid"] == getplayersteamid(userid):
            rank = 1

        # Add the player
        rankings.append('[%s] %s' % (currentWinners['wins'],
                                                       currentWinners['name']))

    # Update popup list
    else:
        count = 0

        for player in currentWinners:
            count += 1

            # Check to see if the player requesting the menu is the player
            # being listed
            if player["uniqueid"] == getplayersteamid(userid):
                rank = count

            # Add the player
            rankings.append('[%s] %s' % (player['wins'], player['name']))

    # Create a new OrderedMenu
    ggRankMenu = OrderedMenu(userid, 'GunGame: Rank Menu', rankings,
                                                        highlightIndex=rank)

    # Send the OrderedMenu on the page the player is on
    ggRankMenu.send_page(get_index_page(rank))
