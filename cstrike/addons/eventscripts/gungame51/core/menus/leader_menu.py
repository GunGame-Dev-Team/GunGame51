# ../core/menus/leader_menu.py

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
import popuplib
from playerlib import getUseridList
from cmdlib import registerSayCommand
from cmdlib import unregisterSayCommand

# GunGame Imports
from gungame51.core.leaders.shortcuts import get_leader_level
from gungame51.core.leaders.shortcuts import get_leader_names
from gungame51.core.weapons.shortcuts import get_level_weapon

# =============================================================================
# >> GLOBALS
# =============================================================================
leaderList = []


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    # Delete the popup if it exists
    if popuplib.exists('ggLeaderMenu'):
        popuplib.unsendname('ggLeaderMenu', getUseridList('#human'))
        popuplib.delete('ggLeaderMenu')

    # Register commands
    es.dbgmsg(0, '\t!leader')
    registerSayCommand('!leader', leader_menu_cmd, 'Displays a !leader menu.')
    es.dbgmsg(0, '\t!leaders')
    registerSayCommand('!leaders', leader_menu_cmd,
        'Displays a !leaders menu.')


def unload():
    # Delete the popup if it exists
    if popuplib.exists('ggLeaderMenu'):
        popuplib.unsendname('ggLeaderMenu', getUseridList('#human'))
        popuplib.delete('ggLeaderMenu')

    # Unregister commands
    unregisterSayCommand('!leader')
    unregisterSayCommand('!leaders')


# =============================================================================
# >> MENU FUNCTIONS
# =============================================================================
def leader_menu_cmd(userid, args):
    global leaderList

    # Make sure player exists
    if not es.exists('userid', userid) and userid != 0:
        return

    # Get menu contents
    newLeaderList = ['->1. Current Leaders:']
    leaderNames = get_leader_names()

    # Add names if we have leaders
    if leaderNames:
        # Add leader level and weapon
        leaderLevel = get_leader_level()
        newLeaderList.append('    Level %s (%s)' % (leaderLevel,
                                get_level_weapon(leaderLevel)))

        # Divider
        newLeaderList.append('-' * 26)

        # Add player names
        for player_name in leaderNames:
            newLeaderList.append('   * %s' % player_name)

    # No leader
    else:
        newLeaderList.extend(('-' * 26, '   * There currently is no leader'))

    # Finish popup with divider and exit
    newLeaderList.extend(('-' * 26, '0. Exit'))

    # Does the popup exists ?
    if popuplib.exists('ggLeaderMenu'):

        # Send the user the current popup ?
        if newLeaderList == leaderList:
            popuplib.send('ggLeaderMenu', userid)
            return

        # Delete the popup
        popuplib.unsendname('ggLeaderMenu', getUseridList('#human'))
        popuplib.delete('ggLeaderMenu')

    # Build new popup
    ggLeaderMenu = popuplib.create('ggLeaderMenu')
    ggLeaderMenu.timeout('send', 10)
    ggLeaderMenu.timeout('view', 10)

    # Add lines to new popup
    for line in newLeaderList:
        ggLeaderMenu.addline(line)

    # Save current popup
    leaderList = newLeaderList

    # Send it
    popuplib.send('ggLeaderMenu', userid)
