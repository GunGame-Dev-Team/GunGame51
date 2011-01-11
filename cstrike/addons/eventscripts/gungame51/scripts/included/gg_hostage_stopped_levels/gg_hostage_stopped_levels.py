# ../scripts/included/gg_hostage_stopped_levels/gg_hostage_stopped_levels.py

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
from playerlib import getPlayer

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
info.name = 'gg_hostage_stopped_levels'
info.title = 'GG Hostage Stopped'
info.author = 'GG Dev Team'
info.version = "5.1.%s" % "$Rev$".split('$Rev: ')[1].split()[0]

# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
gg_hostage_stopped_levels = es.ServerVar('gg_hostage_stopped_levels')
gg_hostage_stopped_stops = es.ServerVar('gg_hostage_stopped_stops')
gg_hostage_stopped_skip_knife = es.ServerVar('gg_hostage_stopped_skip_knife')
gg_hostage_stopped_skip_nade = es.ServerVar('gg_hostage_stopped_skip_nade')

# =============================================================================
# >> CLASSES
# =============================================================================


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    es.dbgmsg(0, 'Loaded: %s' % info.name)

    # Start all current players hostage stop counters
    setAttribute('#all', 'hostage_stopped', 0)


def unload():
    es.dbgmsg(0, 'Unloaded: %s' % info.name)


# =============================================================================
# >> GAME EVENTS
# =============================================================================
def es_map_start(event_var):
    # Reset all hostage stop player counters
    setAttribute('#all', 'hostage_stopped', 0)


def player_activate(event_var):
    # Set rescue player counter
    setAttribute(event_var['userid'], 'hostage_stopped', 0)


def player_death(event_var):
    # Find the number of hostages following the victim
    handle = getPlayer(event_var['userid']).handle
    hostages = len(filter(lambda index: es.getindexprop(index,
        'CHostage.m_leader') == handle, es.createentitylist('hostage_entity')))

    # Were any hostages following?
    if not hostages:
        return

    # Was suicide?
    attacker = int(event_var['attacker'])
    if not attacker:
        return

    # Was a team kill?
    if event_var['es_userteam'] == event_var['es_attackerteam']:
        return

    # Get the attacker instance
    ggPlayer = Player(attacker)

    # Increment player hostage stops
    ggPlayer.hostage_stopped += hostages

    # Enough hostages stopped to level player up?
    if ggPlayer.hostage_stopped >= int(gg_hostage_stopped_stops):

        # Decrease the hostage stopped counter
        ggPlayer.hostage_stopped -= int(gg_hostage_stopped_stops)

        # The number of levels we will level up the player
        levels = 1

        # If they shouldn't be skipping their current level, stop here
        if (not int(gg_hostage_stopped_skip_nade)
          and ggPlayer.weapon == 'hegrenade') or (
          not int(gg_hostage_stopped_skip_knife)
          and ggPlayer.weapon == 'knife'):
            msg(ggPlayer.userid, 'CannotSkipLevel_ByStopping',
                {'level': ggPlayer.weapon})
            return

        # Loop through weapons of the levels we plan to level the player past
        for weapon in getLevelupList(ggPlayer.level,
          ggPlayer.level + int(gg_hostage_stopped_levels)):
            # If gg_hostage_stopped_skip_knife or gg_hostage_stopped_skip_nade
            # are disabled, make sure the player will not skip that level
            if (not int(gg_hostage_stopped_skip_knife)
              and weapon == 'knife') or (
              not int(gg_hostage_stopped_skip_nade)
              and weapon == 'hegrenade'):
                msg(ggPlayer.userid, 'CannotSkipLevel_ByStopping',
                    {'level': weapon})
                break

            # Add to the number of levels they will gain
            levels += 1

        ggPlayer.levelup(levels, 0, 'hostage_stopped')


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
