# ../addons/eventscripts/gungame51/scripts/included/gg_dead_strip/gg_dead_strip.py

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
import gamethread
from playerlib import getPlayer
from weaponlib import getWeaponNameList
from weaponlib import getWeaponList

# SPE Imports
import spe

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.addons import PriorityAddon
from gungame51.core.players.shortcuts import Player
from gungame51.scripts.included.gg_warmup_round.gg_warmup_round import \
    get_warmup_weapon
from gungame51.scripts.included.gg_nade_bonus.gg_nade_bonus import get_weapon

# ============================================================================
# >> ADDON REGISTRATION/INFORMATION
# ============================================================================
info = AddonInfo()
info.name = 'gg_dead_strip'
info.title = 'GG Dead Strip'
info.author = 'GG Dev Team'
info.version = '0.1'

# ============================================================================
# >> GLOBAL VARIABLES
# ============================================================================
# Get the es.ServerVar() instance of "gg_nade_bonus"
gg_nade_bonus = es.ServerVar('gg_nade_bonus')

# Retrieve a list of all available weapon names
list_weaponNameList = getWeaponNameList()

gg_map_strip_exceptions = es.ServerVar('gg_map_strip_exceptions')

# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    # Register the drop command to prevent it from being used.
    es.addons.registerClientCommandFilter(drop_filter)
    
    #Start the idle weapon removal loop
    gamethread.delayedname(5, "gg_removeIdleLoop", removeIdleLoop)

    # Make sure that all owned weapons can NOT be picked up
    for userid in es.getUseridList():
        for weapon in spe.getWeaponDict(userid):
            set_spawn_flags(userid, weapon[7:], 2)

    es.dbgmsg(0, 'Loaded: %s' % info.name)

def unload():
    # Unregister the drop command
    es.addons.unregisterClientCommandFilter(drop_filter)
    
    #Stop the idle weapon removal loop
    gamethread.cancelDelayed('gg_removeIdleLoop')
    
    # Make sure that all weapons can be picked up
    for userid in es.getUseridList():
        for weapon in spe.getWeaponDict(userid):
            set_spawn_flags(userid, weapon[7:], 0)

    es.dbgmsg(0, 'Unloaded: %s' % info.name)

# ============================================================================
# >> GAME EVENTS
# ============================================================================
def round_start(event_var):
    # Remove all idle weapons that exist on the map.
    es.server.queuecmd('es_xfire %s game_weapon_manager ' % es.getuserid() +
                        'AddOutput "maxpieces 0"')

def item_pickup(event_var):
    # Get variables
    item = event_var['item']
    userid = int(event_var['userid'])

    # Is a weapon?
    if ("weapon_%s" % item) not in list_weaponNameList:
        return

    # Client exists?
    if not es.exists('userid', userid):
        return

    # Don't strip the knife
    if item == "knife":
        return

    # Don't strip the c4 if bomb objectives are allowed
    if item == "c4" and not int(es.ServerVar("gg_map_obj")) in [1,2]:
        return

    # Check to see if the weapon is in the player's strip exceptions
    if item in Player(userid).stripexceptions + ['flashbang', 'smokegrenade']:
        # Make sure this weapon can't be picked up
        set_spawn_flags(userid, item, 2)
        return

    # Get the player's GunGame weapon
    currentWeapon = Player(userid).weapon

    # Check to see if the weapon is their gungame weapon
    if item == currentWeapon:
        # Make sure this weapon can't be picked up
        set_spawn_flags(userid, item, 2)
        return

    # Remove player's weapon
    remove_weapon(userid, item)

    # Check if player is on nade level
    if currentWeapon == 'hegrenade':

        # Switch the player knife ?
        if not getPlayer(userid).he:
            es.server.queuecmd('es_xsexec %s "use weapon_knife"' % userid)
            return

    # Switch to their gungame weapon
    es.server.queuecmd('es_xsexec %s "use weapon_%s"' % (userid, currentWeapon)
                                                                            )

# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
def removeIdleLoop():
    list_noStrip = [(x.strip() if x.strip().startswith('weapon_') else \
                    'weapon_%s' % x.strip()) for x in \
                    str(gg_map_strip_exceptions).split(',') if x.strip() != \
                    '']

    for weapon in getWeaponList('#all'):
        # Make sure that the admin doesn't want the weapon left on the map
        if weapon in list_noStrip:
            continue

        # Remove all weapons of this type from the map
        for index in weapon.indexlist:
            # If the weapon has an owner, stop here
            if es.getindexprop(index,'CBaseEntity.m_hOwnerEntity') != -1:
                continue

            spe.removeEntityByIndex(index)

    gamethread.delayedname(5, "gg_removeIdleLoop", removeIdleLoop)

def set_spawn_flags(userid, weapon, flag):
    # Adjusts the ability for weapons to be picked up
    es.server.queuecmd('es_xfire %s weapon_%s ' % (userid, weapon) + 
        'addoutput \"spawnflags %s\"' % flag)

def remove_weapon(userid, item):
    # Remove weapon
    weaponName = "weapon_%s" % item
    theWeapon = spe.ownsWeapon(userid, weaponName)
    if theWeapon:
        spe.dropWeapon(userid, weaponName)
        spe.removeEntityByInstance(theWeapon)

def drop_filter(userid, args):
    # If command not drop, continue
    if len(args) and args[0].lower() != 'drop':
        return 1

    # If the player is no longer on the server, stop here
    if not es.exists("userid", userid):
        return 0

    # Get player's GunGame weapon
    weapon = Player(userid).weapon

    # If gg_warmup_round is loaded, the weapon they should have is the warmup
    # weapon
    if 'gg_warmup_round' in PriorityAddon():
        weapon = get_warmup_weapon()

    # Get the player's current weapon
    curWeapon = getPlayer(userid).attributes['weapon']

    # If playerlib didn't find a current weapon, stop here
    if not curWeapon:
        return

    # Check to see if their current weapon is their level weapon
    if weapon != 'hegrenade':
        return int(curWeapon != 'weapon_%s' % weapon)

    # NADE BONUS CHECK
    if str(gg_nade_bonus) in ('', '0'):
        return 0

    # Do not let them drop their nade bonus weapon
    if curWeapon.replace("weapon_", "") in get_weapon(userid):
        return 0

    # Allow them to drop it
    return 1