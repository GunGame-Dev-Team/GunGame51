# ../core/players/__init__.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
from random import choice
from random import randint

# EventScripts Imports
import es
import gamethread
from playerlib import uniqueid
from playerlib import getPlayer
from usermsg import showVGUIPanel

# SPE Imports
import spe

# GunGame Imports
from gungame51.core.weapons.shortcuts import get_total_levels
from gungame51.core import getOS
from gungame51.core import GunGameError
from gungame51.core.sound import SoundPack
from gungame51.core.leaders.shortcuts import LeaderManager
from gungame51.core.sql import Database
from gungame51.core.sql.shortcuts import insert_winner
from gungame51.core.sql.shortcuts import update_winner
from afk import AFK
from gungame51.core.events import GG_LevelUp
from gungame51.core.events import GG_LevelDown
from gungame51.core.events import GG_Win
from extended_player import *

# =============================================================================
# >> GLOBALS
# =============================================================================
gg_multi_round = es.ServerVar('gg_multi_round')
gg_soundpack = es.ServerVar('gg_soundpack')
recentWinner = False


# =============================================================================
# >> CLASS HELPER FUNCTION
# =============================================================================
def prop(fcn):
    return property(**fcn())


# =============================================================================
# >> CLASSES
# =============================================================================
class CustomAttributeCallbacks(dict):
    '''
    This class is designed to store callback functions for custom attributes
    added to GunGame via a subaddon.
    '''
    def __new__(cls, *p, **k):
        if not '_the_instance' in cls.__dict__:
            cls._the_instance = dict.__new__(cls)
        return cls._the_instance

    def add(self, attribute, function, addon):
        '''
        Adds a callback to execute when a previously created attribute is set
        via the BasePlayer class __setitem__ or __setattr__ methods.

        Note:
            Do not raise errors for GunGame attributes.
        '''
        # Make sure that the function is callable
        if not callable(function):
            raise AttributeError('Callback "%s" is not callable.' % function)

        if not attribute in self:
            self[attribute] = {}

        # Add or update the attribute callback
        self[attribute].update({addon: function})

    def remove(self, attribute, addon):
        '''
        Removes a callback to execute when a previously created attribute is
        set via the BasePlayer class' __getitem__ or __getattr__ methods.

        Note:
            No exceptions are raised if you attempt to delete a non-existant
            callback.
        '''
        # Make sure the attribute callback exists
        if not attribute in self:
            return

        # Make sure that the addon exists in the attribute
        if not addon in self[attribute]:
            return

        # Delete the attribtue callback
        del self[attribute][addon]

        # See if the attribute is now empty
        if not self[attribute]:
            del self[attribute]


class PreventLevel(list):
    '''
    Class designed to handle the PreventLevel player attribute. This class is a
    list type, which allows us to potentially catch errors such as duplicate
    entries of addons in the preventlevel list, as well as preventing errors
    when scripters attempt to remove an entry that does not exist.
    '''
    # =========================================================================
    # >> PreventLevel() CUSTOM CLASS METHODS
    # =========================================================================
    def append(self, name):
        if name not in self:
            list.append(self, name)

    def extend(self, names):
        for name in names:
            if name in self:
                continue

            list.append(self, name)

    def remove(self, name):
        if name in self:
            list.remove(self, name)


