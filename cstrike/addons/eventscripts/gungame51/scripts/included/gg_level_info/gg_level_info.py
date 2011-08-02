# ../scripts/included/gg_level_info/gg_level_info.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# Eventscripts Imports
import es

# GunGame Imports
#   Addons
from gungame51.core.addons import PriorityAddon
from gungame51.core.addons.shortcuts import AddonInfo
#   Leaders
from gungame51.core.leaders.shortcuts import get_leader_count
from gungame51.core.leaders.shortcuts import get_leader_level
from gungame51.core.leaders.shortcuts import is_leader
#   Messaging
from gungame51.core.messaging.shortcuts import langstring
#   Players
from gungame51.core.players.shortcuts import add_attribute_callback
from gungame51.core.players.shortcuts import Player
from gungame51.core.players.shortcuts import remove_callbacks_for_addon
#   Weapons
from gungame51.core.weapons.shortcuts import get_level_multikill
from gungame51.core.weapons.shortcuts import get_level_weapon
from gungame51.core.weapons.shortcuts import get_total_levels

# =============================================================================
# >> ADDON REGISTRATION/INFORMATION
# =============================================================================
info = AddonInfo()
info.name = 'gg_level_info'
info.title = 'GG Level Info'
info.author = 'GG Dev Team'
info.version = "5.1.%s" % "$Rev$".split('$Rev: ')[1].split()[0]
info.translations = ['gg_level_info']


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    # Register Multikill Attribute callback
    add_attribute_callback('multikill', multikill_call_back, info.name)


def unload():
    # Unregister Multikill Attribute callback
    remove_callbacks_for_addon(info.name)


# =============================================================================
# >> GAME EVENTS
# =============================================================================
def player_spawn(event_var):
    # Check for priority addons
    if PriorityAddon():
        return

    # Is a spectator?
    if int(event_var['es_userteam']) < 2:
        return

    # Set the player id
    userid = int(event_var['userid'])

    # Is player dead?
    if es.getplayerprop(userid, 'CBasePlayer.pl.deadflag'):
        return

    # Is the player a bot?
    if not es.isbot(userid):

        # Send the player their level info
        send_level_info_hudhint(Player(userid))


def gg_levelup(event_var):
    # Check for priority addons
    if PriorityAddon():
        return

    # Set player ids
    attacker = int(event_var['attacker'])
    userid = int(event_var['userid'])

    # If each player exists and is not a bot, send the level info hudhint
    if attacker and not es.isbot(attacker):
        send_level_info_hudhint(Player(attacker))
    if userid and not es.isbot(userid):
        send_level_info_hudhint(Player(userid))


# =============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# =============================================================================
def send_level_info_hudhint(ggPlayer):
    # Get the level, total number of levels and leader level for the hudhint
    level = ggPlayer.level
    totalLevels = get_total_levels()
    leaderLevel = get_leader_level()

    # Create a string for the hudhint
    text = langstring('LevelInfo_CurrentLevel', tokens={
                            'level': level,
                            'total': totalLevels},
                            userid=ggPlayer.userid)

    text += langstring('LevelInfo_CurrentWeapon', tokens={
                            'weapon': ggPlayer.weapon},
                            userid=ggPlayer.userid)
    multiKill = get_level_multikill(level)
    if multiKill > 1:
        text += langstring('LevelInfo_RequiredKills', tokens={
                            'kills': ggPlayer.multikill,
                            'total': get_level_multikill(level)},
                            userid=ggPlayer.userid)

    leaderTokens = {}
    # Choose the leaderString based on the player's leadership status
    if get_leader_count() == 0:
        leaderString = 'LevelInfo_NoLeaders'
    elif is_leader(ggPlayer.userid):
        leaderString = 'LevelInfo_CurrentLeader'
        if get_leader_count() > 1:
            leaderString = 'LevelInfo_AmongstLeaders'
    else:
        leaderString = 'LevelInfo_LeaderLevel'
        leaderTokens = {'level': leaderLevel,
                    'total': totalLevels,
                    'weapon': get_level_weapon(leaderLevel)}

    text += langstring(leaderString,
        tokens=leaderTokens, userid=ggPlayer.userid)

    # Send the level information hudhint
    ggPlayer.hudhint(text)


def multikill_call_back(name, value, ggPlayer):
    # Does the player have a multikill value?
    if not hasattr(ggPlayer, 'multikill'):
        return

    # Is the player a bot?
    if es.isbot(ggPlayer.userid):
        return

    # Did the player just level up?
    if value == 0:
        return

    # Get multikills needed
    multikill = get_level_multikill(ggPlayer.level)

    # Is the player going to level up?
    if value >= multikill:
        return

    # Message the player
    ggPlayer.hudhint('MultikillNotification',
        {'kills': value, 'total': multikill})
