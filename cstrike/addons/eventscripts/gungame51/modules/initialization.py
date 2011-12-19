# ../modules/initialization.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python imports
import sys

# EventScripts Imports
#   ES
import es
#   Gamethread
from gamethread import delayed

# GunGame Imports
from gungame51.core import gungame_info
#   Modules
from eventmanager import load_events
from helpers import check_first_gg_start
#   Cfg
from gungame51.core.cfg import load_configs
#   Events
from gungame51.core.events import GG_Load
from gungame51.core.events import gg_resource_file
#   Logs
from gungame51.core.logs import make_log_file
#   Menus
from gungame51.core.menus import MenuManager
#   Messaging
from gungame51.core.messaging.shortcuts import langstring
from gungame51.core.messaging.shortcuts import load_translation
from gungame51.core.messaging.shortcuts import msg
#   Players
from gungame51.core.players.shortcuts import reset_players
#   Sounds
from gungame51.core.sound import make_downloadable
#   Sql
from gungame51.core.sql.shortcuts import prune_winners_db
#   Weapons
from gungame51.core.weapons import WeaponOrderManager


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
gg_weapon_order_file = es.ServerVar('gg_weapon_order_file')


# =============================================================================
# >> FUNCTIONS
# =============================================================================
def initialize():
    '''Tries to initialize GunGame'''

    # Load GunGame's events
    load_events()

    # Load custom events
    gg_resource_file.declare_and_load()

    # Load the base translations
    load_translation('gungame', 'gungame')

    # Send message about GunGame loading
    es.dbgmsg(0, langstring("Load_Start",
            {'version': gungame_info('version')}))

    # Load config files
    load_configs()

    # Load weapon orders
    WeaponOrderManager().load_orders()

    # Load menus
    MenuManager().load_menus()

    # Make the sounds downloadable
    make_downloadable(True)

    # Pause a moment for the configs to be loaded (OB engine requires this)
    delayed(0.1, complete_initialization)


def complete_initialization():
    try:
        finish_initialization()
    except:
        unload_on_error()


def finish_initialization():
    '''Tries to finish GunGame's initialization'''

    # Fire the gg_server.cfg
    es.server.cmd('exec gungame51/gg_server.cfg')

    # Clear out the GunGame system
    reset_players()

    # Restart map
    msg('#human', 'Loaded')

    # Prune the DB
    prune_winners_db()

    # Update GunGame's info
    gungame_info('update')

    # Load error logging
    delayed(3.50, make_log_file)

    # Fire gg_load event
    GG_Load().fire()

    # Send message that loading has completed
    es.dbgmsg(0, langstring("Load_Completed"))

    # Change the value of gg_weapon_order_file to make sure we call
    # server_cvar when reloading gungame51
    gg_weapon_order_file_backup = str(gg_weapon_order_file)
    gg_weapon_order_file.set(0)
    gg_weapon_order_file.set(gg_weapon_order_file_backup)

    # See if we need to fire event gg_start after everything is loaded
    delayed(2, check_first_gg_start)


def unload_on_error():
    es.dbgmsg(0, '[GunGame51] %s' % ('=' * 79))
    es.excepter(*sys.exc_info())
    es.dbgmsg(0, '[GunGame51] %s' % ('=' * 79))
    es.unload('gungame51')
