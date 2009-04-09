import es
from playerlib import uniqueid

class CustomAttributeCallbacks(dict):
    '''
    This class is designed to store subaddons that were loaded as a result of
    being a dependency to another subaddon.
    '''
    
    def add(self, attribute, function):
        '''
        We will only add dependencies (subaddons) that were not loaded via
        configs or that were previously determined as being loaded due to
        being a dependency.
        '''
        # Create a hook list
        if attribute not in self:
            self[attribute] = []
            
        if function in self[attribute]:
            return
            
        # Add the addon to the dependency list
        self[attribute].append(function)
            
    def remove(self, attribute, function):
        '''
        We will remove the addons from the list of dependencies that were
        loaded. If the dependency no longer has any addons that rely on it,
        we will unload the dependency.
        '''
        # Ensure that the subaddon is listed in the dictionary
        if not function in self[attribute]:
            return
            
        # Remove the subaddon from the list
        self[attribute].remove(function)
            
        # If no more addons are listed under the dependency, unload it
        if not self[attribute]:
            del self[attribute]


setHooks = CustomAttributeCallbacks()
getHooks = CustomAttributeCallbacks()

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
        if name in setHooks:
            for function in setHooks[name]:
                function(name, value)
        object.__setattr__(self, name, value)
        
    def __getattr__(self, name):
        '''
        #Getting an attribute is equivalent to getting an item
        '''
        return object.__getattribute__(self, name)
        
    def __setitem__(self, name, value):
        self.__setattr__(name, value)
        
    def __getitem__(self, name):
        return object.__getattribute__(self, name)

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
           
    def addAttributeCallBack(self, attribute, function):
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
        if not hasattr(players[self.userid], attribute):
            raise AttributeError('%s has no attribute: %s' %(players[self.userid], attribute))
            
        setHooks.add(attribute, function)

def player_spawn(event_var): 
    if int(event_var['es_userteam']) > 1:
        myPlayer = Player(event_var['userid'])
        es.dbgmsg(0, '')
        es.dbgmsg(0, 'Player Spawn: (%s)' %myPlayer.steamid)
        es.dbgmsg(0, '-'* 30)
        es.msg('%s\'s level: %s' %(event_var['es_username'], myPlayer.level))
        es.dbgmsg(0, '-'* 30)

def player_death(event_var):
    myPlayer = Player(event_var['attacker'])
    myPlayer.level += 1
    es.dbgmsg(0, '')
    es.dbgmsg(0, 'Player Death: (%s killed %s)' %(event_var['es_attackername'], event_var['es_username']))
    es.dbgmsg(0, '-'* 30)
    es.msg('%s\'s level: %s' %(event_var['es_attackername'], myPlayer.level))
    es.dbgmsg(0, '-'* 30)
    
    myPlayer.customattribute = 5
    es.dbgmsg(0, BasePlayer.__dict__)
    myPlayer.addAttributeCallBack('customattribute', mySetHook)
    myPlayer.customattribute = 1
    es.dbgmsg(0, '%s has a custom attribute of: %s' %(event_var['es_attackername'], myPlayer['customattribute']))

def player_disconnect(event_var): 
    del players[event_var['userid']]
    
def mySetHook(name, value):
    if name == 'customattribute':
        if value not in range(1, 10):
            raise ValueError('%s must be between 1 and 10...it was set to %s, noob.' %(name, value))
    es.dbgmsg(0, 'Set Hook was called for "%s" with a value of %s' %(name, value))