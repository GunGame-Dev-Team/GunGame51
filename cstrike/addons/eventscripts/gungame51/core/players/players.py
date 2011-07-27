# ../core/players/players.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# EventScripts Imports
import es as _es
from playerlib import getPlayer as _getPlayer
from weaponlib import getWeaponList as _getWeaponList

# SPE
import spe as _spe

# GunGame Imports
#   Player Module
from afk import AFK
from callbacks import PlayerCallbacks
from fields import *
from levels import PlayerLevels
from messaging import PlayerMessaging
from sounds import PlayerSounds
from weapons import PlayerWeapons
from winners import PlayerWins
from . import _PlayerMeta
from . import CustomAttributeCallbacks
#   Sound Module
from gungame51.core.sound import SoundPack


# =============================================================================
# >> GLOBALS
# =============================================================================
_VALID_WEAPONS = _getWeaponList('#all')
gg_soundpack = _es.ServerVar('gg_soundpack')


# =============================================================================
# >> CLASSES
# =============================================================================
class UseridError(Exception):
    pass


class PreventLevel(dict):
    class PreventLevelAddons(list):
        def append(self, addon):
            list.append(self, addon)

        def extend(self, addons):
            list.extend(self, addons)

        def insert(self, index, addon):
            self.append(addon)

        def remove(self, addon):
            if addon in self:
                list.remove(self, addon)

    def __init__(self):
        self['levelup'] = self.PreventLevelAddons()
        self['leveldown'] = self.PreventLevelAddons()

    def __call__(self):
        return self['levelup'] + self['leveldown']

    def append(self, addon):
        self['levelup'].append(addon)
        self['leveldown'].append(addon)

    def extend(self, addons):
        self['levelup'].extend(addons)
        self['leveldown'].extend(addons)

    def insert(self, index, addon):
        self['levelup'].insert(index, addon)
        self['leveldown'].insert(index, addon)

    def remove(self, addon):
        self['levelup'].remove(addon)
        self['leveldown'].remove(addon)

    @property
    def levelup(self):
        return self['levelup']

    @property
    def leveldown(self):
        return self['leveldown']


class StripExceptions(list):
    def append(self, weapon):
        weapon = self.format_weapon(weapon)
        list.append(self, weapon)

    def extend(self, weapons):
        weapons = [self.format_weapon(x) for x in weapons]
        list.extend(self, weapons)

    def insert(self, index, weapon):
        weapon = self.format_weapon(weapon)
        self.append(weapon)

    def remove(self, weapon):
        weapon = self.format_weapon(weapon)
        if weapon in self:
            list.remove(self, weapon)

    def format_weapon(self, weapon):
        weapon = str(weapon)
        if not weapon.startswith('weapon_'):
            weapon = "weapon_%s" % weapon
        if not self.is_valid(weapon):
            raise ValueError('"%s" is not a valid weapon.' % weapon)
        return weapon[7:]

    def is_valid(self, weapon):
        return weapon in _VALID_WEAPONS


class _PlayerContainer(dict):
    """(PRIVATE) A class-based dictionary that contains instances of
    Player. This dictionary stores and retrieves players based on their userid.

    """
    def __new__(cls, *p, **k):
        # There can be only one (singleton)
        if not '_the_instance' in cls.__dict__:
            cls._the_instance = dict.__new__(cls)
        return cls._the_instance

    def __getitem__(self, userid):
        try:
            userid = int(userid)
        except (ValueError, TypeError):
            raise UseridError('The userid "%s" is invalid.' % userid)

        # Retrieve or create the Player() instance
        if userid not in self:
            if not _es.exists('userid', userid):
                raise UseridError('Unable to retrieve or create a player' +
                                  ' instance for userid "%s". ' % userid +
                                  'The userid can not be found on the server.')

            # Search for the UniqueID/SteamID
            pInstance = self._find_by_uniqueid(userid)

            # If no matches create a new key, otherwise copy the instance
            if not pInstance:
                self[userid] = _BasePlayer(userid)
            else:
                self._copy_player_instance(userid, pInstance)

        return super(_PlayerContainer, self).__getitem__(userid)

    def _find_by_uniqueid(self, userid):
        """Search for the player's uniqueid to see if they played previously
        in this round. If a match is found, the Player instance is returned. If
        no match is found, None is returned.

        """
        # Retrieve the UniqueID
        steamid = _getPlayer(userid).uniqueid(True)

        # Perform the search
        search = [self[x] for x in self.copy() if self[x].steamid == steamid]

        # Return the Player() instance or None
        if search:
            return search.pop()
        return None

    def _copy_player_instance(self, userid, pInstance):
        """Copies the old _BasePlayer instance to the new userid key, then
        deletes they old userid key, and updates the new instance values.

        """
        # Initialize a new _BasePlayer instance
        self[userid] = _BasePlayer(userid)

        # Update the level value
        self[userid]._level = pInstance.level

        # Update the multikill value
        self[userid].multikill = pInstance.multikill

        # Delete the old _BasePlayer() instance
        del self[pInstance.userid]

    def reset(self):
        self.clear()

    def remove_old(self):
        useridList = _es.getUseridList()

        # For all userids
        for userid in self.copy():
            # If the userid is on the server, stop here
            if userid in useridList:
                continue

            # If the user is no longer in the server, remove their instance
            del self[userid]


