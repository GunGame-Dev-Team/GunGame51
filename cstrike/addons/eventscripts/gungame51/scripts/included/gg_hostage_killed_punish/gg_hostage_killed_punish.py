# ../scripts/included/gg_hostage_killed_punish/gg_hostage_killed_punish.py

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
#   Players
from gungame51.core.players.shortcuts import Player
from gungame51.core.players.shortcuts import setAttribute

# =============================================================================
# >> ADDON REGISTRATION/INFORMATION
# =============================================================================
info = AddonInfo()
info.name = 'gg_hostage_objective'
info.title = 'GG Hostage Objective'
info.author = 'GG Dev Team'
info.version = "5.1.%s" % "$Rev$".split('$Rev: ')[1].split()[0]
info.translations = ['gg_hostage_killed_punish']

# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
gg_hostage_killed_punish = es.ServerVar('gg_hostage_killed_punish')
gg_hostage_killed_kills = es.ServerVar('gg_hostage_killed_kills')

# =============================================================================
# >> CLASSES
# =============================================================================


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    es.dbgmsg(0, 'Loaded: %s' % info.name)

    # Start all current players hostage killed counters
    setAttribute('#all', 'hostage_killed', 0)


def unload():
    es.dbgmsg(0, 'Unloaded: %s' % info.name)


# =============================================================================
# >> GAME EVENTS
# =============================================================================
def es_map_start(event_var):
    # Reset all hostage killed player counters
    setAttribute('#all', 'hostage_killed', 0)


def player_activate(event_var):
    # Set hostage killed player counter
    setAttribute(event_var['userid'], 'hostage_killed', 0)


def hostage_killed(event_var):
    # Was fall damage?
    attacker = int(event_var['userid'])
    if not attacker:
        return

    # Get the attacker instance
    ggPlayer = Player(attacker)

    # Increment player hostage kills
    ggPlayer.hostage_killed += 1

    # Enough hostages killed to punish?
    if ggPlayer.hostage_killed >= int(gg_hostage_killed_kills):

        # Reset hostage killed counter
        ggPlayer.hostage_killed = 0

        # Punish the player
        ggPlayer.leveldown(int(gg_hostage_killed_punish), 0, 'hostage_killed')

        # Message
        ggPlayer.msg('Hostage_Killed_LevelDown', {'newlevel': ggPlayer.level},
                        prefix='gg_hostage_killed_punish')

        # Play the leveldown sound
        ggPlayer.playsound('leveldown')

# =============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# =============================================================================
