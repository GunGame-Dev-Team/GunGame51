# ../addons/eventscripts/gungame51/scripts/included/gg_error_logging/gg_error_logging.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
# Python Imports
from __future__ import with_statement
from time import strftime
from os import path
from os import name as OS
import sys
import traceback

# Eventscripts Imports
import es

# GunGame Imports
from gungame51.core import get_game_dir
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.addons import gungame_info

# ============================================================================
# >> ADDON REGISTRATION/INFORMATION
# ============================================================================
info = AddonInfo()
info.name = 'gg_error_logging'
info.title = 'GG Error Logging'
info.author = 'GG Dev Team'
info.version = '0.1'

# ============================================================================
# >> GLOBAL VARIABLES
# ============================================================================
# Server Vars
spe_version_var = es.ServerVar('spe_version_var')
eventscripts_ver = es.ServerVar('eventscripts_ver')
es_corelib_ver = es.ServerVar('es_corelib_ver')
ip = es.ServerVar('ip')
port = es.ServerVar('hostport')
metamod_version = es.ServerVar('metamod_version')
sourcemod_version = es.ServerVar('sourcemod_version')
mani_admin_plugin_version = es.ServerVar('mani_admin_plugin_version')
est_version = es.ServerVar('est_version')

file_name = (get_game_dir('cfg/gungame51/logs') +
                    '/GunGame%s_Log.txt' % gungame_info('version').replace('.','_'))

# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    # Checking error log
    make_log_file()

    # Trackback hook
    sys.excepthook = gungame_except_hook

    es.dbgmsg(0, 'Loaded: %s' % info.name)
    
def unload():
    es.dbgmsg(0, 'Unloaded: %s' % info.name)
    
# ============================================================================
# >> GAME EVENTS
# ============================================================================
def gungame_except_hook(tb_type, value, trace_back):
    # If this error was called to stop an attribute from being set, do not log
    # it.
    if str(value) == "gg_cancel_callback":
        return

    tb = traceback.format_exception(tb_type, value, trace_back)

    # If not a gungame error, send to ES and return
    if 'gungame51' not in str(tb).lower():
        es.excepter(tb_type, value, trace_back)
        return

    # Format the traceback
    for i in range(len(tb)):

        # Remove long file names ?
        if tb[i].strip().startswith('File \"'):
            tb[i] = (tb[i].replace(tb[i][(tb[i].find('File \"') +
                    6):tb[i].find('eventscripts')], '../')).replace('\\', '/')
    tb[-2] = tb[-2] + '\n'

    # turn tb into a string
    tb = reduce((lambda a, b: a + b), tb)

    # Print traceback to console
    es.dbgmsg(0, '\n')
    es.dbgmsg(0, '# ' + '='*48)
    es.dbgmsg(0, '# >>' + 'GunGame 5.1 Exception Caught!'.rjust(50))
    es.dbgmsg(0, '# ' + '='*48)
    es.dbgmsg(0, tb)
    es.dbgmsg(0, '# ' + '='*48)
    es.dbgmsg(0, '\n')

    # Use Log File
    with open(file_name, 'r+') as log_file:
        # Get contents
        log_contents = log_file.read()

        # Look for duplicate error
        find_error_index = log_contents.find(tb)

        # File has no duplicate error ?
        if find_error_index == -1:

            # Error template
            error_format = ['-='*39 + '-\n', (('LAST EVENT: ' +
                            '%s' % strftime('[%m/%d/%Y @ %H:%M:%S]')) + ' '*9 +
                            ' TOTAL OCCURENCES: [0001]').center(79) + '\n',
                            '-='*39 + '-\n', '\n', tb, '\n', '\n']

            # No duplicate, appending to end of file
            '''
            For some reason we get an error if we do not read again here
            if someone knows why, please let me know!
                - Monday
            '''
            log_file.read()
            log_file.writelines(error_format)

        else:
            # Go to the back to the begining of the file
            log_file.seek(0)

            # Increase occurence count
            error_count = (int(log_contents[(find_error_index - 92):\
            (find_error_index - 88)]) + 1)
            
            # Write change w/ new date and occurence count
            log_file.write(log_contents[:(find_error_index - 241)] + 
            log_contents[(find_error_index + len(tb) + 2):] + '-='*39 + '-\n' +
            (('LAST EVENT: ' + '%s' % strftime('[%m/%d/%Y @ %H:%M:%S]')) +
            ' '*9 + ' TOTAL OCCURENCES: [%04i]' % error_count).center(79) + '\n' + '-='*39 +
            '-\n\n' + tb + '\n\n')
            
# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
def make_log_file():
    # Log file header
    header = ['*'*79 + '\n', '*' + ' '*68 + 'v%s ' % info.version + '*\n',
              '*' + 'GUNGAME v5.1 ERROR LOGGING'.center(77) + '*' + '\n',
              '*' + 'HTTP://WWW.GUNGAME5.COM/'.center(77) + '*\n',
              '*' + ' '*77 + '*\n',
              ('*' + 'GG VERSION: '.rjust(19) +
               gungame_info('version').ljust(19) +
                'IP: '.rjust(19) + str(ip).upper().ljust(15) + ' '*5 + '*\n'),
              ('*' + 'SPE VERSION: '.rjust(19) +
               str(spe_version_var).ljust(19) +
                'PORT: '.rjust(19) + str(port).ljust(15) + ' '*5 + '*\n'),
              ('*' + 'PLATFORM: '.rjust(19) + str(OS).upper().ljust(19) +
                'DATE: '.rjust(19) + strftime('%m-%d-%Y').ljust(15) +
                ' '*5 + '*\n'), ('*' + 'ES VERSION: '.rjust(19) +
               str(eventscripts_ver).ljust(19) +
               'ES CORE VERSION: '.rjust(19) + str(es_corelib_ver).ljust(15) +
               ' '*5 + '*\n'), ('*' + 'MM VERSION: '.rjust(19) +
               str(metamod_version).ljust(19) + 'SM VERSION: '.rjust(19) +
               str(sourcemod_version).ljust(15) + ' '*5 + '*\n'),
               ('*' + 'MANI VERSION: '.rjust(19) +
               str(mani_admin_plugin_version).ljust(19) +
               'EST VERSION: '.rjust(19) + str(est_version).ljust(15) +
               ' '*5 + '*\n'),
               '*' + ' '*77 + '*\n', '*'*79 + '\n', '\n', '\n']

    # Does the file allready exists ?
    if path.isfile(file_name):

        # Read the file
        with open(file_name, 'r') as log_file:
            readlines = log_file.readlines()

        # Does the header match ?
        for i in range(len(header)):
            if readlines[i] != header[i]:
                if i == 7 and header[7][20:39] == readlines[7][20:39]:
                    continue
                break

        # Header matched, use this file
        else:
            return

        # Find a new file name for the old file
        n = 0
        while True:
            n += 1
            new_file_name = (get_game_dir('cfg/gungame51/logs') +
                                    '/GunGame%s_Log_Old[%01i].txt' % (gungame_info('version').replace('.','_'), n))
            if not path.isfile(new_file_name):
                break

        # Make new file w/ old errors
        with open(new_file_name, 'w') as log_file:
            log_file.writelines(readlines)
            
    # Start new log file
    with open(file_name, 'w') as log_file:
        log_file.writelines(header)