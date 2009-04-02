# ../cstrike/addons/eventscripts/gungame/gungame.py

# ============================================================================
# >> IMPORTS
# ============================================================================
# EventScripts Imports
import es

# GunGame Imports
from core.addons import AddonInfo
from core.addons import AddonManager
from core.addons.shortcuts import loadAddon
from core.addons.shortcuts import unloadAddon


# ============================================================================
# >> TEST CODE
# ============================================================================
loadAddon('gg_deathmatch')
#unloadAddon('gg_deathmatch')

from core.addons.shortcuts import getAddonInfo

loadAddon('gg_assist')
    
es.dbgmsg(0, '# of addons loaded: %i' %len(getAddonInfo()))
unloadAddon('gg_assist')
es.dbgmsg(0, '# of addons loaded: %i' %len(getAddonInfo()))
#es.dbgmsg(0, str(AddonManager.getAddonInfo('gg_assist')))

# Print out how many addons we have stored (should be 3)
#es.dbgmsg(0, 'Addons stored: %i' %(len(getAddons())))

#loadAddon('gg_elimination')
#unloadAddon('gg_elimination')