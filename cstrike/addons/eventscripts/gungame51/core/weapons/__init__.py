# ../addons/eventscripts/gungame/core/weapons/__init__.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
# Python imports
import os.path
import random

# EventScripts Imports
import es
from weaponlib import getWeaponList
from gamethread import delayedname
from gamethread import cancelDelayed

# GunGame Imports
from gungame51.core import getGameDir

# ============================================================================
# >> CLASSES
# ============================================================================           
class BaseWeaponOrders(object):
    '''
    Class designed for storing individual weapon orders.
    '''
    # =========================================================================
    # >> BaseWeaponOrders() CLASS INITIALIZATION
    # =========================================================================
    def __init__(self, name):
        self.file = name
        self.filepath = getGameDir('cfg/gungame51/weapon_orders/%s.txt' %self.file)
        self.title = 'Untitled Weapon Order'
        self.type = '#default'
        self.order = {}

        # Parse the weapon order file
        self.parse()

    # =========================================================================
    # >> BaseWeaponOrders() CLASS ATTRIBUTE METHODS
    # =========================================================================
    def __getitem__(self, item):
        return object.__getattribute__(self, item)

    def __setitem__(self, item, value):
        return self.__setattr__(item, value)

    def __setattr__(self, name, value):
        if name == 'type':
            if value not in ['#default', '#reversed', '#random']:
                raise AttributeError('Invalid attribute value for type: "%s".'
                    %value + ' Use only "%s".' %'", "'.join(['#default',
                        '#reversed', '#random']))

            if not hasattr(self, name):
                object.__setattr__(self, name, value)

            # If the type is the same, do nothing
            if self.type == value and value != '#random':
                return

            object.__setattr__(self, name, self.__setWeaponOrderType(value))
        else:
            object.__setattr__(self, name, value)

    # =========================================================================
    # >> BaseWeaponOrders() CUSTOM CLASS METHODS
    # =========================================================================
    def parse(self):
        '''
        Parses the weapon file.
        '''
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

    def __setWeaponOrderType(self, type):
        # =====================================================================
        # RANDOM WEAPON ORDER
        # =====================================================================
        if type == '#random':
            # Get weapons
            weapons = self.order.values()

            # Setup variables
            knifeData = None
            nadeData = None

            # Get knife and grenade data
            for weapon in weapons[:]:
                if weapon[0] == 'knife':
                    # Get data
                    knifeData = weapon

                    # Remove
                    weapons.remove(weapon)

                elif weapon[0] == 'hegrenade':
                    # Get data
                    nadeData = weapon

                    # Remove
                    weapons.remove(weapon)

            # Shuffle
            random.shuffle(weapons)

            # Set weapon order
            self.order = dict(zip(range(1, len(weapons)+1), weapons))

            # Re-add knife and grenade to the end
            if nadeData != None:
                self.order[len(self.order)+1] = nadeData

            if knifeData != None:
                self.order[len(self.order)+1] = knifeData

        # =====================================================================
        # DEFAULT WEAPON ORDER
        # =====================================================================
        elif type == '#default':
            # Re-parse the file
            self.parse()

        # =====================================================================
        # REVERSED WEAPON ORDER
        # =====================================================================
        elif type == '#reversed':
            # Get weapons
            weapons = self.order.values()

            # Setup variables
            knifeData = None
            nadeData = None

            # Get knife and grenade data
            for weapon in weapons[:]:
                if weapon[0] == 'knife':
                    # Get data
                    knifeData = weapon

                    # Remove
                    weapons.remove(weapon)

                elif weapon[0] == 'hegrenade':
                    # Get data
                    nadeData = weapon

                    # Remove
                    weapons.remove(weapon)

            # Reverse
            weapons.reverse()

            # Set weapon order
            self.order = dict(zip(range(1, len(weapons)+1), weapons))

            # Re-add knife and grenade to the end
            if nadeData != None:
                self.order[len(self.order)+1] = nadeData

            if knifeData != None:
                self.order[len(self.order)+1] = knifeData

        # When the weapon order changes, we create/cancel a delayed name so
        # that we do not restart the round multiple times due to one weapon
        # order change
        cancelDelayed('gg_mp_restartgame')
        delayedname(1, 'gg_mp_restartgame', self.restartRound, ())

        # Set the new order type
        return type

    def setMultiKillOverride(self, value):
        '''
        Sets the multikill override.
        '''
        value = int(value)

        if not value > 1:
            value = 1

        # Loop through the weapon order dictionary
        for level in self.order:
            # Set multikill if its not a knife or a hegrenade
            if self.order[level][0] != 'knife' and self.order[level][0] != 'hegrenade':
                self.order[level][1] = value

        # When the weapon order changes, we create/cancel a delayed name so
        # that we do not restart the round multiple times due to one weapon
        # order change
        cancelDelayed('gg_mp_restartgame')
        delayedname(1, 'gg_mp_restartgame', self.restartRound, ())

    def restartRound(self):
        if not self.file == weaponorders.gungameorder:
            return

        es.server.cmd('mp_restartgame 2')
        es.msg('Weapon Order Changed! Restarting in 2 seconds!')

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
            es.dbgmsg(0, '[GunGame] |  %2s   |     %d     | %13s |' % (level, multikill, weapon))
        es.dbgmsg(0, '[GunGame] +-------+-----------+---------------+')

    def getWeapon(self, level):
        if not level in range(1, len(self.order) + 1):
            raise ValueError('Can not get weapon for level: "%s".'
                %level + ' Level is out of range (1-%s).' %len(self.order))
        return self.order[level][0]

    def getMultiKill(self, level):
        if not level in range(1, len(self.order) + 1):
            raise ValueError('Can not get multikill value for level: "%s".'
                %level + ' Level is out of range (1-%s).' %len(self.order))
        return self.order[level][1]

    def getTotalLevels(self):
        return len(self.order)


