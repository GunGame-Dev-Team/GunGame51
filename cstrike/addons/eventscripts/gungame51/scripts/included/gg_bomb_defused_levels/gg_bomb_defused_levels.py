# ../scripts/included/gg_bomb_defused_levels/gg_bomb_defused_levels.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports


# Eventscripts Imports
import es

# GunGame Imports
#   Addons
from gungame51.core.addons.shortcuts import AddonInfo
#   Messaging
from gungame51.core.messaging.shortcuts import msg
#   Players
from gungame51.core.players.shortcuts import Player
#   Weapons
from gungame51.core.weapons.shortcuts import get_level_weapon
from gungame51.core.weapons.shortcuts import get_total_levels

# =============================================================================
# >> ADDON REGISTRATION/INFORMATION
# =============================================================================
info = AddonInfo()
info.name = 'gg_bomb_defused_levels'
info.title = 'GG Welcome Message'
info.author = 'GG Dev Team'
info.version = "5.1.%s" % "$Rev$".split('$Rev: ')[1].split()[0]
info.translations = ['gg_bomb_defused_levels']

# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
gg_bomb_defused_levels = es.ServerVar('gg_bomb_defused_levels')
gg_bomb_defused_skip_knife = es.ServerVar('gg_bomb_defused_skip_knife')
gg_bomb_defused_skip_nade = es.ServerVar('gg_bomb_defused_skip_nade')


# =============================================================================
# >> GAME EVENTS
# =============================================================================
def bomb_defused(event_var):
    # Get the player instance
    ggPlayer = Player(event_var['userid'])

    # The number of levels we will level up the player
    levels = 1

    # If they shouldn't be skipping their current level, stop here
    if (not int(gg_bomb_defused_skip_nade) and ggPlayer.weapon == '' +
            'hegrenade') \
      or (not int(gg_bomb_defused_skip_knife) and ggPlayer.weapon == 'knife'):
        msg(ggPlayer.userid, 'CannotSkipLevel_ByDefusing',
            {'level': ggPlayer.weapon})
        return

    # Loop through weapons of the levels we plan to level the player up past
    for weapon in getLevelupList(ggPlayer.level,
      ggPlayer.level + int(gg_bomb_defused_levels)):
        # If gg_bomb_defused_skip_knife or gg_bomb_defused_skip_nade are
        # disabled, make sure the player will not skip that level
        if (not int(gg_bomb_defused_skip_knife) and weapon == 'knife') or \
            (not int(gg_bomb_defused_skip_nade) and weapon == 'hegrenade'):
            msg(ggPlayer.userid, 'CannotSkipLevel_ByDefusing',
                {'level': weapon})
            break

        # Add to the number of levels they will gain
        levels += 1

    # Level up the player
    ggPlayer.levelup(levels, 0, 'bomb_defused')


# =============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# =============================================================================
def getLevelupList(currentLevel, levelupLevel):
    levelupList = []

    # Get the total number of levels
    totalLevels = get_total_levels()

    # If the player would exceed the total number of levels, stop at the total
    if levelupLevel > totalLevels:
        levelupLevel = totalLevels

    # Create a list of the weapon names for levels we plan to level the player
    # up past
    for level in xrange(currentLevel + 1, levelupLevel):
        levelupList.append(get_level_weapon(level))

    # Return the list
    return levelupList
