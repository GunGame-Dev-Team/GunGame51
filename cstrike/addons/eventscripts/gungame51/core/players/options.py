# ../core/players/options.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''


# =============================================================================
# >> CLASSES
# =============================================================================
class PlayerOptions(object):
    '''
    Class that controls/stores custom player options.
    '''
    # =========================================================================
    # >> PlayerOptions() CLASS ATTRIBUTE METHODS
    # =========================================================================
    def __setattr__(self, name, value):
        # Set the attribute value
        object.__setattr__(self, name, value)

    def __getattr__(self, name):
        # Return the attribute value
        return object.__getattribute__(self, name)

    def __setitem__(self, name, value):
        # Forward to __setattr__
        self.__setattr__(name, value)

    def __getitem__(self, name):
        # Return using __getattr__
        return self.__getattr__(name)


class Options(object):
    '''
    Class used for custom individual player options.

    Example:
        ggPlayer = Player(userid)
        ggPlayer.options.sound = Options()
        ggPlayer.options.sound.title = 'Sounds'
        ggPlayer.options.sound.popup = popuplib.find('gg_sounds_menu')
        ggPlayer.options.sound.pack = 'default'
    '''
    # =========================================================================
    # >> Options() CLASS INITIALIZATION
    # =========================================================================
    def __init__(self):
        # Define the title
        self.title = None
        self.popup = None

    # =========================================================================
    # >> OPTIONS() CLASS ATTRIBUTE METHODS
    # =========================================================================
    def __setattr__(self, name, value):
        # Set the attribute value
        object.__setattr__(self, name, value)

    def __getattr__(self, name):
        # Return the attribute value
        return object.__getattribute__(self, name)

    def __setitem__(self, name, value):
        # Forward to __setattr__
        self.__setattr__(name, value)

    def __getitem__(self, name):
        # Return using __getattr__
        return self.__getattr__(name)