class WeaponOrdersDict(dict):
    '''
    A class-based dictionary to contain instances of BaseWeapons.
    
    Note:
        This class is meant for private use.
    '''
    # =========================================================================
    # >> WeaponOrdersDict() CLASS ATTRIBUTE METHODS
    # =========================================================================
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

    # =========================================================================
    # >> WeaponOrdersDict() CUSTOM CLASS METHODS
    # =========================================================================
    def clear(self): 
        """ Invariably you will put something here """
        es.dbgmsg(0, 'WeaponOrdersDict cleared!')
        super(WeaponOrdersDict, self).clear()


orders = WeaponOrdersDict()


class WeaponManager(object):
    # =========================================================================
    # >> WeaponManager() CLASS INITIALIZATION
    # =========================================================================
    def __init__(self):
        self.__weaponorders__ = {}
        self.gungameorder = 'default_weapon_order'
        self.currentorder = None

    # =========================================================================
    # >> WeaponManager() CLASS ATTRIBUTE METHODS
    # =========================================================================
    def __getitem__(self, item):
        if name in ['currentorder', '__weaponorders__', 'gungameorder']:
            return object.__getattr__(self, item)
        else:
            if not self.currentorder:
                raise AttributeError('There is no weapon order set! Use setOrder(order_name) first!')

            # Return the item from the WeaponOrdersDict instance
            return orders[self.currentorder][item]

    def __setitem__(self, item, value):
        if item in ['currentorder', '__weaponorders__', 'gungameorder']:
            object.__setattr__(self, item, value)
        else:
            if not self.currentorder:
                raise AttributeError('There is no weapon order set! Use setOrder(order_name) first!')

            # We only directly allow the attribute "userid" to be set
            orders[self.currentorder][item] = value

    def __getattr__(self, name):
        if name in ['currentorder', '__weaponorders__', 'gungameorder']:
            # We only directly allow the attribute "userid" to be retrieved
            object.__getattr__(self, name)
        else:
            if not self.currentorder:
                raise AttributeError('There is no weapon order set! Use setOrder(order_name) first!')
            # Redirect to the PlayerDict instance
            return orders[self.currentorder][name]

    def __setattr__(self, name, value):
        if name in ['currentorder', '__weaponorders__', 'gungameorder']:
            # Set these attributes as they belong to this class
            object.__setattr__(self, name, value)
        else:
            if not self.currentorder:
                raise AttributeError('There is no weapon order set! Use setOrder(order_name) first!')

            # Redirect to the PlayerDict instance
            orders[self.currentorder][name] = value

    # =========================================================================
    # >> WeaponManager() CUSTOM CLASS METHODS
    # =========================================================================
    def load(self, name):
        '''
        Load a weapon order by name.
        
        Note:
            This does not set the weapon order to be used by GunGame, it only
            loads and parses the weapon order.
        '''
        self.__weaponorders__[name] = orders[name]
        self.currentorder = name
        return self.__weaponorders__[name]

    def unload(self, order):
        '''
        Unload a weapon order by name.
        
        Note:
            This removes the weapon order from stored memory. It is not
            intended to be used
        '''
        # Delete the weapon order instance from our dictionary
        del self.__weaponorders__[name]

        if name == self.currentorder:
            self.currentorder = None
        if name == self.gungameorder:
            self.gungameorder = None

    def setOrder(self, name):
        if name not in self.__weaponorders__:
            self.load(name)
            self.gungameorder = name
        else:
            self.gungameorder = name

        # When the weapon order changes, we create/cancel a delayed name so
        # that we do not restart the round multiple times due to one weapon
        # order change
        cancelDelayed('gg_mp_restartgame')
        delayedname(1, 'gg_mp_restartgame', self.restartRound, ())


weaponorders = WeaponManager()

# ============================================================================
# >> FUNCTIONS
# ============================================================================
def loadWeaponOrders():
    '''
    Loads all weapon orders in the "../<MOD>/cfg/gungame/weapon_orders"
    directory.
    '''
    weaponOrderPath = getGameDir('cfg/gungame51/weapon_orders')

    for item in os.listdir(weaponOrderPath):
        # Ignore subfolders
        if os.path.isdir(os.path.join(weaponOrderPath, item)):
            continue

        weaponorders.load(item)

loadWeaponOrders()