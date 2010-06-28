# ../addons/eventscripts/gungame51/core/events/__init__.py

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
import gamethread

# GunGame imports
from gungame51.core.weapons.shortcuts import get_total_levels

# ============================================================================
# >> GLOBAL VARIABLES
# ============================================================================
gg_multi_round = es.ServerVar('gg_multi_round')
recentWinner = False

# ============================================================================
# >> GLOBAL Functions
# ============================================================================
def fireEvent(eventName, eventValues={}):
        """
        Fires a custom event. Ensures that we can delay this by 1 tick to
            prevent crashing.

        Thanks to Freddukes for this example.

        @param str eventName The name of the event to fire
        @param dict|mixed eventValues A dictionary containing the event
            variables to fire with the event
        """
        es.event("initialize", eventName)
        for event_var, event_values in eventValues.iteritems():
            es.event("set" + event_values[0], eventName, event_var,
                                                            event_values[1])
        es.event("fire", eventName)

# ============================================================================
# >> CLASSES
# ============================================================================
class EventManager(object):
    # =========================================================================
    # >> EventManager() CUSTOM CLASS METHODS
    # =========================================================================

    # =========================================================================
    # >> LEVELING EVENTS
    # =========================================================================
    def gg_levelup(self, playerInstance, levelsAwarded, victimInstance, 
      reason):
        '''
        Adds a declared number of levels to the attacker.

        Arguments:
            * playerInstance: (required)
                The stored BasePlayer instance contained within the 
                PlayerManager.
                    - AKA "player[userid]"
            * levelsAwarded: (required)
                The number of levels to award to the attacker.
            * victim: (required)
                The userid of the victim.
            * reason: (required)
                The string reason for leveling up the attacker.
        '''
        # Do not allow levelup if the player's preventlevel list is not empty
        if playerInstance.preventlevel:
            return False

        # Set old level and the new level
        oldLevel = playerInstance.level
        newLevel = playerInstance.level + int(levelsAwarded)

        # Check to see if the player just won
        if newLevel > get_total_levels():
            # If there was a recentWinner, stop here
            if recentWinner:
                return False

            global recentWinner
            # Set recentWinner to True
            recentWinner = True
            # In 1 second, remove the recentWinner
            gamethread.delayed(3, self.remove_recent_winner)

            # If "gg_multi_round" is disabled
            if not int(gg_multi_round):
                # Fire the event "gg_win"
                self.gg_win(playerInstance, victimInstance, round=0)
                return True

            # Fire the event "gg_win" and set the round
            from gungame51.gungame51 import RoundInfo
            self.gg_win(playerInstance, victimInstance, 
                round=int(RoundInfo().remaining))
            return True

        playerInstance.level = newLevel

        # Reset multikill
        playerInstance.multikill = 0

        # Fire the event
        event_values = {}
        event_values["attacker"] = ("int", playerInstance.userid)
        event_values["leveler"] = ("int", playerInstance.userid)
        event_values["old_level"] = ("int", oldLevel)
        event_values["new_level"] = ("int", newLevel)
        event_values["userid"] = ("int",
                            0 if not victimInstance else victimInstance.userid)
        event_values["reason"] = ("string", reason)
        gamethread.delayed(0, fireEvent, ("gg_levelup", event_values))

        return True

    def gg_leveldown(self, playerInstance, levelsTaken, attackerInstance, 
      reason):
        '''
        Removes a declared number of levels from the victim.

        Arguments:
            * playerInstance: (required)
                The stored BasePlayer instance contained within the 
                PlayerManager.
                    - AKA "player[userid]"
            * levelsAwarded: (required)
                The number of levels to award to the attacker.
            * victim: (required)
                The userid of the victim.
            * reason: (required)
                The string reason for leveling up the attacker.
        '''
        # Do not allow leveldown if the player's preventlevel list is not empty
        if playerInstance.preventlevel:
            return False

        # Set old level and the new level
        oldLevel = playerInstance.level
        if (oldLevel - int(levelsTaken)) > 0:
            playerInstance.level = oldLevel - int(levelsTaken)
        else:
            playerInstance.level = 1

        # Reset multikill
        playerInstance.multikill = 0

        # Fire the event
        event_values = {}
        event_values["userid"] = ("int", playerInstance.userid)
        event_values["leveler"] = ("int", playerInstance.userid)
        event_values["old_level"] = ("int", oldLevel)
        event_values["new_level"] = ("int", playerInstance.level)
        event_values["attacker"] = ("int",
                        0 if not attackerInstance else attackerInstance.userid)
        event_values["reason"] = ("string", reason)
        gamethread.delayed(0, fireEvent, ("gg_leveldown", event_values))

        return True

    def gg_win(self, attackerInstance, victimInstance, round):
        event_values = {}
        event_values["attacker"] = ("int", attackerInstance.userid)
        event_values["winner"] = ("int", attackerInstance.userid)
        event_values["userid"] = ("int",
                            0 if not victimInstance else victimInstance.userid)
        event_values["loser"] = ("int",
                            0 if not victimInstance else victimInstance.userid)
        event_values["round"] = ("int",
                                        int(round) if int(round) > 0 else 0)
        gamethread.delayed(0, fireEvent, ("gg_win", event_values))

    # =========================================================================
    # >> LEADER EVENTS
    # =========================================================================
    def gg_new_leader(self, userid):
        from gungame51.core.leaders.shortcuts import LeaderManager
        event_values = {}
        event_values["userid"] = ("int", userid)
        event_values["leveler"] = ("int", userid)
        event_values["leaders"] = ("int",
                        ",".join([str(x) for x in LeaderManager().current[:]]))
        event_values["old_leaders"] = ("int",
                    ",".join([str(x) for x in LeaderManager().previous[:]]))
        event_values["leader_level"] = ("int",
                                                LeaderManager().leaderlevel)
        gamethread.delayed(0, fireEvent, ("gg_new_leader", event_values))

    def gg_tied_leader(self, userid):
        from gungame51.core.leaders.shortcuts import LeaderManager
        event_values = {}
        event_values["userid"] = ("int", userid)
        event_values["leveler"] = ("int", userid)
        event_values["leaders"] = ("int",
                        ",".join([str(x) for x in LeaderManager().current[:]]))
        event_values["old_leaders"] = ("int",
                    ",".join([str(x) for x in LeaderManager().previous[:]]))
        event_values["leader_level"] = ("int",
                                                LeaderManager().leaderlevel)
        gamethread.delayed(0, fireEvent, ("gg_tied_leader", event_values))

    def gg_leader_lostlevel(self, userid):
        from gungame51.core.leaders.shortcuts import LeaderManager
        event_values = {}
        event_values["userid"] = ("int", userid)
        event_values["leveler"] = ("int", userid)
        event_values["leaders"] = ("int",
                        ",".join([str(x) for x in LeaderManager().current[:]]))
        event_values["old_leaders"] = ("int",
                    ",".join([str(x) for x in LeaderManager().previous[:]]))
        event_values["leader_level"] = ("int",
                                                LeaderManager().leaderlevel)
        gamethread.delayed(0, fireEvent, ("gg_leader_lostlevel", event_values))
        
    # =========================================================================
    # >> LOAD/UNLOAD, START/END EVENTS
    # =========================================================================
    def gg_load(self):
        gamethread.delayed(0, fireEvent, ("gg_load"))
        
    def gg_unload(self):
        gamethread.delayed(0, fireEvent, ("gg_unload"))
        
    def gg_start(self):
        gamethread.delayed(0, fireEvent, ("gg_start"))
        
    def gg_map_end(self):
        gamethread.delayed(0, fireEvent, ("gg_map_end"))
    
    # =========================================================================
    # >> ADDON EVENTS
    # =========================================================================
    def gg_addon_loaded(self, addon, type):
        event_values = {}
        event_values["addon"] = ("string", addon)
        event_values["type"] = ("string", type)
        gamethread.delayed(0, fireEvent, ("gg_addon_loaded", event_values))
        
    def gg_addon_unloaded(self, addon, type):
        event_values = {}
        event_values["addon"] = ("string", addon)
        event_values["type"] = ("string", type)
        gamethread.delayed(0, fireEvent, ("gg_addon_unloaded", event_values))
        
    def gg_vote(self):
        gamethread.delayed(0, fireEvent, ("gg_vote"))
        
    def gg_knife_steal(self, attackerInstance, victimInstance):
        '''
        Usage:
            from gungame.core.players.shortcuts import Player
            from gungame.core.events import EventManager
            
            def player_death(event_var):
                # Make sure this was a knife kill
                if event_var['weapon'] != 'knife':
                    return
                
                # Get the attacker's Player() instance
                aInstance = Player(event_var['attacker'])
                
                # Get the victim's Player() instance
                vInstance = Player(event_var['userid'])
                
                # Trigger the event "gg_knife_steal"
                EventManager().gg_knife_steal(aInstance, vInstance)
        '''
        event_values = {}
        event_values["attacker"] = ("int", attackerInstance.userid)
        event_values["attacker_level"] = ("int", attackerInstance.level)
        event_values["userid"] = ("int", victimInstance.userid)
        event_values["userid_level"] = ("int", victimInstance.level)
        gamethread.delayed(0, fireEvent, ("gg_knife_steal", event_values))
        
    def gg_multi_level(self, userid):
        event_values = {}
        event_values["userid"] = ("int", userid)
        event_values["leveler"] = ("int", userid)
        gamethread.delayed(0, fireEvent, ("gg_multi_level", event_values))
    
    def remove_recent_winner(self):
        global recentWinner

        recentWinner = False