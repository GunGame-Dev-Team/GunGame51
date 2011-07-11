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
from playerlib import getPlayer

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
    # Disable objectives
    objectiveToggle('Disable')

    es.dbgmsg(0, 'Loaded: %s' % info.name)


def unload():
    # Enable objectives
    objectiveToggle('Enable')

    es.dbgmsg(0, 'Unloaded: %s' % info.name)


# =============================================================================
# >> GAME EVENTS
# =============================================================================
def round_start(event_var):
    # Disable objectives
    objectiveToggle('Disable')


# =============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# =============================================================================
def objectiveToggle(mode):
    userid = es.getuserid()

    # Get map info
    mapObjectives = int(gg_map_obj)

    # Set up the command to format
    cmd = None

    # If both the BOMB and HOSTAGE objectives are enabled, we do not do
    #   anything else.
    if mapObjectives in range(1, 4):
        # Remove all objectives
        if mapObjectives == 1:
            if len(es.getEntityIndexes('func_bomb_target')):
                cmd = 'es_xfire %d func_bomb_target %s;' % (userid, mode)
                if mode == 'Disable':
                    cmd = cmd + 'es_xfire %d weapon_c4 Kill;' % userid

            elif len(es.getEntityIndexes('func_hostage_rescue')):
                cmd = 'es_xfire %d func_hostage_rescue %s;' % (userid, mode)
                if mode == 'Disable':
                    cmd = cmd + 'es_xfire %d hostage_entity Kill;' % userid

        # Remove bomb objectives
        elif mapObjectives == 2:
            if len(es.getEntityIndexes('func_bomb_target')):
                cmd = 'es_xfire %d func_bomb_target %s;' % (userid, mode)
                if mode == 'Disable':
                    cmd = cmd + 'es_xfire %d weapon_c4 Kill;' % userid

        # Remove hostage objectives
        elif mapObjectives == 3:
            if len(es.getEntityIndexes('func_hostage_rescue')):
                cmd = 'es_xfire %d func_hostage_rescue %s;' % (userid, mode)
                if mode == 'Disable':
                    cmd = cmd + 'es_xfire %d hostage_entity Kill;' % userid

    if cmd:
        es.server.queuecmd(cmd)
