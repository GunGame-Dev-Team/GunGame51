# ../scripts/included/gg_map_vote/modules/nominate.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# EventScripts Imports
#   ES
from es import getplayername
from es import ServerVar
#   Playerlib
from playerlib import getPlayerList
#   Popuplib
from popuplib import easymenu

# GunGame Imports
#   Players
from gungame51.core.players.shortcuts import Player
#   Messaging
from gungame51.core.messaging.shortcuts import langstring
from gungame51.core.messaging.shortcuts import msg
from gungame51.core.messaging.shortcuts import saytext2

# Script Imports
from attributes import AttributeManagement
from lastmaps import last_x_maps
from maplists import maplists
from nominations import NominatedMaps
from players.nominators import NominationPlayers

# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
gg_map_vote_size = ServerVar('gg_map_vote_size')


# =============================================================================
# >> CLASSES
# =============================================================================
class _NominationManagement(object):
    '''Class used to manage Nominations'''

    def __init__(self):
        '''Called when the class instance is initialized'''

        # Store the base attributes
        self.nominations = NominatedMaps()
        self.nominators = NominationPlayers()

    def reset(self):
        '''Resets the base attributes'''

        # Reset the base attributes
        self.nominations.clear()
        self.nominators.clear()

    def player_nominate_command(self, userid, args):
        '''Called when a player uses the nominate command'''

        # Is the MapVote active?
        if AttributeManagement.active:

            # Tell player that voting already in progress
            msg(userid, 'VoteAlreadyInProgress', prefix=True)

            # No need to go further
            return

        # Is there already a MapVote winner?
        if not AttributeManagement.winner is None:

            # Tell player MapVote winner already chosen
            msg(userid, 'Nextmap',
                {'map': AttributeManagement.winner}, prefix=True)

            # No need to go further
            return

        # Get the number of maps allowed in the MapVote
        vote_size = int(gg_map_vote_size)

        # Are there already enough nominations?
        if len(self.nominations) >= vote_size:

            # Tell player that there are already enough nominations
            msg(userid, 'NominationsFull', {'size': vote_size}, True)

            # No need to go further
            return

        # Is the player currently in the nomination menu?
        if userid in self.nominators:

            # No need to go further
            return

        # Get a list of maps for the player to choose from
        maplist = self.get_map_names()

        # Are there any maps to choose from?
        if not maplist:

            # Message the player that there are no maps to choose from
            msg(userid, 'VoteListEmpty', prefix=True)

        # Create the player's Nominate menu
        nominate_menu = easymenu(
            'gg_map_vote_nominate_%s' % userid, 'choice', self.chosen_map)

        # Set the player's Nominate menu's title
        nominate_menu.settitle(langstring('NominateMap', userid=userid))

        # Set the player's Nominate menu to last just 1 second
        nominate_menu.timeout('view', 1)

        # Loop through all maps that can be chosen from
        for map_name in maplist:

            # Add the map to the player's Nominate menu
            nominate_menu.addoption(map_name, map_name)

        # Start the player's nomination loop
        self.nominators[userid].start_menu_loop()

    def chosen_map(self, userid, map_name, popupid):
        '''Adds the chosen map to the Nominations list if needed'''

        # Remove the player from the list of nominators
        del self.nominators[userid]

        # Is the MapVote active?
        if AttributeManagement.active:

            # Do not add to the Nominations list
            return

        # Get the number of maps allowed in the MapVote
        vote_size = int(gg_map_vote_size)

        # Are enough maps already nominated?
        if len(self.nominations) >= vote_size:

            # Tell player that there are already enough nominations
            msg(userid, 'NominationsFull', {'size': vote_size}, True)

            # No need to go further
            return

        # Has the map already been nominated?
        if map_name in self.nominations:

            # If so, return the message and tokens to send to the player
            msg(userid, 'NominatedAlready', {'map': map_name}, True)

        # Add the map to the Nominations list
        self.nominations.append(map_name)

        # Send a message to all players that the map was nominated
        saytext2('#human', Player(userid).index, 'Nominated',
            {'pName': getplayername(userid), 'map': map_name}, True)

    def get_map_names(self):
        '''Method used to get a list of maps that a player can nominate'''

        # Create an empty list to add maps to
        nominate_list = list()

        # Get the current maplist
        maplist = maplists.current

        # Get the number of human players on the server
        players = len(getPlayerList('#human'))

        # Loop through all maps in the maplist
        for map_name in maplist:

            # Does the current map require more players?
            if maplist[map_name].min > players:

                # Do not use this map
                continue

            # Does the current map not have enough players?
            if maplist[map_name].max < players and maplist[map_name].max:

                # Do not use this map
                continue

            # Is the map already nominated?
            if map_name in self.nominations:

                # Do not use this map
                continue

            # Is the map in the last x maps?
            if map_name in last_x_maps:

                # Do not use this map
                continue

            # Allow the map in the Nomination menu
            nominate_list.append(map_name)

        # Return the current maplist
        return nominate_list

# Get the _NominationManagement instance
nominate = _NominationManagement()
