# ../scripts/included/gg_warmup_round/gg_warmup_round.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
#Python Imports
from random import shuffle

# EventScripts Imports
#   ES
import es
#   Cmdlib
from cmdlib import registerServerCommand
from cmdlib import unregisterServerCommand
#   Gamethread
from gamethread import delayed
#   Playerlib
from playerlib import getPlayer
from playerlib import getPlayerList
#   Weaponlib
from weaponlib import getWeaponList

# GunGame Imports
#   Addons
from gungame51.core.addons.info import AddonInfo
from gungame51.core.addons.loaded import LoadedAddons
from gungame51.core.addons.priority import PriorityAddon
#   Events
from gungame51.core.events import GG_Start
#   Messaging
from gungame51.core.messaging.shortcuts import hudhint
from gungame51.core.messaging.shortcuts import msg
#   Players
from gungame51.core.players.shortcuts import Player
#   Repeat
from gungame51.core.repeat import Repeat
#   Weapons
from gungame51.core.weapons.shortcuts import get_level_weapon


# =============================================================================
# >> ADDON REGISTRATION/INFORMATION
# =============================================================================
info = AddonInfo()
info.name = 'gg_warmup_round'
info.title = 'GG Warmup Round'
info.author = 'GG Dev Team'
info.version = "5.1.%s" % "$Rev$".split('$Rev: ')[1].split()[0]
info.translations = ['gg_warmup_round']


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
mp_freezetime = es.ServerVar('mp_freezetime')
warmup_timer = es.ServerVar('gg_warmup_timer')
warmup_weapon = es.ServerVar('gg_warmup_weapon')
warmup_start_file = es.ServerVar('gg_warmup_start_file')
warmup_end_file = es.ServerVar('gg_warmup_end_file')
warmup_round_min_players = es.ServerVar('gg_warmup_round_min_players')
warmup_round_max_extensions = es.ServerVar('gg_warmup_round_max_extensions')
warmup_round_players_reached = es.ServerVar('gg_warmup_round_players_reached')

possible_weapons = [
    weapon.basename for weapon in getWeaponList('#primary')]
possible_weapons.extend(
    weapon.basename for weapon in getWeaponList('#secondary'))
possible_weapons.append('hegrenade')


# =============================================================================
# >> CLASSES
# =============================================================================
class WarmupRoundRepeat(Repeat):
    '''Class that extends the Repeat functionality for use by Warmup Round'''

    def extend_warmup_time(self):
        '''Extends the Warmup timer'''

        # Extend Warmup Time
        self.extend(int(warmup_timer))

    def end_warmup_time(self):
        '''Ends the Warmup timer in 1 second'''

        # Get the time remaining
        remaining = self.timeleft

        # Reduce the time to 1 second
        self.reduce(remaining - 1)


class Priorities(set):
    '''Set to manager Priority Addons used in Warmup'''

    def add(self, addon):
        '''Overriding method that also adds all addons to PriorityAddon'''

        # Is the addon already set as a Priority?
        if not addon in PriorityAddon:

            # Add the addon as a Priority
            PriorityAddon.add(addon)

            # Add the addon to Warmup's priorities
            super(Priorities, self).add(addon)

    def clear(self):
        '''Overriding method that also removes addons from PriorityAddon'''

        # Loop through all addons in the set
        for addon in self:

            # Remove the addon from PriorityAddon
            PriorityAddon.discard(addon)

        # Clear Warmup's priorities
        super(Priorities, self).clear()


