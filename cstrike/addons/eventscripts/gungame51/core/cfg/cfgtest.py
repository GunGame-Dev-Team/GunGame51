'''
    This script is intended to show how we can dynamically create config
files for GunGame. Currently, the script ships with an empty directory
located at "../cstrike/addons/eventscripts/cfgtest/configs/test". Once
you run the script, the GunGame configs will be created in the above
directory. There are several advantages gained by using this method:
    * The variables will always be in the config once the user loads
      GunGame, even if the user accidently deletes a variable, or
      neglects to declare a value. If a variable or value is missing,
      the variable will be replaced with the default value, or the default
      value will be placed on the variable.
    * If a user modifies a value, the value will not be overwritten.
    * We can now ship new variables and default values in an update, and
      not have to worry about overwriting the user's existing configuration.
      
    The other intention of this script is to show how we can go about
restructuring the code of GunGame. If you look at the code in this file, you
will see that I have placed all of the configs in the "configs" directory of
this script. Then, I import all of the configs, and execute the code from
within, instead of creating an elaborate config class and cluttering up an
already oversized and overused library (gungamelib). With this method, no
library is needed and the code takes full advantage of Python's ability to
create script "packages" as outlined here:
    * http://www.network-theory.co.uk/docs/pytut/Packages.html
    
    My basic complaint with GunGame at the current moment is that "gungamelib"
has gotten quite bloated, and is becoming far too difficult to manage. This is
the beginning of my proposed solution; to restructure/reorganize the code into
a more manageable and logical grouping of packages that are independant of one
another, yet co-dependant for GunGame as a whole. This will also help to limit
the possibility of code conflicts/merges via the SVN since the packages will
be spread out, and make it easier to see where as well as when we made any
mistakes.
'''
import es

def load():
    # Start the Showoff Text
    es.dbgmsg(0, '')
    es.dbgmsg(0, 'Initializing GunGame Configs:')
    es.dbgmsg(0, '-'*29)
    
    # Import the Configs (gg_en_config, gg_default_addons, gg_map_vote)
    from configs import *
    
    # Temp reload crap (for updating changes since I am importing the configs instead of es_load'ing them)
    reload(gg_en_config)
    reload(gg_default_addons)
    reload(gg_map_vote)
    
    # Initialize Configs
    gg_en_config.load()
    gg_default_addons.load()
    gg_map_vote.load()
    
    # End the Showoff Text
    es.dbgmsg(0, '-'*29)
    es.dbgmsg(0, '')
    es.dbgmsg(0, 'Check the "%s/configs/test" directory' %str(es.getAddonPath('cfgtest')).replace('\\', '/'))
    es.dbgmsg(0, '')
    
def server_cvar(event_var):
    if 'gg_' in event_var['cvarname']:
        es.dbgmsg(0, '%s has been changed to: %s' %(event_var['cvarname'], event_var['cvarvalue']))