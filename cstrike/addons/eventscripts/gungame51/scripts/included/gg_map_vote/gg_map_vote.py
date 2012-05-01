# ../scripts/included/gg_map_vote/gg_map_vote.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# EventScripts Imports
# ES
from es import ServerCommand
from es import ServerVar

# GunGame Imports
from gungame51.core import get_version
#   Modules
from gungame51.modules.backups import VariableBackups
#   Addons
from gungame51.core.addons.info import AddonInfo
#   Messaging
from gungame51.core.messaging.shortcuts import msg
from gungame51.core.messaging.shortcuts import saytext2
#   Weapons
from gungame51.core.weapons.shortcuts import get_total_levels

# Script Imports
from modules import voting_management
from modules.attributes import AttributeManagement
from modules.events import gg_map_vote_resource
from modules.lastmaps import last_x_maps
from modules.mapvote import mapvote
from modules.nominate import nominate
from modules.rtv import rtv

# =============================================================================
# >> ADDON REGISTRATION/INFORMATION
# =============================================================================
info = AddonInfo()
info.name = 'gg_map_vote'
info.title = 'GG Map Vote'
info.author = 'GG Dev Team'
info.version = get_version('gg_map_vote')
info.translations = ['gg_map_vote']


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    '''Called when the script is loaded'''

    # Register the say commands
    voting_management.register_say_commands()

    # Reset all data
    voting_management.reset()

    # Store the value of eventscripts_maphandler
    VariableBackups['eventscripts_maphandler'].add(info.name)

    # Add the current map to the last maps list
    last_x_maps.append(ServerVar('eventscripts_currentmap'))

    # Declare and load the resource file
    gg_map_vote_resource.declare_and_load()


def unload():
    '''Called when the script is unloaded'''

    # Unregister the say commands
    voting_management.unregister_say_commands()

    # Reset all data
    voting_management.reset()

    # Reset eventscripts_maphandler
    VariableBackups['eventscripts_maphandler'].remove(info.name)

    # Clear the last maps list
    last_x_maps.clear()


# =============================================================================
# >> MAP EVENTS
# =============================================================================
def es_map_start(event_var):
    '''Called when a map is loaded'''

    # Get the current map
    mapname = event_var['mapname']

    # Is the current map the first item in the last maps list?
    if not len(last_x_maps) or not last_x_maps[0] == mapname:

        # Add the map to the list of "last x maps"
        last_x_maps.append(mapname)

    # Load the resource file
    gg_map_vote_resource.load()

    # Reset all data
    voting_management.reset()


# =============================================================================
# >> PLAYER EVENTS
# =============================================================================
def player_death(event_var):
    '''Called when a player dies'''

    # Are dead players supposed to receive the MapVote menu?
    if not int(ServerVar('gg_map_vote_after_death')):

        # If not, just return
        return

    # Send the MapVote to the victim
    mapvote.send_map_vote_to_player(event_var['userid'])


def player_disconnect(event_var):
    '''Called when a player disconnects from the server'''

    # Get the player's userid
    userid = event_var['userid']

    # Remove the player from the voted dictionary
    del mapvote.votes[userid]

    # Remove the player from the set of RTV'ers
    rtv.players.discard(userid)

    # Remove the player from the nominators dictionary
    del nominate.nominators[userid]


# =============================================================================
# >> GUNGAME EVENTS
# =============================================================================
def gg_win(event_var):
    '''Called when a player wins the match'''

    # Is there a winning map?
    if not AttributeManagement.winner is None:

        # Set the "nextlevel" variable
        ServerVar('nextlevel').set(AttributeManagement.winner)


def gg_team_win(event_var):
    '''Called when a team wins the match'''

    # Is there a winning map?
    if not AttributeManagement.winner is None:

        # Set the "nextlevel" variable
        ServerVar('nextlevel').set(AttributeManagement.winner)


def gg_levelup(event_var):
    '''Called when a player levels up'''

    # Check if the vote should start
    check_start_vote(int(event_var['new_level']))


def gg_team_levelup(event_var):
    '''Called when a team levels up'''

    # Check if the vote should start
    check_start_vote(int(event_var['new_level']))


# =============================================================================
# >> SCRIPT EVENTS
# =============================================================================
def gg_map_vote_started(event_var):
    '''Fired when a MapVote is started'''

    # Announce that the MapVote has started
    msg('#human', 'PlaceYourVotes', prefix=True)


def gg_map_vote_submit(event_var):
    '''Fired when a player submits a vote for the MapVote'''

    # Should the player's vote be announced?
    if int(ServerVar('gg_map_vote_show_player_vote')):

        # Announce the player's vote
        saytext2('#human', int(event_var['es_userindex']), 'VotedFor',
            {'name': event_var['es_username'], 'map': event_var['choice']})


def gg_map_vote_ended(event_var):
    '''Fired when a MapVote has ended'''

    # Get the winning map
    winner = event_var['winner']

    # Get the number of votes the winning map received
    votes = int(event_var['votes'])

    # Set the message type
    message = 'WinningMap' if votes else 'NotEnoughVotes'

    # Announce the winning map
    msg('#human', message,
        {'map': winner, 'votes': event_var['votes'],
        'totalVotes': event_var['total_votes']}, True)

    # Set eventscripts_nextmapoverride to the winning map
    ServerVar('eventscripts_nextmapoverride').set(winner)

    # Is Mani loaded?
    if str(ServerVar('mani_admin_plugin_version')) != '0':

        # Set Mani 'nextmap'
        ServerCommand('ma_setnextmap %s' % winner)

    # Is SourceMod loaded?
    if str(ServerVar('sourcemod_version')) != '0':

        # Set SourceMod 'nextmap'
        ServerCommand('sm_nextmap %s' % winner)

    # Was RTV used?
    if AttributeManagement.rtv:

        # End the map
        rtv.end_map()


# =============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# =============================================================================
def check_start_vote(level):
    '''Function used to determine if the vote needs started'''

    # Is the mapvote already active?
    if AttributeManagement.active:

        # If so, simply return
        return

    # Has the next map been set?
    if not AttributeManagement.winner is None:

        # If so, simply return
        return

    # Get the total levels for the match
    levels = get_total_levels()

    # Is the level the player achieved high enough to start vote?
    if levels - int(level) >= int(ServerVar('gg_map_vote_trigger')):

        # Start the vote
        mapvote.start_map_vote()
