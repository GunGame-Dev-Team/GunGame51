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
        'Warren',
        'your-name-here'],

    'Developers':
        ['Saul',
        'HitThePipe',
        'Artsemis',
        'Don',
        'Goodfelladeal',
        'cagemonkey',
        ],

    'Beta Testers':
        ['-=CsFF=- Eagle',
        'Ace Rimmer',
        'aLpO',
        'bonbon',
        'cagemonkey',
        'Chrisber',
        'Cisco',
        'CmG Knight',
        'dajayguy',
        'danzig',
        'DerekRDenholm',
        'disconnect81',
        'DontWannaName',
        'emc0002',
        'Errant',
        'GoodfellaDeal',
        'Hacker Killer',
        'moethelawn',
        'monday',
        'Q2',
        'SIL3NT-DE4TH',
        'sp90378',
        'SquirrelEater',
        'StealthAssassin',
        'Tempe Terror1',
        'tnb=[porsche]911',
        'Predator',
        'Wallslide',
        'Warbucks',
        'waspy',
        'Wire Wolf',
        '{cDS} Blue Ape'],

    'Special Thanks':
        ['Predator',
        'tnb=[porsche]911',
        'RG3 Community',
        'counter-strike.com',
        'gameservers.pro',
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