class BasePlayer(PlayerMessaging, PlayerWeapons, PlayerSounds):
    # =========================================================================
    # >> BasePlayer() CLASS INITIALIZATION
    # =========================================================================
    def __new__(cls, userid):
        self = object.__new__(cls, userid)
        self.userid = int(userid)
        self.steamid = uniqueid(self.userid, 1)
        self.afk = AFK(self.userid)
        self.index = int(getPlayer(str(self.userid)).index)
        return self

    def __init__(self, userid):
        self.preventlevel = PreventLevel()
        self.preventlevelup = PreventLevel()
        self.preventleveldown = PreventLevel()
        self._level = 1
        self.multikill = 0
        self.stripexceptions = []
        self.soundpack = SoundPack(str(gg_soundpack))

    # =========================================================================
    # >> BasePlayer() CLASS ATTRIBUTE METHODS
    # =========================================================================
    @property
    def weapon(self):
        '''
        Return the weapon name
        '''
        return self.get_weapon()

    @prop
    def level():
        def fget(self):
            return self._level

        def fset(self, value):
            if not self.preventlevel:

                # Prevent player from leveling up?
                if self.preventlevelup and value > self._level:
                    return

                # Prevent player from leveling down?
                if self.preventleveldown and value < self._level:
                    return

                # Set the attribute value
                self._level = value
                LeaderManager().check(self)
        # Required for @prop
        return locals()

    @prop
    def team():
        '''
        Player(userid).team is just the same as es.getplayerteam(userid)
        Player(userid).team = 1 move player to spec
        Player(userid).team = 2 move player to terrorist
        Player(userid).team = 3 move player to counter-terrorist
        '''
        def fget(self):
            return es.getplayerteam(self.userid)

        def fset(self, value):
            if not es.exists('userid', self.userid):
                raise ValueError('userid (%s) doesn\'t exist.' % self.userid)
            try:
                value = int(value)
            except (TypeError, ValueError):
                raise ValueError('"%s" is an invalid team' % value)

            # Is the value in range ?
            if value not in xrange(1, 3):
                raise ValueError('"%s" is an invalid teamid' % value)

            # Retrieve a playerlib instance
            pPlayer = getPlayer(self.userid)

            # Make sure we are not moving the player to the same team
            if pPlayer.teamid == value:
                return

            # Change the team
            spe.switchTeam(self.userid, value)

            # No model change needed if going to spectator
            if value == 1:
                return

            # Change to Terrorist Models
            if value == 2:
                pPlayer.model = 'player/%s' % choice(('t_arctic', 't_guerilla',
                                                      't_leet', 't_phoenix'))
            # Change to Counter-Terrorist Models
            else:
                pPlayer.model = 'player/%s' % choice(('ct_gign', 'ct_gsg9',
                                                      'ct_sas', 'ct_urban'))
        # Required for @prop
        return locals()

    @prop
    def wins():
        '''
        Player(userid).wins returns the amount of wins a player has
            * If they are not in the DB it will return 0

        Player(userid).wins += 1 The prefered method of adding a win

        Player(userid).wins = # You may also change the wins setting to a
          value of your choice, although this method should only be used for
          internal ussage.
        '''
        def fget(self):
            # Query the wins database
            winsQuery = Database().select('gg_wins', 'wins', 'where uniqueid' +
                                          ' = "%s"' % self.steamid)
            if winsQuery:
                return int(winsQuery)
            return 0

        def fset(self, value):
            # Bots can't win
            if es.isbot(self.userid):
                return

            # We using a int?
            try:
                value = int(value)
            except (ValueError, TypeError):
                raise ValueError('wins has to be a int value, you passed ' +
                                 '"%s"' % value)

            # Has won before
            if self.wins:
                update_winner('wins', value, uniqueid=self.steamid)
            # New entry
            else:
                name = es.getplayername(self.userid)
                if not name:
                    name = "unnamed"
                insert_winner(name, self.steamid, value)

        # Required for @prop
        return locals()

    def __setattr__(self, name, value):
        # First, we execute the custom attribute callbacks
        if name in CustomAttributeCallbacks():
            for function in CustomAttributeCallbacks()[name].values():
                function(name, value, self)

        # Set the attribute value
        object.__setattr__(self, name, value)

    def __getattr__(self, name):
        # Return the attribute value
        return object.__getattribute__(self, name)

    def __delattr__(self, name):
        # Make sure we don't try to delete required GunGame attributes
        if name in ('userid', 'level', 'preventlevel', 'steamid', 'soundpack',
                    'stripexceptions', 'multikill', 'wins', 'team', 'name',
                    'index', 'preventleveldown', 'preventlevelup', 'afk'):
            raise AttributeError('Unable to delete attribute "%s". ' % name +
                    'This is a required attribute for GunGame.')

        # Remove this attribute from the custom attribute callbacks, if any
        if name in CustomAttributeCallbacks():
            del CustomAttributeCallbacks()[name]

        # Delete the attribute only if it exists
        #   (we don't want to raise errors)
        if hasattr(self, name):
            object.__delattr__(self, name)

    def __setitem__(self, name, value):
        # Forward to __setattr__
        self.__setattr__(name, value)

    def __getitem__(self, name):
        # Return using __getattr__
        return self.__getattr__(name)

    def __delitem__(self, name):
        # Forward to __delattr__
        self.__delattr__(name)

    # =========================================================================
    # >> BasePlayer() LEVELING CLASS METHODS
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
        if self.preventlevel or self.preventlevelup:
            return False

        # Calculate the new level
        newLevel = self.level + int(levelsAwarded)

        # TODO: Winner check would be good for the callback method of eventlib
        # See if we have a winner
        if newLevel > get_total_levels():
            global recentWinner

            # If there was a recentWinner, stop here to prevent multiple wins
            if recentWinner:
                return False

            # Set recentWinner to True
            recentWinner = True

            # In 3 seconds, remove the recentWinner
            gamethread.delayed(3, remove_recent_winner, ())


            # If "gg_multi_round" is disabled
            if not int(gg_multi_round):
                # Set up the gg_win event
                gg_win = GG_Win(attacker=self.userid, winner=self.userid,
                                userid=victim, loser=victim, round=0)
            else:
                # If "gg_multi_round" is enabled
                from gungame51.gungame51 import RoundInfo
                # Set up the gg_win event
                gg_win = GG_Win(attacker=self.userid, winner=self.userid,
                                userid=victim, loser=victim,
                                round=int(RoundInfo().remaining))
            # Fire the gg_win event
            return gg_win.fire()

        # Set the new level
        self.level = newLevel

        # Reset multikill
        self.multikill = 0

        # Set up the gg_levelup event
        gg_levelup = GG_LevelUp(attacker=self.userid, leveler=self.userid,
                                userid=victim, old_level=self.level,
                                new_level=newLevel, reason=reason)

        # Fire the gg_levelup event
        return gg_levelup.fire()

    def leveldown(self, levelsTaken, attacker=0, reason=''):
        '''
        Removes a declared number of levels from the victim.

        Arguments:
            * levelsTaken: (required)
                The number of levels to take from to the victim.
            * attacker: (default of 0)
                The userid of the attacker.
            * reason: (not required)
                The string reason for leveling down the victim.
        '''
        # Return false if we can't level down
        if self.preventlevel or self.preventleveldown:
            return False

        # Make sure the attacker is an int
        attacker = int(attacker)

        # Set old level and the new level
        oldLevel = self.level
        if (oldLevel - int(levelsTaken)) > 0:
            self.level = oldLevel - int(levelsTaken)
        else:
            self.level = 1

        # Reset multikill
        self.multikill = 0

        # Set up the gg_leveldown event
        gg_leveldown = GG_LevelDown(attacker=attacker, leveler=self.userid,
                                    userid=self.userid, old_level=oldLevel,
                                    new_level=self.level, reason=reason)
        # Fire the gg_leveldown event
        return gg_leveldown.fire()

    # =========================================================================
    # >> BasePlayer() MISCELLANEOUS CLASS METHODS
    # =========================================================================
    def respawn(self, force=False):
        '''Respawns the player.'''
        # Player on server ?
        if not es.exists('userid', self.userid):
            return

        # Player in spec or unassigned ?
        if self.team < 2:
            return

        # Player alive? (require force)
        if not getPlayer(self.userid).isdead and not force:
            return

        spe.respawn(self.userid)

    # =========================================================================
    # >> Winner's Database methods
    # =========================================================================
    def database_update(self):
        '''
        Updates the time and the player's name in the database
        '''
        if self.wins:
            update_winner(('name', 'timestamp'), (es.getplayername(
                self.userid), 'strftime("%s","now")'), uniqueid=self.steamid)


