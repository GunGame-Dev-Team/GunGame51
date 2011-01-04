# ../addons/eventscripts/gungame51/scripts/included/gg_dissolver/gg_dissolver.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python imports
import random

# Eventscripts Imports
import es

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo

# =============================================================================
# >> ADDON REGISTRATION/INFORMATION
# =============================================================================
info = AddonInfo()
info.name = 'gg_dissolver'
info.title = 'GG Dissolver' 
info.author = 'GG Dev Team' 
info.version = "5.1.%s" %"$Rev$".split('$Rev: ')[1].split()[0]

# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Get the es.ServerVar() instance of "gg_dissolver"
gg_dissolver = es.ServerVar("gg_dissolver")

# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    es.dbgmsg(0, 'Loaded: %s' % info.name)

def unload():
    es.dbgmsg(0, 'Unloaded: %s' % info.name)

# =============================================================================
# >> GAME EVENTS
# =============================================================================
def round_start(event_var):
    setupDissolver()

def player_death(event_var):
    # Dissolve ragdoll
    dissolveRagdoll(event_var['userid'])

# =============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# =============================================================================
def setupDissolver():
    # Get a userid
    userid = es.getuserid()

    #Give the dissolver entity and set some keyvalues
    cmd = 'es_xgive %s env_entity_dissolver;' %userid + \
          'es_xfire %s env_entity_dissolver ' %userid + \
          'AddOutput "target cs_ragdoll";' + \
          'es_xfire %s env_entity_dissolver AddOutput "magnitude 1"' %userid

    # Run the command
    es.server.queuecmd(cmd)

def dissolveRagdoll(userid):
    # Get dissolver effect
    effect = int(gg_dissolver)

    # Just remove the ragdoll?
    if effect == 1:
        es.delayed(2, 'es_xfire %s cs_ragdoll Kill' %userid)

        return

    # Check to see what effect to use and set up the command
    if effect == 6:
        cmd = 'es_xfire %s env_entity_dissolver AddOutput "dissolvetype %s"' \
            %(userid, random.randint(0, 3))
    else:
        cmd = 'es_xfire %s env_entity_dissolver AddOutput "dissolvetype %s"' \
            %(userid, int(effect) - 2)

    # Run the command
    es.server.queuecmd(cmd)

    # Dissolve the ragdoll then kill the dissolver
    es.delayed('0.01', 'es_xfire %s env_entity_dissolver Dissolve' %userid)