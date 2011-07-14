# ../core/leaders/__init__.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports

# EventScripts Imports
import es

# GunGame Imports
from gungame51.core.events import GG_Leader_Disconnect
from gungame51.core.events import GG_New_Leader
from gungame51.core.events import GG_Leader_LostLevel
from gungame51.core.events import GG_Tied_Leader


# =============================================================================
# >> CLASSES
# =============================================================================
class LeaderManager(object):
    """Class that automatically manages leaders."""
    def __new__(cls, *p, **k):
        if not '_the_instance' in cls.__dict__:
            cls._the_instance = object.__new__(cls)
            # Create the instance variables
            cls._the_instance.previous = []
            cls._the_instance.useridlist = []
            cls._the_instance.levellist = []
        return cls._the_instance

    # =========================================================================
    # >> LeaderManager() READ-ONLY PROPERTIES
    # =========================================================================
    @property
    def leaderlevel(self):
        """Read-only property that returns the highest level from the list of
        players.

        """
        # Make sure there are levels in the level list
        if self.levellist:
            # Return the highest level in the list
            return max(self.levellist)

        # Return 1 as the highest level if no levels are in the level list
        return 1

    @property
    def current(self):
        """Read-only property that returns a list of current leaders' userids.

        """
        return [x for x in self.useridlist \
            if self.levellist[self.useridlist.index(x)] == self.leaderlevel]

    # =========================================================================
    # >> LeaderManager() BASE METHODS
    # =========================================================================
    def check(self, ggPlayer):
        """Checks to see if the leader manager needs to update the leader
        status.

        """

        userid = ggPlayer.userid
        level = ggPlayer.level

        # Is this a current leader?
        if self.is_leader(userid):
            # Same leader
            if level > self.leaderlevel:
                self.new_or_same_leader(ggPlayer, True)

            # Lost leader
            elif level < self.leaderlevel:
                self.lost_leader(ggPlayer)

        # Not a current leader
        else:
            # Tied leader
            # Check leader to make sure leader level is > 1
            if level == self.leaderlevel and self.leaderlevel != 1:
                self.tied_leader(ggPlayer)

            # New leader
            elif level > self.leaderlevel:
                self.new_or_same_leader(ggPlayer)

            # NO LEADER-RELATION
            else:
                self.__update_level(userid, int(level))

    def __update_level(self, userid, level):
        """Adds userids and levels to the appropriate lists."""

        # Do not update the level if leader level and player level are both 1
        if self.leaderlevel == 1 and level == 1:
            return

        # Retrieve the index of the userid
        index = self.__find_index(userid)

        # Does the userid exist in the userid list?
        if index != None:
            # Update the userid with the appropriate level
            self.levellist[index] = level

        # The userid does not exist
        else:
            # Append the userid and level
            self.useridlist.append(userid)
            self.levellist.append(level)

    def __find_index(self, userid):
        """Finds the index of the userid in both the useridlist and the
        levellist.

        """

        # Does the userid exist in the userid list?
        if userid in self.useridlist:
            # Return the index
            return self.useridlist.index(userid)

        return None

    def reset(self):
        """Resets the LeaderManager for a clean start of GunGame."""
        # Call the __init__ to reset the LeaderManager instance
        self.__init__()

    def is_leader(self, userid):
        return (userid in self.current)

    # =========================================================================
    # LeaderManager() STATUS UPDATE METHODS
    # =========================================================================
    def tied_leader(self, ggPlayer, event=True):
        """Adds a leader to the current leader list.

        Notes:
            * This should only be used when there is a tie for the leader.
            * If the player is a new leader, use the setNew() method.
            * Updates the current leaders list.
            * Sends all players a message about the newly tied leader.
            * Fires the GunGame event "gg_tied_leader".

        """
        # Set the previous leaders list
        self.previous = self.current[:]

        # Update the current userid
        self.__update_level(int(ggPlayer.userid), int(ggPlayer.level))

        if event:
            # Set up the gg_tied_leader event
            new_leaders, old_leaders = self._get_leader_strings()

            gg_tied_leader = GG_Tied_Leader(userid=ggPlayer.userid,
                                            leveler=ggPlayer.userid,
                                            leaders=new_leaders,
                                            old_leaders=old_leaders,
                                            leader_level=self.leaderlevel)
            # Fire gg_tied_leader
            return gg_tied_leader.fire()

    def lost_leader(self, ggPlayer, event=True):
        """Removes a player from the current leaders list.

        Notes:
            * Copies the contents of the "current" leaders list to the
              "previous" leaders list.
            * Fires the GunGame event "gg_leader_lostlevel".

        """
        # Make sure the player is a leader
        if not self.is_leader(ggPlayer.userid):
            raise ValueError('Unable to remove "%s" from the current leaders. '
                % userid + 'The userid "%s" is not a current leader.' % userid)

        # Set previous leaders
        self.previous = self.current[:]

        # Update the current userid
        self.__update_level(int(ggPlayer.userid), int(ggPlayer.level))

        if event:
            # Set up the gg_leader_lostlevel event
            new_leaders, old_leaders = self._get_leader_strings()

            leaderLevel = self.leaderlevel

            gg_leader_lostlevel = GG_Leader_LostLevel(userid=ggPlayer.userid,
                                                      leveler=ggPlayer.userid,
                                                      leaders=new_leaders,
                                                      old_leaders=old_leaders,
                                                      leader_level=leaderLevel)
            # Fire gg_leader_lostlevel
            gg_leader_lostlevel.fire()

    def new_or_same_leader(self, ggPlayer, event=True):
        """Sets the current leader list as the new leader's userid.

        Notes:
            * Copies the contents of the "current" leaders list to the
              "previous" leaders list.
            * Updates the current leaders list.
            * Updates the leader level attribute.
            * Sends all players a message about the new leader.
            * Fires the GunGame event "gg_new_leader".

        """
        # Set the previous leaders list
        self.previous = self.current[:]

        # Update the current userid
        self.__update_level(int(ggPlayer.userid), int(ggPlayer.level))

        if not event:
            return

        # Set up the gg_new_leader event
        new_leaders, old_leaders = self._get_leader_strings()

        gg_new_leader = GG_New_Leader(userid=ggPlayer.userid,
                                      leveler=ggPlayer.userid,
                                      leaders=new_leaders,
                                      old_leaders=old_leaders,
                                      leader_level=self.leaderlevel)
        # Fire the "gg_new_leader" event
        return gg_new_leader.fire()

    def disconnected_leader(self, userid):
        """Handles the disconnection of players."""
        userid = int(userid)

        # Make sure the userid no longer exists on the server
        if es.exists("userid", userid):
            return

        # Make sure this player is a leader
        if not self.is_leader(userid):
            # Remove the userid
            self.__remove_userid(userid)

            return

        # Remove the userid
        self.__remove_userid(userid)

        # Set up the gg_leader_disconnect event
        new_leaders, old_leaders = self._get_leader_strings()

        leaderLevel = self.leaderlevel

        gg_leader_disconnect = GG_Leader_Disconnect(userid=userid,
                                                    leaders=new_leaders,
                                                    old_leaders=old_leaders,
                                                    leader_level=leaderLevel)
        # Fire the "gg_leader_disconnect" event
        return gg_leader_disconnect.fire()

    def __remove_userid(self, userid):
        """Removes all relations of the userid from the LeaderManager."""
        # Retrieve the index of the userid
        index = self.__find_index(userid)

        # Make sure that the index exists
        if index != None:
            # Remove the index from the "useridlist" and "levellist"
            del self.useridlist[index]
            del self.levellist[index]

        # See if the userid is in the previous leaders list
        if userid in self.previous:
            # Remove the userid from the previous leader list
            del self.previous[self.previous.index(userid)]

    def _reset(self):
        """Resets the leader lists."""
        del self.useridlist[:]
        del self.levellist[:]
        del self.previous[:]

    def _get_leader_strings(self):
        new_leaders = ",".join([str(x) for x in self.current[:]])
        old_leaders = ",".join([str(x) for x in self.previous[:]])

        new_leaders = new_leaders if new_leaders else "None"
        old_leaders = old_leaders if old_leaders else "None"

        return (new_leaders, old_leaders)
