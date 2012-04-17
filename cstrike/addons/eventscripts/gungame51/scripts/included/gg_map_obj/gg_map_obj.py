# ../scripts/included/gg_map_obj/gg_map_obj.py

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

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo

# =============================================================================
# >> ADDON REGISTRATION/INFORMATION
# =============================================================================
info = AddonInfo()
info.name = 'gg_map_obj'
info.title = 'GG Map Objectives'
info.author = 'GG Dev Team'
info.version = "5.1.%s" % "$Rev$".split('$Rev: ')[1].split()[0]

# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Get the es.ServerVar() instance of "gg_map_obj"
# 1 = All objectives disabled.
# 2 = Bomb objective disabled.
# 3 = Hostage objectives disabled.
gg_map_obj = es.ServerVar('gg_map_obj')


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    '''Called when the script is loaded'''

    # Disable objectives
    modify_objectives()


def unload():
    '''Called when the script is unloaded'''

    # Enable the objectives
    modify_objectives()


# =============================================================================
# >> GAME EVENTS
# =============================================================================
def round_start(event_var):
    '''Called when a new round starts'''

    # Disable objectives
    modify_objectives()


# =============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# =============================================================================
def modify_objectives():
    '''Disables Objectives on the map'''

    # Get a userid
    userid = es.getuserid()

    # Is there a userid on the server?
    if not userid:

        # If not, es_xfire cannot be ran, so simply return
        return

    # Get map info
    map_objectives = int(gg_map_obj)

    # Set up the command to format
    cmd = ''

    # Do Bombing Objectives need removed?
    if map_objectives in (1, 2):

        # Are there any func_bomb_target indexes
        if len(es.getEntityIndexes('func_bomb_target')):

            # Disable all func_bomb_target entities
            cmd += 'es_xfire %d func_bomb_target Disable;' % userid

            # Kill all weapon_c4 entities
            cmd += 'es_xfire %d weapon_c4 Kill;' % userid

    # Do Hostage Objectives need removed?
    if map_objectives in (1, 3):

        # Are there any func_hostage_rescue indexes?
        if len(es.getEntityIndexes('func_hostage_rescue')):

            # Disable all func_hostage_rescue entities
            cmd += 'es_xfire %d func_hostage_rescue Disable;' % userid

            # Kill all hostage_entity entities
            cmd += 'es_xfire %d hostage_entity Kill;' % userid

    # Do the func_ entities need Enabled?
    if map_objectives == 0:

        # Are there any func_bomb_target indexes
        if len(es.getEntityIndexes('func_bomb_target')):

            # Disable all func_bomb_target entities
            cmd += 'es_xfire %d func_bomb_target Enable;' % userid

        # Are there any func_hostage_rescue indexes?
        if len(es.getEntityIndexes('func_hostage_rescue')):

            # Disable all func_hostage_rescue entities
            cmd += 'es_xfire %d func_hostage_rescue Enable;' % userid

    # Is there a command string?
    if cmd:

        # Execute the command string to disable objectives
        es.server.queuecmd(cmd)
