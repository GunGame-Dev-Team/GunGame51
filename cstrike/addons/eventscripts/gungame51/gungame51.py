# ../gungame51.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# EventScripts Imports
#   ES
import es
#   Cmdlib
from cmdlib import registerSayCommand
from cmdlib import unregisterSayCommand

# SPE Imports
try:
    import spe
except ImportError:
    es.unload('gungame51')
    raise ImportError('SPE Is not installed on this server! Please visit ' +
        'http://forums.eventscripts.com/viewtopic.php?t=29657 and download ' +
        'the latest version! SPE is required to run GunGame 5.1.')

# GunGame Imports
from core import gungame_info
#   Modules
from modules.active import ActiveInfo
from modules.eventmanager import unload_events
from modules.helpers import disable_auto_kick
from modules.helpers import thanks
from modules.info import info
from modules.initialization import initialize
from modules.initialization import unload_on_error
#   Addons
from core.addons.manager import AddonManager
#   Cfg
from core.cfg import unload_configs
#   Events
from core.events import GG_Unload
#   Logs
from core.logs import LogManager
#   Menus
from core.menus import MenuManager
#   Messaging
from core.messaging.shortcuts import unload_translation
#   Players
from core.players.players import _PlayerContainer
from core.players.shortcuts import Player
#   Sql
from core.sql.shortcuts import Database
from core.sql.shortcuts import update_winner
#   Weapons
from core.weapons import WeaponOrderManager


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
eventscripts_gg = es.ServerVar('eventscripts_gg')
eventscripts_gg5 = es.ServerVar('eventscripts_gg5')

sv_tags = es.ServerVar('sv_tags')


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    # Exec server.cfg before gungame loads.  If gungame is loaded from autoexec
    # this is needed so that the correct values are stored.
    es.server.cmd('exec server.cfg')

    try:
        initialize()
    except:
        unload_on_error()

    # If the public variables exist, remove them
    if not es.exists('variable', 'eventscripts_gg'):
        eventscripts_gg.removeFlag('notify')
        eventscripts_gg.removeFlag('replicated')
    if not es.exists('variable', 'eventscripts_gg5'):
        eventscripts_gg5.removeFlag('notify')
        eventscripts_gg5.removeFlag('replicated')

    # Create the public variables
    eventscripts_gg.set(gungame_info('version'))
    eventscripts_gg.makepublic()
    eventscripts_gg5.set(gungame_info('version'))
    eventscripts_gg5.makepublic()

    # Update the Included/Custom Addon lists
    gungame_info('update')

    # Register !thanks command
    registerSayCommand('!thanks', thanks, 'Displays a list of those involved' +
                       'with development and testing of GunGame.')

    # Add gungame to sv_tags
    tags = set(str(sv_tags).split(','))
    tags.add('gungame')
    sv_tags.set(','.join(tags))

    # Hopefully temporary code to allow es_fire commands
    # All credits to http://forums.eventscripts.com/viewtopic.php?t=42620
    for userid in es.getUseridList():
        disable_auto_kick(userid)


def unload():
    # Remove gungame from sv_tags
    tags = set(str(sv_tags).split(','))
    tags.discard('gungame')
    sv_tags.set(','.join(tags))

    # Remove the public variables
    eventscripts_gg.removeFlag('notify')
    eventscripts_gg.removeFlag('replicated')
    eventscripts_gg5.removeFlag('notify')
    eventscripts_gg5.removeFlag('replicated')

    # Unregister server_cvar for core.weapons
    WeaponOrderManager().unregister()

    # Unregister events
    unload_events()

    # Unload Menus
    MenuManager().unload_menus()

    # Unload all sub-addons
    AddonManager().unload_all_addons()

    # Unload translations
    unload_translation('gungame', 'gungame')

    # Remove all player instances
    _PlayerContainer().clear()

    # Close the database
    Database().close()

    # Unload configs (removes flags from CVARs)
    unload_configs()

    # Enable Buyzones
    es.server.queuecmd('es_xfire %s func_buyzone Enable' % es.getuserid())

    # Fire gg_unload event
    GG_Unload().fire()

    # Unregister !thanks command
    unregisterSayCommand('!thanks')

    # Set GunGame as not loaded
    ActiveInfo.loaded = False

    # Unregister the logging system
    LogManager.clean_logging()


# =============================================================================
# >> ROUND ACTIVE EVENTS
# =============================================================================
def es_map_start(event_var):
    '''Called when a new map is loaded'''

    # Set the round as inactive
    ActiveInfo.round = False

    # Set GunGame as inactive
    ActiveInfo.gungame = False


def gg_start(event_var):
    '''Called when GunGame starts'''

    # Set GunGame as active
    ActiveInfo.gungame = True


def gg_win(event_var):
    '''Called when a player wins GunGame'''

    # Set GunGame as inactive
    ActiveInfo.gungame = False


def gg_team_win(event_var):
    '''Called when a team wins GunGame'''

    # Set GunGame as inactive
    ActiveInfo.gungame = False


def round_start(event_var):
    '''Called at the start of every round'''

    # Set the round as active
    ActiveInfo.round = True

    # Retrieve a random userid
    userid = es.getuserid()

    # Disable Buyzones
    es.server.queuecmd('es_xfire %s func_buyzone Disable' % userid)


def round_end(event_var):
    '''Called at the end of each round'''

    # Set the round as inactive
    ActiveInfo.round = False


def cs_win_panel_match(event_var):
    '''Called when a map ends'''

    # Set GunGame as inactive
    ActiveInfo.gungame = False


# =============================================================================
# >> OTHER GAME EVENTS
# =============================================================================
def player_changename(event_var):
    '''Called when a player changes their name while on the server'''

    # Update the player's name in the winners database if they are in it
    if Player(int(event_var['userid'])).wins:
        update_winner('name', event_var['newname'],
            uniqueid=event_var['es_steamid'])
