# ../addons/eventscripts/gungame/core/menu/__init__.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
# Python Imports
from os import listdir
from os import path

# Eventscripts
import es
import popuplib
from playerlib import getUseridList

# GunGame Imports
from gungame51.core import get_file_list
from gungame51.core import get_game_dir

# ============================================================================
# >> GLOBAL VARIABLES
# ============================================================================


# ============================================================================
# >> CLASSES
# ============================================================================
class MenuManager(object):
    '''
    Class for managing menus
    '''
    def __new__(cls, *p, **k):
        if not '_gg_menus' in cls.__dict__:
            cls._gg_menus = object.__new__(cls)

        return cls._gg_menus

    def __init__(self):
        self.__loaded__ = {}

    def load(self, name):
        if name in self.__loaded__:
            raise NameError('GunGame menu "%s" is already loaded' % name)
            
        menu_folder = get_game_dir('addons/eventscripts/gungame51/core/menus')

        if name == '#all':
            menu_files = []
            for file_name in listdir(menu_folder):

                if path.isdir(file_name):
                    continue
                file_name = file_name.split('.')

                if file_name[0] == '__init__':
                    continue

                if file_name[-1] != 'py':
                    continue

                if file_name[0] not in self.__loaded__.keys():
                    self.load(file_name[0])

        elif path.isfile(menu_folder + '/%s.py' % name):
            menuInstance = self.get_menu_by_name(name)
            self.__loaded__[name] = menuInstance
            self.call_block(menuInstance, 'load')

        else:
            raise NameError('"%s" is not a valid menu name.' % name)
        
    def unload(self, name):
        if name == '#all':
            for menu_name in self.__loaded__:
                self.unload(menu_name)

        elif name not in self.__loaded__:
            raise NameError('GunGame menu "%s" is not loaded' % name)

        else:
            menu_instance = self.get_menu_by_name(name)
            self.call_block(menu_instance, 'unload')
            del self.__loaded__[name]
            
    def send(self, name, filter_type):
        if name not in self.__loaded__:
            raise NameError('"%s" is not a loaded menu name.' % name)
            
        elif str(filter_type).isdigit():
            menu_instance = self.get_menu_by_name(name)
            self.call_block(menu_instance, 'send_menu', filter_type)
            
        elif str(filter_type).startswith('#'):
            for userid in getUseridList(filter_type):
                self.send(name, userid)
                
        else:
            raise ValueError('"%s" is not a value filter/userid' % filter_type)

    def get_menu_by_name(self, name):
        '''
        Returns the module of an addon by name
        '''
        # If the menu is loaded we have stored the module
        if name in self.__loaded__:
            return self.__loaded__[name]

        # If the menu is not loaded we need to import it
        loadedMenu = __import__(('gungame51.core.menus.%s' % name),
                                                     globals(), locals(), [''])

        # We have to reload the module to re-instantiate the globals
        reload(loadedMenu)
        return loadedMenu

    def call_block(self, menu_instance, blockname, *a, **kw):
        """ Calls a block in a loaded sub-addon """
        menu_globals = menu_instance.__dict__
        if blockname in menu_globals and callable(menu_globals[blockname]):
            menu_globals[blockname](*a, **kw)
            
# ============================================================================
# >> FUNCTIONS
# ============================================================================