# ../addons/eventscripts/gungame51/scripts/included/gg_thanks/gg_thanks.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# ============================================================================
# >> IMPORTS
# ============================================================================

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
info.translations = ["gg_thanks"]

# ============================================================================
# >> GLOBAL VARIABLES
# ============================================================================
credits = {
    'Project Leaders':
        ['XE_ManUp',
        'Warren Alpert',
        'your-name-here',
        'Monday'],

    'Developers':
        ['cagemonkey',
        'llamaelite',
        'RideGuy'],

    'Beta Testers':
        ['Sir_Die',
        'pyro',
        'tnarocks',
        'D3X',
        'nad',
        'Knight',
        'Evil_SNipE',
        'k@rma',
        'tnarocks',
        'Warbucks',],

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
    registerSayCommand('!thanks', thanks, 'Displays a list of those involved' +
                       'with development and testing of GunGame.')

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
    for x in credits.keys():
        # Print category
        es.cexec(userid, 'echo [GG Thanks] %s:' % (x))
        
        # Show all in this category
        for y in credits[x]:
            es.cexec(userid, 'echo [GG Thanks]    %s' % y)
        
        es.cexec(userid, 'echo [GG Thanks] ')
        
def player_activate(event_var):
    if event_var['es_steamid'] in ('STEAM_0:1:5021657', 'STEAM_0:1:5244720', 
      'STEAM_0:0:11051207', 'STEAM_0:0:2641607'):
        es.msg('#multi', '#green[GG Thanks] #defaultProject Leader ' +
                '%s has joined the server.' % event_var['es_username'])