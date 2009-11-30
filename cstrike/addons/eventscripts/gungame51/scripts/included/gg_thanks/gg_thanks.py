# ../addons/eventscripts/gungame/scripts/included/gg_thanks/gg_thanks.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
# Python Imports


# Eventscripts Imports
import es
from cmdlib import registerSayCommand
from cmdlib import unregisterSayCommand

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.messaging.shortcuts import msg

# ============================================================================
# >> ADDON REGISTRATION/INFORMATION
# ============================================================================
info = AddonInfo()
info.name = 'gg_thanks'
info.title = 'GG Thanks' 
info.author = 'GG Dev Team' 
info.version = '0.1'

# ============================================================================
# >> GLOBAL VARIABLES
# ============================================================================
credits = {
    'Project Leaders':
        ['XE_ManUp',
        'RideGuy',
        'Warren Alpert',
        'your-name-here',
        'Monday'],

    'Developers':
        ['cagemonkey'],

    'Beta Testers':
        [],

    'Special Thanks':
        ['gameservers.pro',
        'Predator',
        'tnb=[porsche]911',
        'RG3 Community',
        'counter-strike.com',
        'The Cheebs'],
}

# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    es.dbgmsg(0, 'Loaded: %s' % info.name)
    registerSayCommand('!thanks', thanks, 'Displays a list of those involved with development and testing of GunGame.')

def unload():
    es.dbgmsg(0, 'Unloaded: %s' % info.name)
    unregisterSayCommand('!thanks')

# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
def thanks(userid, args):
    msg(userid, 'CheckConsole')
    
    es.cexec(userid, 'echo [GG Thanks] ')
    # Loop through the credits
    for x in ('Project Leaders', 'Developers', 'Beta Testers', 'Special Thanks'):
        # Print category
        es.cexec(userid, 'echo [GG Thanks] %s:' % (x))
        
        # Show all in this category
        for y in credits[x]:
            es.cexec(userid, 'echo [GG Thanks]    %s' % y)
        
        es.cexec(userid, 'echo [GG Thanks] ')