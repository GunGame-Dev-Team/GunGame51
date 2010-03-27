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

# SPE Imports
# Import SPE if installed
try:
    import spe
except ImportError:
    raise ImportError('SPE Is not installed on this server! Please visit ' +
        'http://forums.eventscripts.com/viewtopic.php?t=29657 and download ' +
        'the latest version!')

# GunGame Imports
from gungame51.core.weapons.shortcuts import get_level_weapon
from gungame51.core import getOS
from gungame51.core import GunGameError
from gungame51.core.messaging import MessageManager
from gungame51.core.sound import SoundPack
from gungame51.core.leaders.shortcuts import LeaderManager
from gungame51.core.sql import Database
from gungame51.core.sql.shortcuts import insert_winner
from gungame51.core.sql.shortcuts import update_winner
from afk import AFK

# ============================================================================
# >> GLOBALS
# ============================================================================
list_pWeapons = getWeaponNameList('#primary')
list_sWeapons = getWeaponNameList('#secondary')
list_allWeapons = getWeaponNameList()
eventscripts_lastgive = es.ServerVar('eventscripts_lastgive')
gg_soundpack = es.ServerVar('gg_soundpack')

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
    def __new__(cls, userid):
        self = object.__new__(cls, userid)
        self.userid = int(userid)
        self.steamid = uniqueid(self.userid, 1)
        self.afk = AFK(self.userid)
        self.index = int(getPlayer(str(self.userid)).index)
        return self
    
    def __init__(self, userid):
        self.preventlevel = PreventLevel()
        self.level = 1
        self.multikill = 0
        self.stripexceptions = []
        self.ownedWeapons = []
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
                #from spe.games import cstrike
                import spe

            # No SPE ?
            except ImportError:

                # Move the player in a very basic manner
                es.changeteam(self.userid, value)

                # Raise error, and request for SPE to be installed.
                raise ImportError('SPE Is not installed on this server! ' +
                        'Please visit http://forums.eventscripts.com/viewtop' +
                        'ic.php?t=29657 and download the latest version!')

            # Change the team
            # With the latest SPE, you no longer have to import 
            # cstrike manually. Just do spe.<moduleFunction>!
            spe.switchTeam(self.userid, value)
            
            #cstrike.switchTeam(self.userid, value)

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
            # Has won before
            if self.wins:
                update_winner('wins', value, uniqueid=self.steamid)

            # New entry
            else:
                name = es.getplayername(self.userid)

                if not name:
                    name = "unnamed"

                insert_winner(name, self.steamid, value)
            return

        # Set the attribute value
        object.__setattr__(self, name, value)

    def __getattr__(self, name):

        # Team ?
        if name == 'team':
            return es.getplayerteam(self.userid)

        # From winners DB?
        if name == 'wins':
            winsQuery = Database().select('gg_wins', 'wins',
                                    'where uniqueid = "%s"' % self.steamid)

            if winsQuery:
                return int(winsQuery)

            return 0

        # Return the attribute value
        return object.__getattribute__(self, name)

    def __delattr__(self, name):
        # Make sure we don't try to delete required GunGame attributes
        if name in ('userid', 'level', 'preventlevel', 'steamid', 'soundpack',
          'stripexceptions', 'ownedWeapons', 'multikill', 'wins', 'team', 
                                                    'name', 'index', 'afk'):
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
        return MessageManager().langstring(string, tokens, self.userid, prefix)

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
            # Make them use their knife
            es.server.queuecmd('es_xsexec %s "use weapon_knife"' % (
                                                                self.userid))

            # If there is a level below the user's current level
            if self.level > 1:
                # Strip previous weapons
                self.strip_weapons(get_level_weapon(self.level - 1))
            else:
                self.strip()

        # Nade ?
        elif self.weapon == 'hegrenade':
            # Give them a grenade.
            given_weapon = spe.giveNamedItem(self.userid, "weapon_hegrenade")

            # Make them use the grenade
            es.server.queuecmd('es_xsexec %s "use weapon_hegrenade"' % (
                                                                self.userid))

            # If there is a level below the user's current level
            if self.level > 1:
                # Strip previous weapons
                self.strip_weapons(get_level_weapon(self.level - 1))
            else:
                self.strip()

        else:
            # Player owns this weapon.
            if spe.ownsWeapon(self.userid, "weapon_%s" % self.weapon):
                # Make them use it. If we don't do this, a very 
                # strange bug comes up which prevents the player 
                # from getting their current level's weapon after
                # being stripped,
                es.server.queuecmd('es_xsexec %s "use weapon_%s"' 
                    % (self.userid, self.weapon))

                # Done.
                return

            # Player DOES NOT own this weapon.
            else:
                # Retrieve a list of all weapon names in the player's
                # possession
                playerWeapons = spe.getWeaponDict(self.userid)

                if playerWeapons:
                    # See if there is a primary weapon in the list of weapons
                    pWeapon = set(playerWeapons.keys()).intersection(
                                                                list_pWeapons)

                    # See if there is a primary weapon in the list of weapons
                    sWeapon = set(playerWeapons.keys()).intersection(
                                                                list_sWeapons)

                    # Set up the weapon to strip
                    weapToStrip = None

                    # Strip secondary weapon ?
                    if 'weapon_%s' % self.weapon in list_sWeapons and sWeapon:
                        weapToStrip = sWeapon.pop()

                    # Strip primary weapon ?
                    elif 'weapon_%s' % self.weapon in list_pWeapons and \
                                                                    pWeapon:
                        weapToStrip = pWeapon.pop()

                    if weapToStrip:
                        # Make them drop the weapon
                        spe.dropWeapon(self.userid, weapToStrip)

                        # Now remove it
                        gamethread.delayed(0, spe.removeEntityByInstance,
                                    (playerWeapons[weapToStrip]["instance"]))

                # Now give them the weapon and save the weapon instance
                given_weapon = spe.giveNamedItem(self.userid,
                    "weapon_%s" % self.weapon)

                # Retrieve the weapon instance of the weapon they "should" own
                weapon_check = spe.ownsWeapon(self.userid, "weapon_%s"
                    % self.weapon)

                # Make sure that the player owns the weapon we gave them
                if weapon_check != given_weapon:
                    # Remove the given weapon since the player does not own it
                    gamethread.delayed(0, spe.removeEntityByInstance, (
                                                                given_weapon))

                    # If they don't have the right weapon, fire give_weapon()
                    if not weapon_check:
                        self.give_weapon()
                        return

                # If gg_dead_strip is loaded, we need to keep track of which
                # weapons the player has so that they can be removed whent he
                # player dies
                if int(es.ServerVar('gg_dead_strip')):
                    gamethread.delayed(0, self.update_owned_weapons)

                es.server.queuecmd('es_xsexec %s "use weapon_%s"' 
                    % (self.userid, self.weapon))

    def give(self, weapon, useWeapon=False, strip=False):
        '''
        Gives a player the specified weapon.
        Weapons given by this method will not be stripped by gg_dead_strip.

        Setting strip to True will make it strip the weapon currently
        held in the slot you are trying to give to.
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


        # If the player owns the weapon and the player is not being given a
        # second flashbang, stop here
        if spe.ownsWeapon(self.userid, weapon) and not (weapon == \
                    "weapon_flashbang" and getPlayer(self.userid).getFB() < 2):
            return

        # Strip the weapon ?
        if strip:
            # Retrieve a list of all weapon names in the player's possession
            playerWeapons = spe.getWeaponDict(self.userid)

            if playerWeapons:
                # See if there is a primary weapon in the list of weapons
                pWeapon = set(playerWeapons.keys()).intersection(list_pWeapons)

                # See if there is a primary weapon in the list of weapons
                sWeapon = set(playerWeapons.keys()).intersection(list_sWeapons)

                stripWeapon = None

                # Holding a primary weapon ?
                if weapon in list_pWeapons and pWeapon:
                    stripWeapon = pWeapon.pop()

                # Holding a secondary weapon ?
                elif weapon in list_sWeapons and sWeapon:
                    stripWeapon = sWeapon.pop()

                # Strip the weapon
                if stripWeapon:
                    # Make them drop the weapon
                    spe.dropWeapon(self.userid, stripWeapon)

                    # Remove the weapon
                    gamethread.delayed(0, spe.removeEntityByInstance, (
                                    playerWeapons[stripWeapon]["instance"]))

        # Give the player the weapon
        spe.giveNamedItem(self.userid, weapon)
        
        # If gg_dead_strip is loaded, we need to keep track of which weapons
        # the player has so that they can be removed whent he player dies
        if int(es.ServerVar('gg_dead_strip')):
            gamethread.delayed(0, self.update_owned_weapons)

        if useWeapon:
            es.server.queuecmd('es_xsexec %s "use %s"' % (self.userid, weapon))

    def update_owned_weapons(self):
        # Set the ownedWeapons list to empty
        self.ownedWeapons = []

        # Get the list of the player's weapons
        playerWeapons = spe.getWeaponDict(self.userid)

        # If playerWeapons returned None, stop here
        if not playerWeapons:
            return

        # For each weapon the player owns
        for weapon in playerWeapons:
            # If the weapon is a knife, c4, or not a real weapon, stop here
            if not weapon in list_allWeapons or weapon[7:] in \
                                                            ["knife", "c4"]:
                continue

            # Add the weapon's index to the ownedWeapons list so that it can
            # be removed when the player dies with gg_dead_strip enabled
            self.ownedWeapons.append(playerWeapons[weapon]["index"])

    def strip(self, levelStrip=False, exceptions=[]):
        '''
            * Strips/removes all weapons from the player minus the knife and
              their current levels weapon.

            * If True is specified, then their level weapon is also stripped.

            * Exceptions can be entered in list format, and anything in the
              exceptions will not be stripped.
        '''
        # Retrieve a dictionary of the player's weapons
        pWeapons = spe.getWeaponDict(self.userid)

        if not pWeapons:
            return

        for weapon in pWeapons:
            if (self.weapon == weapon[7:] and not levelStrip) or \
              weapon == 'weapon_knife' or weapon[7:] in exceptions:

                continue

            spe.dropWeapon(self.userid, weapon)
            gamethread.delayed(0, spe.removeEntityByInstance, 
                                                (pWeapons[weapon]["instance"]))

    def strip_weapons(self, stripWeapons):
        '''
        Strips a list of weapons from a player. (Used primarily for selective
            weapon removal when a player gets a new weapon)
        stripWeapons must be a list.
        '''
        # Get the player's current held weapons
        playerWeapons = spe.getWeaponDict(self.userid)

        # Loop through any weapons to strip
        for stripWeapon in stripWeapons:
            weapToStrip = None
            stripWeapon = "weapon_%s" % stripWeapon

            # If the player does not own the weapon, stop here
            if not stripWeapon in playerWeapons:
                continue

            # If the weapon to strip is primary or secondary, set it up to be
            # stripped
            if stripWeapon in list_pWeapons or stripWeapon in list_sWeapons:
                weapToStrip = stripWeapon

            # If stripWeapon is a grenade, and the player is has it,
            # set it up to be stripped
            elif stripWeapon == "weapon_hegrenade" and \
                                        "weapon_hegrenade" in playerWeapons:
                weapToStrip = stripWeapon
            elif stripWeapon == "weapon_flashbang" and \
                                                getPlayer(self.userid).getFB():
                weapToStrip = stripWeapon
            elif stripWeapon == "weapon_smokegrenade" and \
                                        "weapon_smokegrenade" in playerWeapons:
                weapToStrip = stripWeapon

            # Did we find a weapon to strip ?
            if weapToStrip:
                # Drop and remove the weapon
                spe.dropWeapon(self.userid, weapToStrip)
                gamethread.delayed(0, spe.removeEntityByInstance,
                                    (playerWeapons[weapToStrip]["instance"]))

    # =========================================================================
    # >> BasePlayer() MISCELLANEOUS CLASS METHODS
    # =========================================================================
    def respawn(self, force=False):
        '''
        Respawns the player.
        '''
        # Player on server ?
        if not es.exists('userid', self.userid):
            return

        # Player in spec ?
        if self.team == 1:
            return

        # Player alive? (require force)
        if not getPlayer(self.userid).isdead and not force:
            return
            
        spe.respawn(self.userid)

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

    def emitsound(self, sound, volume=1.0, attenuation=1.0):
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
                    ' instance for userid "%s".' %userid)

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


from gungame51.core.events.shortcuts import EventManager