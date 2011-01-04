# ../addons/eventscripts/gungame51/core/menus/winners_menu.py

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
from gungame51.core.sql.shortcuts import get_winners_list
from gungame51.core.menus import OrderedMenu
from gungame51.core.menus.shortcuts import get_index_page

# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    # Register command
    es.dbgmsg(0, '\t!top10')
    registerSayCommand('!top10', winner_menu_cmd, 'Displays a !top10 menu.')
    es.dbgmsg(0, '\t!winners')
    registerSayCommand('!winners', winner_menu_cmd, 'Displays a !top10 menu.')
    es.dbgmsg(0, '\t!top')
    registerSayCommand('!top', winner_menu_cmd, 'Displays a !top10 menu.')

def unload():
    # Unregister commands
    unregisterSayCommand('!top10')
    unregisterSayCommand('!top')
    unregisterSayCommand('!winners')

# =============================================================================
# >> MENU FUNCTIONS
# =============================================================================
def winner_menu_cmd(userid, args):
    # Make sure player exists
    if not es.exists('userid', userid) and userid != 0:
        return

    # Get the winners list with a limit of the top 50 winners
    currentWinners = get_winners_list(50)
    rankings = []
    rank = 0

    # Empty database ?
    if currentWinners == []:
        rankings = ['Nobody has won yet!']

    # 1 Winner ?
    elif isinstance(currentWinners, dict):
        # Check to see if the player requesting the menu is the player being
        # listed
        if currentWinners["uniqueid"] == es.getplayersteamid(userid):
            rank = 1

        # Add the player
        rankings.append('[%s] %s' % (currentWinners['wins'],
                                                       currentWinners['name']))

    # Update popup list
    else:
        count = 0

        for player in currentWinners:
            count += 1

            # Check to see if the player requesting the menu is the player being
            # listed
            if player["uniqueid"] == es.getplayersteamid(userid):
                rank = count

            # Add the player
            rankings.append('[%s] %s' % (player['wins'], player['name']))

    # Create a new OrderedMenu
    ggWinnersMenu = OrderedMenu(userid, 'GunGame: Winners Menu', rankings,
                                                        highlightIndex=rank)

    # Send the OrderedMenu
    ggWinnersMenu.send_page(1)