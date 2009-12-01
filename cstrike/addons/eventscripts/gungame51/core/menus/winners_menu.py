# ../addons/eventscripts/gungame/core/menu/level_menu.py

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
from gungame51.core.players.shortcuts import Player
from gungame51.core.leaders.shortcuts import get_leader_count
from gungame51.core.leaders.shortcuts import get_leader_level
from gungame51.core.leaders.shortcuts import is_leader
from gungame51.core.weapons.shortcuts import get_level_multikill
from gungame51.core.sql.shortcuts import get_winners_list

# ============================================================================
# >> GLOBALS
# ============================================================================
winnersList = []
ggWinnersMenu = None

# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    # Delete the popup if it exists
    if popuplib.exists('ggWinnersMenu'):
        popuplib.unsendname('ggWinnersMenu', getUseridList('#human'))
        popuplib.delete('ggWinnersMenu')

    # Register command
    registerSayCommand('!top10', winner_menu_cmd, 'Displays a !top10 menu.')
    registerSayCommand('!winners', winner_menu_cmd, 'Displays a !top10 menu.')
    registerSayCommand('!top', winner_menu_cmd, 'Displays a !top10 menu.')

def unload():
    # Delete the popup if it exists
    if popuplib.exists('ggWinnersMenu'):
        ggWinnersMenu.delete()

    # Unregister commands
    unregisterSayCommand('!top10')
    unregisterSayCommand('!top')
    unregisterSayCommand('!winners')

# ============================================================================
# >> MENU FUNCTIONS
# ============================================================================
def winner_menu_cmd(userid, args):
    # Make sure player exists
    if not es.exists('userid', userid):
        return

    currentWinners = get_winners_list(50)

    # Does the popup exist ?
    if popuplib.exists('ggWinnersMenu'):

        # Send current menu
        if winnersList == currentWinners:
            ggWinnersMenu.send(userid)
            return

        # Delete the old menu
        popuplib.unsendname('ggWinnersMenu', getUseridList('#human'))
        popuplib.delete('ggWinnersMenu')

    # Update winnersList
    del winnersList[:]
    winnersList.extend(currentWinners)
    rankings = []

    # Empty database ?
    if currentWinners == []:
        rankings = ['Nobody has won yet!']

    # 1 Winner ?
    elif isinstance(currentWinners, dict):
        rankings.append('[%s] %s' % (currentWinners['wins'],
                                                       currentWinners['name']))

    # Update popup list
    else:
        for player in currentWinners:
            rankings.append('[%s] %s' % (player['wins'], player['name']))
            
    # Make new menu
    global ggWinnersMenu
    ggWinnersMenu = popuplib.easylist('ggWinnersMenu', rankings)
    ggWinnersMenu.settitle('GunGame !winners Menu')
    ggWinnersMenu.timeout('view', 30)
    ggWinnersMenu.timeout('send', 30)
    
    # Send the new menu
    ggWinnersMenu.send(userid)