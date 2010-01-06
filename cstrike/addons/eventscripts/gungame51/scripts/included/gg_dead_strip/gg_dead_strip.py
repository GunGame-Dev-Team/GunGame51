# ../addons/eventscripts/gungame/scripts/included/gg_dead_strip/gg_dead_strip.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
import spe

# Eventscripts Imports
import es
from playerlib import getPlayer
from weaponlib import getWeaponNameList

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
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

    es.dbgmsg(0, 'Loaded: %s' % info.name)

def unload():
    # Unregister the drop command
    es.addons.unregisterClientCommandFilter(drop_filter)

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
        return

    # Get the player's GunGame weapon
    currentWeapon = Player(userid).weapon

    # Check to see if the weapon is their gungame weapon
    if item == currentWeapon:
        return

    # Remove player's weapon
    remove_weapon(userid, item)

    # Player carrying the item ?
    if currentWeapon != item:
        return

    # Check if player is on nade level
    if weapon == 'hegrenade':

        # Switch the player knife ?
        if not getPlayer(userid).he:
            es.server.queuecmd('es_xsexec %s "use weapon_knife"' % userid)
            return

    # Switch to their gungame weapon
    es.server.queuecmd('es_xsexec %s "use weapon_%s"' % (userid, weapon))
    
# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
def remove_weapon(userid, item):
    # Remove weapon
    #es.server.queuecmd('es_xremove %s' % getPlayer(userid).getWeaponIndex(
    #                                                "weapon_%s" % item))
    # es.msg("[REMOVE]: remove_weapon. gg_dead_strip.py")
    spe.removeEntityByIndex( getPlayer(userid).getWeaponIndex("weapon_%s" % item) )
    
def drop_filter(userid, args):
    # If command not drop, continue
    if args[0].lower() != 'drop':
        return 1

    # Get player's GunGame weapon
    weapon = Player(userid).weapon

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