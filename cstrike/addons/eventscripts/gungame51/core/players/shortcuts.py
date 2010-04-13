# ../addons/eventscripts/gungame51/core/players/shortcuts.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
# Python Imports
from copy import copy

# EventScripts Imports
from playerlib import getPlayerList

# GunGame Imports
from gungame51.core.players import Player
from gungame51.core.players import PlayerManager
from gungame51.core.leaders.shortcuts import reset_leaders

# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
def add_attribute_callback(attribute, function, addon):
    Player.add_attribute_callback(attribute, function, addon)
    
def remove_attribute_callback(attribute):
    Player.remove_attribute_callback(attribute)
    
def remove_callbacks_for_addon(addon):
    Player.remove_callbacks_for_addon(addon)

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
            Player(userid)[attribute] = copy(value)
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
    Resets the BasePlayer instances, setting their attributes back to default.
    
    Notes:
        * All custom attributes will have to be re-declared after this
          command has been issued.
        * It is recommended that if any custom attributes are set, that
          the scripter uses event gg_start to re-initialize custom
          player attributes.
    '''
    PlayerManager().reset()
    reset_leaders()
    
    
# ============================================================================
# >> DOCTSTRING REDIRECTS
# ============================================================================
# Declare the docstring for add_attribute_callback
add_attribute_callback.__doc__ = Player.add_attribute_callback.__doc__
# Declare the docstring for remove_attribute_callback
remove_attribute_callback.__doc__ = Player.remove_attribute_callback.__doc__
# Declare the docstring for remove_callbacks_for_addon
remove_callbacks_for_addon.__doc__ = Player.remove_callbacks_for_addon.__doc__