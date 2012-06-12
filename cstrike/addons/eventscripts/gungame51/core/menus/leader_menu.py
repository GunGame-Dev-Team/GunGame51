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
#   ES
from es import exists
#   Cmdlib
from cmdlib import registerSayCommand
from cmdlib import unregisterSayCommand
#   Playerlib
from playerlib import getUseridList
#   Popuplib
from popuplib import create
from popuplib import delete
from popuplib import exists as pexists
from popuplib import send
from popuplib import unsendname

# GunGame Imports
#   Leaders
from gungame51.core.leaders.shortcuts import get_leader_level
from gungame51.core.leaders.shortcuts import get_leader_names
#   Weapons
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
    if pexists('ggLeaderMenu'):
        unsendname('ggLeaderMenu', getUseridList('#human'))
        delete('ggLeaderMenu')

    # Register commands
    registerSayCommand('!leader', leader_menu_cmd, 'Displays a !leader menu.')
    registerSayCommand('!leaders', leader_menu_cmd,
        'Displays a !leaders menu.')


def unload():
    # Delete the popup if it exists
    if pexists('ggLeaderMenu'):
        unsendname('ggLeaderMenu', getUseridList('#human'))
        delete('ggLeaderMenu')

    # Unregister commands
    unregisterSayCommand('!leader')
    unregisterSayCommand('!leaders')


# =============================================================================
# >> MENU FUNCTIONS
# =============================================================================
def leader_menu_cmd(userid, args):
    global leaderList

    # Make sure player exists
    if not exists('userid', userid) and userid != 0:
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
    if pexists('ggLeaderMenu'):

        # Send the user the current popup ?
        if newLeaderList == leaderList:
            send('ggLeaderMenu', userid)
            return

        # Delete the popup
        unsendname('ggLeaderMenu', getUseridList('#human'))
        delete('ggLeaderMenu')

    # Build new popup
    ggLeaderMenu = create('ggLeaderMenu')
    ggLeaderMenu.timeout('send', 10)
    ggLeaderMenu.timeout('view', 10)

    # Add lines to new popup
    for line in newLeaderList:
        ggLeaderMenu.addline(line)

    # Save current popup
    leaderList = newLeaderList

    # Send it
    send('ggLeaderMenu', userid)
