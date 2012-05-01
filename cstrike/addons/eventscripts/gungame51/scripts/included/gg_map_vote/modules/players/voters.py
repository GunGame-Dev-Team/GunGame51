# ../scripts/included/gg_map_vote/modules/players/voters.py

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
from es import getuserid
#   Gamethread
from gamethread import cancelDelayed
from gamethread import delayedname
#   Popuplib
from popuplib import find


# =============================================================================
# >> CLASSES
# =============================================================================
class DictionaryOfPlayers(dict):
    '''Class used to store players and their votes'''

    def __getitem__(self, userid):
        '''Returns the player's _Player instance'''

        # Typecast the given userid
        userid = int(userid)

        # Is the userid already in the dictionary?
        if userid in self:

            # Return the player's _Player instance
            return super(DictionaryOfPlayers, self).__getitem__(userid)

        # Get the player's _Player instance
        value = self[userid] = _Player(userid)

        # Return the player's _Player instance
        return value

    def __delitem__(self, userid):
        '''Removes the given player from the dictionary'''

        # Typecast the given userid
        userid = int(userid)

        # Is the userid in the dictionary?
        if not userid in self:

            # If not, return
            return

        # Cancel the player's loop
        self[userid].stop_loop()

        # Remove the player from the dictionary
        super(DictionaryOfPlayers, self).__delitem__(userid)

    def clear(self):
        '''Removes all players from the dictionary'''

        # Loop through all userids in the dictionary
        for userid in list(self):

            # Remove the userid from the dictionary
            del self[userid]


class _Player(object):
    '''Class that repeatedly sends the MapVote
        to a player until they make a choice or
        the MapVote ends and stores their vote'''

    def __init__(self, userid):
        '''Called when an instance is initialized'''

        # Store the given userid
        self.userid = userid

        # Store the player's vote as None
        self.choice = None

    def start_menu_loop(self):
        '''Starts the menu loop for the player's MapVote menu'''

        # Find the MapVote menu
        self.menu = find('gg_map_vote')

        # Start the loop
        self.menu_loop()

    def menu_loop(self):
        '''Loops through to send the MapVote to a player'''

        # Send the MapVote menu
        self.menu.send(self.userid)

        # Loop through every four seconds to re-send the MapVote menu
        delayedname(4, 'gg_map_vote_%s' % self.userid, self.menu_loop)

    def stop_loop(self):
        '''Stops the loop'''

        # Cancel the loop
        cancelDelayed('gg_map_vote_%s' % self.userid)
