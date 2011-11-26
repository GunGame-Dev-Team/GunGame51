# ../core/cfg/loaded.py

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

# GunGame Imports
#   Addons
from gungame51.core.addons.valid import ValidAddons


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
_base_configs = path(__file__).parent.joinpath('files')


# =============================================================================
# >> CLASSES
# =============================================================================
class _LoadedConfigs(dict):
    '''Class used to store loaded config files'''

    def __getitem__(self, item):
        '''Verify that the given item is a config file instance and store it'''

        # Is the item already in the dictionary?
        if item in self:

            # Return the item
            return super(_LoadedConfigs, self).__getitem__(item)

        # Get the path if the item is an addon
        addon = item.replace('_config', '')

        # Is the item a Valid Addon?
        if addon in ValidAddons.all:

            # Set the path to import
            import_path = 'gungame51.scripts.%s.%s.%s' % (
                ValidAddons.get_addon_type(addon), addon, item)

        # Is the item a base config?
        elif _base_configs.joinpath(item + '.py').isfile():

            # Set the path to import
            import_path = 'gungame51.core.cfg.files.%s' % item

        # Is the given item neither a Valid Addon nor a base config?
        else:

            # Raise an error
            raise ValueError('"%s" is an invalid config file' % item)

        # Import the config file
        config = self[item] = __import__(
            import_path, globals(), locals(), [''])

        # Reload the config file
        reload(config)

        # Does the config have a load function?
        if 'load' in config.__dict__:

            # Execute the load function
            config.load()

        # Return the imported config file
        return config

    def clear(self):
        '''Unloads all configs within the dicionary'''

        # Loop through all configs in the dictionary
        for config in self:

            # Does the config have an unload function?
            if 'unload' in self[config].__dict__:

                # Execute the unload function
                self[config].unload()

        # Clear the dictionary
        super(_LoadedConfigs, self).clear()

# Get the LoadedConfigs instance
LoadedConfigs = _LoadedConfigs()
