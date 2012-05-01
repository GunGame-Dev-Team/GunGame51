# ../scripts/included/gg_map_vote/modules/events.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
#   Path
from path import path

# GunGame Imports
#   Eventlib
#       Base
from gungame51.core.events.eventlib import ESEvent
#       Resource
from gungame51.core.events.eventlib.resource import ResourceFile
#       Fields
from gungame51.core.events.eventlib.fields import ByteField
from gungame51.core.events.eventlib.fields import ShortField
from gungame51.core.events.eventlib.fields import StringField


# =============================================================================
# >> EVENT CLASSES
# =============================================================================
class GG_Map_Vote_Started(ESEvent):
    '''Fires when the MapVote is started'''

    maps = StringField(
        comment='Maps, separated by commas, that are in the MapVote')

    duration = ByteField(min_value=1,
        comment='The duration of the current MapVote')


class GG_Map_Vote_Ended(ESEvent):
    '''Fires when the MapVote ends'''

    winner = StringField(comment='The map that won the MapVote')

    votes = ByteField(min_value=0,
        comment='The number of votes that the winning map received')

    total_votes = ByteField(min_value=0,
        comment='The total number of votes cast during the MapVote')


class GG_Map_Vote_Submit(ESEvent):
    '''Fires when a player submits a vote for the MapVote'''

    userid = ShortField(min_value=2,
        comment='The userid of the player that submitted the vote')

    choice = StringField(comment='The name of the map the player voted for')

# Get the ResourceFile instance to create the .res file
gg_map_vote_resource = ResourceFile(
    path(__file__).parent.joinpath('gg_map_vote.res'))

# Write the .res file
gg_map_vote_resource.write([GG_Map_Vote_Started,
    GG_Map_Vote_Ended, GG_Map_Vote_Submit], overwrite=True)
