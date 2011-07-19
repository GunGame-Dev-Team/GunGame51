# ../core/players/extended_player.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
from random import choice
from random import randint

# EventScripts Imports
import es
import gamethread
from playerlib import getPlayer
from weaponlib import getWeaponNameList

# SPE Imports
import spe

# GunGame Imports
from gungame51.core.messaging import MessageManager
from gungame51.core.weapons.shortcuts import get_level_weapon


# =============================================================================
# >> GLOBALS
# =============================================================================
__all__ = ['PlayerMessaging', 'PlayerWeapons', 'PlayerSounds']
list_pWeapons = getWeaponNameList('#primary')
list_sWeapons = getWeaponNameList('#secondary')
list_allWeapons = getWeaponNameList()


# =============================================================================
# >> CLASSES
# =============================================================================
class PlayerMessaging(object):
    """Adds messaging methods to the BasePlayer class."""
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


class PlayerWeapons(object):
    """Adds weapon methods to the BasePlayer class."""
    def get_weapon(self):
        return get_level_weapon(self.level)

    def give_weapon(self):
        '''
        Gives a player their current levels weapon.
        '''
        error = None
        # Make sure player is on a team
        if self.team < 2:
            error = ('Unable to give player weapon (%s): ' % self.userid +
                     'is not on a team.')

        # Make sure player is alive
        elif getPlayer(self.userid).isdead:
            error = ('Unable to give player weapon (%s): ' % self.userid +
                     'is not alive.')

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
                        spe.removeEntityByInstance(playerWeapons
                                                    [weapToStrip]["instance"])

                # Now give them the weapon and save the weapon instance
                given_weapon = spe.giveNamedItem(self.userid,
                    "weapon_%s" % self.weapon)

                # Retrieve the weapon instance of the weapon they "should" own
                weapon_check = spe.ownsWeapon(self.userid, "weapon_%s"
                    % self.weapon)

                # Make sure that the player owns the weapon we gave them
                if weapon_check != given_weapon:
                    # Remove the given weapon since the player does not own it
                    spe.removeEntityByInstance(given_weapon)

                    # If they don't have the right weapon, fire give_weapon()
                    if not weapon_check:
                        self.give_weapon()
                        return

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
                    spe.removeEntityByInstance(playerWeapons[stripWeapon]["i" +
                                                                    "nstance"])

        # Give the player the weapon
        spe.giveNamedItem(self.userid, weapon)

        if useWeapon:
            es.server.queuecmd('es_xsexec %s "use %s"' % (self.userid, weapon))

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
            if ((self.weapon == weapon[7:] and not levelStrip) or
              weapon in ('weapon_knife', 'weapon_c4') or
              weapon[7:] in exceptions):
                continue

            spe.dropWeapon(self.userid, weapon)
            spe.removeEntityByInstance(pWeapons[weapon]["instance"])

    def strip_weapons(self, stripWeapons):
        '''
        Strips a list of weapons from a player. (Used primarily for selective
            weapon removal when a player gets a new weapon)
        stripWeapons must be a list.
        '''
        # Get the player's current held weapons
        playerWeapons = spe.getWeaponDict(self.userid)

        # Format the stripWeapons list for all names to start with "weapon_"
        stripWeapons = [w if w.startswith("weapon_") else \
            "weapon_%s" % w for w in stripWeapons]

        # Insure that the player owns the weapons by using 2 sets intersection
        remWeapons = set(stripWeapons).intersection(
            set(playerWeapons.keys())).difference(set(["weapon_knife"]))

        # Loop through any weapons to strip
        for stripWeapon in remWeapons:
            # Drop the weapon
            spe.dropWeapon(self.userid, stripWeapon)

            # Remove the weapon
            spe.removeEntityByInstance(playerWeapons[stripWeapon]["instance"])


class PlayerSounds(object):
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

        # Return the sound used
        return sound

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

        # Return the sound used
        return sound

    def stopsound(self, sound):
        '''
        Stops the sound from being played for the player.
        '''
        # Format the sound
        sound = self._format_sound(sound)

        # Make sure the sound exists
        if sound:
            # Stop the sound
            es.stopsound(self.userid, sound)

        # Return the sound used
        return sound

    def _format_sound(self, sound):
        if not self.soundpack[sound]:
            return None
        return self.soundpack[sound]