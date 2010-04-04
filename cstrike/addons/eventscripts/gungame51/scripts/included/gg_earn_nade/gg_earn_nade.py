# ../addons/eventscripts/gungame/scripts/included/gg_earn_nade/gg_earn_nade.py

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

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.players import Player
from gungame51.core.players.shortcuts import add_attribute_callback
from gungame51.core.players.shortcuts import remove_callbacks_for_addon
from gungame51.core.weapons.shortcuts import get_level_weapon

# ============================================================================
# >> GLOBAL VARIABLES
# ============================================================================
# players level up internally before our player_death, so we added a callback
# and store the userid who just got on hegrenade to check on in player_death
recentlyOnHegrenade = []

# ============================================================================
# >> ADDON REGISTRATION/INFORMATION
# ============================================================================
info = AddonInfo()
info.name = 'gg_earn_nade'
info.title = 'GG Earn Grenade' 
info.author = 'GG Dev Team' 
info.version = '0.1'

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

    # If the player did not level up to hegrenade level, stop here
    if get_level_weapon(value) != "hegrenade":
        return

    # Add the player to recentlyOnHegrenade for a short time so that we will
    # know in player_death that they just leveled up to hegrenade level
    recentlyOnHegrenade.append(ggPlayer.userid)
    gamethread.delayed(0.2, recentlyOnHegrenade.remove, ggPlayer.userid)

def player_death(event_var):
    attacker = int(event_var['attacker'])

    # Make sure it wasn't a suicide
    if attacker == 0:
        return

    # Make sure it wasn't a teamkill
    if event_var['es_attackerteam'] == event_var['es_userteam']:
        return

    # Make sure the player didn't kill with an hegrenade
    if event_var['weapon'] == 'hegrenade':
        return

    # Only give a nade to a player on nade level
    if Player(attacker).weapon == 'hegrenade':
        gamethread.delayed(0.11, give_nade, attacker)

# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
def give_nade(userid):
    # Is the player dead ?
    if getPlayer(userid).isdead:
        return
        
    # Is the player on a team ?
    if es.getplayerteam(userid) < 2:
        return

    # If the player just got the kill to get to hegrenade level, stop here
    if userid in recentlyOnHegrenade:
        return

    # Only give a nade if this player does not have one.
    if int(getPlayer(userid).get('he')) == 0:
        es.server.queuecmd('es_xgive %s weapon_hegrenade' % userid)
    # If the player had a grenade, and gg_multi_nade is enabled
    elif int(es.ServerVar("gg_multi_nade")):
        ggPlayer = Player(userid)
        
        # If the player has already used up their multi-nades, subtract two
        # from the number of detonations because gg_earn_nade gave them a
        # grenade to detonate which gg_multi_nade didn't account for
        if int(ggPlayer.grenades_detonated) == \
                                int(es.ServerVar("gg_multi_nade_max_nades")):
            ggPlayer.grenades_detonated -= 2
        # If the player has yet to use up their multi-nades, subtract one
        # from the number of detonations
        else:
            ggPlayer.grenades_detonated -= 1