class PlayerManager(dict):
    '''
    A class-based dictionary to contain instances of BasePlayer.

    Note:
        This class is meant for private use.
    '''
    def __new__(cls, *p, **k):
        if not '_the_instance' in cls.__dict__:
            cls._the_instance = dict.__new__(cls)
        return cls._the_instance

    # =========================================================================
    # >> PlayerManager() CLASS ATTRIBUTE METHODS
    # =========================================================================
    def __getitem__(self, userid):
        '''
        When we get an item in the dictionary BasePlayer is instantiated if it
        hasn't been already.
        '''
        userid = int(userid)

        # Do we have an instance for this userid?
        if userid not in self:
            # Does the userid exist on the server?
            if not es.exists("userid", userid):
                # Without a way to find the uniqueid, the is no legitimate way
                # to see if the player has played previously. Nor is there any
                # reason to create a "junk" instance for this player.
                raise ValueError('Unable to retrieve or create a player' +
                    ' instance for userid "%s".' % userid)

            # Get the uniqueid
            steamid = uniqueid(userid, 1)

            # Search for the player's uniqueid to see if they played previously
            # in this round. Do so by iterating through all steamids in this
            # dictionary via list comprehension. If a match is found, add the
            # player instance to the list. Otherwise, the list will be empty.
            list_check = [self[x] for x in self.copy() \
                if self[x].steamid == steamid]

            # The list is empty - no player was found
            if not list_check:
                # Create a new instance
                self[userid] = BasePlayer(userid)

            # A previous BasePlayer instance was found
            else:
                # Copy the BasePlayer() instance to the current userid
                self[userid] = list_check.pop()

                # Delete the old BasePlayer() instance
                del self[self[userid].userid]

                # Set the BasePlayer() instance userid to the current
                self[userid].userid = userid

                # Set the BasePlayer() instance index to the current
                self[userid].index = int(getPlayer(str(userid)).index)

                # Set the BasePlayer() .AFK() instance userid
                self[userid].afk.userid = userid

        # We don't want to call our __getitem__ again
        return super(PlayerManager, self).__getitem__(userid)

    def clear(self):
        '''
        Clear the player dictionary to start fresh with a clean slate.
        '''
        super(PlayerManager, self).clear()

    def remove_old(self):
        useridList = es.getUseridList()

        # For all userids
        for userid in self.copy():
            # If the userid is on the server, stop here
            if userid in useridList:
                continue

            # If the user is no longer in the server, remove their instance
            del self[userid]

    def reset(self, userid=None):
        # If a single userid was implemented, reset them
        if userid:
            # If the userid is not int he player manager, stop here
            if not userid in self:
                return

            userid = int(userid)
            self[userid].__init__(userid)
            return

        # Reset all userids
        for userid in self:
            self[userid].__init__(userid)


