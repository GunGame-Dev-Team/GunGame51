# ../cstrike/addons/eventscripts/gungame51/core/weapons/__init__.py

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
from weaponlib import getWeaponList

# GunGame Imports
from gungame51.core import getGameDir

# ============================================================================
# >> CLASSES
# ============================================================================           
class BaseWeaponOrders(object):
    def __init__(self, name):
        es.dbgmsg(0, 'INSIDE BASEWEAPONORDERS: %s' %name)
        self.file = name
        self.filepath = getGameDir('cfg/gungame51/weapon_orders/%s.txt' %self.file)
        self.title = 'Untitled Weapon Order'
        self.type = None
        self.order = {}
        
        # Parse the weapon order file
        self.parse()
        
    def parse(self):
        '''Parses the weapon file.'''
        # Try to open the file
        try:
            weaponOrderFile = open(self.filepath, 'r')
        except IOError, e:
            raise IOError('Cannot parse weapon order file (%s): IOError: %s' % (self.filepath, e))
            
        # Clean and format the lines
        lines = [x.strip() for x in weaponOrderFile.readlines()]
        lines = filter(lambda x: x and (not x.startswith('//')), lines)
        lines = [x.split('//')[0] for x in lines]
        lines = [' '.join(x.split()) for x in lines]
        
        # Close the file, we have the lines
        weaponOrderFile.close()
        
        # Set a variable to keep track of the levels for each weapon as we
        # parse the file
        levelCounter = 0
        
        # Parse each line searching for title, weapon, and multikill values0
        for line in lines:
            # Check to see if the line is set for the title of the weapon order
            if line.startswith('@'):
                self.title = line[1:].strip()
                continue
                
            # Backwards compatible title (SOON TO BE DEPRECATED)
            if line.startswith('=>'):
                self.title = line[2:].strip()
                continue
                
            # Convert the line to lower-case
            line = line.lower()
            
            if len(line.split()) > 1:
                weapon, multikill = line.split()
            else:
                weapon, multikill = [line, 1]
                multikill = int(multikill)
            
            # Check the weapon here with
            if 'weapon_%s' %weapon not in getWeaponList('#primary') \
                + getWeaponList('#secondary') + ['weapon_hegrenade',
                'weapon_knife']:
                    raise ValueError('"%s" is not a valid weapon!' %weapon)
                    
            # Increment the level count
            levelCounter += 1
            
            # Set level values as a list
            self.order[levelCounter] = [weapon, multikill]
            
    def __getitem__(self, item):
        return object.__getattribute__(self, item)
        
    def echo(self):
        '''
        Echos (prints) the current weapon order to console.
        '''
        es.dbgmsg(0, '')
        es.dbgmsg(0, '[GunGame] Weapon Order: %s' %self.file)
        es.dbgmsg(0, '')
        es.dbgmsg(0, '[GunGame] +-------+-----------+---------------+')
        es.dbgmsg(0, '[GunGame] | Level | Multikill |    Weapon     |')
        es.dbgmsg(0, '[GunGame] +-------+-----------+---------------+')
        for level in self.order:
            weapon = self.order[level][0]
            multikill = self.order[level][1]
            #es.dbgmsg(0, '[GunGame] |  %2s   |     %s     | %13s |' % (level, weapon, multikill))
            es.dbgmsg(0, '[GunGame] |  %2s   |     %d     | %13s |' % (level, int(multikill), weapon))
        es.dbgmsg(0, '[GunGame] +-------+-----------+---------------+')
        
        
class WeaponOrdersDict(dict):
    '''
    A class-based dictionary to contain instances of BaseWeapons.
    
    Note:
        This class is meant for private use.
    '''
    def __getitem__(self, name): 
        '''
        When we get an item in the dictionary BaseWeapons is instantiated if it
        hasn't been already.
        '''
        name = str(name).split('.')[0]

        if name not in self:
            self[name] = BaseWeaponOrders(name)            
            
        # We don't want to call our __getitem__ again 
        return super(WeaponOrdersDict, self).__getitem__(name)

    def __delitem__(self, name): 
        '''
        Putting the existence check here makes it easier to delete orders.
        '''
        name = str(name)
        if name in self:
            del super(WeaponOrdersDict, self)[name]

    def clear(self): 
        """ Invariably you will put something here """
        es.msg('Dictionary cleared!')
        super(WeaponOrdersDict, self).clear()


orders = WeaponOrdersDict()

class WeaponManager(object):
    def __init__(self):
        self.__weaponorders__ = {}
        self.currentorder = None
        
    def load(self, name):
        '''
        Load a weapon order by name.
        
        Note:
            This does not set the weapon order to be used by GunGame, it only
            loads and parses the weapon order.
            
        Usage:
        '''
        self.__weaponorders__[name] = orders[name]
        es.dbgmsg(0, 'self.__weaponorders__[%s] = %s' %(name, self.__weaponorders__[name]))
        
    def unload(self, order):
        '''
        Unload a weapon order by name.
        
        Note:
            This removes the weapon order from stored memory. It is not
            intended to be used
        '''
        # Meh
        del self.__weaponorders__[name]
        
        if name == self.currentorder:
            self.currentorder = None
        
    def setOrder(self, name):
        if name in self.__weaponorders__:
            self.currentorder = name
        
        # Things that will restart the round:
        '''
        gg_multikill_override
        Setting a new weapon order
        Changing the weapon order type
        '''
    def __getitem__(self, item):
        if name in ['currentorder', '__weaponorders__']:
            return object.__getattr__(self, item)
        else:
            if not self.currentorder:
                raise AttributeError('There is no weapon order set! Use setOrder(order_name) first!')
            
            # Return the item from the WeaponOrdersDict instance
            return orders[self.currentorder][item]
        
    def __setitem__(self, item, value):
        if name in ['currentorder', '__weaponorders__']:
            object.__setattr__(self, item, value)
        else:
            if not self.currentorder:
                raise AttributeError('There is no weapon order set! Use setOrder(order_name) first!')
                
            # We only directly allow the attribute "userid" to be set
            orders[self.currentorder][item] = value
    
    def __getattr__(self, name):
        if name in ['currentorder', '__weaponorders__']:
            # We only directly allow the attribute "userid" to be retrieved
            object.__getattr__(self, name)
        else:
            if not self.currentorder:
                raise AttributeError('There is no weapon order set! Use setOrder(order_name) first!')
            # Redirect to the PlayerDict instance
            return orders[self.currentorder][name]
      
    def __setattr__(self, name, value):
        if name in ['currentorder', '__weaponorders__']:
            # We only directly allow the attribute "userid" to be set
            object.__setattr__(self, name, value)
        else:
            if not self.currentorder:
                raise AttributeError('There is no weapon order set! Use setOrder(order_name) first!')
            # Redirect to the PlayerDict instance
            orders[self.currentorder][name] = value
    

weaponorders = WeaponManager()