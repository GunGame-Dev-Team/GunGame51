# ../core/cfg/dictionary.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
from path import path


# =============================================================================
# >> CLASSES
# =============================================================================
class ConfigTypeDictionary(dict):
    '''A dictionary that stores config files
        by type (main, included, and custom)'''

    def __new__(cls):
        '''Method used to make sure class is a singleton'''

        if not '_the_instance' in cls.__dict__:
            cls._the_instance = dict.__new__(cls)
        return cls._the_instance

    def __getitem__(self, item):
        '''Override the __getitem__ method of dict
            type to return the config files by type'''

        # Is the item already in the dictionary
        if item in self:

            # Return the list of cfg files
            return super(ConfigTypeDictionary, self).__getitem__(item)

        # Add the item to the dictionary and get a list of cfg files
        values = self[item] = self._get_configs_by_type(item)

        # Return the list of cfg files
        return values

    def __getattr__(self, attr):
        '''Redirects to __getitem__ since this is a dictionary'''

        # Return the item
        return self.__getitem__(attr)

    def _get_config_list(self, cfg_type=None):
        '''Returns a list of configs for the given type'''

        # Was there a given type?
        if cfg_type is None:

            # If not type is given, return all configs
            return [item.namebase for item in
                self.main.union(self.included).union(self.custom)]

        # Return the configs for the given type
        return [item.namebase for item in self[cfg_type]]

    @staticmethod
    def _get_configs_by_type(cfg_type):
        '''Returns a set of cfg files by type'''

        # Is cfg_type a proper type of cfg?
        if not cfg_type in ('main', 'included', 'custom'):

            # If not, raise an error
            raise ValueError('"%s" is not a valid config type' % cfg_type)

        # Is the cfg_type main?
        if cfg_type == 'main':

            # Get the path to the base *_config.py files
            cfg_paths = path(__file__).parent.joinpath('files')

        # Is the cfg_type for one of the script types?
        else:

            # Get the path to the script types' *_config.py files
            cfg_paths = path(path(
              __file__).parent.rsplit('core')[0]).joinpath('scripts', cfg_type)

        # Return a set of path instances of the *_config.py files
        return set(cfg_paths.walkfiles('*_config.py'))
