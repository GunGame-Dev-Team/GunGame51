# ../core/leaders/__init__.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame Imports
#   Events
from gungame51.core.events import GG_Leader_Disconnect
from gungame51.core.events import GG_New_Leader
from gungame51.core.events import GG_Leader_LostLevel
from gungame51.core.events import GG_Tied_Leader


# =============================================================================
# >> CLASSES
# =============================================================================
class LeaderManager(dict):
    """Dictionary-based class that stores player levels for keeping track of
    leaders.

    """
    def __new__(cls, *p, **k):
        # There can be only one (singleton)
        if not '_the_instance' in cls.__dict__:
            cls._the_instance = dict.__new__(cls)
        return cls._the_instance

    @property
    def leaderlevel(self):
        """Read-only property that returns the highest level from the
        dictionary of players.

        """
        return max(self.values() + [1])

    @property
    def current(self):
        """Read-only property that returns a list of current leaders' userids.

        """
        leaderlevel = self.leaderlevel
        return [x for x in self.keys() if self[x] == leaderlevel]

    # =========================================================================
    # Public Methods
    # =========================================================================
    def check(self, ggPlayer):
        """Checks to see if the leader manager needs to update the leader
        status.

        """
        userid = ggPlayer.userid
        level = ggPlayer.level
        leaderlevel = self.leaderlevel

        # Is this a current leader?
        if self.is_leader(userid):
            # Same leader
            if level > leaderlevel:
                self._new_or_same_leader(ggPlayer)

            # Lost leader
            elif level < leaderlevel:
                self._lost_leader(ggPlayer)

        # Not a current leader
        else:
            # Tied leader
            # Check leader to make sure leader level is > 1
            if level == leaderlevel and leaderlevel != 1:
                self._tied_leader(ggPlayer)

            # New leader
            elif level > leaderlevel:
                self._new_or_same_leader(ggPlayer)

            # NO LEADER-RELATION
            else:
                self._update_level(userid, int(level))

    def is_leader(self, userid):
        """Checks to see if the userid is a current leader."""
        return userid in self.current

    def reset(self):
        """Resets the LeaderManager for a clean start of GunGame."""
        # Clear the LeaderManager dictionary
        self.clear()

    # =========================================================================
    # Private Methods
    # =========================================================================
    def _update_level(self, userid, level):
        """Adds userid and level to the dictionary."""
        # Do not update the level if leader level and player level are both 1
        if self.leaderlevel == 1 and level == 1:
            return

        self[userid] = level

    def _tied_leader(self, ggPlayer):
        """Adds a leader to the current leader list."""

        # Store the old leaders
        old_leaders = self._get_leader_string()

        # Update the current userid
        self._update_level(ggPlayer.userid, ggPlayer.level)

        # Set up the gg_tied_leader event
        new_leaders = self._get_leader_string()
        gg_tied_leader = GG_Tied_Leader(userid=ggPlayer.userid,
                                        leveler=ggPlayer.userid,
                                        leaders=new_leaders,
                                        old_leaders=old_leaders,
                                        leader_level=self.leaderlevel)
        # Fire gg_tied_leader
        return gg_tied_leader.fire()

    def _lost_leader(self, ggPlayer):
        """Removes a player from the current leaders list."""
        # Make sure the player is a leader
        if not self.is_leader(ggPlayer.userid):
            raise ValueError('Unable to remove "%s" from the current leaders. '
                % userid + 'The userid "%s" is not a current leader.' % userid)

        # Store the old leaders
        old_leaders = self._get_leader_string()

        # Update the current userid
        self._update_level(ggPlayer.userid, ggPlayer.level)

        # Set up the gg_leader_lostlevel event
        new_leaders = self._get_leader_string()
        leaderLevel = self.leaderlevel
        gg_leader_lostlevel = GG_Leader_LostLevel(userid=ggPlayer.userid,
                                                  leveler=ggPlayer.userid,
                                                  leaders=new_leaders,
                                                  old_leaders=old_leaders,
                                                  leader_level=leaderLevel)
        # Fire gg_leader_lostlevel
        gg_leader_lostlevel.fire()

    def _new_or_same_leader(self, ggPlayer):
        """Sets the current leader list as the new leader's userid."""

        # Store the old leaders
        old_leaders = self._get_leader_string()

        # Update the current userid
        self._update_level(ggPlayer.userid, ggPlayer.level)

        # Set up the gg_new_leader event
        new_leaders = self._get_leader_string()
        gg_new_leader = GG_New_Leader(userid=ggPlayer.userid,
                                      leveler=ggPlayer.userid,
                                      leaders=new_leaders,
                                      old_leaders=old_leaders,
                                      leader_level=self.leaderlevel)
        # Fire the "gg_new_leader" event
        return gg_new_leader.fire()

    def disconnected_leader(self, userid):
        """Handles the disconnection of players."""
        import es
        # Make sure the userid no longer exists on the server
        if es.exists("userid", userid):
            return

        # Make sure this player is a leader
        if not self.is_leader(userid):
            self._remove_userid(userid)
            return

        # Store the old leaders
        old_leaders = self._get_leader_string()

        # Remove the userid
        self._remove_userid(userid)

        # Set up the gg_leader_disconnect event
        new_leaders = self._get_leader_string()
        leaderLevel = self.leaderlevel
        gg_leader_disconnect = GG_Leader_Disconnect(userid=userid,
                                                    leaders=new_leaders,
                                                    old_leaders=old_leaders,
                                                    leader_level=leaderLevel)
        # Fire the "gg_leader_disconnect" event
        return gg_leader_disconnect.fire()

    def _remove_userid(self, userid):
        """Removes all relations of the userid from the LeaderManager
        dictionary.

        """
        # Make sure that the userid exists
        if userid in self:
            del self[userid]

    def _get_leader_string(self):
        """Returns a comma separated value string of the current leaders'
        userids or a string of None if no leaders.

        """
        new_leaders = ",".join([str(x) for x in self.current[:]])
        new_leaders = new_leaders if new_leaders else "None"
        return new_leaders
