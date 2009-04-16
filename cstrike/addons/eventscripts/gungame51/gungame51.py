# ../cstrike/addons/eventscripts/gungame/gungame.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
# EventScripts Imports
import es
import gamethread

# GunGame Imports
from core.addons.shortcuts import loadAddon
from core.addons.shortcuts import unloadAddon
from core.addons.shortcuts import getAddonInfo
from core.addons.shortcuts import addonExists
from core.cfg.files import *
from core.cfg import __configs__
from core.cfg import getConfigList
from core.weapons.shortcuts import setWeaponOrder
from core.weapons.shortcuts import getWeaponOrder
'''
import core.addons.unittest as addons

addons.testAddonInfo()
addons.testAddonExists()
addons.testGetAddonType()
'''

# ==================================
#      THIS WILL BE IMPORTANT LATER
# LOAD WEAPON ORDERS
# LOAD CONFIGS
# LOAD ADDONS
# LOAD PLAYER CLASS
# ==================================

# ============================================================================
# >> TEST CODE
# ============================================================================
def load():
    # Load custom events
    es.loadevents('declare', 'addons/eventscripts/gungame51/core/events/data/es_gungame_events.res')
    
    currentOrder = setWeaponOrder('default_weapon_order', '#reversed')
    currentOrder.echo()
    es.dbgmsg(0, '(current) The weapon for level 7 is: %s' %currentOrder.getWeapon(7))
    es.dbgmsg(0, '(current) The multikill for level 7 is: %s' %currentOrder.getMultiKill(7))
    
    myOrder = getWeaponOrder('weapon_short.txt.zomg.whatrudoing.u.bastard')
    myOrder.echo()
    es.dbgmsg(0, '(short) The weapon for level 3 is: %s' %myOrder.getWeapon(3))
    es.dbgmsg(0, '(short) The multikill for level 3 is: %s' %myOrder.getMultiKill(3))
    es.dbgmsg(0, '(current) The weapon for level 3 is: %s' %currentOrder.getWeapon(3))
    es.dbgmsg(0, '(current) The multikill for level 3 is: %s' %currentOrder.getMultiKill(3))
    '''
    # Load our test addons
    es.dbgmsg(0, '')
    es.dbgmsg(0, 'LOADING ADDONS:')
    es.dbgmsg(0, '-'*30)
    es.server.cmd('gg_deathmatch 1')
    
    # Wow! I have to use a delay to list the addons because they load so quickly!
    #gamethread.delayed(0, listAddons, ())
    #es.server.cmd('gg_assist 1')
    '''
    loadAddon('gg_assist')
    '''
    #es.server.cmd('gg_multi_level 1')
    
    # Oops! We can't unload turbo...it is a requirement of gg_deathmatch...
    #es.server.cmd('gg_turbo 0')
    #es.server.cmd('gg_deathmatch 0')
    
    es.dbgmsg(0, '-'*30)
    es.dbgmsg(0, '')
    '''
    
def es_map_start(event_var):
    # Load custom GunGame events
    es.loadevents('declare', 'addons/eventscripts/gungame51/core/events/data/es_gungame_events.res')
    
def listAddons():
    from core.addons import __addons__
    list_addons = __addons__.__order__[:]
    for addon in list_addons:
        es.dbgmsg(0, '\t%s' %addon)
    es.dbgmsg(0, '# of addons remaining: %i' %len(getAddonInfo()))
    
def unload():
    from core.addons import __addons__
    es.dbgmsg(0, '')
    es.dbgmsg(0, 'UNLOADING ADDONS:')
    es.dbgmsg(0, '-'*30)
    es.dbgmsg(0, '# of addons loaded: %i' %len(getAddonInfo()))
    # Create a copy of the list of addons
    list_addons = __addons__.__order__[:]
    # We need to unload in reverse due to DependencyErrors
    list_addons.reverse()
    for name in list_addons:
        if name not in __addons__.__order__:
            continue
        unloadAddon(name)
        es.dbgmsg(0, '# of addons remaining: %i' %len(getAddonInfo()))
    es.dbgmsg(0, '-'*30)
    es.dbgmsg(0, '')
    
    # Testing the unloading of configs and removal of flags
    __configs__.unload('gg_en_config')