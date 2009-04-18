# ../cstrike/addons/eventscripts/gungame51/core/players/shortcuts.py

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

# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
def addAttributeCallBack(attribute, function, addon):
    Player.addAttributeCallBack(attribute, function, addon)
# Declare the docstring for addAttributeCallBack
addAttributeCallBack.__doc__ = Player.addAttributeCallBack.__doc__
    
def removeAttributeCallBack(attribute):
    Player.removeAttributeCallBack(attribute)
# Declare the docstring for removeAttributeCallBack
removeAttributeCallBack.__doc__ = Player.removeAttributeCallBack.__doc__
    
def removeCallBacksForAddon(addon):
    Player.removeCallBacksForAddon(addon)
# Declare the docstring for removeCallBacksForAddon
removeCallBacksForAddon.__doc__ = Player.removeCallBacksForAddon.__doc__

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
    if '#' in filter:
        for userid in getPlayerList(filter):
            del Player(userid)[attribute]
        return
    del Player(filter)[attribute]