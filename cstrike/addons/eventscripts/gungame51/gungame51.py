# ../cstrike/addons/eventscripts/gungame/gungame.py

# ============================================================================
# >> IMPORTS
# ============================================================================
# EventScripts Imports
import es

# GunGame Imports
from core.addons.shortcuts import Addon
from core.addons.shortcuts import getAddon
from core.addons.shortcuts import getAddons

# ============================================================================
# >> TEST CODE
# ============================================================================

# Create "example_addon1" and set attributes
info1 = Addon('example_addon1')
info1.name = 'example_addon1'
info1.title = 'Example addon 1' 
info1.author = 'SuperDave' 
info1.version = '1.0' 
info1.requires = ['gg_addon1', 'gg_addon2'] 
info1.conflicts= ['gg_addon3', 'gg_addon4']

# Create "example_addon2" and set attributes
info2 = Addon('example_addon2')
info2.name = 'example_addon2'
info2.title = 'Example addon 2' 
info2.author = 'XE_ManUp'
info2.version = '2.0' 
info2.requires = ['gg_addon1', 'gg_addon2'] 
info2.conflicts = ['gg_addon3', 'gg_addon4']

# Loop through the addons that we created above and list their attributes
es.dbgmsg(0, '')
for addon in getAddons():
    es.dbgmsg(0, '%s:' %addon)
    es.dbgmsg(0, '-'*40)
    for attribute in getAddons()[addon]:
        es.dbgmsg(0, '%s = %s' %(attribute, getAddons()[addon][attribute]))
    es.dbgmsg(0, '-'*40)
    es.dbgmsg(0, '')
    
# Test the getAddon() function by looking up example_addon2's title
es.dbgmsg(0, getAddon('example_addon2').title)

# Print out how many addons we have stored (should be 2)
es.dbgmsg(0, 'Addons stored: %i' %(len(getAddons())))

# Delete "example_addon2"
del info2

# Print out how many addons we have stored (should be 1)
es.dbgmsg(0, 'Addons stored: %i' %(len(getAddons())))

# Raise an error by looking up example_addon2's title
es.dbgmsg(0, getAddon('example_addon2').title)