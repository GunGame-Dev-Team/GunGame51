# ../scripts/included/gg_leader_messages/gg_leader_messages.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# Eventscripts Imports
import es
from playerlib import getPlayer

# GunGame Imports
#   Addons
from gungame51.core.addons.shortcuts import AddonInfo
#   Messaging
from gungame51.core.messaging.shortcuts import msg
from gungame51.core.messaging.shortcuts import saytext2

# =============================================================================
# >> ADDON REGISTRATION/INFORMATION
# =============================================================================
info = AddonInfo()
info.name = 'gg_leader_messages'
info.title = 'GG Leader Messages'
info.author = 'GG Dev Team'
info.version = "5.1.%s" % "$Rev$".split('$Rev: ')[1].split()[0]
info.translations = ['gg_leader_messages']


# =============================================================================
# >> GAME EVENTS
# =============================================================================
def gg_new_leader(event_var):
    saytext2('#human', event_var['es_userindex'], 'NewLeader',
        {'player': event_var['es_username'],
        'level': event_var['leader_level']})


def gg_tied_leader(event_var):
    # Get the number of current leaders
    leaders = len(event_var['leaders'].split(','))

    # Are there only 2 leaders now?
    if leaders == 2:

        # Send message that the player just tied the other leader
        saytext2('#human', event_var['es_userindex'], 'TiedLeader_Singular',
            {'player': event_var['es_username'],
            'level': event_var['leader_level']})

    # Is there a tie of 3 or more players?
    else:

        # Send message that the player just tied the other leaders
        saytext2('#human', event_var['es_userindex'], 'TiedLeader_Plural',
            {'count': leaders,
            'player': event_var['es_username'],
            'level': event_var['leader_level']})


def gg_leader_disconnect(event_var):
    # Are there any current leaders?
    if event_var['leaders'] == "None":
        return

    # Get the userids of each of the current leaders in a list
    leaders = [int(userid) for userid in event_var['leaders'].split(',')]

    # Is there only 1 leader?
    if len(leaders) == 1:

        # Is the player still on the server?
        if not es.exists('userid', leaders[0]):
            return

        # Send message about the new leader
        saytext2('#human', getPlayer(leaders[0]).index, 'NewLeader',
            {'player': es.getplayername(leaders[0]),
            'level': event_var['leader_level']})

    # Are there multiple leaders currently?
    else:

        # Get a list of leader names
        leader_names = [es.getplayername(userid) for
            userid in leaders if es.exists('userid', userid)]

        # Are there any leaders?
        if not leader_names:

            # If not, return
            return

        # Send message about all the current leaders
        msg('#human', 'NewLeaders',
            {'players': ', '.join(leader_names),
             'level': event_var['leader_level']})
