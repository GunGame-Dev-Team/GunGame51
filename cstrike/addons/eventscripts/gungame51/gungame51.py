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
info1 = Addon('example_addon1')
info1.name = 'example_addon1'
info1.title = 'Example addon 1' 
info1.author = 'SuperDave' 
info1.version = '1.0' 
info1.requires = ['gg_addon1', 'gg_addon2'] 
info1.conflicts= ['gg_addon3', 'gg_addon4']

info2 = Addon('example_addon2')
info2.name = 'example_addon2'
info2.title = 'Example addon 2' 
info2.author = 'XE_ManUp'
info2.version = '2.0' 
info2.requires = ['gg_addon1', 'gg_addon2'] 
info2.conflicts = ['gg_addon3', 'gg_addon4']

es.dbgmsg(0, '')
for addon in getAddons():
    es.dbgmsg(0, '%s:' %addon)
    es.dbgmsg(0, '-'*40)
    for attribute in getAddons()[addon]:
        es.dbgmsg(0, '%s = %s' %(attribute, getAddons()[addon][attribute]))
    es.dbgmsg(0, '-'*40)
    es.dbgmsg(0, '')
    
es.dbgmsg(0, getAddon('example_addon2').title)
es.dbgmsg(0, 'Addons stored: %i' %(len(getAddons())))
del info2
es.dbgmsg(0, 'Addons stored: %i' %(len(getAddons())))
es.dbgmsg(0, getAddon('example_addon2').title)