import os.path
from gungame51.core import getGameDir
from gungame51.core.messaging import __messages__

def loadTranslation(name=None):
    '''
    Returns a list of valid addon names from the included and custom addons
    directory.
    '''
    path = getGameDir('cfg/gungame5/translations')
    
    if name:
        # Format the name to contain a ".ini" extension
        if not '.' in name and not 'ini' in name.lower():
            name = '%s.ini' %name
        
        # Check to see if the translation file exists    
        if not os.path.isfile(os.path.join(path, name)):
            raise IOError('Unable to load the translation file "%s". The '
                %name.strip('.ini') + 'specified file path does not exist: ' +
                '"%s".' %os.path.join(path, name).replace('\\', '/'))
        
        # Load the translation file
        __messages__.load(name.split('.')[0])
    else:
        for item in os.listdir(path):
            # Ignore anything that is not a file
            if not os.path.isfile(os.path.join(path, item)):
                continue
        
            # Ignore anything that is not an INI or that does not have an extension
            if '.' in item and not 'ini' in item.split('.')[1].lower():
                continue
            
            # Load the INI
            __messages__.load(item.split('.')[0])