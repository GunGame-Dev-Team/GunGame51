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
# >> GLOBAL VARIABLES
# =============================================================================


# =============================================================================
# >> CLASSES
# =============================================================================


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    # Loaded Message
    es.dbgmsg(0, 'Loaded: %s' % info.name)


def unload():
    # Unload Message
    es.dbgmsg(0, 'Unloaded: %s' % info.name)


# =============================================================================
# >> GAME EVENTS
# =============================================================================
def gg_new_leader(event_var):
    saytext2('#human', event_var['es_userindex'], 'NewLeader',
        {'player': event_var['es_username'],
        'level': event_var['leader_level']})


def gg_tied_leader(event_var):
    leaders = event_var['leaders'].split(',')
    if len(leaders) == 2:
        saytext2('#human', event_var['es_userindex'], 'TiedLeader_Singular',
            {'player': event_var['es_username'],
            'level': event_var['leader_level']})
    else:
        saytext2('#human', event_var['es_userindex'], 'TiedLeader_Plural',
            {'count': len(leaders),
            'player': event_var['es_username'],
            'level': event_var['leader_level']})


def gg_leader_disconnect(event_var):
    if event_var['leaders'] == "None":
        return

    leaders = [int(x) for x in event_var['leaders'].split(',')]
    if len(leaders) == 1:
        saytext2('#human', getPlayer(leaders[0]).index, 'NewLeader',
            {'player': es.getplayername(leaders[0]),
            'level': event_var['leader_level']})
    else:
        msg('#human', 'NewLeaders',
            {'players': ', '.join([es.getplayername(x) for x in leaders]),
            'level': event_var['leader_level']})


# =============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# =============================================================================
