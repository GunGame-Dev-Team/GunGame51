# ../scripts/included/gg_retry_punish/gg_retry_punish.py

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
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.players.shortcuts import Player
from gungame51.core.players.fields.exceptions import ValidationError


# =============================================================================
# >> ADDON REGISTRATION/INFORMATION
# =============================================================================
info = AddonInfo()
info.name = 'gg_retry_punish'
info.title = 'GG Retry Punish'
info.author = 'GG Dev Team'
info.version = "5.1.%s" % "$Rev$".split('$Rev: ')[1].split()[0]


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Get the es.ServerVar() instance of "gg_retry_punish"
gg_retry_punish = es.ServerVar('gg_retry_punish')


# =============================================================================
# >> GAME EVENTS
# =============================================================================
def player_activate(event_var):
    # Get the Player() object
    ggPlayer = Player(event_var['userid'])

    if ggPlayer.level > 1:
        try:

            # Get the new value to set the player's level
            # Use max with 1 to make sure the player's
            # level will not be set to an invalid number.
            value = max(1, ggPlayer.level - int(gg_retry_punish))

            # Set the player's level
            ggPlayer.level = value

        except ValidationError:
            pass
        except (ValueError, TypeError):
            raise
