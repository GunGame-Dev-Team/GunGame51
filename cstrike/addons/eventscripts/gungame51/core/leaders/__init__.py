# ../cstrike/addons/eventscripts/gungame/core/leaders/__init__.py

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
from gungame51.core.players.shortcuts import Player
from gungame51.core.players.shortcuts import players
from gungame51.core.events.shortcuts import events

# =============================================================================
# >> CLASSES
# =============================================================================
class LeaderManager(object):
    '''
    Class designed to handle the GunGame leaders.
    '''
    # =========================================================================
    # >> LeaderManager() CLASS INITIALIZATION
    # =========================================================================
    def __init__(self):
        self.leaderlevel = 1
        self.current = []
        self.previous = []
        
    # =========================================================================
    # >> LeaderManager() CUSTOM CLASS METHODS
    # =========================================================================
    def add(self, userid):
        '''
        Adds a leader to the current leader list.
        
        Notes:
            * Automatically determines which method to use:
                - LeaderManager.addTie(userid)
                - LeaderManager.addNew(userid)
            * This method is recommended over the direct methods listed above.
        '''
        level = Player(userid).level
        if not level >= self.leaderlevel:
            raise ValueError('Unable to set "%s" as a current leader. '
                %userid + 'The leader level "%s" is not greater than or '
                %self.leaderlevel + 'equal to the player\'s level "%s".'
                %level)
        
        # Determine if this is a tied leader or new leader
        if level == self.leaderlevel:
            self.addTie(userid)
        else:
            self.setNew(userid)
    
    def addTie(self, userid):
        '''
        Adds a leader to the current leader list.
        
        Notes:
            * This should only be used when there is a tie for the leader.
            * If the player is a new leader, use the setNew() method.
            * Updates the current leaders list.
            * Sends all players a message about the newly tied leader.
            * Fires the GunGame event "gg_tied_leader".
        '''
        # Make sure that the player's level is equal to the leader level
        if not Player(userid).level == self.leaderlevel:
            raise ValueError('Unable to set "%s" as a current leader. '
                %userid + 'The leader level "%s" is not equal to '
                %self.leaderlevel + 'the player\'s level "%s".'
                %Player(userid).level)
        
        # Make sure the player is not a leader
        if self.isLeader(userid):
            raise ValueError('Unable to set "%s" as a current leader. '
                %userid + 'The userid "%s" is already a current leader.'
                %userid)
                
        # Add the userid to the current leaders list
        self.current.append(userid)
            
        '''
        # Tied leader messaging
        leaderCount = len(self.current)
        gungamePlayer = getPlayer(userid)
        if leaderCount == 2:
            saytext2('gungame', '#all', gungamePlayer.index, 'TiedLeader_Singular', {'player': gungamePlayer.name, 'level': self.leaderLevel}, False)
        else:
            saytext2('gungame', '#all', gungamePlayer.index, 'TiedLeader_Plural', {'count': leaderCount, 'player': gungamePlayer.name, 'level': self.leaderLevel}, False)
        '''
        
        # Fire gg_tied_leader
        events.gg_tied_leader(userid)
        
            
    def setNew(self, userid):
        '''
        Sets the current leader list as the new leader's userid.
        
        Notes:
            * Copies the contents of the "current" leaders list to the
              "previous" leaders list.
            * Updates the current leaders list.
            * Updates the leader level attribute.
            * Sends all players a message about the new leader.
            * Fires the GunGame event "gg_new_leader".
        '''
        # Make sure that the player's level is higher than the leader level
        if not Player(userid).level > self.leaderlevel:
            raise ValueError('Unable to set "%s" as a new leader. '
                %userid + 'The leader level "%s" is higher than '
                %self.leaderlevel + 'the player\'s level "%s".'
                %Player(userid).level)
        
        # Set previous leaders list
        self.previous = self.current[:]
        
        # Set current leaders list
        self.current = [userid]
        
        # Set leader level
        self.leaderlevel = Player(userid).level
        
        '''
        # Message about new leader
        gungamePlayer = getPlayer(userid)
        saytext2('gungame', '#all', gungamePlayer.index, 'NewLeader', {'player': gungamePlayer.name, 'level': self.leaderLevel}, False)
        '''
        
        # Fire gg_new_leader
        events.gg_new_leader(userid)
        
    def remove(self, userid):
        '''
        Removes a player from the current leaders list.
        
        Notes:
            * Copies the contents of the "current" leaders list to the
              "previous" leaders list.
            * Updates the current leaders list.
            * Fires the GunGame event "gg_leader_lostlevel".
        '''
        # Make sure the player is a leader
        if not self.isLeader(userid):
            raise ValueError('Unable to remove "%s" from the current leaders. '
                %userid + 'The userid "%s" is not a current leader.' %userid)
            
        # Set previous leaders
        self.previous = self.current[:]
        
        # Remove the userid from the current leaders list
        self.current.remove(userid)
        
        # Check to see if we need to find new leaders
        if not len(self.current):
            self.refresh()
            
        # Fire gg_leader_lostlevel
        events.gg_leader_lostlevel(userid)
        
    def reset(self):
        '''
        Resets the LeaderManager for a clean start of GunGame.
        '''
        # Call the __init__ to reset the LeaderManager instance
        super(LeaderManager, self).__init__()
        
    def cleanup(self, listname):
        '''
        Removes disconnected userids from the list.
        '''
        if not listname in ['current', 'previous']:
            raise AttributeError('LevelManager has no attribute: "%s".'
                %listname)
                
        leaderList = getattr(self, listname)
        for userid in leaderList[:]:
            if not es.exists('userid', userid):
                leaderList.remove(userid)
                
        return leaderList[:]
        
    def isLeader(self, userid):
        '''
        Returns True/False if the userid is a current leader.
        '''
        return (userid in self.current)
        
    def refresh(self):
        '''
        Repopulates the current leaders list from the players available.
        
        Notes:
            * This method is intended to be used when the current leaders list
              becomes empty and needs to be repopulated while in the middle of
              a GunGame round.
              - This will typically be called during the GunGame event
                "gg_leveldown".
        '''
        # Reset the leader level
        self.leaderlevel = 1
        
        # Reset the current leaders list
        self.current = []
        
        # Loop through the players
        for userid in players:
            # Is the player on the server?
            if not es.exists('userid', userid):
                continue
                
            # Get player info
            level = Player(userid).level
            
            # Create new leader variable and set new level
            if level > self.leaderlevel:
                self.current = [userid]
                self.leaderlevel = level
            
            # Another leader
            elif level == self.leaderlevel:
                self.leaders.append(userid)
        
        # Set old leaders, if they have changed
        if self.current[:] != self.previous[:]:
            self.previous = self.current[:]
        
        # 1 new leader
        if len(self.current) == 1:
            '''
            # Message about new leader
            saytext2('gungame', '#all', getPlayer(self.current[0])['index'], 'NewLeader', {'player': getPlayer(self.current[0])['name'], 'level': self.leaderlevel}, False)
            '''
            # Fire gg_new_leader
            events.gg_new_leader(userid)
        
    # =========================================================================
    # LeaderManager() STATIC CLASS METHODS
    # =========================================================================
        
leaders = LeaderManager()