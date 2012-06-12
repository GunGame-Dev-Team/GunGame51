# ../core/messaging/__init__.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# Eventscripts Imports
import es
from langlib import Strings
from langlib import getLangAbbreviation
from playerlib import getPlayer
from playerlib import getUseridList
import usermsg

# GunGame Imports
from gungame51.core import get_game_dir


# =============================================================================
# >> CLASSES
# =============================================================================
class MessageStrings(Strings):
    # =========================================================================
    # >> MessageStrings() CLASS METHODS
    # =========================================================================
    def __setitem__(self, item, value):
        # Do not allow duplicate message strings to be added
        if item in self:
            raise ValueError('Unable to add message translation string "%s". '
                % item + 'The message string "%s" already exists from another '
                % item + 'translation file.')

        super(MessageStrings, self).__setitem__(item, value)

    # =========================================================================
    # >> MessageStrings() CUSTOM CLASS METHODS
    # =========================================================================
    def clear(self):
        super(MessageStrings, self).clear()


__strings__ = MessageStrings()


class AddonStrings(object):
    # =========================================================================
    # >> AddonStrings() CLASS INITIALIZATION
    # =========================================================================
    def __init__(self, addon):
        '''Initializes the class.'''
        self.addon = addon
        self.strings = None
        self.__denied__ = []

        # Retrieve the addon INI
        addonINI = self.get_addon_ini(addon)

        # Load the addon's translations via langlib.Strings() if they exist
        if not addonINI.isfile():
            return

        # Retrieve the langlib Strings()
        self.strings = Strings(addonINI)

        # Loop through all strings
        for string in self.strings:
            try:
                # Try adding the langlib.Strings() to MessageStrings()
                __strings__[string] = self.strings[string]
            except ValueError, e:
                if not string in self.__denied__:
                    self.__denied__.append(string)
                es.dbgmsg(0, '%s: %s' % (self.addon, e))

    # =========================================================================
    # AddonStrings() STATIC CLASS METHODS
    # =========================================================================
    @staticmethod
    def get_addon_ini(addon):
        # If the INI is the main GunGame INI, return the path to the INI
        if addon == "gungame":
            return get_game_dir("addons/eventscripts/gungame51/gungame.ini")

        # The INI must be either included or custom at this point
        from gungame51.core.addons.valid import ValidAddons

        # Get the addon type
        addon_type = ValidAddons.get_addon_type(addon)

        # Return the path to the addon INI
        return get_game_dir("addons/eventscripts/gungame51/scripts/" +
            "%s/%s/%s.ini" % (addon_type, addon, addon))