class Player(PlayerManager):
    """Redirects to the PlayerManager instance for ease of use"""
    # =========================================================================
    # >> Player() CLASS INITIALIZATION
    # =========================================================================
    def __new__(cls, userid):
        return PlayerManager().__getitem__(userid)

    # =========================================================================
    # BasePlayer() STATIC CLASS METHODS
    # =========================================================================
    @staticmethod
    def add_attribute_callback(attribute, function, addon):
        '''
        Adds a callback function when an attribute is set using the class-
        based dictionary CustomAttributeCallbacks. The callback function
        must have 2 arguments declared. The first argument will be the
        actual name of the attribute. The second argument will be the value
        that it was set to.

        Notes:
            * If an error is raised in your callback, the value will not be
              set.
            * You can set callbacks before you set the custom attribute on the
              player instances.
            * The intention of this method is to be able to check the value of
              custom attributes, and raise errors if they are not within
              certain ranges/specifications.

        Usage:
            Player.add_attribute_callback('attributeName', callbackFunction,
                                        'gg_addon_name')

            def callbackFunction(name_of_the_attribute, value_to_be_checked):
                if name_of_the_attribute == 'attributeName':
                    if value_to_be_checked > 0 and value_to_be_checked < 10:
                        pass
                    else:
                        raise ValueError('Value must be between 1 and 10!')
        '''
        # Add the attribute callback to the CustomAttributeCallbacks instance
        CustomAttributeCallbacks().add(attribute, function, addon)

    @staticmethod
    def remove_attribute_callback(attribute):
        '''
        Removes a callback function that is called when a named attribute is
        set using the class-based dictionary CustomAttributeCallbacks.

        Note:
            Attempting to remove a non-existant attribute callback will not
            raise an exception.

        Usage:
            Player.remove_attribute_callback('attributeName')
        '''
        # Remove the callback from the CustomAttributeCallbacks instance
        CustomAttributeCallbacks().remove(attribute)

    @staticmethod
    def remove_callbacks_for_addon(addon):
        '''
        Removes all attribute callbacks from the class-based dictionary
        CustomAttributeCallBacks that have been associated with the named
        addon.

        Usage:
            Player.remove_callbacks_for_addon('gg_addon_name')

        Note:
            Attempting to remove attributes from an addon that does not exist
            or if no attributes exist that are associated with the addon will
            not raise an exception.
        '''
        # Loop through each attribute in the CustomAttributeCallBacks instance
        for attribute in CustomAttributeCallbacks().keys():
            # Continue to the next attribute if the addon name is not found
            if not addon in CustomAttributeCallbacks()[attribute]:
                continue

            # Remove the custom attribute callback
            CustomAttributeCallbacks().remove(attribute, addon)


# =============================================================================
# Functions
# =============================================================================
def remove_recent_winner():
    global recentWinner
    recentWinner = False
