# ../core/events/__init__.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# EventScripts Imports
import es
import gamethread

# GunGame imports
from gungame51.core.weapons.shortcuts import get_total_levels

# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
gg_multi_round = es.ServerVar('gg_multi_round')
recentWinner = False


# =============================================================================
# >> CLASSES
# =============================================================================
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
            global recentWinner

            # If there was a recentWinner, stop here
            if recentWinner:
                return False

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
        es.event('initialize', 'gg_levelup')
        es.event('setint', 'gg_levelup', 'attacker', playerInstance.userid)
        es.event('setint', 'gg_levelup', 'leveler', playerInstance.userid)
        es.event('setint', 'gg_levelup', 'old_level', oldLevel)
        es.event('setint', 'gg_levelup', 'new_level', newLevel)
        es.event('setint', 'gg_levelup', 'userid',
                 '0' if not victimInstance else victimInstance.userid)
        es.event('setstring', 'gg_levelup', 'reason', reason)
        es.event('fire', 'gg_levelup')

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
        es.event('initialize', 'gg_leveldown')
        es.event('setint', 'gg_leveldown', 'userid', playerInstance.userid)
        es.event('setint', 'gg_leveldown', 'leveler', playerInstance.userid)
        es.event('setint', 'gg_leveldown', 'old_level', oldLevel)
        es.event('setint', 'gg_leveldown', 'new_level', playerInstance.level)
        es.event('setint', 'gg_leveldown', 'attacker',
                 '0' if not attackerInstance else attackerInstance.userid)
        es.event('setstring', 'gg_leveldown', 'reason', reason)
        es.event('fire', 'gg_leveldown')

        return True

    def gg_win(self, attackerInstance, victimInstance, round):
        es.event('initialize', 'gg_win')
        es.event('setint', 'gg_win', 'attacker', attackerInstance.userid)
        es.event('setint', 'gg_win', 'winner', attackerInstance.userid)
        es.event('setint', 'gg_win', 'userid',
                 '0' if not victimInstance else victimInstance.userid)
        es.event('setint', 'gg_win', 'loser',
                 '0' if not victimInstance else victimInstance.userid)
        es.event('setint', 'gg_win', 'round',
                 int(round) if int(round) > 0 else '0')
        es.event('fire', 'gg_win')

    # =========================================================================
    # >> LEADER EVENTS
    # =========================================================================
    def gg_new_leader(self, userid):
        from gungame51.core.leaders.shortcuts import LeaderManager

        # Set up leaders strings
        new_leaders = ",".join([str(x) for x in LeaderManager().current[:]])
        old_leaders = ",".join([str(x) for x in LeaderManager().previous[:]])

        es.event('initialize', 'gg_new_leader')
        es.event('setint', 'gg_new_leader', 'userid', userid)
        es.event('setint', 'gg_new_leader', 'leveler', userid)
        es.event('setstring', 'gg_new_leader', 'leaders',
            new_leaders if new_leaders else "None")
        es.event('setstring', 'gg_new_leader', 'old_leaders',
            old_leaders if old_leaders else "None")
        es.event('setint', 'gg_new_leader', 'leader_level',
                 LeaderManager().leaderlevel)
        es.event('fire', 'gg_new_leader')

    def gg_tied_leader(self, userid):
        from gungame51.core.leaders.shortcuts import LeaderManager

        # Set up leaders strings
        new_leaders = ",".join([str(x) for x in LeaderManager().current[:]])
        old_leaders = ",".join([str(x) for x in LeaderManager().previous[:]])

        es.event('initialize', 'gg_tied_leader')
        es.event('setint', 'gg_tied_leader', 'userid', userid)
        es.event('setint', 'gg_tied_leader', 'leveler', userid)
        es.event('setstring', 'gg_tied_leader', 'leaders',
            new_leaders if new_leaders else "None")
        es.event('setstring', 'gg_tied_leader', 'old_leaders',
            old_leaders if old_leaders else "None")
        es.event('setint', 'gg_tied_leader', 'leader_level',
                 LeaderManager().leaderlevel)
        es.event('fire', 'gg_tied_leader')

    def gg_leader_lostlevel(self, userid):
        from gungame51.core.leaders.shortcuts import LeaderManager

        # Set up leaders strings
        new_leaders = ",".join([str(x) for x in LeaderManager().current[:]])
        old_leaders = ",".join([str(x) for x in LeaderManager().previous[:]])

        es.event('initialize', 'gg_leader_lostlevel')
        es.event('setint', 'gg_leader_lostlevel', 'userid', userid)
        es.event('setint', 'gg_leader_lostlevel', 'leveler', userid)
        es.event('setstring', 'gg_leader_lostlevel', 'leaders',
            new_leaders if new_leaders else "None")
        es.event('setstring', 'gg_leader_lostlevel', 'old_leaders',
            old_leaders if old_leaders else "None")
        es.event('setint', 'gg_leader_lostlevel', 'leader_level',
                 LeaderManager().leaderlevel)
        es.event('fire', 'gg_leader_lostlevel')

    # =========================================================================
    # >> LOAD/UNLOAD, START/END EVENTS
    # =========================================================================
    def gg_load(self):
        es.event('initialize', 'gg_load')
        es.event('fire', 'gg_load')

    def gg_unload(self):
        es.event('initialize', 'gg_unload')
        es.event('fire', 'gg_unload')

    def gg_start(self):
        es.event('initialize', 'gg_start')
        es.event('fire', 'gg_start')

    def gg_map_end(self):
        es.event('initialize', 'gg_map_end')
        es.event('fire', 'gg_map_end')

    # =========================================================================
    # >> ADDON EVENTS
    # =========================================================================
    def gg_addon_loaded(self, addon, type):
        es.event('initialize', 'gg_addon_loaded')
        es.event('setstring', 'gg_addon_loaded', 'addon', addon)
        es.event('setstring', 'gg_addon_loaded', 'type', type)
        es.event('fire', 'gg_addon_loaded')

    def gg_addon_unloaded(self, addon, type):
        es.event('initialize', 'gg_addon_unloaded')
        es.event('setstring', 'gg_addon_unloaded', 'addon', addon)
        es.event('setstring', 'gg_addon_unloaded', 'type', type)
        es.event('fire', 'gg_addon_unloaded')

    def gg_vote(self):
        es.event('initialize', 'gg_vote')
        es.event('fire', 'gg_vote')

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
        es.event('initialize', 'gg_knife_steal')
        es.event('setint', 'gg_knife_steal', 'attacker',
                 attackerInstance.userid)
        es.event('setint', 'gg_knife_steal', 'attacker_level',
                 attackerInstance.level)
        es.event('setint', 'gg_knife_steal', 'userid', victimInstance.userid)
        es.event('setint', 'gg_knife_steal', 'userid_level',
                 victimInstance.level)
        es.event('fire', 'gg_knife_steal')

    def gg_multi_level(self, attackerInstance, victimInstance):
        '''
        Usage:
            import es
            from gungame.core.players.shortcuts import Player
            from gungame.core.events import EventManager

            def gg_levelup(event_var):
                # Get the attacker's Player() instance
                aInstance = Player(event_var['attacker'])

                # Get the victim's Player() instance
                vInstance = Player(event_var['userid'])

                # Set the attacker's multilevel
                aInstance.multilevel += 1

                # Get the attacker's multilevel
                aMultiLevel = aInstance.multilevel

                # Get what multilevel the player needs to achieve
                neededMultiLevel = int(es.ServerVar('gg_multi_level'))

                # See if the attacker has achieved multilevel. If not, return.
                if aInstance.multilevel != int(es.ServerVar('gg_multi_level')):
                    return

                # Trigger the event "gg_knife_steal"
                EventManager().gg_multi_level(aInstance, vInstance)
        '''
        es.event('initialize', 'gg_multi_level')
        es.event('setint', 'gg_multi_level', 'userid', attacker)
        es.event('setint', 'gg_multi_level', 'leveler', attacker)
        es.event('fire', 'gg_multi_level')

    def remove_recent_winner(self):
        global recentWinner

        recentWinner = False