class MessageManager(object):
    def __new__(cls, *p, **k):
        if not '_the_instance' in cls.__dict__:
            cls._the_instance = object.__new__(cls)
            # Create the class instance variables
            cls._the_instance.__loaded__ = {}
            cls._the_instance.__addontranslations__ = {}
        return cls._the_instance

    # =========================================================================
    # >> MessageManager() CUSTOM CLASS METHODS
    # =========================================================================
    def load(self, name, addon):
        # If the translation file is loaded we cannot load it again
        if name not in self.__loaded__:
            '''
            raise NameError('GunGame translation file "%s" is already loaded.'
                %name)
            '''

            # Import strings to MessageStrings() class via AddonStrings()
            strings = AddonStrings(name)

            # Save the translation file by name so we know that it is loaded
            self.__loaded__[name] = strings

            # Add a key for the translation file and create a list containing
            #  this addon's name
            self.__addontranslations__[name] = [addon]

        else:
            # Append the addon to the addon translations list for this
            #   translation file
            self.__addontranslations__[name].append(addon)

    def unload(self, name, addon):
        # If the translation file is not loaded we cannot unload it
        if name not in self.__loaded__:
            raise NameError('GunGame translation file "%s" is not loaded.'
                % name)

        # If the translation file is not loaded via an addon, we cannot unload
        if addon not in self.__addontranslations__[name]:
            raise NameError('GunGame translation file "%s" is not loaded '
                % name + 'for addon "%s"' % addon)

        # Remove the addon from the addon translations list
        self.__addontranslations__[name].remove(addon)

        # See if any more addons are using this translation file
        if len(self.__addontranslations__[name]):
            return

        # Remove the strings from the MessageStrings() container
        for message in self.__loaded__[name].strings:
            # Only remove the string if it was not previously denied
            if not message in self.__loaded__[name].__denied__:
                del __strings__[message]

        # Remove the translation file from the loaded translations dictionary
        del self.__loaded__[name]

    def __format_filter(self, filter):
        filter = str(filter)

        if filter.isdigit():
            return int(filter)

        return filter

    def __clean_string(self, string):
        '''Cleans the string for output to the console.'''
        return string.replace('\3', '').replace('\4',
                    '').replace('\1', '').replace('\5', '')

    def __format_string(self, string, tokens, userid=0):
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
        string = string.replace('#lightgreen', '\3').replace('#green',
            '\4').replace('#default', '\1').replace('#darkgreen',
            '\5').replace('"', "'")

        '''
        # Not sure what this does, so I will leave it commented out for now:
        string = encodings.codecs.escape_decode(rtnStr)
        '''
        # Return the string
        return string

    def __format_prefix(self, prefix, string):
        if prefix:
            from gungame51.core.addons import AddonManager
            from gungame51.core.addons.shortcuts import get_addon_info
            if prefix == True:
                # Retrieve the addon title that contains the message string
                for addon in self.__loaded__:
                    if not string in self.__loaded__[addon].strings:
                        continue

                    if not addon in AddonManager().__loaded__:
                        continue

                    return '\4[%s]\1 ' % get_addon_info(addon).title

                return ''
            else:
                if not prefix in AddonManager().__loaded__:
                    return ''

                # Get the addon title that we were given
                return '\4[%s]\1 ' % get_addon_info(prefix).title
        else:
            return ''

    def msg(self, filter, string, tokens={}, prefix=False):
        # Format the filter
        filter = self.__format_filter(filter)

        # Format the message with the prefix if needed
        prefix = self.__format_prefix(prefix, string)

        # Check if this is a normal message
        if not str(string) in __strings__:
            if isinstance(filter, int):
                # Send message to the userid
                return es.tell(
                    filter, '#multi', '#default%s%s' % (prefix, string))

            # Send message to the userids from the playerlib filter
            for userid in getUseridList(filter):
                es.tell(userid, '#multi', '#default%s%s' % (prefix, string))
        else:
            if isinstance(filter, int):
                # Send message to the userid
                return es.tell(filter, '#multi', '#default%s%s'
                    % (prefix, self.__format_string(string, tokens, filter)))

            # Send message to the userids from the playerlib filter
            for userid in getUseridList(filter):
                es.tell(userid, '#multi', '#default%s%s'
                    % (prefix, self.__format_string(string, tokens, userid)))

    def saytext2(self, filter, index, string, tokens={}, prefix=False):
        # Setup filter
        self.__format_filter(filter)

        # Format the message with the prefix if needed
        prefix = self.__format_prefix(prefix, string)

        # Check if this is a normal message
        if not str(string) in __strings__:
            # Send message to the userid
            if isinstance(filter, int):
                return usermsg.saytext2(filter, index, '\1%s%s'
                    % (prefix, string), 0, 0, 0, 0)

            # Playerlib filter
            for userid in getUseridList(filter):
                usermsg.saytext2(userid, index, '\1%s%s' % (prefix, string), 0,
                    0, 0, 0)
        else:
            # Send message to the userid
            if isinstance(filter, int):
                return usermsg.saytext2(filter, index, '\1%s%s'
                    % (prefix, self.__format_string(string, tokens, filter)),
                        0, 0, 0, 0)

            # Send message to the userids from the playerlib filter
            for userid in getUseridList(filter):
                usermsg.saytext2(userid, index, '\1%s%s'
                    % (prefix, self.__format_string(string, tokens, userid)),
                        0, 0, 0, 0)

        # Show in console
        '''
        if self.filter == '#all':
            self.echo(0, 0, string, tokens, showPrefix)
        '''

    def centermsg(self, filter, string, tokens={}):
        # Setup filter
        filter = self.__format_filter(filter)

        # Check if this is a normal message
        if not str(string) in __strings__:
            # Send message to the userid
            if isinstance(filter, int):
                return usermsg.centermsg(filter, string)

            # Send message to the userids from the playerlib filter
            for userid in getUseridList(filter):
                usermsg.centermsg(userid, string)
        else:
            # Send message to the userid
            if isinstance(filter, int):
                return usermsg.centermsg(filter,
                    self.__format_string(string, tokens, filter))

            # Send message to the userids from the playerlib filter
            for userid in getUseridList(filter):
                usermsg.centermsg(userid,
                    self.__format_string(string, tokens, userid))

    def hudhint(self, filter, string, tokens={}):
        # Setup filter
        filter = self.__format_filter(filter)

        # Check if this is a normal message
        if not str(string) in __strings__:
            # Send message to the userid
            if isinstance(filter, int):
                return usermsg.hudhint(filter, string)

            # Send message to the userids from the playerlib filter
            for userid in getUseridList(filter):
                usermsg.hudhint(userid, string)
        else:
            # Send message to the userid
            if isinstance(filter, int):
                return usermsg.hudhint(filter,
                    self.__format_string(string, tokens, filter))

            # Send message to the userids from the playerlib filter
            for userid in getUseridList(filter):
                usermsg.hudhint(userid,
                    self.__format_string(string, tokens, userid))

    def toptext(self, filter, duration, color, string, tokens={}):
        # Setup filter
        filter = self.__format_filter(filter)

        # Check if this is a normal message
        if not str(string) in __strings__:
            # Send message to the userid
            if isinstance(filter, int):
                return es.toptext(filter, duration, color, string)

            # Send message to the userids from the playerlib filter
            for userid in getUseridList(filter):
                es.toptext(userid, duration, color, string)
        else:
            # Send message to the userid
            if isinstance(filter, int):
                return es.toptext(filter, duration, color,
                    self.__format_string(string, tokens, filter))

            # Send message to the userids from the playerlib filter
            for userid in getUseridList(filter):
                es.toptext(userid, duration, color,
                    self.__format_string(string, tokens, userid))

    def echo(self, filter, level, string, tokens={}, prefix=False):
        # Setup filter
        filter = self.__format_filter(filter)

        '''
        # Is the debug level high enough?
        if int(gungameDebugLevel) < level:
            return
        '''

        # Format the message with the prefix if needed
        prefix = self.__format_prefix(prefix, string)

        # Check if this is a normal message
        if not str(string) in __strings__:
            # Get clean string
            string = self.__clean_string(string)

            # Console or Userid
            if isinstance(filter, int):
                # Send message
                return usermsg.echo(filter, '%s%s' % (prefix, string))

            # Send message to the userids from the playerlib filter
            for userid in getUseridList(filter):
                # Send message
                usermsg.echo(userid, '%s%s' % (prefix, string))
        else:
            # Console or Userid
            if isinstance(filter, int):
                # Get clean string
                string = self.__clean_string(self.__format_string(string,
                                                            tokens, filter))

                # Send message
                return usermsg.echo(filter, '%s%s' % (prefix, string))

            # Send message to the userids from the playerlib filter
            for userid in getUseridList(filter):
                # Send message
                usermsg.echo(userid, '%s%s' % (prefix,
                    self.__clean_string(self.__format_string(string,
                                                            tokens, userid))))

    def langstring(self, string='', tokens={}, userid=0, prefix=False):
        # Format the message with the prefix if needed
        prefix = self.__format_prefix(prefix, string)

        # Return the formatted language string
        return '%s%s' % (prefix,
            self.__clean_string(self.__format_string(string, tokens, userid)))
