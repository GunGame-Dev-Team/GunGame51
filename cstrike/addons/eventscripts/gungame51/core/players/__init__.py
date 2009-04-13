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

# GunGame Imports
from gungame51.core.events import events

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
        '''
        # Make sure the attribute callback exists
        if not attribute in self:
            return
            
        # Delete the attribtue callback
        del self[attribute]


setHooks = CustomAttributeCallbacks()


class BasePlayer(object): 
    def __init__(self, userid): 
        self.userid = userid 
        self.level = 1
        self.preventlevel = []
        self.multikill = 0
        self.steamid = uniqueid(str(self.userid), 1)
      
    def __setattr__(self, name, value):
        '''
        #Setting an attribute is equivalent to setting an item
        '''
        # First, we execute the custom attribute callbacks
        if name in setHooks:
            setHooks[name][0](name, value)
            
        # Set the attribute value
        object.__setattr__(self, name, value)
        
    def __getattr__(self, name):
        '''
        #Getting an attribute is equivalent to getting an item
        '''
        if name in getHooks:
            getHooks[name](name, value)
        return object.__getattribute__(self, name)
        
    def __delattr__(self, name):
        if name in ['userid', 'level', 'preventlevel', 'steamid', 'multikill']:
            raise AttributeError('Unable to delete attribute "%s". '
                % attribute + 'This is a required attribute for GunGame.')
        
        # Remove this attribute from the custom attribute callbacks
        if name in setHooks:
            del setHooks[name]
            
        object.__delattr__(self, name)
        
    def __setitem__(self, name, value):
        self.__setattr__(name, value)
        
    def __getitem__(self, name):
        return object.__getattribute__(self, name)
        
    def __delitem__(self, name):
        self.__delattr__(name)
        
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
            
        # Use the EventManager to call the gg_levelup event
        events.gg_levelup(self.userid, levelsAwarded, victim, reason)
        
    def leveldown(self, levelsTaken, attacker=0, reason=''):
        '''
        This player should be the victim (the player that is levelling down)
        '''
        # Return false if we can't level down
        if len(self.preventlevel):
            return False
            
        # Use the EventManager to call the gg_leveldown event
        events.gg_leveldown(self.userid, levelsTaken, attacker, reason)
        
    def msg(self):
        es.msg('We just sent %s a message!' %es.getplayername(self.userid))


class PlayerDict(dict): 
    def __getitem__(self, userid): 
        """ 
        When we get an item in the dictionary BasePlayer is instantiated 
        if it hasn't been already 
        """ 
        userid = int(userid) 
        if userid not in self: 
            self[userid] = BasePlayer(userid) 
            
        # We don't want to call our __getitem__ again 
        return super(PlayerDict, self).__getitem__(userid)

    def __delitem__(self, userid): 
        """ Putting the existence check here makes it easier to delete players """ 
        userid = int(userid) 
        if userid in self: 
            del super(PlayerDict, self)[userid] 

    def clear(self): 
        """ Invariably you will put something here """ 
        es.msg('Dictionary cleared!') 
        super(PlayerDict, self).clear() 


players = PlayerDict()


class Player(object):
    def __init__(self, userid):
        self.userid = int(userid)
        
    def __getitem__(self, item):
        return players[self.userid][item]
        
    def __setitem__(self, item, value):
        players[self.userid][item] = value
    
    def __getattr__(self, name):
        if name == 'userid':
            object.__getattr__(self, name)
        else:
            return players[self.userid][name]
      
    def __setattr__(self, name, value):
        if name == 'userid':
            object.__setattr__(self, name, value)
        else:
            players[self.userid][name] = value
            
    def __delitem__(self, name):
        del players[self.userid][name]
        
    def __delattr__(self, name):
        del players[self.userid][name]
            
    # ========================================================================
    # Player() Static Class Methods
    # ========================================================================
    @staticmethod
    def addAttributeCallBack(attribute, function, addon):
        '''
        Description:
            Adds a callback function when an attribute is set. The callback
            function must have 2 arguments declared. The first argument will
            be the actual name of the attribute. The second argument will be
            the value that it was set to.
        
        Notes:
            You must set (instantiate) a custom attribute before adding an
            attribute callback to it.
            
            If an error is raised in your callback, the value will not be set.
        
        Usage:
            addAttributeCallBack(attributeName, callbackFunction)
            
            def callbackFunction(name_of_the_attribute, value_to_be_checked):
                if value > 0 and value < 10:
                    pass
                else:
                    raise ValueError('Value must be between 1 and 10!')
        '''
        setHooks.add(attribute, function, addon)
        
    @staticmethod
    def removeAttributeCallBack(attribute):
        setHooks.remove(attribute)
        
    @staticmethod
    def removeCallBacksForAddon(addon):
        for attribute in list(setHooks):
            if not addon in setHooks[attribute]:
                continue
                
            # Remove the custom attribute callback
            setHooks.remove(attribute)