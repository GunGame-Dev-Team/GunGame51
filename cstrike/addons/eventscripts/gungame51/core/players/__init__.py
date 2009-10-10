# ../addons/eventscripts/gungame/core/players/__init__.py

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
import gamethread
from playerlib import uniqueid
from playerlib import getPlayer
from weaponlib import getWeaponNameList

# GunGame Imports
from gungame51.core.weapons.shortcuts import getLevelWeapon
from gungame51.core.weapons.shortcuts import getLevelMultiKill
from gungame51.core import getOS
from gungame51.core import GunGameError
from gungame51.core.messaging import __messages__
from gungame51.core.sound import SoundPack
from afk import AFK

# ============================================================================
# >> GLOBALS
# ============================================================================
list_pWeapons = getWeaponNameList('#primary')
list_sWeapons = getWeaponNameList('#secondary')
eventscripts_lastgive = es.ServerVar('eventscripts_lastgive')
gg_respawn_cmd = es.ServerVar('gg_respawn_cmd')

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


class BasePlayer(object):
    # =========================================================================
    # >> BasePlayer() CLASS INITIALIZATION
    # =========================================================================
    def __init__(self, userid): 
        self.userid = userid 
        self.level = 1
        self.preventlevel = PreventLevel()
        self.afk = AFK(self.userid)
        self.multikill = 0
        self.steamid = uniqueid(str(self.userid), 1)
        self.index = int(getPlayer(str(self.userid)).index)
        self.stripexceptions = []
        self.soundpack = SoundPack('default')

    # =========================================================================
    # >> BasePlayer() CLASS ATTRIBUTE METHODS
    # =========================================================================
    @property
    def weapon(self):
        """Return the weapon name"""
        return self.getWeapon()
        
    def __setattr__(self, name, value):
        # First, we execute the custom attribute callbacks
        if name in setHooks:
            setHooks[name][0](name, value)

        # Set the attribute value
        object.__setattr__(self, name, value)

    def __getattr__(self, name):
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
        EventManager().gg_levelup(self, levelsAwarded, victim, reason)

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
        if len(self.preventlevel):
            return False

        # Get the attacker's Player() instance
        if attacker:
            attacker = Player(attacker)

        # Use the EventManager to call the gg_leveldown event
        EventManager().gg_leveldown(self, levelsTaken, attacker, reason)

    def msg(self, string, tokens={}, prefix=False):
        __messages__.msg(self.userid, string, tokens, prefix)

    def saytext2(self, index, string, tokens={}, prefix=False):
        __messages__.saytext2(self.userid, index, string, tokens, prefix)

    def centermsg(self, string, tokens={}):
        __messages__.centermsg(self.userid, string, tokens)

    def hudhint(self, string, tokens={}):
        __messages__.hudhint(self.userid, string, tokens)

    def toptext(self, duration, color, string, tokens={}):
        __messages__.toptext(self.userid, duration, color, string, tokens)

    def echo(self, level, string, tokens={}, prefix=False):
        __messages__.echo(self.userid, level, string, tokens, prefix)

    def langstring(self, string, tokens={}, prefix=False):
        return __messages__.langstring(self.userid, string, tokens, prefix)

    def getWeapon(self):
        return getLevelWeapon(self.level)

    def giveWeapon(self, strip=True):
        '''
        Gives a player their current levels weapon.
        '''
        # Make sure player is on a team
        if es.getplayerteam(self.userid) < 2:
            raise GunGameError('Unable to give player weapon (%s):'
                %self.userid + ' is not on a team.')

        # Make sure player is alive
        if getPlayer(self.userid).isdead:
            raise GunGameError('Unable to give player weapon (%s):'
                %self.userid + ' is not alive.')

        # Do we want to strip the player's given weapon slot?
        if strip:
        
            # Retrieve a playerlib.Player() instance
            pPlayer = getPlayer(self.userid)

            # Check to see if the weapon is a primary
            if "weapon_%s" %self.weapon in list_pWeapons:

                # Get primary weapon name
                pWeapon = pPlayer.getPrimary()

                # Strip primary weapon
                if pWeapon:
                    if self.steamid[0:4] != 'BOT_':
                        es.remove(pPlayer.getWeaponIndex(pWeapon))
                    else:
                        es.server.queuecmd('es_xremove %s' \
                        % pPlayer.getWeaponIndex(pWeapon))

            # Is the weapon a secondary weapon?
            elif "weapon_%s" %self.weapon in list_sWeapons:

                # Get the secondary weapon name
                sWeapon = pPlayer.getSecondary()

                # Strip secondary weapon
                if sWeapon:
                    if self.steamid[0:4] != 'BOT_':
                        es.remove(pPlayer.getWeaponIndex(sWeapon))
                    else:
                        es.server.queuecmd('es_xremove %s' \
                        % pPlayer.getWeaponIndex(sWeapon))

        # Give the player their weapon if it is not a knife
        if self.weapon != 'knife':
            '''
            The method of using item_pickup is causing considerable/massive lag 
            on a live server.  Commented out for now, as it does no harm for 
            the time being.
            '''
            # Register wrongWeaponCheck to ensure that the correct 
            #  weapon was received
            es.addons.registerForEvent(self, 'item_pickup', 
            self.wrongWeaponCheck)
            
            # Give new weapon
            es.server.queuecmd('es_xgive %s %s' % (self.userid, 
            'weapon_%s' %self.weapon))
            
            gamethread.delayed(0.05, es.addons.unregisterForEvent, 
            (self, 'item_pickup'))
        # If the weapon is a knife or hegrenade, strip
        if self.weapon in ['knife', 'hegrenade']:
            self.strip()

        # Make them use the new weapon via es_xsexec
        # We use this because es.sexec is too fast in some cases.
        es.delayed(0, 'es_xsexec %s "use weapon_%s"' %(self.userid, 
        self.weapon))
        
        gamethread.delayed(0.05, self.noWeaponCheck)
    
    def noWeaponCheck(self):
        # Retrieve a playerlib.Player() instance
        pPlayer = getPlayer(self.userid)
        
        # Store the weapon you are holding in the weapon slot which your 
        #  level's weapon
        # should be in
        if "weapon_%s" %self.weapon in list_pWeapons:
            weapon = pPlayer.getPrimary()
            slot = '2'
        elif "weapon_%s" %self.weapon in list_sWeapons:
            weapon = pPlayer.getSecondary()
            slot = '1'
        else:
            return

        # If you have a weapon, return
        if weapon:
            return

        # Get the index of the last given entity
        int_lastgive = int(eventscripts_lastgive)

        # Repeat giveWeapon to re-strip the slot and give your weapon
        self.giveWeapon()

        # If there was no lastgive, return
        if not int_lastgive:
            return

        # If the last given entity is held by someone other than you
        owner = es.getindexprop(int_lastgive, 'CBaseEntity.m_hOwnerEntity')
        if owner != es.getplayerhandle(self.userid):
            userid = es.getuserid(owner)
            es.server.queuecmd('es_xsexec %s "use weapon_%s"' %(userid, 
            Player(userid).weapon))
            # If the weapon on the ground is the same as the weapon that was 
            #   dropped
            if es.createentitylist()[int_lastgive]['classname'] == \
            'weapon_' + self.weapon:
                # Remove the weapon
                es.remove(int_lastgive)

    def wrongWeaponCheck(self, event_var):
        '''
        Ensures the correct weapon is received, and if not, repeats giveWeapon
        '''
        item = event_var['item']

        # If this item_pickup was not for the user we want it to be for, return
        if int(event_var['userid']) != self.userid:
            return

        # Unregister wrongWeaponCheck, since we already caught the pickup
        gamethread.delayed(0, es.addons.unregisterForEvent, 
        (self, 'item_pickup'))

        # If the item picked up is the item you want, or a knife, return
        if event_var['item'] in [self.weapon, 'knife']:
            return

        # Format the item picked up, and the weapon the player is on
        weapon = 'weapon_%s' % item
        levelWeapon = 'weapon_%s' % self.weapon

        # Make sure that we only repeat giveWeapon if the item picked up
        # Is taking up the slot we need to receive our weapon in

        if weapon in list_pWeapons and levelWeapon in list_sWeapons:
            return

        if weapon in list_sWeapons and levelWeapon in list_pWeapons:
            return

        # Get the index of the last given entity
        int_lastgive = int(eventscripts_lastgive)

        # Repeat giveWeapon to re-strip the slot and give your weapon
        self.giveWeapon()

        # If there was no lastgive, return
        if not int_lastgive:
            return

        # If the last given entity was the extra weapon on the floor
        if es.getindexprop(int_lastgive, 'CBaseEntity.m_hOwnerEntity') == -1:
            # If the weapon on the ground is the same as the weapon that was 
            #   dropped
            if es.createentitylist()[int_lastgive]['classname'] == \
            'weapon_' + self.weapon:
                # Remove the weapon
                es.remove(int_lastgive)

    def give(self, weapon, useWeapon=0):
        '''
        Gives a player the specified weapon.
        Weapons given by this method will not be stripped by gg_dead_strip.
        '''
        # Check if the weapon is valid
        weapon = str(weapon).replace('weapon_', '')

        if weapon not in list_pWeapons + list_sWeapons + \
            ['hegrenade', 'flashbang', 'smokegrenade']:
                raise ValueError('Unable to give (%s): is not a valid weapon'
                    %weapon)

        # Add weapon to strip exceptions so gg_dead_strip will not 
        #   strip the weapon
        self.stripexceptions.append(weapon)

        # Delay removing the weapon long enough for gg_dead_strip to fire
        gamethread.delayed(0.1, self.stripexceptions.remove, (weapon))

        # Give the player the weapon
        cmd = 'es_xgive %s weapon_%s;' %(self.userid, weapon)

        if useWeapon:
            cmd += 'es_xsexec %s "use weapon_%s"' %(self.userid, weapon)

        es.server.queuecmd(cmd)

    def strip(self, fullStrip=False):
        '''
        Strips/removes all weapons from the player minus the knife and their
        current levels weapon. Unless True is specified, and their level weapon
        is also stripped.
        '''
        # Retrieve a playerlib.Player() instance
        pPlayer = getPlayer(self.userid)

        for weapon in pPlayer.getWeaponList():
            if ('weapon_%s' %self.weapon == weapon and not fullStrip) or \
            weapon == 'weapon_knife':
                continue

            # Remove the weapon
            es.server.cmd('es_xremove %s' %pPlayer.getWeaponIndex(weapon))

    def respawn(self):
        '''
        Respawns the player.
        '''
        # Check if the respawn command requires the "#" symbol
        if '#' not in str(gg_respawn_cmd):
            # Userids not requiring the "#" symbol
            es.server.queuecmd('%s %s' % (gg_respawn_cmd, self.userid))
        else:
            # SourceMod Workaround
            es.server.queuecmd('%s%s' % (gg_respawn_cmd, self.userid))

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
            # Get the uniqueid
            steamid = uniqueid(str(userid), 1)
            
            # Search for the player's uniqueid to see if they played previously
            if not steamid in [self[playerid].steamid for playerid in self]:
                self[userid] = BasePlayer(userid)
            else:
                for playerid in self.copy():
                    if self[playerid].steamid == steamid:
                        # Copy the BasePlayer() instance to the current userid
                        self[userid] = self[playerid]

                        # Delete the old BasePlayer() instance
                        del self[playerid]

                        # Set the BasePlayer() instance userid to the current
                        self[userid].userid = userid

                        # Set the BasePlayer() .AFK() instance userid
                        self[userid].afk.userid = userid

                        break

        # We don't want to call our __getitem__ again
        return super(PlayerDict, self).__getitem__(userid)

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

    
from gungame51.core.events.shortcuts import EventManager