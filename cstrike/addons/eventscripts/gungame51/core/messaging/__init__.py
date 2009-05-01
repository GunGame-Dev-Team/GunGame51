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
from gungame51.core.players.shortcuts import Player
from gungame51.core.addons.shortcuts import getAddonInfo

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
            
    def __formatfilter(self, filter):
        filter = str(filter)
        
        if filter.isdigit():
            filter = int(filter)
            return filter
            
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

    def msg(self, filter, string, tokens={}, showPrefix=False):
        if not str(string) in __strings__:
            # Send the message as-as
            es.msg(string)
            return
            
        # Format the message
        if showPrefix:
            '''
            NEED TO FIGURE OUT THE BEST WAY TO DO THIS (get the addon title)
            '''
            message = '\4[%s]\1 ' % getAddonInfo(self.addonName)
        else:
            message = ''
            
        # Just a userid
        if isinstance(self.filter, int):
            es.tell(self.filter, '#multi', '%s%s' % (message, self.__formatString(string, tokens, self.filter)))
        
        # Playerlib filter
        else:
            # Send message
            for userid in playerlib.getUseridList(self.filter):
                es.tell(userid, '#multi', '%s%s' % (message, self.__formatString(string, tokens, userid)))
        
        
__messages__ = MessageManager()

'''

class BaseMessage(object):
    """Message class is used to broadcast linguistic messages around the server,
    with the use of translation files."""
    
    def __init__(self, addon):
        """Initializes the class."""
        self.addon = addon
        self.strings = None
        
        # Load the addon's translations via langlib.Strings() if they exist
        if not os.path.isfile(getGameDir('cfg/gungame5/translations/%s.ini'
            % self.addon)):
        self.strings = Strings(getGameDir('cfg/gungame5/translations/%s.ini' % self.addon))
        
    def __formatFilter(self, filter):
        # Format filter
        filter = str(filter)
        if filter.isdigit():
            self.filter = int(filter)
        else:
            self.filter = filter
    
    def __loadStrings(self):
        """Loads the Strings instance into the class."""
        # Does the language file exist?
        if os.path.isfile(getGameDir('cfg/gungame5/translations/%s.ini' % self.addonName)):
            self.strings = langlib.Strings(getGameDir('cfg/gungame5/translations/%s.ini' % self.addonName))
        else:
            raise IOError('Cannot load strings (%s): no string file exists.' % self.addonName)
    
    def __cleanString(self, string):
        """Cleans the string for output to the console."""
        return string.replace('\3', '').replace('\4', '').replace('\1', '')
    
    def __formatString(self, string, tokens, userid=None):
        """Retrieves and formats the string."""
        # Set the default string (generally english)
        rtnStr = self.strings(string, tokens)
        
        # Is the console, use the value of "eventscripts_language"
        if userid == 'CONSOLE':
            # !!!DO NOT EDIT BELOW!!!
            var = es.ServerVar('eventscripts_language')
            var = str(var)
            # !!!DO NOT EDIT ABOVE!!!
            
            # Get language and get the string
            langAbrv = langlib.getLangAbbreviation(var)
            rtnStr = self.strings(string, tokens, langAbrv)
        
        # Get the player's language (if we were supplied with a userid)
        elif userid:
            if playerExists(userid):
                assert playerExists(userid), ('__formatString called with invalid userid: %s' % userid)
                rtnStr = self.strings(string, tokens, getPlayer(userid).language)
        
        # Format it
        rtnStr = rtnStr.replace('#lightgreen', '\3').replace('#green', '\4').replace('#default', '\1')
        rtnStr = encodings.codecs.escape_decode(rtnStr)
        
        # Crash prevention
        # !! DO NOT REMOVE !!
        if isinstance(rtnStr, tuple):
            rtnStr = list(rtnStr)
            return rtnStr[0] + ' '
        
        # Return the string
        return rtnStr + ' '
    
    def lang(self, string, tokens={}, usePlayerLang=None):
        return self.__formatString(string, tokens, usePlayerLang)
    
    def msg(self, filter, string, tokens, showPrefix = False):
        # Setup filter
        self.__formatFilter(filter)
        
        # Format the message
        if showPrefix:
            message = '\4[%s]\1 ' % getAddonDisplayName(self.addonName)
        else:
            message = ''
        
        # Just a userid
        if isinstance(self.filter, int):
            es.tell(self.filter, '#multi', '%s%s' % (message, self.__formatString(string, tokens, self.filter)))
        
        # Playerlib filter
        else:
            # Send message
            for userid in playerlib.getUseridList(self.filter):
                es.tell(userid, '#multi', '%s%s' % (message, self.__formatString(string, tokens, userid)))
        
        # Show in console
        if self.filter == '#all':
            self.echo(0, 0, string, tokens, showPrefix)
    
    def toptext(self, filter, duration, color, string, tokens):
        # Setup filter
        self.__formatFilter(filter)
        
        # Just a userid
        if isinstance(self.filter, int):
            es.toptext(self.filter, duration, color, self.__formatString(string, tokens, self.filter))
        
        # Playerlib filter
        else:
            # Send message
            for userid in playerlib.getUseridList(self.filter):
                es.toptext(userid, duration, color, self.__formatString(string, tokens, userid))
    
    def hudhint(self, filter, string, tokens):
        # Setup filter
        self.__formatFilter(filter)
        
        # Just a userid
        if isinstance(self.filter, int):
            usermsg.hudhint(self.filter, self.__formatString(string, tokens, self.filter))
        
        # Playerlib filter
        else:
            # Send message
            for userid in playerlib.getUseridList(self.filter):
                usermsg.hudhint(userid, self.__formatString(string, tokens, userid))
    
    def saytext2(self, filter, index, string, tokens, showPrefix = False):
        # Setup filter
        self.__formatFilter(filter)
        
        # Format the message
        if showPrefix:
            message = '\4[%s]\1 ' % getAddonDisplayName(self.addonName)
        else:
            message = ''
        
        # Just a userid
        if isinstance(self.filter, int):
            usermsg.saytext2(self.filter, index, '\1%s%s' % (message, self.__formatString(string, tokens, self.filter)))
        
        # Playerlib filter
        else:
            # Send message
            for userid in playerlib.getUseridList(self.filter):
                usermsg.saytext2(userid, index, '\1%s%s' % (message, self.__formatString(string, tokens, userid)))
        
        # Show in console
        if self.filter == '#all':
            self.echo(0, 0, string, tokens, showPrefix)
    
    def centermsg(self, filter, string, tokens):
        # Setup filter
        self.__formatFilter(filter)
        
        # Just a userid
        if isinstance(self.filter, int):
            usermsg.centermsg(self.filter, self.__formatString(string, tokens, self.filter))
        
        # Playerlib filter
        else:
            # Send message
            for player in playerlib.getPlayerList(self.filter):
                usermsg.centermsg(player.userid, self.__formatString(string, tokens, player.userid))
    
    def echo(self, filter, level, string, tokens, showPrefix = False):
        # Setup filter
        self.__formatFilter(filter)
        
        # Is the debug level high enough?
        if int(gungameDebugLevel) < level:
            return
        
        # Format the message
        if showPrefix:
            message = '[%s] ' % getAddonDisplayName(self.addonName)
        else:
            message = ''
        
        # Just a userid
        if isinstance(self.filter, int) and self.filter != 0:
            # Get clean string
            cleanStr = self.__cleanString(self.__formatString(string, tokens, self.filter))
            
            # Send message
            usermsg.echo(self.filter, '%s%s' % (message, cleanStr))
        
        # Console
        elif self.filter == 0:
            # Get clean string
            cleanStr = self.__cleanString(self.__formatString(string, tokens, 'CONSOLE'))
            
            # Print message
            es.dbgmsg(0, '%s%s' % (message, cleanStr))
        
        # Playerlib filter
        else:
            for userid in playerlib.getUseridList(self.filter):
                # Get clean string
                cleanStr = self.__cleanString(self.__formatString(string, tokens, userid))
                
                # Send message
                usermsg.echo(userid, '%s%s' % (message, cleanStr))
'''