# ../addons/eventscripts/gungame/core/players/shortcuts.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
# EventScripts Imports
from playerlib import getPlayerList

# GunGame Imports
from gungame51.core.players import Player
from gungame51.core.players import players
from gungame51.core.players import isDead
from gungame51.core.players import isSpectator

# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
def addAttributeCallBack(attribute, function, addon):
    Player.addAttributeCallBack(attribute, function, addon)
    
def removeAttributeCallBack(attribute):
    Player.removeAttributeCallBack(attribute)
    
def removeCallBacksForAddon(addon):
    Player.removeCallBacksForAddon(addon)

def setAttribute(filter, attribute, value):
    '''
    Sets a Player() attribute by userid or by filter:
        #all, #alive, #dead, #human, #bot, #un, #spec
    Note:
        See playerlib.getPlayerList() for the appropriate filters.

    Usage:
        from gungame.core.players.shortcuts import setAttribute

        # Set a custom attribute for all players
        setAttribute('#all', 'myattribute', 0)

        # Call this attribute (from some event that provides a userid)
        es.msg('myattribute for %s = %s'
            %(event_var['es_username'], Player(event_var['userid']).myattribute))
    '''
    if isinstance(filter, int):
        filter = str(filter)

    if '#' in filter:
        for userid in getPlayerList(filter):
            import es
            es.dbgmsg(0, 'Set attribute "%s" for %s to "%s"' %(attribute, es.getplayername(userid), value))
            Player(userid)[attribute] = value
        return
    Player(filter)[attribute] = value

def deleteAttribute(filter, attribute):
    '''
    Deletes a Player() attribute by userid or by filter:
        #all, #alive, #dead, #human, #bot, #un, #spec

    Note:
        See playerlib.getPlayerList() for the appropriate filters.

    Usage:
        from gungame.core.players.shortcuts import deleteAttribute

        # Delete a custom attribute for all players
        deleteAttribute('#all', 'myattribute')

        # Delete a custom attribute from one player
        deleteAttribute(event_var['userid'], 'myattribute')
    '''
    if isinstance(filter, int):
        filter = str(filter)

    if '#' in filter:
        for userid in getPlayerList(filter):
            del Player(userid)[attribute]
        return
    del Player(filter)[attribute]

def resetPlayers():
    '''
    Resets the PlayerDict instance, deleting all instances of BasePlayer
    contained within, which effectively resets all players' attributes.
    
    Notes:
        * All custom attributes will have to be re-declared after this
          command has been issued.
        * It is recommended that if any custom attributes are set, that
          the scripter uses event gg_start to re-initialize custom
          player attributes.
    '''
    players.clear()
    
# ============================================================================
# >> DOCTSTRING REDIRECTS
# ============================================================================
# Declare the docstring for addAttributeCallBack
addAttributeCallBack.__doc__ = Player.addAttributeCallBack.__doc__
# Declare the docstring for removeAttributeCallBack
removeAttributeCallBack.__doc__ = Player.removeAttributeCallBack.__doc__
# Declare the docstring for removeCallBacksForAddon
removeCallBacksForAddon.__doc__ = Player.removeCallBacksForAddon.__doc__