# ../addons/eventscripts/gungame/core/players/__init__.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
# Python Imports
import random

# SPE Imports
from spe.games import cstrike

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
from gungame51.core.messaging import MessageManager
from gungame51.core.sound import SoundPack
from afk import AFK
from gungame51.core.leaders.shortcuts import LeaderManager

# ============================================================================
# >> GLOBALS
# ============================================================================
list_pWeapons = getWeaponNameList('#primary')
list_sWeapons = getWeaponNameList('#secondary')
eventscripts_lastgive = es.ServerVar('eventscripts_lastgive')
gg_respawn_cmd = es.ServerVar('gg_respawn_cmd')
recent_give_userids = []

# ============================================================================
# >> CLASSES
# ============================================================================
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
            raise AttributeError('Callback "%s" is not callable.' %function)

        if not self.has_key(attribute):
            self[attribute] = {}

        # Add or update the attribute callback
        self[attribute].update({addon:function})

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
        if not self[attribute].has_key(addon):
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


class BasePlayer(object):
    # =========================================================================
    # >> BasePlayer() CLASS INITIALIZATION
    # =========================================================================
    def __init__(self, userid): 
        self.userid = userid 
        self.preventlevel = PreventLevel()
        self.level = 1
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
        if CustomAttributeCallbacks().has_key(name):
            for function in CustomAttributeCallbacks()[name].values():
                function(name, value, self)

        # Are they setting the "level" attribute?
        if name == 'level':
            # Return if preventlevel is set
            if self.preventlevel:
                return
            else:
                # Set the attribute value
                object.__setattr__(self, name, value)
                LeaderManager().check(self)
        else:
            # Set the attribute value
            object.__setattr__(self, name, value)

    def __getattr__(self, name):
        # Return the attribute value
        return object.__getattribute__(self, name)

    def __delattr__(self, name):
        # Make sure we don't try to delete required GunGame attributes
        if name in ['userid', 'level', 'preventlevel', 'steamid', 'multikill']:
            raise AttributeError('Unable to delete attribute "%s". '
                % name + 'This is a required attribute for GunGame.')

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

    # =========================================================================
    # >> BasePlayer() MESSAGING CLASS METHODS
    # =========================================================================
    def msg(self, string, tokens={}, prefix=False):
        MessageManager().msg(self.userid, string, tokens, prefix)

    def saytext2(self, index, string, tokens={}, prefix=False):
        MessageManager().saytext2(self.userid, index, string, tokens, prefix)

    def centermsg(self, string, tokens={}):
        MessageManager().centermsg(self.userid, string, tokens)

    def hudhint(self, string, tokens={}):
        MessageManager().hudhint(self.userid, string, tokens)

    def toptext(self, duration, color, string, tokens={}):
        MessageManager().toptext(self.userid, duration, color, string, tokens)

    def echo(self, level, string, tokens={}, prefix=False):
        MessageManager().echo(self.userid, level, string, tokens, prefix)

    def langstring(self, string, tokens={}, prefix=False):
        return MessageManager().langstring(self.userid, string, tokens, prefix)

    # =========================================================================
    # >> BasePlayer() WEAPON CLASS METHODS
    # =========================================================================
    def getWeapon(self):
        return getLevelWeapon(self.level)

    def giveWeapon(self):
        '''
        Gives a player their current levels weapon.
        '''
        error = None
        # Make sure player is on a team
        if es.getplayerteam(self.userid) < 2:
            error = ('Unable to give player weapon (%s):' 
                % self.userid + ' is not on a team.')

        # Make sure player is alive
        elif getPlayer(self.userid).isdead:
            error = ('Unable to give player weapon (%s):' 
                % self.userid + ' is not alive.')
        
        # Error ?
        if error:
            # Was the player looping ?
            if self.userid in recent_give_userids:
                recent_give_userids.remove(userid)    
            
            raise GunGameError(error)
        
        # Knife ?
        elif self.weapon == 'knife':
            es.server.queuecmd('es_xsexec %i "use weapon_knife"' % (
                                                                self.userid))
            self.strip()                
        
        # Nade ?
        elif self.weapon == 'hegrenade':
            es.server.queuecmd('es_xgive %i weapon_hegrenade;' % (
                                                                self.userid))                                                        
            self.strip()
        
        # All other weapons 
        else:
            # Get player's weapons
            pPlayer = getPlayer(self.userid)
            pWeapon = pPlayer.getPrimary()
            sWeapon = pPlayer.getSecondary()
            strip = None
            
            # Already have the current weapon ?            
            if 'weapon_%s' % self.weapon == pWeapon or \
                'weapon_%s' % self.weapon == sWeapon:
                
                # Use it ?
                if pPlayer.weapon != self.weapon:
                    es.server.queuecmd('es_xsexec %s "use weapon_%s"' % (
                                                    self.userid, self.weapon))
                return            
            
            # Strip secondary weapon ?
            if 'weapon_%s' % self.weapon in list_sWeapons and sWeapon: 
                strip = sWeapon
            
            # Strip primary weapon ?
            elif 'weapon_%s' % self.weapon in list_pWeapons and pWeapon:
                strip = pWeapon
            
            if strip:
                # cstrike.removeEntityByIndex(pPlayer.getWeaponIndex(strip))
                es.server.queuecmd('es_xremove %s' % (
                                                pPlayer.getWeaponIndex(strip)))
                
                # Check for no weapon in 0.08 seconds
                gamethread.delayedname(0.08, 'gg_noweap_%i' % self.userid,
                                        Player(self.userid).noWeaponCheck, ())
            
            # Give new gun                           
            #cstrike.call("GiveItem", 
            #    cstrike.getPlayer(self.userid), 'weapon_%s' % self.weapon, 0)                       
            es.server.queuecmd('es_xgive %i weapon_%s' % (self.userid, 
                                                                self.weapon))
        
            # Make bots use it ? (Bots sometimes don't equip the new gun.)
            if es.isbot(self.userid):
                    es.delayed(0, 'es_xsexec %s "use weapon_%s"' % (
                                                    self.userid, self.weapon))                
            
            # Add the userid to the list ?
            if self.userid not in recent_give_userids:
                recent_give_userids.append(self.userid)
    
    def noWeaponCheck(self, newWeapon=None):
        # Retrieve a playerlib.Player() instance
        pPlayer = getPlayer(self.userid)
        # Store the weapon you are holding in the weapon slot which your 
        #  level's weapon
        # should be in
        if "weapon_%s" % self.weapon in list_pWeapons:
            weapon = pPlayer.getPrimary()
        elif "weapon_%s" % self.weapon in list_sWeapons:
            weapon = pPlayer.getSecondary()
        else:
            return

        # If you have a weapon, return
        if not weapon:

            # Using give() ?
            if newWeapon:
                self.give(weapon)

            # Repeat giveWeapon to re-strip the slot and give your weapon
            else:
                self.giveWeapon()

        # Get the index of the last given entity
        int_lastgive = int(eventscripts_lastgive)

        # If there was no lastgive, return
        if not int_lastgive:
            return

        # If the last given entity is held by someone other than you
        owner = es.getindexprop(int_lastgive, 'CBaseEntity.m_hOwnerEntity')

        if owner != es.getplayerhandle(self.userid):
            # Owner is a person ?
            if owner > -1:
                owner_userid = es.getuserid(owner)
                # Make the wrong owner use their own weapon ?
                if getPlayer(owner_userid).weapon != \
                    'weapon_%s' % Player(owner_userid).weapon: 
                    es.server.queuecmd('es_xsexec %s "use weapon_%s"' % (
                        owner_userid, Player(owner_userid).weapon))
            
            # If the weapon is the same as the weapon that was dropped
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
        weapon = weapon.replace('weapon_', '')
        
        if 'weapon_%s' % weapon not in list_pWeapons + list_sWeapons + \
        ['weapon_hegrenade', 'weapon_flashbang', 'weapon_smokegrenade']:
            raise ValueError('Unable to give (%s): ' % weapon +
                             'is not a valid weapon')

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

    def strip(self, levelStrip=False, exceptions=[]):
        '''
            * Strips/removes all weapons from the player minus the knife and 
              their current levels weapon. 
        
            * If True is specified, then their level weapon is also stripped.
        
            * Exceptions can be entered in list format, and anything in the
              exceptions will not be stripped.                       
        '''
        # Retrieve a playerlib.Player() instance
        pPlayer = getPlayer(self.userid)

        for weapon in pPlayer.getWeaponList():
            if (self.weapon == weapon[7:] and not levelStrip) or \
            weapon == 'weapon_knife' or weapon[7:] in exceptions:
            
                continue

            # Remove the weapon
            es.server.cmd('es_xremove %s' %pPlayer.getWeaponIndex(weapon))

    # =========================================================================
    # >> BasePlayer() MISCELLANEOUS CLASS METHODS
    # =========================================================================
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

    # =========================================================================
    # >> BasePlayer() SOUND CLASS METHODS
    # =========================================================================
    def playsound(self, sound, volume=1.0):
        '''
        Plays the declared sound to the player.
        '''
        # Format the sound
        sound = self._format_sound(sound)
        
        # Make sure the sound exists
        if sound:
            # Play the sound
            es.playsound(self.userid, sound, volume)

    def emitsound(self, sound, volume=1.0, attenuation=0.0):
        '''
        Emits the declared sound from the player.
        '''
        # Format the sound
        sound = self._format_sound(sound)
        
        # Make sure the sound exists
        if sound:
            # Play the sound
            es.emitsound('player', self.userid, sound, volume, attenuation)
    
    def stopsound(self, sound):
        '''
        Plays the declared sound to the player.
        '''
        # Format the sound
        sound = self._format_sound(sound)
        
        # Make sure the sound exists
        if sound:
            # Play the sound
            es.stopsound(self.userid, sound)

    def _format_sound(self, sound):
        if not self.soundpack[sound]:
            return sound
        return self.soundpack[sound]


