# ../scripts/included/gg_stats_logging/gg_stats_logging.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
from __future__ import with_statement

# Eventscripts Imports
import es

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core import get_game_dir


# =============================================================================
# >> ADDON REGISTRATION/INFORMATION
# =============================================================================
info = AddonInfo()
info.name = 'gg_stats_logging'
info.title = 'GG Stats Logging'
info.author = 'GG Dev Team'
info.version = "5.1.%s" % "$Rev$".split('$Rev: ')[1].split()[0]


# =============================================================================
# >> CLASSES
# =============================================================================
class StatsLogging(object):
    '''Class used to store and log GunGame Events'''

    def __new__(cls):
        '''Method used to make sure we have a singleton object'''

        if not '_the_instance' in cls.__dict__:
            cls._the_instance = object.__new__(cls)
        return cls._the_instance

    def register_for_events(self):
        '''Method used to register events to be logged'''

        # Open the file that lists the events to log
        with get_game_dir('cfg/gungame51/' +
          'included_addon_configs/gg_stats_logging.txt').open() as f:

            # Store all events listed in the file
            self.list_events = [
              x.strip() for x in f.readlines() if not x.startswith('//') and x]

        # Loop through all events to be logged
        for event in self.list_events:

            # Register the event to be logged
            es.addons.registerForEvent(self, event, self.log_event)

    def unregister_for_events(self):
        '''Method used to unregister events that were being logged'''

        # Loop through all events that were being logged
        for event in self.list_events:

            # Unregister the event
            es.addons.unregisterForEvent(self, event)

    def log_event(self, event_var):
        '''Method used to log the given event'''

        # Store the event and userid Event Variables
        event = event_var['es_event']
        userid = event_var['userid']

        # Is this an event that needs to log the "attacker" instead?
        if event in ('gg_levelup', 'gg_knife_steal', 'gg_win'):

            # Store the attacker's userid
            userid = event_var['attacker']

        # Is the player still on the server?
        if not es.exists('userid', userid) and userid != 0:

            # If not, return
            return

        # Get all other information to be logged
        player_name = es.getplayername(userid)
        steamid = es.getplayersteamid(userid)
        team_name = self.get_team_name(userid)

        # Log the event with the necessary information
        es.server.queuecmd('es_xlogq "%s<%s><%s><%s>" triggered "%s"'
            % (playerName, userid, steamid, teamName, event))

    @staticmethod
    def get_team_name(userid):
        '''Method used to get the name of a player's team'''

        # Get the player's team number
        team = es.getplayerteam(userid)

        # Is the player on the Terrorist team?
        if team == 2:

            # Return the string
            return 'TERRORIST'

        # Is the player on the Counter-Terrorist team?
        if team == 3:

            # Return the string
            return 'CT'

        # If not on a team, return UNKNOWN
        return 'UNKNOWN'


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    '''Fired when the script is first loaded'''

    # Register the events to be logged
    StatsLogging().register_for_events()


def unload():
    '''Fires when the script is unloaded'''

    # Unregister the events
    StatsLogging().unregister_for_events()