class _ExtendedPlayerBase(PlayerLevels, PlayerSounds, PlayerMessaging,
                          PlayerWeapons, PlayerWins):
    """Class that extends the functionality of levels, sound, messaging, and
    weapons to the _BasePlayer class.

    """
    pass


class _BasePlayer(_ExtendedPlayerBase, _PlayerMeta):
    # Declare the default attribute fields
    _fields = make_fields(multikill = IntegerField(min_value=0),
                          _afk = InstanceField(instance=AFK),
                          soundpack = InstanceField(instance=SoundPack),
                          _userid = IntegerField(min_value=2),
                          _steamid = StringField(),
                          _index = IntegerField(),
                          _preventlevel = InstanceField(instance=PreventLevel),
                          stripexceptions = InstanceField(
                                                instance=StripExceptions),
                          )

    # =========================================================================
    # Class Properties and Property Methods
    # =========================================================================
    # Player().userid (read-only)
    @property
    def userid(self):
        """Returns the player\'s userid."""
        return self._userid

    # Player().steamid (read-only)
    @property
    def steamid(self):
        """Returns the player\'s UniqueID value from playerlib."""
        return self._steamid

    # Player().index (read-only)
    @property
    def index(self):
        """Returns the player's index from playerlib."""
        return self._index

    # Player().afk (read-only)
    @property
    def afk(self):
        return self._afk

    # Player().preventlevel (read-only)
    @property
    def preventlevel(self):
        return self._preventlevel

    # Player().team (read and write)
    def _get_team(self):
        """Returns the player\'s current team."""
        return _es.getplayerteam(self.userid)

    def _set_team(self, value):
        # Does the player still exist?
        if not _es.exists('userid', self.userid):
            raise ValueError('userid (%s) doesn\'t exist.' % self.userid)

        # Check for valid team values
        try:
            value = int(value)
            if value not in xrange(1, 3):
                raise ValueError
        except (TypeError, ValueError):
            raise ValueError('"%s" is an invalid team' % value)

        # Make sure we are not moving the player to the same team
        if self.team == value:
            return

        # Change the team
        _spe.switchTeam(self.userid, value)

        # No model change needed if going to spectator
        if value == 1:
            return

        # Retrieve a playerlib instance
        pPlayer = _getPlayer(self.userid)

        # Change to Terrorist Models
        if value == 2:
            pPlayer.model = 'player/%s' % choice(('t_arctic', 't_guerilla',
                                                  't_leet', 't_phoenix'))
        # Change to Counter-Terrorist Models
        else:
            pPlayer.model = 'player/%s' % choice(('ct_gign', 'ct_gsg9',
                                                  'ct_sas', 'ct_urban'))

    team = property(fget=_get_team, fset=_set_team)

    # =========================================================================
    # Special class methods
    # =========================================================================
    def __init__(self, userid):
        self._userid = int(userid)
        self._steamid = _getPlayer(self.userid).uniqueid(True)
        self._index = _getPlayer(self.userid).index
        self._afk = AFK(self.userid)
        self.multikill = 0
        self.stripexceptions = StripExceptions()
        self.soundpack = SoundPack(str(gg_soundpack))
        self._preventlevel = PreventLevel()
        super(_BasePlayer, self).__init__()

    def __delattr__(self, name):
        # Make sure we don't try to delete required GunGame attributes
        if name in ('userid', 'level', 'preventlevel', 'steamid', 'soundpack',
                    'stripexceptions', 'multikill', 'wins', 'team', 'name',
                    'index', 'afk'):
            raise AttributeError('Unable to delete attribute "%s". ' % name +
                    'This is a required attribute for GunGame.')

    def __getitem__(self, name):
        return getattr(self, name)

    def __setitem__(self, name, value):
        object.__setattr__(self, name, value)

    def __delitem__(self, name):
        self.__delattr__(name)

    def __str__(self):
        return str(self.userid)

    def __int__(self):
        return self.userid

    def respawn(self, force=False):
        """Respawns the player."""
        # Player on server ?
        if not _es.exists('userid', self.userid):
            return

        # Player in spec or unassigned ?
        if self.team < 2:
            return

        # Player alive? (require force)
        if not _getPlayer(self.userid).isdead and not force:
            return

        _spe.respawn(self.userid)


class Player(PlayerCallbacks):
    def __new__(cls, userid):
        return _PlayerContainer()[userid]
