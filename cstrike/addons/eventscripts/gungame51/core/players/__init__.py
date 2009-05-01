# ../cstrike/addons/eventscripts/gungame51/core/players/__init__.py

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
from playerlib import uniqueid
from playerlib import getPlayer

# GunGame Imports
from gungame51.core.weapons.shortcuts import getLevelWeapon
from gungame51.core.weapons.shortcuts import getLevelMultiKill
from gungame51.core import getOS
from gungame51.core import GunGameError
#from gungame51.core.messaging import __messages__

# ============================================================================
# >> CLASSES
# ============================================================================
class CustomAttributeCallbacks(dict):
    '''
    This class is designed to store callback functions for custom attributes
    added to GunGame via a subaddon.
    '''
    def add(self, attribute, function, addon):
        '''
        Adds a callback to execute when a previously created attribute is set
        via the BasePlayer class' __setitem__ or __setattr__ methods.
        
        Note:
            You can not add callbacks for primary GunGame attributes:
                * userid
                * steamid
                * level
                * preventlevel
                * multikill
        '''
        # Do not let them add callbacks to GunGame's attributes
        if attribute in ['userid', 'level', 'preventlevel',
                         'steamid', 'multikill']:
            raise AttributeError('No callbacks are allowed to be set for "%s".'
                %attribute)
        
        # Make sure that the function is callable
        if not callable(function):
            raise AttributeError('Callback "%s" is not callable.' %function)
            
        # Create the attribute callback
        self[attribute] = (function, addon)
            
    def remove(self, attribute):
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
            
        # Delete the attribtue callback
        del self[attribute]


setHooks = CustomAttributeCallbacks()


class BasePlayer(object):
    # =========================================================================
    # >> BasePlayer() CLASS INITIALIZATION
    # =========================================================================
    def __init__(self, userid): 
        self.userid = userid 
        self.level = 1
        self.preventlevel = []
        self.multikill = 0
        self.steamid = uniqueid(str(self.userid), 1)
        self.weapon = getLevelWeapon(self.level)

    # =========================================================================
    # >> BasePlayer() CLASS ATTRIBUTE METHODS
    # =========================================================================
    def __setattr__(self, name, value):
        # First, we execute the custom attribute callbacks
        if name in setHooks:
            setHooks[name][0](name, value)
            
        # Set the attribute value
        object.__setattr__(self, name, value)

    def __getattr__(self, name):
        if name == 'weapon':
            self.weapon = getLevelWeapon(self.level)
        # Return the attribute value
        return object.__getattribute__(self, name)

    def __delattr__(self, name):
        # Make sure we don't try to delete required GunGame attributes
        if name in ['userid', 'level', 'preventlevel', 'steamid', 'multikill']:
            raise AttributeError('Unable to delete attribute "%s". '
                % attribute + 'This is a required attribute for GunGame.')

        # Remove this attribute from the custom attribute callbacks, if any
        if name in setHooks:
            del setHooks[name]

        # Delete the attribute only if it exists (we don't want to raise errors)
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
    # >> BasePlayer() CUSTOM CLASS METHODS
    # =========================================================================
    def levelup(self, levelsAwarded, victim=0, reason=''):
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
        # Return false if we can't level up
        if len(self.preventlevel):
            return False
            
        # Get the victim's Player() instance
        if victim:
            victim = Player(victim)

        # Use the EventManager to call the gg_levelup event
        events.gg_levelup(self, levelsAwarded, victim, reason)

    def leveldown(self, levelsTaken, attacker=0, reason=''):
        '''
        Removes a declared number of levels from the victim.

        Arguments:
            * levelsAwarded: (required)
                The number of levels to award to the attacker.
            * victim: (default of 0)
                The userid of the victim.
            * reason: (not required)
                The string reason for leveling up the attacker.
        '''
        # Return false if we can't level down
        if len(self.preventlevel):
            return False

        # Get the attacker's Player() instance
        if attacker:
            attacker = Player(attacker)
            
        # Use the EventManager to call the gg_leveldown event
        events.gg_leveldown(self, levelsTaken, attacker, reason)

    def msg(self):
        # This is where we will handle/send translated GunGame messages
        es.msg('We just sent %s a message!' %es.getplayername(self.userid))

    def hudhint(self):
        # This is where we will handle/send translated GunGame hudhints
        es.msg('We just sent %s a hudhint!' %es.getplayername(self.userid))

    def getWeapon(self):
        return getLevelWeapon(self.level)

    def giveWeapon(self):
        '''
        Gives a player their current level's weapon.
        '''
        # Make sure player is on a team
        if isSpectator(self.userid):
            raise GunGameError('Unable to give player weapon (%s):'
                %self.userid + ' is not on a team.')

        # Make sure player is alive
        if isDead(self.userid):
            raise GunGameError('Unable to give player weapon (%s):'
                %self.userid + ' is not alive.')

        # Get active weapon
        if self.weapon != 'knife':
            es.delayed(0, 'es_xgive %s weapon_%s;es_xsexec %s "use weapon_%s"'
                %(self.userid, self.weapon, self.userid, self.weapon))

    def strip(self):
        '''
        Strips the player of their primary and secondary weapon.
        '''
        if getOS() == 'posix':
            stripFormat = 'es_xgive %s weapon_knife;' %self.userid + \
                'es_xgive %s player_weaponstrip;' %self.userid + \
                'es_xfire %s player_weaponstrip Strip;' %self.userid + \
                'es_xfire %s player_weaponstrip Kill' %self.userid
            return

        # Retrieve a playerlib.Player() instance
        pPlayer = getPlayer(self.userid)

        # Get the primary and secondary weapon indexes
        pWeapon, sWeapon = pPlayer.getPrimary(), pPlayer.getSecondary()

        # Strip primary weapon
        if pWeapon:
            es.server.cmd('es_xremove %i' %pPlayer.getWeaponIndex(pWeapon))

        # Strip secondary weapon
        if sWeapon:
            es.server.cmd('es_xremove %i' %pPlayer.getWeaponIndex(sWeapon))


