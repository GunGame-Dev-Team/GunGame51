# ../core/players/sounds.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''
# =============================================================================
# IMPORTS
# =============================================================================
import es


# =============================================================================
# >> CLASSES
# =============================================================================
class PlayerSounds(object):
    def playsound(self, sound, volume=1.0):
        '''
        Plays the declared sound to the player.
        '''
        # Format the sound
        sound = self._format_sound(sound)

        # Make sure the sound exists
        if sound:
            # Play the sound
            es.playsound(self.userid, sound, volume)

        # Return the sound used
        return sound

    def emitsound(self, sound, volume=1.0, attenuation=1.0):
        '''
        Emits the declared sound from the player.
        '''
        # Format the sound
        sound = self._format_sound(sound)

        # Make sure the sound exists
        if sound:
            # Play the sound
            es.emitsound('player', self.userid, sound, volume, attenuation)

        # Return the sound used
        return sound

    def stopsound(self, sound):
        '''
        Stops the sound from being played for the player.
        '''
        # Format the sound
        sound = self._format_sound(sound)

        # Make sure the sound exists
        if sound:
            # Stop the sound
            es.stopsound(self.userid, sound)

        # Return the sound used
        return sound

    def _format_sound(self, sound):
        if not self.soundpack[sound]:
            return None
        return self.soundpack[sound]