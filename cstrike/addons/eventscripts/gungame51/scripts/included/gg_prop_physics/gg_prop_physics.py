# ../scripts/included/gg_prop_physics/gg_prop_physics.py

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
from gamethread import delayed

# GunGame Imports
#   Addons
from gungame51.core.addons.shortcuts import AddonInfo
#   Messaging
from gungame51.core.messaging.shortcuts import msg
#   Players
from gungame51.core.players.shortcuts import Player
#   Weapons
from gungame51.core.weapons.shortcuts import get_level_multikill

# =============================================================================
# >> ADDON REGISTRATION/INFORMATION
# =============================================================================
info = AddonInfo()
info.name = 'gg_prop_physics'
info.title = 'GG Prop Physics'
info.author = 'Satoon101'
info.version = "5.1.%s" % "$Rev$".split('$Rev: ')[1].split()[0]
info.translations = ['gg_prop_physics']

# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
gg_prop_physics_nade = es.ServerVar('gg_prop_physics_increment_nade')
gg_prop_physics_knife = es.ServerVar('gg_prop_physics_increment_knife')

gg_multi_messages = set()


# =============================================================================
# >> GAME EVENTS
# =============================================================================
def player_death(event_var):
    # Was the death caused by prop_physics?
    if event_var['weapon'] != 'prop_physics':
        return

    attacker = event_var['attacker']
    userid = event_var['userid']

    # Was there an attacker, or was it a suicide?
    if attacker in (userid, '0'):
        return

    # Was it a Team Kill?
    if event_var['es_userteam'] == event_var['es_attackerteam']:
        return

    # Get the Player instance
    ggPlayer = Player(attacker)

    # Get the multikill amount
    multiKill = get_level_multikill(ggPlayer.level)

    # Is the weapon able to be levelled up?
    if (not int(gg_prop_physics_nade)
      and ggPlayer.weapon == 'hegrenade') or (
      not int(gg_prop_physics_knife)
      and ggPlayer.weapon == 'knife'):

        # Send a message if it hasn't already been sent
        if not ggPlayer.userid in gg_multi_messages:

            # Get the difference between multikill amounts
            killDifference = multiKill - ggPlayer.multikill

            # Which message should we send
            message = 'Cannot%sLevel_WithPropPhysics' % (
                'Skip' if killDifference == 1 else 'Increment')

            # Send the message
            msg(ggPlayer.userid, message, {'level': ggPlayer.weapon})

            # Add userid to gg_multi_messages, so they don't get sent multiples
            gg_multi_messages.add(ggPlayer.userid)

            # Delay to remove userid from gg_multi_messages
            delayed(0, gg_multi_messages.discard, ggPlayer.userid)

        return

    # If set to 1, level the player up
    if multiKill == 1:

        # Level them up
        levelup_player(ggPlayer, userid)
        return

    # Multikill value is > 1 ... add 1 to the multikill
    ggPlayer.multikill += 1

    # Finished the multikill?
    if ggPlayer.multikill >= multiKill:

        # Level them up
        levelup_player(ggPlayer, userid)

    # Increment their current multikill value
    else:

        # Message the attacker
        multiKill = get_level_multikill(ggPlayer.level)
        ggPlayer.hudhint('MultikillNotification',
                           {'kills': ggPlayer.multikill, 'total': multiKill})

        # Play the multikill sound
        ggPlayer.playsound('multikill')


# =============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# =============================================================================
def levelup_player(ggPlayer, userid):
    # Level player up
    ggPlayer.levelup(1, userid, 'kill')

    # Play the levelup sound
    ggPlayer.playsound('levelup')
