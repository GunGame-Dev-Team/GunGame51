# ../cstrike/addons/eventscripts/gungame51/core/events/__init__.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
# EventScripts Imports
import es

# GunGame imports
from gungame51.core.leaders.shortcuts import leaders
from gungame51.core.leaders.shortcuts import getLeaderLevel

# ============================================================================
# >> CLASSES
# ============================================================================
class EventManager(object):
    # =========================================================================
    # >> EventManager() CUSTOM CLASS METHODS
    # =========================================================================
    def gg_levelup(self, playerInstance, levelsAwarded, victim, reason):
        '''
        Adds a declared number of levels to the attacker.

        Arguments:
            * playerInstance: (required)
                The stored BasePlayer instance contained within the PlayerDict.
                    - AKA "player[userid]"
            * levelsAwarded: (required)
                The number of levels to award to the attacker.
            * victim: (required)
                The userid of the victim.
            * reason: (required)
                The string reason for leveling up the attacker.
        '''
        # Set old level and the new level
        oldLevel = playerInstance.level
        newLevel = playerInstance.level + int(levelsAwarded)
        playerInstance.level = newLevel

        # Reset multikill
        playerInstance.multikill = 0

        # Check to see if the player is a leader
        if newLevel >= getLeaderLevel():
            leaders.add(playerInstance.userid)
        
        # Fire the event
        es.event('initialize', 'gg_levelup')
        es.event('setint', 'gg_levelup', 'attacker', playerInstance.userid)
        es.event('setint', 'gg_levelup', 'leveler', playerInstance.userid)
        es.event('setint', 'gg_levelup', 'old_level', oldLevel)
        es.event('setint', 'gg_levelup', 'new_level', newLevel)
        es.event('setint', 'gg_levelup', 'userid', victim)
        es.event('setstring', 'gg_levelup', 'reason', reason)
        es.event('fire', 'gg_levelup')

        return True

    def gg_leveldown(self, playerInstance, levelsTaken, attacker, reason):
        '''
        Removes a declared number of levels from the victim.

        Arguments:
            * playerInstance: (required)
                The stored BasePlayer instance contained within the PlayerDict.
                    - AKA "player[userid]"
            * levelsAwarded: (required)
                The number of levels to award to the attacker.
            * victim: (required)
                The userid of the victim.
            * reason: (required)
                The string reason for leveling up the attacker.
        '''
        # Set old level and the new level
        oldLevel = playerInstance.level
        if (oldLevel - int(levelsTaken)) > 0:
            playerInstance.level = oldLevel - int(levelsTaken)
        else:
            playerInstance.level = 1

        # Reset multikill
        playerInstance.multikill = 0

        # Fire the event
        es.event('initialize', 'gg_leveldown')
        es.event('setint', 'gg_leveldown', 'userid', playerInstance.userid)
        es.event('setint', 'gg_leveldown', 'leveler', playerInstance.userid)
        es.event('setint', 'gg_leveldown', 'old_level', oldLevel)
        es.event('setint', 'gg_leveldown', 'new_level', playerInstance.level)
        es.event('setint', 'gg_leveldown', 'attacker', attacker)
        es.event('setstring', 'gg_leveldown', 'reason', reason)
        es.event('fire', 'gg_leveldown')

        return True

events = EventManager()