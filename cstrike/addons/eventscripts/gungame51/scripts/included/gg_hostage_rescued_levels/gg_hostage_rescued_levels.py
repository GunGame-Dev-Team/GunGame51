# ../addons/eventscripts/gungame51/scripts/included/gg_hostage_rescued_levels/gg_hostage_rescued_levels.py

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
from gungame51.core.players.shortcuts import setAttribute
#   Weapons
from gungame51.core.weapons.shortcuts import get_level_weapon
from gungame51.core.weapons.shortcuts import get_total_levels

# =============================================================================
# >> ADDON REGISTRATION/INFORMATION
# =============================================================================
info = AddonInfo()
info.name = 'gg_hostage_rescued_levels'
info.title = 'GG Hostage Rescued' 
info.author = 'GG Dev Team' 
info.version = "5.1.%s" %"$Rev$".split('$Rev: ')[1].split()[0]

# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
gg_hostage_rescued_levels = es.ServerVar('gg_hostage_rescued_levels')
gg_hostage_rescued_rescues = es.ServerVar('gg_hostage_rescued_rescues')
gg_hostage_rescued_skip_knife = es.ServerVar('gg_hostage_rescued_skip_knife')
gg_hostage_rescued_skip_nade = es.ServerVar('gg_hostage_rescued_skip_nade')

# =============================================================================
# >> CLASSES
# =============================================================================


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    es.dbgmsg(0, 'Loaded: %s' % info.name)

    # Start all current players hostage rescue counters
    setAttribute('#all', 'hostage_rescued', 0)

def unload():
    es.dbgmsg(0, 'Unloaded: %s' % info.name)

# =============================================================================
# >> GAME EVENTS
# =============================================================================
def es_map_start(event_var):
    # Reset all hostage rescue player counters
    setAttribute('#all', 'hostage_rescued', 0)

def player_activate(event_var):
    # Set rescue player counter
    setAttribute(event_var['userid'], 'hostage_rescued', 0)

def hostage_rescued(event_var):
    # Get the player instance
    ggPlayer = Player(event_var['userid'])

    # Increment player rescues
    ggPlayer.hostage_rescued += 1

    # Enough hostages rescued to level player up?
    if ggPlayer.hostage_rescued >= int(gg_hostage_rescued_rescues):

        # Reset hostage rescued counter
        ggPlayer.hostage_rescued = 0

        # The number of levels we will level up the player
        levels = 1

        # If they shouldn't be skipping their current level, stop here
        if (not int(gg_hostage_rescued_skip_nade) and ggPlayer.weapon == 'hegrenade') \
          or (not int(gg_hostage_rescued_skip_knife) and ggPlayer.weapon == 'knife'):
            msg(ggPlayer.userid, 'CannotSkipLevel_ByRescuing',
                {'level':weapon})
            return

        # Loop through weapons of the levels we plan to level the player up past
        for weapon in getLevelupList(ggPlayer.level, 
          ggPlayer.level + int(gg_hostage_rescued_levels)):
            # If gg_hostage_rescued_skip_knife or gg_hostage_rescued_skip_nade are
            # disabled, make sure the player will not skip that level
            if (not int(gg_hostage_rescued_skip_knife) and weapon == 'knife') or \
                (not int(gg_hostage_rescued_skip_nade) and weapon == 'hegrenade'):
                msg(ggPlayer.userid, 'CannotSkipLevel_ByRescuing',
                    {'level':weapon})
                break

            # Add to the number of levels they will gain
            levels += 1

        ggPlayer.levelup(levels, 0, 'hostage_rescued')

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