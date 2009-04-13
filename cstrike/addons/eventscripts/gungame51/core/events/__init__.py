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

# ============================================================================
# >> CLASSES
# ============================================================================
class EventManager(object):
    def gg_levelup(self, userid, levelsAwarded, victim, reason):
        '''
        Adds a declared number of levels to the attacker.
        
        Arguments:
            * levelsAwarded: (required)
                The number of levels to award to the attacker.
            * victim: (default of 0)
                The userid of the victim.
            * reason: (not required)
                The string reason for leveling up the attacker.
        '''
        from gungame51.core.players import players
        
        # Set old level and the new level
        oldLevel = players[userid].level
        newLevel = players[userid].level + int(levelsAwarded)
        players[userid].level = newLevel
        
        # Fire the event
        es.event('initialize', 'gg_levelup')
        es.event('setint', 'gg_levelup', 'attacker', userid)
        es.event('setint', 'gg_levelup', 'leveler', userid)
        es.event('setint', 'gg_levelup', 'old_level', oldLevel)
        es.event('setint', 'gg_levelup', 'new_level', newLevel)
        es.event('setint', 'gg_levelup', 'userid', victim)
        es.event('setstring', 'gg_levelup', 'reason', reason)
        es.event('fire', 'gg_levelup')
        
        return True
        
    def gg_leveldown(self, userid, levelsTaken, attacker, reason):
        '''
        This player should be the victim (the player that is levelling down)
        '''
        from gungame51.core.players import players
        # Set old level and the new level
        oldLevel = players[userid].level
        players[userid].level = oldLevel - int(levelsTaken)
        
        # Fire the event
        es.event('initialize', 'gg_leveldown')
        es.event('setint', 'gg_leveldown', 'userid', userid)
        es.event('setint', 'gg_leveldown', 'leveler', userid)
        es.event('setint', 'gg_leveldown', 'old_level', oldLevel)
        es.event('setint', 'gg_leveldown', 'new_level', players[userid].level)
        es.event('setint', 'gg_leveldown', 'attacker', attacker)
        es.event('setstring', 'gg_leveldown', 'reason', reason)
        es.event('fire', 'gg_leveldown')
        
        
events = EventManager()