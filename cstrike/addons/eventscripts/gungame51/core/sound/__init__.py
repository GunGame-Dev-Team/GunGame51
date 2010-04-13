# ../addons/eventscripts/gungame51/core/sound/__init__.py

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
from random import shuffle
from mp3lib import mp3info
from wave import open as wave_open

# EventScripts Imports
import es
import gamethread

# ============================================================================
# >> GLOBALS
# ============================================================================
# Get the es.ServerVar() instance of "eventscripts_gamedir"
eventscripts_gamedir = es.ServerVar('eventscripts_gamedir')
# Get the es.ServerVar() instance of "eventscripts_currentmap"
eventscripts_currentmap = es.ServerVar('eventscripts_currentmap')
# Get the es.ServerVar() instance of "gg_dynamic_chattime"
gg_dynamic_chattime = es.ServerVar("gg_dynamic_chattime")
# Get the es.ServerVar() instance of "mp_chattime"
mp_chattime = es.ServerVar("mp_chattime")

soundDir = path('%s/sound' %str(eventscripts_gamedir).replace('\\', '/'))
iniDir = path('%s/cfg/gungame51/sound_packs'
    %str(eventscripts_gamedir).replace('\\', '/'))

# winnerSounds stores a shuffled list of winner sounds to come if random winner
# sounds is enabled
winnerSounds = []
# defaultChatTime stores the default mp_chattime for gg_dynamic_chattime to use
# if it cannot check the length of the winner sound
defaultChatTime = -1

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
                # If we are looking for a random winner sound, return the random winner
                # sound chosen for the current round
                if name == "winner":
                    return winnerSounds[0]

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
                # If we are looking for a random winner sound, return the random winner
                # sound chosen for the current round
                if name == "winner":
                    return winnerSounds[0]

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
    # Make the global variable winnerSounds global to this function in case we
    # use it below
    global winnerSounds

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

                # If we are on a random winner sound, and we have more sounds
                # in the current list of random sounds, choose one and make it
                # downloadable
                if name == "winner" and winnerSounds:
                    # If there are winner sounds left in the shuffled list,
                    # remove the last used sound
                    if len(winnerSounds) > 1:
                        winnerSounds.pop(0)
                        # Make the new random winner sound downloadable
                        if sound_exists(winnerSounds[0]):
                            es.stringtable('downloadables', 'sound/%s' % \
                                                            winnerSounds[0])
                        # If gg_dynamic_chattime is enabled, set the chattime
                        if int(gg_dynamic_chattime):
                            set_chattime()

                        continue
                    # If the last used winner sound is the only thing left,
                    # clear the list so that we can fill it below
                    winnerSounds = []

                # Loop through all sounds in the file
                for sound in randomFile.readlines():
                    # Remove the line return character and whitespace,
                    sound = sound.strip('\\n').strip()

                    # Do not add comment lines
                    if sound.startswith("//"):
                        continue

                    # If we are on a random winner sound, add it to the
                    # random winner sounds list
                    if name == "winner":
                        winnerSounds.append(sound)

                        # We will make the winner sound chosen for this round
                        # downloadable below this loop
                        continue

                    # Make sure that the sound file exists at the given path
                    if sound_exists(sound):
                        # Make the sound downloadable
                        es.stringtable('downloadables', 'sound/%s' % sound)

                # Now that we are done adding random winner sounds to
                # the winnerSounds list, choose one to make downloadable
                if name == "winner":
                    # Shuffle the list of new winner sounds
                    shuffle(winnerSounds)
                    # Make the new random winner sound downloadable
                    if sound_exists(winnerSounds[0]):
                        es.stringtable('downloadables', 'sound/%s' % \
                                                            winnerSounds[0])
                    # If gg_dynamic_chattime is enabled, set the chattime
                    if int(gg_dynamic_chattime):
                        set_chattime()

                # Close the random sound file
                randomFile.close()

def set_chattime():
    # Make the global variable defaultChatTime global to this function in case
    # we need to modify it
    global defaultChatTime

    # If this is the first time setting the chattime, store the default time
    if defaultChatTime == -1:
        defaultChatTime = int(mp_chattime)
    
    # If the sound does not exist on the server, use the defaultChatTime
    if not sound_exists(winnerSounds[0]):
        mp_chattime.set(defaultChatTime)
        return
    
    # Get the path and extension of the sound file
    soundPath = soundDir.joinpath(winnerSounds[0])
    extension = winnerSounds[0].split(".")[-1]
    
    duration = defaultChatTime
    
    # If the sound file is an mp3, use mp3info to find its duration
    if extension == 'mp3':
        try:
            info = mp3info(soundPath)
            duration = info['MM'] * 60 + info['SS']
        except:
            pass
    
    # If the sound file is a wav, use the wave module to find its duration
    elif extension == 'wav':
        try:
            w = wave_open(soundPath, 'rb')
            duration = float(w.getnframes()) / w.getframerate()
        except:
            pass
        finally:
            w.close()

    # If the duration is greater than 30 seconds, set it to 30 seconds
    if duration > 30:
        duration = 30

    # Set the new mp_chattime
    gamethread.delayed(5, mp_chattime.set, duration)

def sound_exists(sound):
    return (path.isfile(soundDir.joinpath(sound)))