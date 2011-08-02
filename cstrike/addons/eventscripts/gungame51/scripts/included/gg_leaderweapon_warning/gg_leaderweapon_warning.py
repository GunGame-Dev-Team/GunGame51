# ../scripts/included/gg_leaderweapon_warning/gg_leaderweapon_warning.py

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
from playerlib import getUseridList

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.players.shortcuts import Player
from gungame51.core.leaders.shortcuts import get_leader_level
from gungame51.core.weapons.shortcuts import get_level_weapon
from gungame51.core.weapons.shortcuts import get_total_levels

# =============================================================================
# >> GLOBALS
# =============================================================================
warn_last_level_only = es.ServerVar('gg_leaderweapon_warning_only_last')

played_knife = False
played_nade = False
nade_level = 0
knife_level = 0


# =============================================================================
# >> ADDON REGISTRATION/INFORMATION
# =============================================================================
info = AddonInfo()
info.name = 'gg_leaderweapon_warning'
info.title = 'GG Leader Weapon Warning'
info.author = 'GG Dev Team'
info.version = "5.1.%s" % "$Rev$".split('$Rev: ')[1].split()[0]


# =============================================================================
# >> GAME EVENTS
# =============================================================================
def gg_start(event_var):
    global played_knife
    global played_nade
    global knife_level
    global nade_level

    # Reset the globals when GG starts
    played_knife = False
    played_nade = False
    nade_level = 0
    knife_level = 0

    # Loop through all levels
    for level in xrange(1, get_total_levels() + 1):

        # Get the weapon for the current level
        weapon = get_level_weapon(level)

        # Is the weapon hegrenade?
        if weapon == 'hegrenade':

            # Each time hegrenade is found, change nade_level so
            # that nade_level ends up being the last hegrenade level
            nade_level = level

        # Is the weapon knife?
        if weapon == 'knife':

            # Each time knife is found, change knife_level so
            # that knife_level ends up being the last knife level
            knife_level = level


def round_start(event_var):
    global played_knife
    global played_nade

    # Reset the played_ variables
    played_knife = False
    played_nade = False

    # Check to see if a sound needs played
    check_leader_warning(get_leader_level())


def gg_levelup(event_var):
    # Get the attacker
    attacker = int(event_var['attacker'])

    # Get the attacker's instance
    ggPlayer = Player(attacker)

    # Is the attacker on the leader level?
    if ggPlayer.level == get_leader_level():

        # Check to see if a sound needs played
        check_leader_warning(ggPlayer.level)


# =============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# =============================================================================
def check_leader_warning(level):
    global played_knife
    global played_nade

    # Set sound to False for use later
    sound = False

    # Get the leader's weapon
    weapon = get_level_weapon(level)

    # Is the player on knife level?
    if weapon == 'knife':

        # Has the knifelevel sound been played?
        if played_knife:
            return

        # Does the knifelevel sound always get played
        # or is the leader on the last knife level?
        if not int(warn_last_level_only) or level == knife_level:

            # Set the sound to knifelevel
            sound = 'knifelevel'

            # Set played_knife so it does not get played again this round
            played_knife = True

    # Is the player on hegrenade level?
    if weapon == 'hegrenade':

        # Has the nadelevel sound been played?
        if played_nade:
            return

        # Does the nadelevel sound always get played
        # or is the leader on the last nade level?
        if not int(warn_last_level_only) or level == nade_level:

            # Set the sound to nadelevel
            sound = 'nadelevel'

            # Set played_nade so it does not get played again this round
            played_nade = True

    # Is a sound supposed to be played?
    if not sound:

        # Do not play any sound
        return

    # Loop through all human players
    for userid in getUseridList('#human'):

        # Play the leader level sound
        Player(userid).playsound(sound)
