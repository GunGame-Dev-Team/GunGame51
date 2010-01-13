# ../addons/eventscripts/gungame/core/leaders/__init__.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
# Python Imports

# EventScripts Imports
import es

# GunGame Imports
from gungame51.core.events.shortcuts import EventManager
from gungame51.core.messaging.shortcuts import saytext2

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
        # DEV NOTE: "if index" will not work due to returning an index of 0
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

        # Tied leader messaging
        leaderCount = len(self.current)

        if leaderCount == 2:
            saytext2('#human', ggPlayer.index, 'TiedLeader_Singular',
                {'player': es.getplayername(ggPlayer.userid),
                'level': self.leaderlevel}, False)
        else:
            saytext2('#human', ggPlayer.index, 'TiedLeader_Plural',
                {'count': leaderCount,
                'player': es.getplayername(ggPlayer.userid),
                'level': self.leaderlevel}, False)

        if event:
            # Fire gg_tied_leader
            EventManager().gg_tied_leader(ggPlayer.userid)
    
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
                %userid + 'The userid "%s" is not a current leader.' %userid)

        # Set previous leaders
        self.previous = self.current[:]

        # Update the current userid
        self.__update_level(int(ggPlayer.userid), int(ggPlayer.level))

        if event:
            # Fire gg_leader_lostlevel
            EventManager().gg_leader_lostlevel(ggPlayer.userid)

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

        # Message about new leader
        saytext2('#human', ggPlayer.index, 'NewLeader',
            {'player': es.getplayername(ggPlayer.userid),
            'level': self.leaderlevel}, False)

        if not event:
            return

        # Fire the "gg_new_leader" event
        EventManager().gg_new_leader(ggPlayer.userid)

    def disconnected_leader(self, userid):
        """Handles the disconnection of players."""
        userid = int(userid)

        # Make sure the userid no longer exists on the server
        if es.exists(userid):
            return

        # Make sure this player is a leader
        if not self.is_leader(userid):
            # Remove the userid
            self.__remove_userid(userid)

            return

        # Set up a variable for triggering a new leader message
        newLeader = False

        # See if we need to message a new leader
        if len(self.current) == 1:
            newLeader = True

        # Remove the userid
        self.__remove_userid(userid)
        
        # Trigger new leader messaging if a single leader is found
        if newLeader and len(self.current) == 1:
            from gungame51.core.players.shortcuts import Player
            # Message about new leader 
            saytext2('#human', Player(userid).index, 'NewLeader',
                {'player': es.getplayername(userid),
                'level': self.leaderlevel}, False)

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