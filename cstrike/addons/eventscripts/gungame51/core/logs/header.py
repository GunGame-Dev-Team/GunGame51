# ../core/logs/header.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
from __future__ import with_statement
#   Time
from time import strftime

# EventScripts Imports
#   ES
from es import ServerVar

# GunGame Imports
from gungame51.core import get_os
from gungame51.core import GunGameInfo


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
ip = ServerVar('ip')
port = ServerVar('hostport')
eventscripts_ver = ServerVar('eventscripts_ver')
es_corelib_ver = ServerVar('es_corelib_ver')
spe_version = ServerVar('spe_version')
metamod_version = ServerVar('metamod_version')
sourcemod_version = ServerVar('sourcemod_version')
mani_admin_plugin_version = ServerVar('mani_admin_plugin_version')


# =============================================================================
# >> CLASSES
# =============================================================================
class _HeaderManager(object):
    '''Class used to store the new header and check against
        the old file's header (if there is an old file)'''

    @property
    def header(self):
        '''Returns the header with the current plugin versions'''

        # Has the _header attribute been set?
        if not hasattr(self, '_header'):

            # Get the plugin values and create the header
            self._header = ['*' * 79 + '\n',
                '*' + ' ' * 77 + '*\n',
                '*' + 'GUNGAME v5.1 ERROR LOGGING'.center(77) + '*\n',
                '*' + 'HTTP://FORUMS.GUNGAME.NET/'.center(77) + '*\n',
                '*' + ('GG VERSION: %s' %
                  GunGameInfo.version).center(77) + '*\n',
                self.get_header_line(
                  'DATE', strftime('%m-%d-%Y'), 'IP', str(ip).upper()),
                self.get_header_line('PLATFORM',
                  get_os().upper(), 'PORT', str(port)),
                self.get_header_line('ES VERSION', str(eventscripts_ver),
                  'ES CORE VERSION', str(es_corelib_ver)),
                self.get_header_line('SPE VERSION',
                  str(spe_version), 'MM VERSION', str(metamod_version)),
                self.get_header_line('SM VERSION', str(sourcemod_version),
                  'MANI VERSION', str(mani_admin_plugin_version)),
                '*' + ' ' * 77 + '*\n', '*' * 79 + '\n', '\n', '\n']

        # Return the _header attribute
        return self._header

    @property
    def old_header(self):
        '''Returns the old files header to compare to the new header'''

        # Open the old file
        with self.filepath.open() as open_file:

            # Read the old file's contents and get its header
            old_header = open_file.readlines()[:14]

        # Get the new header's "DATE", since we do not want to compare the date
        new_date = self.header[5].split('DATE: ')[1].split()[0]

        # Get the old file's "DATE" line
        date_line = old_header[5]

        # Get the old file's "IP"
        old_ip = date_line.split('IP: ')[1].split()[0]

        # Modify the old file's "DATE" in order
        # to compare to the new file's contents
        old_header[5] = self.get_header_line(
          'DATE', new_date, 'IP', old_ip)

        # Return the modified old header
        return old_header

    @staticmethod
    def get_header_line(string_one, variable_one, string_two, variable_two):
        '''Static Method used to return a
            formatted string for the current line'''

        # Return a formatted string for the current line
        return ('*' + ('%s: ' % string_one).rjust(25) +
          variable_one.ljust(14) + ('%s: ' % string_two).rjust(19) +
          variable_two.ljust(19) + '*\n')
