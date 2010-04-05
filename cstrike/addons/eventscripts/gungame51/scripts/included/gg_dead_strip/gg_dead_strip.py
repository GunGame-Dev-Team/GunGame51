# ../addons/eventscripts/gungame/scripts/included/gg_dead_strip/gg_dead_strip.py

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

# SPE Imports
import spe

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.addons import PriorityAddon
from gungame51.core.players.shortcuts import Player

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

# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    # Register the drop command to prevent it from being used.
    es.addons.registerClientCommandFilter(drop_filter)

    # Make sure that all owned weapons can NOT be picked up
    for userid in es.getUseridList():
        for weapon in spe.getWeaponDict(userid):
            set_spawn_flags(userid, weapon[7:], 2)

    es.dbgmsg(0, 'Loaded: %s' % info.name)

def unload():
    # Unregister the drop command
    es.addons.unregisterClientCommandFilter(drop_filter)
    
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
def set_spawn_flags(userid, weapon, flag):
    # Adjusts the ability for weapons to be picked up
    es.server.queuecmd('es_xfire %s weapon_%s addoutput \"spawnflags %s\"' % (userid, weapon, flag))

def remove_weapon(userid, item):
    # Remove weapon
    weaponName = "weapon_%s" % item
    theWeapon = spe.ownsWeapon(userid, weaponName)
    if theWeapon:
        spe.dropWeapon(userid, weaponName)
        spe.removeEntityByInstance(theWeapon)

def drop_filter(userid, args):
    # If command not drop, continue
    if args[0].lower() != 'drop':
        return 1

    # Get player's GunGame weapon
    weapon = Player(userid).weapon

    # If gg_warmup_round is loaded, the weapon they should have is the warmup
    # weapon
    if 'gg_warmup_round' in PriorityAddon():
        weapon = str(es.ServerVar("gg_warmup_weapon"))

    # Get the player's current weapon
    curWeapon = getPlayer(userid).attributes['weapon']

    # Check to see if their current weapon is their level weapon
    if weapon != 'hegrenade':
        return int(curWeapon != 'weapon_%s' % weapon)

    # NADE BONUS CHECK
    if str(gg_nade_bonus) in ('', '0'):
        return 0

    # Allow them to drop it
    return 1