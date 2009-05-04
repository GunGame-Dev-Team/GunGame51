# ../cstrike/addons/eventscripts/gungame51/core/messaging/__init__.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
import os.path

# Eventscripts Imports
import es
from langlib import Strings
from langlib import getLangAbbreviation
from playerlib import getPlayer

# GunGame Imports
from gungame51.core import getGameDir


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================


# =============================================================================
# >> CLASSES
# =============================================================================
class MessageStrings(Strings):
    # =========================================================================
    # >> MessageStrings() CLASS METHODS
    # =========================================================================
    def __setitem__(self, item, value):
        # Do not allow duplicate message strings to be added
        if self.has_key(item):
            raise ValueError('Unable to add message translation string "%s". '
                %item + 'The message string "%s" already exists from another '
                %item + 'translation file.')

        super(MessageStrings, self).__setitem__(item, value)

    # =========================================================================
    # >> MessageStrings() CUSTOM CLASS METHODS
    # =========================================================================
    def clear(self):
        super(MessageStrings, self).clear()


__strings__ = MessageStrings()


class AddonMessage(object):
    # =========================================================================
    # >> AddonMessage() CLASS INITIALIZATION
    # =========================================================================
    def __init__(self, addon):
        '''Initializes the class.'''
        self.addon = addon
        self.strings = None
        self.__denied__ = []
        
        # Load the addon's translations via langlib.Strings() if they exist
        if not os.path.isfile(getGameDir('cfg/gungame5/translations/%s.ini'
            % self.addon)):
            return
            
        # Retrieve the langlib Strings()
        self.strings = Strings(getGameDir('cfg/gungame5/translations/%s.ini' % self.addon))
        
        # Loop through all strings
        for string in self.strings:
            try:
                # Try adding the langlib.Strings() to MessageStrings()
                __strings__[string] = self.strings[string]
            except ValueError, e:
                if not string in self.__denied__:
                    self.__denied__.append(string)
                es.dbgmsg(0, '%s: %s' %(self.addon, e))


class MessageManager(object):
    # =========================================================================
    # >> MessageManager() CLASS INITIALIZATION
    # =========================================================================
    def __init__(self):
        self.__loaded__ = {}
        
    # =========================================================================
    # >> MessageManager() CUSTOM CLASS METHODS
    # =========================================================================
    def load(self, name):
        # If the translation file is loaded we cannot load it again
        if name in self.__loaded__:
            raise NameError('GunGame translation file "%s" is already loaded.'
                %name)
            
        # Import strings to MessageStrings() class via AddonMessage()
        strings = AddonMessage(name)
        
        # Save the translation file by name so we know that it is loaded
        self.__loaded__[name] = strings
        
    def unload(self, name):
        # If the translation file is not loaded we cannot unload it
        if name not in self.__loaded__:
            raise NameError('GunGame translation file "%s" is not loaded.'
                %name)
                
        # Remove the strings from the MessageStrings() container
        for message in self.__loaded__[name].strings:
            # Only remove the string if it was not previously denied
            if not message in self.__loaded__[name].__denied__:
                del __strings__[message]
        
        # Remove the translation file from the loaded translations dictionary
        del self.__loaded__[name]
            
    def __formatFilter(self, filter):
        filter = str(filter)
        
        if filter.isdigit():
            return int(filter)
            
        return filter
    
    def __formatString(self, string, tokens, userid=0):
        '''Retrieves and formats the string.'''
        # Make the userid an int
        userid = int(userid)
        
        if userid > 0:
            language = getPlayer(userid).getLanguage()
        else:
            # Is the console, use the value of "eventscripts_language"
            language = str(es.ServerVar('eventscripts_language'))
            
            # Get language and get the string
            language = getLangAbbreviation(language)
        
        string = __strings__(string, tokens, language)
        
        # Format it
        string = string.replace('#lightgreen', '\3').replace('#green', '\4').replace('#default', '\1')
        
        '''
        # Not sure what this does, so I will leave it commented out for now:
        string = encodings.codecs.escape_decode(rtnStr)
        '''
        # Return the string
        return string
        
    def __formatPrefix(self, prefix, string):
        if prefix:
            from gungame51.core.addons import __addons__
            from gungame51.core.addons.shortcuts import getAddonInfo
            if prefix == True:
                # Retrieve the addon title that contains the message string
                for addon in self.__loaded__:
                    if not string in self.__loaded__[addon].strings:
                        continue
                        
                    if not addon in __addons__.__loaded__:
                        continue
                        
                    return '\4[%s]\1 ' %getAddonInfo(addon).title
                    
                return ''
            else:
                if not prefix in __addons__.__loaded__:
                    return ''
                    
                # Get the addon title that we were given
                return '\4[%s]\1 ' %getAddonInfo(prefix).title
        else:
            return ''
            
    def msg(self, filter, string, tokens={}, prefix=False):
        # Format the filter
        filter = self.__formatFilter(filter)
        
        # Format the message with the prefix if needed
        prefix = self.__formatPrefix(prefix, string)
        
        # Check if this is a normal message
        if not str(string) in __strings__:
            # Send the message "as-is"
            if isinstance(filter, int):
                # Just a userid
                es.tell(filter, '#multi', '%s%s' %(prefix, string))
            else:
                # Send message to the userids from the playerlib filter
                for userid in playerlib.getUseridList(filter):
                    es.tell(userid, '#multi', '%s%s' %(prefix, string))
        else:
            if isinstance(filter, int):
                # Just a userid
                es.tell(filter, '#multi', '%s%s'
                    %(prefix, self.__formatString(string, tokens, filter)))
            else:
                # Send message to the userids from the playerlib filter
                for userid in playerlib.getUseridList(filter):
                    es.tell(userid, '#multi', '%s%s'
                        %(prefix, self.__formatString(string, tokens, userid)))


__messages__ = MessageManager()

from gungame51.core.players.shortcuts import Player