class PlayerDict(dict):
    '''
    A class-based dictionary to contain instances of BasePlayer.

    Note:
        This class is meant for private use.
    '''
    # =========================================================================
    # >> PlayerDict() CLASS ATTRIBUTE METHODS
    # =========================================================================
    def __getitem__(self, userid): 
        '''
        When we get an item in the dictionary BasePlayer is instantiated if it
        hasn't been already.
        '''
        userid = int(userid) 
        if userid not in self: 
            self[userid] = BasePlayer(userid) 

        # We don't want to call our __getitem__ again 
        return super(PlayerDict, self).__getitem__(userid)

    def __delitem__(self, userid): 
        '''
        Putting the existence check here makes it easier to delete players.
        '''
        userid = int(userid)
        if userid in self:
            del super(PlayerDict, self)[userid]

    def clear(self): 
        '''
        Clear the player dictionary to start fresh with a clean slate.
        '''
        super(PlayerDict, self).clear()


players = PlayerDict()


class Player(object):
    '''
    This class is intended to be used as the class container for interaction
    with all GunGame-based player attributes. This class forwards to the stored
    PlayerDict instance of the player's userid, which in return forwards to the
    BasePlayer class.
    
    Usage:
        # Setting attributes
        Player(userid).customattribute = value
        Player(userid)['customattribute'] = value
        
        # Getting attributes
        level = Player(userid).level
        level = Player(userid)['level']
        
        # Deleting custom attributes
        del Player(userid).customattribute
        
    Note:
        For class methods, see the gungame.core.players.BasePlayer class.
    '''
    # =========================================================================
    # >> Player() CLASS INITIALIZATION
    # =========================================================================
    def __init__(self, userid):
        self.userid = int(userid)

    # =========================================================================
    # >> Player() CLASS ATTRIBUTE METHODS
    # =========================================================================
    def __getitem__(self, item):
        # We only directly allow the attribute "userid" to be set
        return players[self.userid][item]

    def __setitem__(self, item, value):
        # We only directly allow the attribute "userid" to be set
        players[self.userid][item] = value

    def __getattr__(self, name):
        if name == 'userid':
            # We only directly allow the attribute "userid" to be retrieved
            object.__getattr__(self, name)
        else:
            # Redirect to the PlayerDict instance
            return players[self.userid][name]

    def __setattr__(self, name, value):
        if name == 'userid':
            # We only directly allow the attribute "userid" to be set
            object.__setattr__(self, name, value)
        else:
            # Redirect to the PlayerDict instance
            players[self.userid][name] = value

    def __delitem__(self, name):
        # Redirect to the PlayerDict instance
        del players[self.userid][name]

    def __delattr__(self, name):
        # Redirect to the PlayerDict instance
        del players[self.userid][name]

    # ========================================================================
    # Player() STATIC CLASS METHODS
    # ========================================================================
    @staticmethod
    def addAttributeCallBack(attribute, function, addon):
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
            Player.addAttributeCallBack('attributeName', callbackFunction,
                                        'gg_addon_name')

            def callbackFunction(name_of_the_attribute, value_to_be_checked):
                if name_of_the_attribute == 'attributeName':
                    if value_to_be_checked > 0 and value_to_be_checked < 10:
                        pass
                    else:
                        raise ValueError('Value must be between 1 and 10!')
        '''
        # Add the attribute callback to the CustomAttributeCallbacks instance
        setHooks.add(attribute, function, addon)

    @staticmethod
    def removeAttributeCallBack(attribute):
        '''
        Removes a callback function that is called when a named attribute is
        set using the class-based dictionary CustomAttributeCallbacks.

        Note:
            Attempting to remove a non-existant attribute callback will not
            raise an exception.

        Usage:
            Player.removeAttributeCallBack('attributeName')
        '''
        # Remove the callback from the CustomAttributeCallbacks instance
        setHooks.remove(attribute)

    @staticmethod
    def removeCallBacksForAddon(addon):
        '''
        Removes all attribute callbacks from the class-based dictionary
        CustomAttributeCallBacks that have been associated with the named
        addon.

        Usage:
            Player.removeCallBacksForAddon('gg_addon_name')

        Note:
            Attempting to remove attributes from an addon that does not exist
            or if no attributes exist that are associated with the addon will
            not raise an exception.
        '''
        # Loop through each attribute in the CustomAttributeCallBacks instance
        for attribute in list(setHooks):
            # Continue to the next attribute if the addon name is not found
            if not addon in setHooks[attribute]:
                continue

            # Remove the custom attribute callback
            setHooks.remove(attribute)
            
def isDead(userid):
    '''
    Checks to see if the player is dead.

    Notes:
        * 1 = The player is dead.
        * 0 = The player is alive.

    Usage:
        import es
        from gungame.core.players.shortcuts import isDead
        
        def customFunction(userid):
            if isDead(userid):
                es.msg('This player is dead!')
            else:   
                es.msg('This player is alive!')
    '''
    return es.getplayerprop(userid, 'CBasePlayer.pl.deadflag')

def isSpectator(userid):
    '''
    Checks to see if the is a spectator or unassigned.

    Notes:
        * True = The player is a spectator, currently connecting or not on the
                 server.
        * False = The player is on an active team.
        
    Usage:
        import es
        from gungame.core.players.shortcuts import isSpectator
        
        def player_spawn(event_var):
            if isSpectator(event_var['userid']):
                es.msg('This player is not on a team!')
            else:   
                es.msg('This player is on a team!')
    '''
    return es.getplayerteam(userid) <= 1
    
from gungame51.core.events.shortcuts import events