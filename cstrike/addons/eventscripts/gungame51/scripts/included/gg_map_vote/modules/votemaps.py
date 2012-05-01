# ../scripts/included/gg_map_vote/modules/votemaps.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
#   Random
from random import sample

# EventScripts Imports
#   ES
from es import ServerVar
#   Playerlib
from playerlib import getPlayerList

# Script Imports
from lastmaps import last_x_maps
from maplists import maplists
from nominate import nominate


# =============================================================================
# >> CLASSES
# =============================================================================
class VoteMapList(list):
    '''Class used to get a list of maps to use for the MapVote'''

    def __init__(self):
        '''Called when the class is initialized'''

        # Get a list of maps that can be voted on
        votemaps = self.get_map_names()

        # Get the nominated maps
        nominations = [map_name for map_name in
            votemaps if map_name in nominate.nominations]

        # Get the MapVote size
        vote_size = int(ServerVar('gg_map_vote_size'))

        # Do more maps need added to the MapVote?
        if vote_size > len(nominations):

            # Get all non-nominated maps
            non_nominated = [map_name for map_name in votemaps
              if not map_name in nominate.nominations]

            # Are any maps remaining?
            if non_nominated:

                # Get a sample of maps from the remaining list
                non_nominated = sample(
                    non_nominated, vote_size - len(nominations))

            # Add the nominated maps to the non nominated selected maps
            votemaps = nominations + non_nominated

        # Were no more maps needed?
        else:

            # Set votemaps to simply be the nominations
            votemaps = nominations

        # Are there any maps to vote on?
        if not votemaps:

            # Raise an error
            raise ValueError('No maps to vote on!')

        # Add the remaining maps to the main list
        self.extend(votemaps)

    @staticmethod
    def get_map_names():
        '''Method used to get a list of maps that a player can vote on'''

        # Create an empty list to add maps to
        vote_list = list()

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

            # Is the map in the last x maps?
            if map_name in last_x_maps:

                # Do not use this map
                continue

            # Allow the map in the Nomination menu
            vote_list.append(map_name)

        # Return the current maplist
        return vote_list
