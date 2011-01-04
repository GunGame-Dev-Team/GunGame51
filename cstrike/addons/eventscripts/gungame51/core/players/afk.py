# ../addons/eventscripts/gungame51/core/players/afk.py

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
from playerlib import getPlayer

# =============================================================================
# >> CLASSES
# =============================================================================
class AFK(object):
    def __init__(self, userid):
        self.userid = int(userid)
        self.total = None
        self.rounds = 0

    def __call__(self):
        return (self.total == self.calculate())

    def reset(self):
        '''Resets a players AFK math total.'''
        # Check the player exists
        if not es.exists('userid', self.userid):
            return

        # Update the AFK math total
        self.total = self.calculate()

    def calculate(self):
        # Check the player exists
        if not es.exists('userid', self.userid):
            return

        # Get the player's location
        x, y, z = es.getplayerlocation(self.userid)

        return int(x) + int(y) + int(es.getplayerprop(self.userid,
                   'CCSPlayer.m_angEyeAngles[0]')) + \
                    int(es.getplayerprop(self.userid, 'CCSPlayer.m_angEyeAngles[1]'))

    def isActive(self):
        '''
        Sets the player to a state that is NOT AFK.
        Only used when we know that the player is active and NOT AFK.

        Example:
            event player_jump
        '''
        # Make sure player is on a team
        if es.getplayerteam(self.userid) < 2:
            raise ValueError('Unable to make player active (%s): not on a team.' % self.userid)

        # Reset player math total
        self.total = 0
        self.afkrounds = 0

    def teleport(self, x, y, z, eyeangle0=0, eyeangle1=0):
        '''
        Teleport the player.

        Recalculates the player's location automatically for the scripter.
        '''
        # Make sure player is on a team
        if es.getplayerteam(self.userid) < 2:
            raise ValueError('Unable to teleport player (%s): not on a team.'
                %self.userid)

        # Make sure the player is alive
        if getPlayer(userid).isdead:
            raise ValueError('Unable to teleport player (%s): not alive.'
                %self.userid)

        # Set position
        es.server.queuecmd('es_xsetpos %d %s %s %s' % (self.userid, x, y, z))

        # Set eye angles
        if eyeangle0 != 0 or eyeangle1 != 0:
            es.server.queuecmd('es_xsetang %d %s %s' %(self.userid, eyeangle0,
                                                       eyeangle1))

        # Reset player AFK calculation
        gamethread.delayed(0.1, self.reset, ())

    def eyeangles(self, eyeAngle0=0, eyeAngle1=0):
        '''Sets a players view angle.'''
        # Make sure player is on a team
        if es.getplayerteam(self.userid) < 2:
            raise ValueError('Unable to set player angles (%s): not on a team'
                %self.userid)

        # Make sure player is alive
        if getPlayer(userid).isdead:
            raise ValueError('Unable to set player angles (%s): not alive.'
                %self.userid)

        # Set angles
        es.server.queuecmd('es_xsetang %d %s %s' %(self.userid, eyeangle0,
                                                   eyeangle1))

        # Reset player AFK calculation
        gamethread.delayed(0.1, self.reset, ())