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
from random import choice
from random import randint

# EventScripts Imports
import es
import gamethread
from playerlib import uniqueid
from playerlib import getPlayer
from weaponlib import getWeaponNameList
from usermsg import showVGUIPanel

# GunGame Imports
from gungame51.core.weapons.shortcuts import get_level_weapon
from gungame51.core.weapons.shortcuts import get_level_multikill
from gungame51.core import getOS
from gungame51.core import GunGameError
from gungame51.core.messaging import MessageManager
from gungame51.core.sound import SoundPack
from gungame51.core.leaders.shortcuts import LeaderManager
from gungame51.core.sql import Database
from afk import AFK

# ============================================================================
# >> GLOBALS
# ============================================================================
list_pWeapons = getWeaponNameList('#primary')
list_sWeapons = getWeaponNameList('#secondary')
eventscripts_lastgive = es.ServerVar('eventscripts_lastgive')
gg_respawn_cmd_override = es.ServerVar('gg_respawn_cmd_override')

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
        self.index = int(getPlayer(str(self.userid)).index)
        self.stripexceptions = []
        self.soundpack = SoundPack('default')
        self.name = getPlayer(self.userid).name

    # =========================================================================
    # >> BasePlayer() CLASS ATTRIBUTE METHODS
    # =========================================================================
    @property
    def weapon(self):
        '''
        Return the weapon name
        '''
        return self.get_weapon()

    @property
    def steamid(self):
        '''
        This was done because playerlib will throw an error for bots from
        time to time
        '''
        try:
            _steamid = uniqueid(str(self.userid), 1)
        except:
            _steamid = None
        return _steamid

    def __setattr__(self, name, value):
        # First, we execute the custom attribute callbacks
        if CustomAttributeCallbacks().has_key(name):
            for function in CustomAttributeCallbacks()[name].values():
                function(name, value, self)

        # Are they setting the "level" attribute?
        if name == 'level':
            # Return if preventlevel is set
            if not self.preventlevel:
                # Set the attribute value
                object.__setattr__(self, name, value)
                LeaderManager().check(self)
            return

        '''
        Player(userid).team is just the same as es.getplayerteam(userid)
        Player(userid).team = 1 move player to spec
        Player(userid).team = 2 move player to terrorist
        Player(userid).team = 3 move player to counter-terrorist

        * Dead players will be moved using es.changeteam()
        * Alive players will be moved using SPE
        '''

        # Team change
        if name == 'team':
            if not es.exists('userid', self.userid):
                raise ValueError('userid (%s) doesn\'t exist.' % self.userid)

            # Is the value a int ?
            if not str(value).isdigit():

                # Other CT values
                if value in ('ct', '#ct'):
                    value = 3

                # Other T values
                elif value in ('t', '#t'):
                    value = 2

                # Raise error
                else:
                    raise ValueError('"%s" is an invalid team' % value)

            # Is the value in range ?
            elif int(value) not in range(1,4):
                raise ValueError('"%s" is an invalid teamid' % value)

            pPlayer = getPlayer(self.userid)
            value = int(value)

            # Make sure we are not moving the player to the same team
            if pPlayer.teamid == value:
                return

            # If the player is dead, use es.changeteam()
            elif pPlayer.isdead:
                es.changeteam(self.userid, value)

                # going to spectator ?
                if value == 1:
                    return

                # Terrorist ?
                if value == 2:
                    iClass = randint(1,4)
                    menuname = 'class_ter'

                # Counter-Terrorist ?
                else:
                    iClass = randint(4,8)
                    menuname = 'class_ct'

                # Set prop & hide vgui
                es.setplayerprop(self.userid, 'CCSPlayer.m_iClass', iClass)
                showVGUIPanel(self.userid, menuname, False, {})

                # If player is a bot, kill him
                if es.isbot(self.userid):
                    es.server.queuecmd('es_xsexec %s kill' % self.userid)
                return

            # Import SPE if installed
            try:
                from spe.games import cstrike

            # No SPE ?
            except ImportError:

                # Move the player in a very basic manner
                es.changeteam(self.userid, value)

                # Raise error, and request for SPE to be installed.
                raise ImportError('SPE Is not installed on this server! ' +
                        'Please visit http://forums.eventscripts.com/viewtop' +
                        'ic.php?t=29657 and download the latest version!')

            # Change the team
            cstrike.switchTeam(self.userid, value)

            # Change the model
            if value == 1:
                return

            # Terrorist Models
            if int(value) == 2:
                pPlayer.model = 'player/%s' \
                    % choice(('t_arctic', 't_guerilla', 't_leet', 't_phoenix'))

            # Counter-Terrorist Models
            else:
                pPlayer.model = 'player/%s' \
                    % choice(('ct_gign', 'ct_gsg9', 'ct_sas', 'ct_urban'))
            return

        '''
        Player(userid).wins returns the amount of wins a player has
            * If they are not in the DB it will return 0

        Player(userid).wins += 1 The prefered method of adding a win

        Player(userid).wins = # You may also change the wins setting to a
          value of your choice, although this method should only be used for
          internal ussage.
        '''

        # From winner's DB ?
        if name == 'wins':
            # We using a int?
            if not str(value).isdigit():
                raise ValueError('wins has to be a int value, you passed ' +
                                '"%s"' % value)

            # Bots can't win
            if es.isbot(self.userid):
                return

            value = int(value)
            ggDB = Database()

            # Has won before
            if self.wins:
                ggDB.query("UPDATE gg_wins SET wins=%s " % value +
                           "WHERE uniqueid = '%s'" % self.steamid)

            # New entry
            else:
                ggDB.query("INSERT INTO gg_wins " +
                    "(name, uniqueid, wins, timestamp) " +
                    "VALUES ('%s', '%s', '%s', strftime('%s','now'))" %
                    (self.name, self.steamid, value, '%s'))

            ggDB.commit()
            return

        # Set the attribute value
        object.__setattr__(self, name, value)

    def __getattr__(self, name):

        # Team ?
        if name == 'team':
            return es.getplayerteam(self.userid)

        # From winners DB?
        if name == 'wins':
            _query = Database().select('gg_wins', 'wins',
                                    "where uniqueid = '%s'" % self.steamid)

            if _query:
                return int(_query)

            return 0

        # Return the attribute value
        return object.__getattribute__(self, name)

    def __delattr__(self, name):
        # Make sure we don't try to delete required GunGame attributes
        if name in ('userid', 'level', 'preventlevel', 'steamid', 'soundpack',
          'stripexceptions', 'multikill', 'wins', 'team', 'name', 'index',
                                                                        'afk'):
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
    def get_weapon(self):
        return get_level_weapon(self.level)

    def give_weapon(self):
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
            raise GunGameError(error)

        # Knife ?
        if self.weapon == 'knife':
            es.server.queuecmd('es_xsexec %s "use weapon_knife"' % (
                                                                self.userid))
            self.strip()

        # Nade ?
        elif self.weapon == 'hegrenade':
            es.server.queuecmd('es_xgive %s weapon_hegrenade;' % (
                                                                self.userid))
            self.strip()

        # All other weapons
        else:
            # Get player's weapons
            pPlayer = getPlayer(self.userid)
            pWeapon = pPlayer.getPrimary()
            sWeapon = pPlayer.getSecondary()
            weapToStrip = None

            # Already have the current weapon ?
            if 'weapon_%s' % self.weapon == pWeapon or \
                'weapon_%s' % self.weapon == sWeapon:

                # Use it ?
                if pPlayer.weapon != 'weapon_%s' % self.weapon:
                    es.server.queuecmd('es_xsexec %s "use weapon_%s"' % (
                                                    self.userid, self.weapon))
                return

            # Strip secondary weapon ?
            if 'weapon_%s' % self.weapon in list_sWeapons and sWeapon:
                weapToStrip = sWeapon

            # Strip primary weapon ?
            elif 'weapon_%s' % self.weapon in list_pWeapons and pWeapon:
                weapToStrip = pWeapon

            if weapToStrip:
                es.server.queuecmd('es_xremove %s' % (
                                          pPlayer.getWeaponIndex(weapToStrip)))

                # Check for no weapon in 0.05 seconds
                gamethread.delayed(0.05, Player(self.userid).no_weapon_check)

            # Give new gun
            es.server.queuecmd('es_xgive %s weapon_%s' % (self.userid,
                                                                self.weapon))

            # Make bots use it ? (Bots sometimes don't equip the new gun.)
            if es.isbot(self.userid):
                    es.delayed(0.25, 'es_xsexec %s "use weapon_%s"' % (
                                                    self.userid, self.weapon))

    def no_weapon_check(self, newWeapon=None):
        # Retrieve a playerlib.Player() instance
        pPlayer = getPlayer(self.userid)

        # Stop if the player is not eligiable for a new weapon
        if es.exists('userid', self.userid) or pPlayer.isdead or \
          pPlayer.teamid < 2:
            return

        # Store the weapon you are holding in the weapon slot which your
        #  level's weapon should be in

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
                self.give(newWeapon)
                return

            # Repeat give_weapon to re-strip the slot and give your weapon
            gamethread.delayed(0.025, Player(self.userid).give_weapon)

        # Get the index of the last given entity
        int_lastgive = int(eventscripts_lastgive)

        # If there was no lastgive, return
        if not int_lastgive:
            return

        # If the last given entity is held by someone other than you
        owner = es.getindexprop(int_lastgive, 'CBaseEntity.m_hOwnerEntity')

        if owner != es.getplayerhandle(self.userid):
            # Owner is a person ?
            if owner > 0:
                owner_userid = es.getuserid(owner)
                # Make the wrong owner use their own weapon ?
                if getPlayer(owner_userid).weapon != \
                    'weapon_%s' % Player(owner_userid).weapon:
                    es.server.queuecmd('es_xsexec %s "use weapon_%s"' % (
                        owner_userid, Player(owner_userid).weapon))

            # Make sure index is still existing
            if not es.createentitylist().has_key(int_lastgive):
                return

            # If the weapon is the same as the weapon that was dropped
            if es.createentitylist()[int_lastgive]['classname'] == \
                                                    'weapon_' + self.weapon:

                # Remove the weapon
                es.server.queuecmd('es_xremove %s' % int_lastgive)

    def give(self, weapon, useWeapon=False, strip=False, noWeaponCheck=False):

        '''
        Gives a player the specified weapon.
        Weapons given by this method will not be stripped by gg_dead_strip.

        Setting strip to True will make it strip the weapon currently
        held in the slot you are trying to give to.

        Setting no_weapon_check to True will make give() preform alot like
        give_weapon() It will verify the weapon was not delivered to the wrong
        player, and that the correct player ends up with the weapon you give.
        '''

        # Format weapon
        weapon = 'weapon_%s' % str(weapon).replace('weapon_', '')

        # Check if weapon is valid
        if weapon not in list_pWeapons + list_sWeapons + \
        ['weapon_hegrenade', 'weapon_flashbang', 'weapon_smokegrenade']:
            raise ValueError('Unable to give "%s": ' % weapon[7:] +
                             'is not a valid weapon')

        # Add weapon to strip exceptions so gg_dead_strip will not
        #   strip the weapon
        if int(es.ServerVar('gg_dead_strip')):
            self.stripexceptions.append(weapon[7:])

            # Delay removing the weapon long enough for gg_dead_strip to fire
            gamethread.delayed(0.10, self.stripexceptions.remove, (weapon[7:]))

        pPlayer = getPlayer(self.userid)
        sWeapon = pPlayer.secondary
        pWeapon = pPlayer.primary

        # Player allready has weapon ?
        if weapon in [sWeapon, pWeapon]:
            return

        # Strip the weapon ?
        if strip:
            stripWeapon = None

            # Holding a primary weapon ?
            if weapon in list_pWeapons and pWeapon:
                stripWeapon = pWeapon

            # Holding a secondary weapon ?
            elif weapon in list_sWeapons and sWeapon:
                stripWeapon = sWeapon

            # Strip the weapon
            if stripWeapon:
                es.server.queuecmd('es_xremove %s' % (
                                          pPlayer.getWeaponIndex(stripWeapon)))

        # Give the player the weapon
        cmd = 'es_xgive %s %s;' % (self.userid, weapon)

        if useWeapon:
            cmd += ' es_xsexec %s "use %s"' % (self.userid, weapon)

        es.server.queuecmd(cmd)

        # No weapon check
        if noWeaponCheck:
            gamethread.delayed(0.065, Player(self.userid).no_weapon_check,
                                                                        weapon)

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
    def respawn(self, force=False):
        '''
        Respawns the player.
        '''
        if str(gg_respawn_cmd_override) in ('', '0'):
            # Import SPE if installed
            try:
                from spe.games import cstrike

            except ImportError:
                raise ImportError('SPE Is not installed on this server! ' +
                        'Please visit http://forums.eventscripts.com/viewtop' +
                        'ic.php?t=29657 and download the latest version!')

            # Player on server ?
            if not es.exists('userid', self.userid):
                return

            # Player in spec ?
            if self.team == 1:
                return

            # Player alive? (require force)
            if not getPlayer(self.userid).isdead and not force:
                return
                
            cstrike.respawn(self.userid)

        # Check if the respawn command requires the "#" symbol
        elif '#' not in str(gg_respawn_cmd_override):
            # Userids not requiring the "#" symbol
            es.server.queuecmd('%s %s' % (gg_respawn_cmd_override,
                                                                  self.userid))
        else:
            # SourceMod Workaround
            es.server.queuecmd('%s%s' % (gg_respawn_cmd_override, self.userid))

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

    # =========================================================================
    # >> Winner's Database methods
    # =========================================================================
    def database_update(self):
        '''
        Updates the time and the player's name in the database
        '''
        if self.wins:
            ggDB = Database()
            ggDB.query("UPDATE gg_wins SET " +
                       "timestamp=strftime('%s','now'), " +
                       "name='%s' " % self.name +
                       "WHERE uniqueid = '%s'" % self.steamid)
            ggDB.commit()

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

from gungame51.core.events.shortcuts import EventManager