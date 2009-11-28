# ../addons/eventscripts/gungame/scripts/included/gg_stats_logging/gg_stats_logging.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
# Python Imports
from __future__ import with_statement

# Eventscripts Imports
import es

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core import get_game_dir

# ============================================================================
# >> ADDON REGISTRATION/INFORMATION
# ============================================================================
info = AddonInfo()
info.name = 'gg_stats_logging'
info.title = 'GG Stats Logging' 
info.author = 'GG Dev Team' 
info.version = '0.1'

# ============================================================================
# >> GLOBAL VARIABLES
# ============================================================================
list_events = []

# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    global list_events

    this = __import__(__name__)

    # Get the file
    with open(get_game_dir('cfg/gungame51/included_addon_configs/' + \
        'gg_stats_logging.txt'), 'r') as f:

        # Create a list of lines in the file
        list_lines = [x.strip() for x in f.readlines()]

        # Remove commented out and blank lines
        list_lines = filter(lambda x: not x.startswith('//') and x, list_lines)

        # Loop through all lines in the file
        for line in list_lines:
            # Register this addon for the specified event
            es.addons.registerForEvent(this, line, logEvent)

            # Add the event to the list of events
            list_events.append(line)

    es.dbgmsg(0, 'Loaded: %s' % info.name)

def unload():
    global list_events

    this = __import__(__name__)

    # Loop through each named event in the list of events
    for event in list_events:
        # Unregister for the event
        es.addons.unregisterForEvent(this, event)

    es.dbgmsg(0, 'Unloaded: %s' % info.name)

# ==============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ==============================================================================
def logEvent(event_var):
    # Get event info
    event = event_var['es_event']
    userid = event_var['userid']

    if event in ('gg_levelup', 'gg_knife_steal', 'gg_win'):
        userid = event_var['attacker']

    # Make sure the player exists
    if not es.exists('userid', userid):
        return

    # Get player data
    playerName = es.getplayername(userid)
    steamid = es.getplayersteamid(userid)
    teamName = getTeamName(es.getplayerteam(userid))

    # Log it
    es.server.queuecmd('es_xlogq "%s<%s><%s><%s>" triggered "%s"' 
        %(playerName, userid, steamid, teamName, event))

def getTeamName(team):
    if team == 2:
        return 'TERRORIST'
    elif team == 3:
        return 'CT'
    else:
        return 'UNKNOWN'