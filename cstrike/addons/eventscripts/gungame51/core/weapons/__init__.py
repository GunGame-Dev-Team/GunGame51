# ../addons/eventscripts/gungame51/core/weapons/__init__.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
# Python imports
from __future__ import with_statement
import random

# EventScripts Imports
import es
from weaponlib import getWeaponList
from gamethread import delayedname
from gamethread import cancelDelayed
from playerlib import getPlayer
from playerlib import getUseridList

# GunGame Imports
from gungame51.core import get_game_dir

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
        self.filepath = get_game_dir('cfg/gungame51/weapon_orders/' + 
            '%s.txt' % self.file)
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

            object.__setattr__(self, name, self.__set_weapon_order_type(value))
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
            with open(self.filepath, 'r') as weaponOrderFile:
                # Clean and format the lines
                lines = [x.strip() for x in weaponOrderFile.readlines()]
                lines = filter(lambda x: x and (not x.startswith('//')), lines)
                lines = [x.split('//')[0] for x in lines]
                lines = [' '.join(x.split()) for x in lines]

        except IOError, e:
            raise IOError('Cannot parse weapon order file ' +
                '(%s): IOError: %s' % (self.filepath, e))

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

    def __set_weapon_order_type(self, type):
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
        delayedname(1, 'gg_mp_restartgame', self.restart_round, ())

        # Set the new order type
        return type

    def set_multikill_override(self, value):
        '''
        Sets the multikill override.
        '''
        value = int(value)

        if not value > 1:
            value = 1

        # Loop through the weapon order dictionary
        for level in self.order:
            # Set multikill if its not a knife or a hegrenade
            if self.order[level][0] != 'knife' and \
              self.order[level][0] != 'hegrenade':
                self.order[level][1] = value

        # When the weapon order changes, we create/cancel a delayed name so
        # that we do not restart the round multiple times due to one weapon
        # order change
        cancelDelayed('gg_mp_restartgame')
        delayedname(1, 'gg_mp_restartgame', self.restart_round, ())

    def restart_round(self):
        if not self.file == WeaponManager().gungameorder:
            return

        # Give players godmode so that they can't level up
        #
        # Spawning players in the next 2 seconds will be killable, but this is
        # unlikely and not worth the resources to prevent because killing a
        # spawning player in the 2 seconds after a weapon order is changed on
        # an active map (through rcon) will likely never happen, and if so,
        # will result in a levelup
        for userid in getUseridList("#alive"):
            getPlayer(userid).godmode = 1

        es.server.queuecmd('mp_restartgame 2')
        es.msg('Weapon Order Changed! Restarting in 2 seconds!')

    def echo(self):
        '''
        Echos (prints) the current weapon order to console.
        '''
        es.dbgmsg(0, ' ')
        es.dbgmsg(0, '[GunGame] Weapon Order: %s' %self.file)
        es.dbgmsg(0, ' ')
        es.dbgmsg(0, '[GunGame] +-------+-----------+---------------+')
        es.dbgmsg(0, '[GunGame] | Level | Multikill |    Weapon     |')
        es.dbgmsg(0, '[GunGame] +-------+-----------+---------------+')
        for level in self.order:
            weapon = self.order[level][0]
            multikill = self.order[level][1]
            es.dbgmsg(0, '[GunGame] |  %2s   |     %d     | %13s |' % (level, 
                                                            multikill, weapon))
        es.dbgmsg(0, '[GunGame] +-------+-----------+---------------+')

    def get_weapon(self, level):
        if not level in range(1, len(self.order) + 1):
            raise ValueError('Can not get weapon for level: "%s".'
                %level + ' Level is out of range (1-%s).' %len(self.order))
        return self.order[level][0]

    def get_multikill(self, level):
        if not level in range(1, len(self.order) + 1):
            raise ValueError('Can not get multikill value for level: "%s".'
                %level + ' Level is out of range (1-%s).' %len(self.order))
        return self.order[level][1]

    def get_total_levels(self):
        return len(self.order)


class WeaponOrdersDict(dict):
    '''
    A class-based dictionary to contain instances of BaseWeapons.
    
    Note:
        This class is meant for private use.
    '''
    def __new__(cls, *p, **k):
        if not '_the_instance' in cls.__dict__:
            cls._the_instance = dict.__new__(cls)
        return cls._the_instance

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


class WeaponManager(object):
    def __new__(cls, *p, **k):
        if not '_the_instance' in cls.__dict__:
            cls._the_instance = object.__new__(cls)
            # Set up the instance variables
            cls._the_instance.__weaponorders__ = {}
            cls._the_instance.gungameorder = 'default_weapon_order'
            cls._the_instance.currentorder = None
        return cls._the_instance

    # =========================================================================
    # >> WeaponManager() CLASS ATTRIBUTE METHODS
    # =========================================================================
    def __getitem__(self, item):
        if name in ['currentorder', '__weaponorders__', 'gungameorder']:
            return object.__getattr__(self, item)
        else:
            if not self.currentorder:
                raise AttributeError('There is no weapon order set! ' + 
                        'Use set_order(order_name) first!')

            # Return the item from the WeaponOrdersDict instance
            return WeaponOrdersDict()[self.currentorder][item]

    def __setitem__(self, item, value):
        if item in ['currentorder', '__weaponorders__', 'gungameorder']:
            object.__setattr__(self, item, value)
        else:
            if not self.currentorder:
                raise AttributeError('There is no weapon order set! ' +
                        'Use set_order(order_name) first!')

            # We only directly allow the attribute "userid" to be set
            WeaponOrdersDict()[self.currentorder][item] = value

    def __getattr__(self, name):
        if name in ['currentorder', '__weaponorders__', 'gungameorder']:
            # We only directly allow the attribute "userid" to be retrieved
            object.__getattr__(self, name)
        else:
            if not self.currentorder:
                raise AttributeError('There is no weapon order set! ' + 
                        'Use set_order(order_name) first!')
            # Redirect to the WeaponOrdersDict instance
            return WeaponOrdersDict()[self.currentorder][name]

    def __setattr__(self, name, value):
        if name in ['currentorder', '__weaponorders__', 'gungameorder']:
            # Set these attributes as they belong to this class
            object.__setattr__(self, name, value)
        else:
            if not self.currentorder:
                raise AttributeError('There is no weapon order set! ' + 
                        'Use set_order(order_name) first!')

            # Redirect to the WeaponOrdersDict instance
            WeaponOrdersDict()[self.currentorder][name] = value

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
        self.__weaponorders__[name] = WeaponOrdersDict()[name]
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

    def set_order(self, name):
        if name not in self.__weaponorders__:
            self.load(name)
            self.gungameorder = name
        else:
            self.gungameorder = name

        # When the weapon order changes, we create/cancel a delayed name so
        # that we do not restart the round multiple times due to one weapon
        # order change
        cancelDelayed('gg_mp_restartgame')
        delayedname(1, 'gg_mp_restartgame', self.restart_round, ())

# ============================================================================
# >> FUNCTIONS
# ============================================================================
def load_weapon_orders():
    '''
    Loads all weapon orders in the "../<MOD>/cfg/gungame51/weapon_orders"
    directory.
    '''
    weaponOrderPath = get_game_dir('cfg/gungame51/weapon_orders')

    for item in weaponOrderPath.files("*.txt"):
        WeaponManager().load(item.name)

load_weapon_orders()