class PlayerDict(dict):
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
        return PlayerDict()[self.userid][item]

    def __setitem__(self, item, value):
        # We only directly allow the attribute "userid" to be set
        PlayerDict()[self.userid][item] = value

    def __getattr__(self, name):
        if name == 'userid':
            # We only directly allow the attribute "userid" to be retrieved
            object.__getattr__(self, name)
        else:
            # Redirect to the PlayerDict instance
            return PlayerDict()[self.userid][name]

    def __setattr__(self, name, value):
        if name == 'userid':
            # We only directly allow the attribute "userid" to be set
            object.__setattr__(self, name, value)
        else:
            # Redirect to the PlayerDict instance
            PlayerDict()[self.userid][name] = value

    def __delitem__(self, name):
        # Redirect to the PlayerDict instance
        del PlayerDict()[self.userid][name]

    def __delattr__(self, name):
        # Redirect to the PlayerDict instance
        del PlayerDict()[self.userid][name]

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
        CustomAttributeCallbacks().add(attribute, function, addon)

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
        CustomAttributeCallbacks().remove(attribute)

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
        for attribute in CustomAttributeCallbacks().keys():
            # Continue to the next attribute if the addon name is not found
            if not addon in CustomAttributeCallbacks()[attribute]:
                continue

            # Remove the custom attribute callback
            CustomAttributeCallbacks().remove(attribute, addon)

