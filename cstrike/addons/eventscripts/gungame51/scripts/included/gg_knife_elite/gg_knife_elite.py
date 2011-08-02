# ../scripts/included/gg_knife_elite/gg_knife_elite.py

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
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.players import Player

# =============================================================================
# >> ADDON REGISTRATION/INFORMATION
# =============================================================================
info = AddonInfo()
info.name = 'gg_knife_elite'
info.title = 'GG Knife Elite'
info.author = 'GG Dev Team'
info.version = "5.1.%s" % "$Rev$".split('$Rev: ')[1].split()[0]
info.requires = ['gg_dead_strip']
info.conflicts = ['gg_turbo']


# =============================================================================
# >> GAME EVENTS
# =============================================================================
def gg_levelup(event_var):
    # Get userid
    attacker = int(event_var['attacker'])

    # Switch the player to knife
    es.server.queuecmd('es_xsexec %s "use weapon_knife"' % attacker)

    # Strip player of all weapons but a knife
    Player(attacker).strip(True)
