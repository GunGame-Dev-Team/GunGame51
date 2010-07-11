# ../addons/eventscripts/gungame51/scripts/included/gg_reload/gg_reload.py

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
from weaponlib import getWeapon

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.players.shortcuts import Player
from gungame51.core.players.shortcuts import add_attribute_callback
from gungame51.core.players.shortcuts import remove_callbacks_for_addon
from gungame51.core.weapons.shortcuts import get_level_weapon
from gungame51.scripts.included.gg_nade_bonus.gg_nade_bonus import get_weapon

# ============================================================================
# >> ADDON REGISTRATION/INFORMATION
# ============================================================================
info = AddonInfo()
info.name = 'gg_reload'
info.title = 'GG Reload' 
info.author = 'GG Dev Team' 
info.version = "5.1.%s" %"$Rev$".split('$Rev: ')[1].split()[0]

# ============================================================================
# >> GLOBAL VARIABLES
# ============================================================================
gg_nade_bonus = es.ServerVar('gg_nade_bonus')
gg_turbo = es.ServerVar('gg_turbo')

# Players level up internally before our player_death, so we added a callback
# and store the userid who just leveled up to check on in player_death
recentlyLeveled = []

# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    add_attribute_callback('level', level_call_back, info.name)
    es.dbgmsg(0, 'Loaded: %s' % info.name)

def unload():
    remove_callbacks_for_addon(info.name)
    es.dbgmsg(0, 'Unloaded: %s' % info.name)

# ============================================================================
# >> GAME EVENTS
# ============================================================================
def level_call_back(name, value, ggPlayer):
    # If the player is getting their level attribute set for the first time, we
    # can't get it yet
    if not hasattr(ggPlayer, "level"):
        return

    # Add the player to recentlyLeveled for a short time so that we will
    # know in player_death that they just leveled up
    recentlyLeveled.append(ggPlayer.userid)
    gamethread.delayed(0.2, recentlyLeveled.remove, ggPlayer.userid)

def player_death(event_var):
    # Get the userids of the attacker and victim
    attacker = int(event_var['attacker'])
    userid = int(event_var['userid'])

    # If there is no attacker (falling to death), return
    if not attacker:
        return

    # If the kill was a suicide, return
    if attacker == userid:
        return

    # If the kill was a teamkill, return
    if event_var['es_attackerteam'] == event_var['es_userteam']:
        return

    # Get the name of the weapon used to get the kill
    weapon = event_var['weapon']

    ggPlayer = Player(attacker)
    level = ggPlayer.level

    # If the player has already leveled up internally, check their last level
    if attacker in recentlyLeveled:
        level -= 1
        level = 1 if level < 1 else level

    reloadWeapons = [get_level_weapon(level)]
    # If nade bonus is loaded, add the bonus weapons to reloadWeapons
    if not str(gg_nade_bonus) in ('', '0'):
        reloadWeapons.extend(get_weapon(userid))

    # If the weapon name doesn't match the player's level's weapon name at the
    # time, return
    if not weapon in reloadWeapons:
        return

    # If the player is on hegrenade or knife level, return
    if weapon in ('hegrenade', 'knife'):
        return

    # Get the weapon object and the size if its clip
    weaponObject = getWeapon(weapon)

    # Find the attacker's weapon index to be used to reload the weapon
    playerHandle = es.getplayerhandle(attacker)

    for index in weaponObject.indexlist:
        # When the attacker's handle matches the index handle we have found 
        # the attacker's weapon index
        if es.getindexprop(index,'CBaseEntity.m_hOwnerEntity') == playerHandle:
            # Set the clip to the maximum ammo allowed
            getPlayer(attacker)['clip'][weaponObject] = weaponObject.clip
            break
