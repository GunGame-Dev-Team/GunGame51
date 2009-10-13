# ../addons/eventscripts/gungame/core/sound/__init__.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
# Python Imports
from configobj import ConfigObj
from path import path

# EventScripts Imports
import es

# ============================================================================
# >> GLOBALS
# ============================================================================
# Get the es.ServerVar() instance of "eventscripts_gamedir"
eventscripts_gamedir = es.ServerVar('eventscripts_gamedir')
# Get the es.ServerVar() instance of "eventscripts_currentmap"
eventscripts_currentmap = es.ServerVar('eventscripts_currentmap')

soundDir = path('%s/sound' %str(eventscripts_gamedir).replace('\\', '/'))
iniDir = path('%s/cfg/gungame51/sound_packs'
    %str(eventscripts_gamedir).replace('\\', '/'))

# ============================================================================
# >> CLASSES
# ============================================================================
class SoundPack(object):    
    def __init__(self, name):
        self.__pack__ = ConfigObj('%s/%s.ini' %(iniDir, name))

    def __getitem__(self, name):
        if self.__pack__.has_key(name):
            return self.__pack__[name]
        else:
            return None

    def __getattr__(self, name):
        if self.__pack__.has_key(name):
            return self.__pack__[name]
        else:
            return None

def make_downloadable():
    # Make sure we are in a map
    if str(eventscripts_currentmap) == '':
        return

    # Loop through all files in the sound_pack directory
    for f in iniDir.walkfiles():
        # Make sure the extension is ".ini"
        if not f.ext.lower() == '.ini':
            continue

        # Grab the ConfigObj for the INI
        config = ConfigObj('%s/%s' %(iniDir, f.name))

        # Loop through all names (keys) in the INI
        for name in config:
            # Make sure the name isn't "title"
            if name.lower() == 'title':
                continue

            # Make sure that the sound file exists at the given path
            if path.isfile(soundDir.joinpath(config[name])):
                # Make the sound downloadable
                es.stringtable('downloadables', 'sound/%s' %config[name])