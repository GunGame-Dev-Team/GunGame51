# ../addons/eventscripts/gungame/scripts/included/gg_knife_pro/gg_knife_pro.py

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

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.players.shortcuts import Player
from gungame51.core.players.shortcuts import add_attribute_callback
from gungame51.core.players.shortcuts import remove_callbacks_for_addon
from gungame51.core.weapons.shortcuts import get_total_levels
from gungame51.core.weapons.shortcuts import get_level_weapon
from gungame51.core.messaging.shortcuts import msg
from gungame51.core.messaging.shortcuts import saytext2

# ============================================================================
# >> ADDON REGISTRATION/INFORMATION
# ============================================================================
info = AddonInfo()
info.name = 'gg_knife_pro'
info.title = 'GG Knife Pro' 
info.author = 'GG Dev Team' 
info.version = '0.2'
info.translations = ['gg_knife_pro']

# ============================================================================
# >> GLOBAL VARIABLES
# ============================================================================
gg_knife_pro_limit = es.ServerVar('gg_knife_pro_limit')
gg_allow_afk_levels = es.ServerVar('gg_allow_afk_levels')
gg_allow_afk_levels_knife  = es.ServerVar('gg_allow_afk_levels_knife')
gg_knife_pro_always_level = es.ServerVar('gg_knife_pro_always_level')

# players level up internally before our player_death, so we added a callback
# and store the userid who just got off of knife to check on in player_death
recentlyOffKnife = []

# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    add_attribute_callback('level', level_call_back, info.name)
    es.dbgmsg(0, 'Loaded: %s' % info.name)

def unload():
    es.dbgmsg(0, 'Unloaded: %s' % info.name)
    remove_callbacks_for_addon(info.name)

# ============================================================================
# >> GAME EVENTS
# ============================================================================
def level_call_back(name, value, ggPlayer):
    # If the player is getting their level attribute set for the first time, we
    # can't get it yet
    if not hasattr(ggPlayer, "level"):
        return

    # If the player did not level up off of knife level, stop here
    if get_level_weapon(ggPlayer.level) != "knife":
        return

    # Add the player to recentlyOffKnife for a short time so that we will know
    # in player_death that they just leveled up off of knife level
    recentlyOffKnife.append(ggPlayer.userid)
    gamethread.delayed(0.2, recentlyOffKnife.remove, ggPlayer.userid)

def player_death(event_var):
    # ===================
    # Was weapon a knife
    # ===================
    if event_var['weapon'] != 'knife':
        return

    # ===================
    # Player Information
    # ===================
    attacker = int(event_var['attacker'])
    victim   = int(event_var['userid'])
    userteam = event_var['es_userteam']
    attackerteam = event_var['es_attackerteam']
    # ===================
    # Check for suicide
    # ===================
    if (attackerteam == userteam) or (victim == attacker) or (attacker == 0):
        return

    ggAttacker = Player(attacker)
    # gg_levelup fires before this because internal events fire first, so:
    # If the player just got off of knife level, set their weapon to knife
    attackerWeapon = "knife" if attacker in recentlyOffKnife else \
                                                            ggAttacker.weapon

    # ===================
    # Attacker checks
    # ===================
    ggVictim = Player(victim)

    # Is the victim AFK?
    if ggVictim.afk():
        # If we do not allow afk levelups through knife kills, stop here
        if not (int(gg_allow_afk_levels) and int(gg_allow_afk_levels_knife)):
            msg(attacker, 'VictimAFK', prefix=True)
            return

    # Never skip hegrenade level
    if attackerWeapon == 'hegrenade':
        # If gg_knife_pro_always_level is enabled, level down the victim
        if int(gg_knife_pro_always_level):
            level_down_victim(attacker, victim)

        msg(attacker, 'CannotSkipThisLevel', prefix=True)
        return

    # If the attacker is on knife level, stop here
    if attackerWeapon == 'knife':
        # If gg_knife_pro_always_level is enabled, level down the victim first
        if int(gg_knife_pro_always_level):
            level_down_victim(attacker, victim)

        return

    # ===================
    # Victim checks
    # ===================
    # Is victim on level 1?
    if ggVictim.level == 1:

        # Checking for always level mode
        if not int(gg_knife_pro_always_level):
            msg(attacker, 'VictimLevel1', prefix=True)
            return

    # If the level difference is higher than the limit
    if is_out_of_limit(ggAttacker.level, ggVictim.level):
        # If gg_knife_pro_always_level is off, stop here
        if not int(gg_knife_pro_always_level):
            msg(attacker, 'LevelDifferenceLimit', 
                {'limit': int(gg_knife_pro_limit)}, prefix=True)
            return

    # ===================
    # Attacker Levelup
    # ===================
    # Can the attacker level up ?
    if not ggAttacker.preventlevel:

        # If the victim gets stopped by one of our checks before leveling down,
        # still fire the steal event here because there was still a knife pro
        # steal
        if not level_down_victim(attacker, victim):
            fire_gg_knife_steal(attacker, victim)

        # Play sound & levelup
        ggAttacker.playsound('levelsteal')
        ggAttacker.levelup(1, victim, 'steal')

def level_down_victim(attacker, victim):
    ggAttacker = Player(attacker)
    ggVictim = Player(victim)

    # Can the victim level down ?
    if ggVictim.level == 1:
        return False

    # Send message to attacker if victim cannot level down?
    if ggVictim.preventlevel:

        # Always level mode (do not bother the attacker)?
        if not int(gg_knife_pro_always_level):
            msg(attacker, 'VictimPreventLevel', prefix=True)

            # The steal event didn't get fired
            return False

    # Level down the victim
    # If the level difference is higher than the limit, stop here
    if is_out_of_limit(ggAttacker.level, ggVictim.level):

        # The steal event didn't get fired
        return False

    # Play sound & send message
    ggVictim.playsound('leveldown')
    ggVictim.leveldown(1, attacker, 'steal')

    fire_gg_knife_steal(attacker, victim)
    # The steal event got fired
    return True

def is_out_of_limit(attackerLevel, victimLevel):
    # Is the level difference higher than the limit?
    if (attackerLevel - victimLevel) > int(gg_knife_pro_limit) and \
                                            int(gg_knife_pro_limit) != 0:
        return True
    return False

def fire_gg_knife_steal(attacker, victim):
    ggAttacker = Player(attacker)

    # ===================
    # Fire the event
    # ===================
    es.event('initialize', 'gg_knife_steal')
    es.event('setint', 'gg_knife_steal', 'attacker', attacker)
    es.event('setint', 'gg_knife_steal', 'attacker_level', ggAttacker.level)
    es.event('setint', 'gg_knife_steal', 'userid_level', Player(victim).level)
    es.event('setint', 'gg_knife_steal', 'userid', victim)
    es.event('fire', 'gg_knife_steal')

    # Announce the level steal
    saytext2('#human', ggAttacker.index, 'StoleLevel', 
        {'attacker': es.getplayername(attacker), 
        'victim': es.getplayername(victim)})