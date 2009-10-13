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
from random import choice

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
            # See if this is a random sound file
            if self._is_random(self.__pack__[name]):
                # Return the random sound from the file
                return self.get_random_sound(self.__pack__[name])

            # Return the sound name
            return self.__pack__[name]
        else:
            return None

    def __getattr__(self, name):
        if self.__pack__.has_key(name):
            # See if this is a random sound file
            if self._is_random(self.__pack__[name]):
                # Return the random sound from the file
                return self.get_random_sound(self.__pack__[name])

            # Return the sound name
            return self.__pack__[name]
        else:
            return None

    def _is_random(self, name):
        return (name.endswith('.txt'))

    def _random_exists(self, name):
        return (path.isfile(iniDir.joinpath('random_sound_files/%s' % name)))

    def get_random_sound(self, name):
        # Make sure the random sound file exists
        if not self._random_exists(name):
            return None

        # Open the random sound file
        randomFile = open(iniDir.joinpath('random_sound_files/%s' % name))

        # Select a random sound from the list
        randomSounds = [x.strip('\\n').strip() for x in randomFile.readlines()]

        # Close the random file
        randomFile.close()

        # Return the randomly selected sound if the list is not empty
        return choice(randomSounds) if randomSounds else None

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
            if sound_exists(config[name]):
                # Make the sound downloadable
                es.stringtable('downloadables', 'sound/%s' %config[name])
            else:
                # See if the file is a random sound text file
                if not path.isfile(iniDir.joinpath('random_sound_files/%s'
                    %config[name])):

                    continue

                # Open the random sound file
                randomFile = open(iniDir.joinpath('random_sound_files/%s'
                    %config[name]))

                # Loop through all sounds in the file
                for sound in randomFile.readlines():
                    # Remove the line return character and whitespace,
                    sound = sound.strip('\\n').strip()

                    # Make sure that the sound file exists at the given path
                    if sound_exists(sound):
                        # Make the sound downloadable
                        es.stringtable('downloadables', 'sound/%s' %sound)
                            
                # Close the random sound file
                randomFile.close()
                        
def sound_exists(sound):
    return (path.isfile(soundDir.joinpath(sound)))