'''>> Note to Devs:
        This actually does not seem to be working, but then again, it also
        does not seem to be needed...  I will look into this soon.
            (item_pickup)
        
                        - Monday
'''
def item_pickup(event_var):
    userid = int(event_var['userid'])
    ggPlayer = Player(userid)
    # lastgive = int(eventscripts_lastgive)
    
    # Stop noWeapon() check?
    if 'gg_noweap_%i' % userid in gamethread.listDelayed():
        gamethread.cancelDelayed('gg_noweap_%i' % userid)    
    
    # Was a knife ?
    if 'knife' == event_var['item']:
        return
            
    # We checking this player ?
    if userid not in recent_give_userids:
        return
        
    # Player got what they needed ?
    if ggPlayer.weapon == event_var['item']:

        # Use it ?
        if getPlayer(userid).weapon != 'weapon_%s' % ggPlayer.weapon:
            es.server.queuecmd('es_xsexec %s "use weapon_%s"' % (userid, 
                                                            ggPlayer.weapon))            
        # Remove from list and stop
        recent_give_userids.remove(userid)
        return    
    
    # Weapon iterator
    witr = ['weapon_%s' % ggPlayer.weapon, 'weapon_%s' % event_var['item']]
    
    #   Did the player pick up a weapon that takes up the gungame weapon  
    #   slot? Is so, the player is given another weapon, and the one that 
    #   was picked up is striped in giveWeapon()      
    if all([(x in list_sWeapons) for x in wpn_iter]) or \
                all([(x in list_pWeapons) for x in wpn_iter]):
        ggPlayer.giveWeapon()
    
from gungame51.core.events.shortcuts import EventManager