# ../core/players/levels/levels.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# EventScripts Imports
import es as _es
import gamethread as _gamethread

# GunGame Imports
#   Player Module
from . import _PlayerMeta
from fields import IntegerField as _IntegerField
from fields import make_fields as _make_fields
#   Leaders Module
from gungame51.core.leaders import LeaderManager as _LeaderManager
#   Weapons Module
from gungame51.core.weapons.shortcuts import get_total_levels as _total_levels
#   Events Module
from gungame51.core.events import GG_LevelUp as _GG_LevelUp
from gungame51.core.events import GG_LevelDown as _GG_LevelDown
from gungame51.core.events import GG_Win as _GG_Win


# =============================================================================
# >> GLOBALS
# =============================================================================
_LEADERS = _LeaderManager()
recentWinner = False
gg_multi_round = _es.ServerVar('gg_multi_round')


# =============================================================================
# >> CLASSES
# =============================================================================
class PlayerLevels(_PlayerMeta):
    # Declare the default attribute fields
    _fields = _make_fields(_level=_IntegerField(min_value=1))

    def __init__(self, *args, **kwargs):
        self._level = 1

    # =========================================================================
    # Class Properties and Property Methods
    # =========================================================================
    def _get_level(self):
        return self._level

    def _set_level(self, value):
        if self.preventlevel():
            # Prevent player from leveling up?
            if self.preventlevel.levelup and value > self._level:
                return

            # Prevent player from leveling down?
            if self.preventlevel.leveldown and value < self._level:
                return

        # Set the attribute value
        self._level = value

        # Perform leader check
        _LEADERS.check(self)

    level = property(fget=_get_level, fset=_set_level)

    # =========================================================================
    # Methods
    # =========================================================================
    def levelup(self, levelsAwarded, victim=0, reason=''):
        """ Adds a declared number of levels to the attacker.

        Arguments:
            * levelsAwarded: (required)
                The number of levels to award to the attacker.
            * victim: (default of 0)
                The userid of the victim.
            * reason: (not required)
                The string reason for leveling up the attacker.

        """
        # Return false if we can't level up
        if self.preventlevel.levelup:
            return False

        # Calculate the new level
        newLevel = self.level + int(levelsAwarded)

        # TODO: Winner check would be good for the callback method of eventlib
        # See if we have a winner
        if newLevel > _total_levels():
            global recentWinner

            # If there was a recentWinner, stop here to prevent multiple wins
            if recentWinner:
                return False

            # Set recentWinner to True
            recentWinner = True

            # In 3 seconds, remove the recentWinner
            _gamethread.delayed(3, _remove_recent_winner, ())

            # If "gg_multi_round" is disabled
            if not int(gg_multi_round):
                # Set up the gg_win event
                gg_win = _GG_Win(attacker=self.userid, winner=self.userid,
                                 userid=victim, loser=victim, round=0)
            else:
                # If "gg_multi_round" is enabled
                from gungame51.gungame51 import RoundInfo
                # Set up the gg_win event
                gg_win = _GG_Win(attacker=self.userid, winner=self.userid,
                                 userid=victim, loser=victim,
                                 round=int(RoundInfo().remaining))
            # Fire the gg_win event
            return gg_win.fire()

        # Set the new level
        self.level = newLevel

        # Play the levelup sound
        self.playsound('levelup')

        # Reset multikill
        self.multikill = 0

        # Set up the gg_levelup event
        gg_levelup = _GG_LevelUp(attacker=self.userid, leveler=self.userid,
                                 userid=victim, old_level=self.level,
                                 new_level=newLevel, reason=reason)

        # Fire the gg_levelup event
        return gg_levelup.fire()

    def leveldown(self, levelsTaken, attacker=0, reason=''):
        """Removes a declared number of levels from the victim.

        Arguments:
            * levelsTaken: (required)
                The number of levels to take from to the victim.
            * attacker: (default of 0)
                The userid of the attacker.
            * reason: (not required)
                The string reason for leveling down the victim.

        """
        # Return false if we can't level down
        if self.preventlevel.leveldown:
            return False

        # Set old level and the new level
        oldLevel = self.level
        levelsTaken = int(levelsTaken)
        if (oldLevel - levelsTaken) > 0:
            self.level = oldLevel - levelsTaken
        else:
            self.level = 1

        # Reset multikill
        self.multikill = 0

        # Set up the gg_leveldown event
        gg_leveldown = _GG_LevelDown(attacker=attacker, leveler=self.userid,
                                     userid=self.userid, old_level=oldLevel,
                                     new_level=self.level, reason=reason)
        # Fire the gg_leveldown event
        return gg_leveldown.fire()


def _remove_recent_winner():
    global recentWinner
    recentWinner = False
