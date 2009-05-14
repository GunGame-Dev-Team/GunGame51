# gungame/scripts/included/gg_dissolver.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
# Python imports
import random

# Eventscripts Imports
import es

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo

# ============================================================================
# >> ADDON REGISTRATION/INFORMATION
# ============================================================================
info = AddonInfo()
info.name = 'gg_dissolver'
info.title = 'GG Dissolver' 
info.author = 'GG Dev Team' 
info.version = '0.1'

# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    es.dbgmsg(0, 'Loaded: %s' % info.name)
    
def unload():
    es.dbgmsg(0, 'Unloaded: %s' % info.name)
    
# ============================================================================
# >> GAME EVENTS
# ============================================================================
def player_death(event_var):

    # Get userid
    userid = int(event_var['userid'])

    # Dissolve ragdoll
    dissolveRagdoll(userid)
    

# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
def dissolveRagdoll(userid):

    # Get dissolver effect
    effect = int(es.ServerVar("gg_dissolver"))

    # Just remove the ragdoll?
    if effect == 1:
        es.delayed('2', 'es_xfire %s cs_ragdoll Kill' % userid)
    else:
        # Give the entity dissolver and set its KeyValues
        cmdFormat = 'es_xgive %s env_entity_dissolver; ' % userid
        cmdFormat += 'es_xfire %s env_entity_dissolver AddOutput "target cs_ragdoll"; ' % userid
        cmdFormat += 'es_xfire %s env_entity_dissolver AddOutput "magnitude 1"; ' % userid
        
        # Check to see what effect to use
        if effect == 6:
            cmdFormat += 'es_xfire %s env_entity_dissolver AddOutput "dissolvetype %s"' % (userid, random.randint(0, 3))
        else:
            cmdFormat += 'es_xfire %s env_entity_dissolver AddOutput "dissolvetype %s"' % (userid, int(effect) - 1)
        
        es.server.queuecmd(cmdFormat)
        
        # Dissolve the ragdoll then kill the dissolver
        es.delayed('0.01', 'es_xfire %s env_entity_dissolver Dissolve' % userid)
        es.delayed('4', 'es_xfire %s env_entity_dissolver Kill' % userid)
        es.delayed('4', 'es_xfire %s cs_ragdoll Kill' % userid)




















