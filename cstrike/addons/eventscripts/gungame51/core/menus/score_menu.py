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

# ============================================================================
# >> GLOBALS
# ============================================================================
scoreList = []
ggScoreMenu = None

# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    # Delete the popup if it exists
    if popuplib.exists('ggScoreMenu'):
        popuplib.unsendname('ggScoreMenu', getUseridList('#human'))
        popuplib.delete('ggScoreMenu')

    # Register command
    registerSayCommand('!score', score_menu_cmd, 'Displays a !score menu.')

def unload():
    # Delete the popup if it exists
    if popuplib.exists('ggScoreMenu'):
        ggScoreMenu.delete()

    # Unregister commands
    unregisterSayCommand('!score')

# ============================================================================
# >> MENU FUNCTIONS
# ============================================================================
def score_menu_cmd(userid, args):
    # Make sure player exists
    if not es.exists('userid', userid):
        return

    # Get list of levels
    newScoreList = []
    for player in getUseridList('#all'):
        newScoreList.append('[%s] %s' % (Player(player).level,
                                                    es.getplayername(player)))
    # Sort from highest to lowest
    newScoreList.sort(reverse=True)

    # Is the list empty ?
    if not newScoreList:
        return

    # Get the page the player is on
    page = ((newScoreList.index('[%s] %s' % (Player(userid).level,
                                        es.getplayername(player))) + 1) / 10)
                                        
    # Menu has not changed ?
    if newScoreList == scoreList:
        ggScoreMenu.sendPage(userid, page)
        return
        
    # Rewrite scoreList
    del scoreList[:]
    scoreList.extend(newScoreList)

    # Delete the popup if it exists
    if popuplib.exists('ggScoreMenu'):
        popuplib.unsendname('ggScoreMenu', getUseridList('#human'))
        popuplib.delete('ggScoreMenu')

    # Let's create the new ggScoreMenu popup
    global ggScoreMenu
    ggScoreMenu = popuplib.easylist('ggScoreMenu', newScoreList)
    ggScoreMenu.settitle('GunGame !score Menu')
    ggScoreMenu.timeout('view', 15)
    ggScoreMenu.timeout('send', 15)

    # Send menu
    ggScoreMenu.sendPage(userid, page)