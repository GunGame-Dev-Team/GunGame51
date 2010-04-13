# ../addons/eventscripts/gungame51/scripts/included/gg_map_obj/gg_map_obj.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
# Eventscripts Imports
import es
from playerlib import getPlayer

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo

# ============================================================================
# >> ADDON REGISTRATION/INFORMATION
# ============================================================================
info = AddonInfo()
info.name = 'gg_map_obj'
info.title = 'GG Map Objectives' 
info.author = 'GG Dev Team' 
info.version = '0.1'

# ============================================================================
# >> GLOBAL VARIABLES
# ============================================================================
# Get the es.ServerVar() instance of "gg_map_obj"
# 1 = All objectives disabled.
# 2 = Bomb objective disabled.
# 3 = Hostage objectives disabled.
gg_map_obj = es.ServerVar('gg_map_obj')

# Get the es.ServerVar() instance of "gg_player_defuser"
gg_player_defuser = es.ServerVar('gg_player_defuser')

# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    # Disable objectives
    objectiveToggle('Disable')

    es.dbgmsg(0, 'Loaded: %s' %info.name)

def unload():
    # Enable objectives
    objectiveToggle('Enable')

    es.dbgmsg(0, 'Unloaded: %s' %info.name)

def round_start(event_var):
    # Disable objectives
    objectiveToggle('Disable')

def player_spawn(event_var):
    userid = event_var['userid']

    if es.getplayerteam(userid) < 2:
        return

    if getPlayer(userid).isdead:
        return

    # Are we in a map that has a bombzone?
    if not len(es.createentitylist('func_bomb_target')):
        return

    # Check to see if this player is a CT
    if not int(event_var['es_userteam']) == 3:
        return

    # Do we want to give a defuser?
    if not int(gg_player_defuser):
        return

    # Make sure the player doesn't already have a defuser
    if not getPlayer(userid).defuser:
        getPlayer(userid).defuser = 1

def objectiveToggle(mode):
    userid = es.getuserid()

    # Get map info
    mapObjectives = int(gg_map_obj)

    # Set up the command to format
    cmd = None

    # If both the BOMB and HOSTAGE objectives are enabled, we don't do anything else
    if mapObjectives in range(1, 4):
        # Remove all objectives
        if mapObjectives == 1:
            if len(es.createentitylist('func_bomb_target')):
                cmd = 'es_xfire %d func_bomb_target %s;' %(userid, mode)
                if mode == 'Disable':
                    cmd = cmd + 'es_xfire %d weapon_c4 Kill;' %userid

            elif len(es.createentitylist('func_hostage_rescue')):
                cmd = 'es_xfire %d func_hostage_rescue %s;' %(userid, mode)
                if mode == 'Disable':
                    cmd = cmd + 'es_xfire %d hostage_entity Kill;' %userid

        # Remove bomb objectives
        elif mapObjectives == 2:
            if len(es.createentitylist('func_bomb_target')):
                cmd = 'es_xfire %d func_bomb_target %s;' %(userid, mode)
                if mode == 'Disable':
                    cmd = cmd + 'es_xfire %d weapon_c4 Kill;' % userid

        # Remove hostage objectives
        elif mapObjectives == 3:
            if len(es.createentitylist('func_hostage_rescue')):
                cmd = 'es_xfire %d func_hostage_rescue %s;' %(userid, mode)
                if mode == 'Disable':
                    cmd = cmd + 'es_xfire %d hostage_entity Kill;' % userid

    if cmd:
        es.server.queuecmd(cmd)