class WarmupRound(object):
    '''Class used to manage Warmup Round'''

    def first_load(self):
        '''Called when Warmup Round is loaded'''

        # Create a set to store Priority Addons
        self.priorities = Priorities()

        # Create the Repeat instance
        self.repeat = WarmupRoundRepeat('gg_warmup_round', self.count_down)

        # Create set_on_load variable
        self.set_on_load = False

        # Create the godmode variable
        self.godmode = False

        # Create extensions variable
        self.extensions = 0

        # Create weapon variable
        # If another script calls get_warmup_weapon
        # too quickly, it will return None
        self.weapon = None

        # Register a server command to end Warmup Round
        registerServerCommand('gg_end_warmup',
            self.end_warmup_cmd, 'Server Command to end Warmup Round')

        # Create a list of weapons to be used each Warmup Round
        self.list_of_weapons = []

        # Start Warmup Round
        self.start_warmup()

        # The weapon only needs set once on first load
        self.set_on_load = True

        # After a delay, allow the weapon to be set again in the future
        delayed(1, self.__setattr__, ('set_on_load', False))

    def end_warmup_cmd(self, args):
        '''Callback for command to end Warmup Round'''

        # Set the message to be sent to Warmup_End_Forced
        self.message = 'Warmup_End_Forced'

        # End the current Warmup Round
        self.end_warmup()

    def unload_warmup(self):
        '''Unloads Warmup Round'''

        # Remove the repeat
        self.repeat.delete()

        # Unregister the server command used to end Warmup Round
        unregisterServerCommand('gg_end_warmup')

        # Set the message to be sent to Warmup_End_Forced
        self.message = 'Warmup_End_Forced'

        # End Warmup Round if it is still active
        self.end_warmup()

    def start_warmup(self):
        '''Called when Warmup Round needs to start'''

        # Add Warmup Round to PriorityAddon
        self.priorities.add(info.name)

        # Set the Warmup Message
        self.message = 'Timer_Ended'

        # Store a backup of mp_freezetime
        self.freezetime = int(mp_freezetime)

        # Set Freeze Time to 0
        mp_freezetime.set(0)

        # Execute the Start Warmup Round cfg
        es.mexec('gungame51/' + str(warmup_start_file))

        # Get the Warmup Weapon
        self.weapon = self.set_warmup_weapon()

        # Start the count down
        self.repeat.start(1, int(warmup_timer))

        # Loop through all living players
        for player in getPlayerList('#alive'):

            # Give the player the warmup weapon
            self.give_warmup_weapon(player.userid)

        # Wait until adding other PriortyAddons
        delayed(0.1, self.add_priority_addons)

    def add_priority_addons(self):
        '''Adds all Loader Addons to Priority'''

        # Loop through all loaded addons
        for addon in LoadedAddons:

            # Add the addon as a Priority
            self.priorities.add(addon)

    def count_down(self):
        '''
            Finds how many seconds are left and how many
            human players are active, then determines whether
            to extend, end, or continue the count down.
        '''

        # Get the time remaining
        remaining = self.repeat.timeleft

        # Is the countdown over?
        if remaining == 0:

            # End Warmup
            self.end_warmup()

            # No need to go any further
            return

        # Get the number of human players on teams
        players = self.get_human_players

        # Are there enough players to start the game?
        if players >= int(warmup_round_min_players):

            # Get the players reached value
            players_reached = int(warmup_round_players_reached)

            # Does the warmup need to end now?
            if players_reached == 2 or (
              self.extensions and players_reached == 1):

                # Set the message to be sent on
                # Warmup End to Players_Reached
                self.message = 'Players_Reached'

                # Reduce the Warmup Round to end in 1 second
                self.repeat.end_warmup_time()

                # No need to go any further
                return

        # Is the timer at 1?
        if remaining == 1:

            # Does the count down need extended?
            if self.extensions < int(warmup_round_max_extensions):

                # Increase extensions used
                self.extensions += 1

                # Send message to players that Warmup has been extended
                hudhint('#human', 'Timer_Extended')

                # Extend the count down
                self.repeat.extend_warmup_time()

                # No need to go any further
                return

            # Send hudhint message to all players
            hudhint('#human', 'Timer_Singular')

        # Is there more than 1 second left?
        else:

            # Send hudhint message to all players
            hudhint('#human', 'Timer_Plural', {'time': int(remaining)})

        # Does a beep sound need to be played?
        if remaining <= 5:

            # Play the beep
            self.play_beep()

    def set_warmup_weapon(self):
        '''Used to set the Warmup Weapon'''

        # Did the weapon just get set on load?
        if self.set_on_load:

            # Return the weapon that was already selected
            return self.weapon

        # Is the variable set to a specific weapon?
        if str(warmup_weapon) in possible_weapons:

            # Return the weapon
            return str(warmup_weapon)

        # Are there weapons in the weapon list?
        if len(self.list_of_weapons):

            # Return the next weapon
            return self.list_of_weapons.pop(0)

        # Is the weapon supposed to be random?
        if str(warmup_weapon) == '#random':

            # Get all weapons
            self.list_of_weapons = list(possible_weapons)

            # Randomize the weapons
            shuffle(self.list_of_weapons)

            # Return the first weapon
            return self.list_of_weapons.pop(0)

        # Is there a specific list of weapons?
        if ',' in str(warmup_weapon):

            # Create a list of the weapons
            self.list_of_weapons = str(warmup_weapon).split(',')

            # Return the first weapon
            return self.list_of_weapons.pop(0)

        # If all else fails, return the first level weapon
        return get_level_weapon(1)

    def end_warmup(self):
        '''Ends the current Warmup Round'''

        # Is Warmup Round currently active?
        if not info.name in PriorityAddon:

            # If not, there is no need to end the Warmup Round
            return

        # Send stop command to repeat loop
        self.repeat.stop()
        
        # Send hudhint to players that Warmup has ended
        hudhint('#human', self.message)

        # Remove Priority Addons
        self.priorities.clear()

        # Reset the number of extensions
        self.extensions = 0

        # Reset mp_freezetime
        mp_freezetime.set(self.freezetime)

        # Execute the End Warmup Round cfg file
        es.mexec('gungame51/' + str(warmup_end_file))

        # Restart the game
        es.server.queuecmd('mp_restartgame 1')

        # Set all living players godmode value to True
        self.set_all_players_godmode(True)

        # After a 1 second delay, clean up this Warmup Round
        delayed(1, self.clean_up)

    def set_all_players_godmode(self, value):
        '''Sets all players GodMode to the given value'''

        # Store the value to be used on player_spawn
        self.godmode = value

        # Loop through all living players
        for player in getPlayerList('#alive'):

            # Give the player GodMode
            player.godmode = value

    def clean_up(self):
        '''Cleans up any residuals at the time that GunGame round should start
        '''

        # Set all players back to no godmode
        self.set_all_players_godmode(False)

        # Call GG_Start event
        # This should also cause player levels and multikills
        # to be reset as soon as the GunGame match starts
        GG_Start().fire()

    def player_spawn(self, userid):
        # Is Warmup Round in PriorityAddon?
        if info.name in PriorityAddon:

            # Give player the warmup weapon
            self.give_warmup_weapon(userid)

        # Does the player need GodMode set?
        if self.godmode:

            # Give player weapon
            getPlayer(userid).godmode = True

    def give_warmup_weapon(self, userid):
        '''Gives the player the warmup weapon'''

        # Is the player on the server?
        if not es.exists('userid', userid):

            # If not, no need to give them a weapon
            return

        # Is the player on a team?
        if es.getplayerteam(userid) < 2:

            # If not, no need to give them a weapon
            return

        # Is the player alive?
        if getPlayer(userid).isdead:

            # If not, no need to give them a weapon
            return

        # Get the player's Player instance
        ggPlayer = Player(userid)

        # Set the delay time
        delay = 0.05

        # Is the player a bot?
        if es.isbot(userid):

            # Increase bot delay to make sure they get the proper weapon
            delay += 0.2

        # Strip the player's weapons (split second delay)
        delayed(delay, ggPlayer.strip, (True, [warmup_weapon]))

        # Give the player the Warmup Weapon
        delayed(delay, ggPlayer.give, (self.weapon, True, True))

    def give_hegrenade(self, event_var):
        '''Checks to see if a player needs to recieve another hegrenade'''

        # Is Warmup Round active?
        if not info.name in PriorityAddon:

            # If not, return
            return

        # Is Warmup Weapon set to hegrenade
        if self.weapon != 'hegrenade':

            # If not, return
            return

        # Get the player's userid
        userid = int(event_var['userid'])

        # Is the client still on the server?
        if not es.exists('userid', userid) and userid != 0:

            # If not, return
            return

        # Is the player on a team?
        if int(event_var['es_userteam']) < 2:

            # If not, return
            return

        # Is the player alive?
        if getPlayer(userid).isdead:

            # If not, return
            return

        # Give the player another hegrenade
        Player(userid).give('hegrenade')

    @staticmethod
    def play_beep():
        '''Plays a beep sound to all players'''

        # Loop through all players
        for player in getPlayerList('#human'):

            # Play the sound
            Player(player.userid).playsound('countDownBeep')

    @property
    def get_human_players(self):
        '''Returns the number of human players on a team'''

        # Return the number of human players on either team
        return len(getPlayerList('#human,!spec,!un'))

# Get the WarmupRound instance
warmup = WarmupRound()


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    warmup.first_load()


def unload():
    warmup.unload_warmup()


# =============================================================================
# >> GAME EVENTS
# =============================================================================
def es_map_start(event_var):
    warmup.start_warmup()


def player_spawn(event_var):
    warmup.player_spawn(event_var['userid'])


def hegrenade_detonate(event_var):
    warmup.give_hegrenade(event_var)


def cs_win_panel_match(event_var):
    warmup.repeat.stop()


# =============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# =============================================================================
def get_warmup_weapon():
    return warmup.weapon
