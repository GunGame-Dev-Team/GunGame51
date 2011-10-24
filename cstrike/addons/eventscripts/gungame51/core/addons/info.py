# ../core/addons/info.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''


# =============================================================================
# >> CLASSES
# =============================================================================
class AddonInfo(dict):
    '''
    This will hold the sub-addon info similar to es.AddonInfo().
    It will be initialized in sub-addons that wish to use it.
    '''
    # =========================================================================
    # >> AddonInfo() CLASS INITIALIZATION
    # =========================================================================
    def __init__(self):
        '''
        Initialize the dictionary and populate it with mandatory
        information.

        NOTE:
            This class is intended for internal use only.

        USAGE:
            from gungame.core.addons import AddonInfo

            info = AddonInfo()

            # The addon's name, as if you were unsing es_load
            info.name = 'example_addon'

            # The title of the addon, as it would be displayed in a menu
            info.title = 'Example Addon'

            # The author's name
            info.author = 'yournamehere'

            # The version number
            info.version = '1.0'
                * This number will be overrided if you have the SVN keyword
                  Rev in the doc string

            # GunGame scripts that are required for your addon to run properly
            # This MUST be a list
            info.requires = ['gg_addon1', 'gg_addon2']

            # GunGame scripts that will conflict with your addon if loaded
            # This MUST be a list
            info.conflicts= ['gg_addon3', 'gg_addon4']
        '''

        self.name = ''
        self.title = ''
        self.author = ''
        self.requires = []
        self.conflicts = []
        self.translations = []

    # =========================================================================
    # >> AddonInfo() CLASS ATTRIBUTE METHODS
    # =========================================================================
    def __setattr__(self, attr, value):
        '''
        Setting an attribute is equivalent to setting an item
        '''

        # Set the item
        self.__setitem__(attr, value)

    def __getattr__(self, attr):
        '''
        Getting an attribute is equivalent to getting an item
        '''

        # Get the item
        return self.__getitem__(attr)

    def __setitem__(self, item, value):
        '''Verifies that the "item" is a proper key name before setting'''

        # Is the "item" a proper key name?
        if not item in self._get_key_list():

            # If not, raise an error about the given "item"
            raise KeyError(
                'AddonInfo instance has no key: "%s".  Use only "%s"' %
                (item, '", "'.join(self._get_key_list())))

        # Set the key to the given value
        super(AddonInfo, self).__setitem__(item, value)

    def __getitem__(self, item):
        '''Verifies that the "item" is a proper key name before getting'''

        # Is the "item" a proper key name?
        if not item in self._get_key_list():

            # If not, raise an error about the given "item"
            raise KeyError(
                'AddonInfo instance has no key: "%s". Use only "%s".' %
                (item, '", "'.join(self._get_key_list())))

        # Is the item wanted "version"?
        if item == 'version':

            # Has a "version" been set?
            if not item in self:

                # If not, return 0 as the current version
                return '0.0'

        # Return the item's value
        return super(AddonInfo, self).__getitem__(item)

    # =========================================================================
    # AddonInfo() STATIC CLASS METHODS
    # =========================================================================
    @staticmethod
    def _get_key_list():
        '''
        Return a list of valid attributes.
        '''
        return ['name', 'title', 'author', 'version', 'requires', 'conflicts',
                'translations']
