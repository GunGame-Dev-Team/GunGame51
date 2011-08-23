# ../scripts/included/gg_deathmatch/gg_deathmatch.py

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
from playerlib import getPlayer
from playerlib import getUseridList
import repeat
import gamethread

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.messaging.shortcuts import hudhint
from gungame51.core.players.shortcuts import Player

# =============================================================================
# >> ADDON REGISTRATION/INFORMATION
# =============================================================================
info = AddonInfo()
info.name = 'gg_deathmatch'
info.title = 'GG Deathmatch'
info.author = 'GG Dev Team'
info.version = "5.1.%s" % "$Rev$".split('$Rev: ')[1].split()[0]
info.requires = ['gg_dead_strip', 'gg_dissolver']
info.conflicts = ['gg_elimination', 'gg_teamplay', 'gg_teamwork']
info.translations = ['gg_deathmatch']

# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Server Vars
gg_dm_respawn_delay = es.ServerVar('gg_dm_respawn_delay')
mp_freezetime = es.ServerVar('mp_freezetime')
mp_roundtime = es.ServerVar('mp_roundtime')

# Misc
mpFreezetimeBackup = int(mp_freezetime)
mpRoundtimeBackup = int(mp_roundtime)


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    # Don't allow respawn
    global respawnAllowed
    respawnAllowed = False

    # Set freezetime and roundtime to avoid gameplay interuptions
    mp_freezetime.set('0')
    mp_roundtime.set('9')

    # Create repeats for all players on the server
    for userid in getUseridList('#all'):
        respawnPlayer = repeat.find('gungameRespawnPlayer%s' % userid)

        if not respawnPlayer:
            repeat.create(
                'gungameRespawnPlayer%s' % userid, respawn_count_down, userid)

    # Respawn all dead players
    for userid in getUseridList('#dead'):
        # If the player is not on CT or T, stop here
        if es.getplayerteam(userid) < 2:
            continue

        # Start the respawn countdown
        repeat.start('gungameRespawnPlayer%s' % userid, 1,
                                                      int(gg_dm_respawn_delay))

    # Register the joinclass command to trigger the first spawn.
    es.addons.registerClientCommandFilter(joinclass_filter)


def unload():
    # Set freezetime and roundtime back to their original values
    mp_freezetime.set(mpFreezetimeBackup)
    mp_roundtime.set(mpRoundtimeBackup)

    # Delete all player respawns
    for userid in getUseridList('#all'):
        if repeat.find('gungameRespawnPlayer%s' % userid):
            repeat.delete('gungameRespawnPlayer%s' % userid)

    # Unregister the joinclass command
    es.addons.unregisterClientCommandFilter(joinclass_filter)


# =============================================================================
# >> GAME EVENTS
# =============================================================================
def es_map_start(event_var):
    # Don't allow respawn
    global respawnAllowed
    respawnAllowed = False


def round_start(event_var):
    # Allow respawn
    global respawnAllowed
    respawnAllowed = True


def round_end(event_var):
    # Don't allow respawn
    global respawnAllowed
    respawnAllowed = False


def gg_win(event_var):
    # Cancel pending respawns
    for userid in getUseridList('#all'):
        if repeat.find('gungameRespawnPlayer%s' % userid):
            repeat.delete('gungameRespawnPlayer%s' % userid)


def joinclass_filter(userid, args):
    # If the command is not joinclass, stop here
    if (not len(args)) or args[0].lower() != 'joinclass':
        return 1

    teamid = es.getplayerteam(userid)

    # No respawn delay and joining an active team?
    if int(gg_dm_respawn_delay) == 0 and teamid > 1:
        gamethread.delayed(0.50, Player(userid).respawn)
        return 1

    # If the player does not have a respawn repeat, create one
    respawnPlayer = repeat.find('gungameRespawnPlayer%s' % userid)
    if not respawnPlayer:
        repeat.create('gungameRespawnPlayer%s' % userid,
                                                respawn_count_down, userid)
    # Don't allow spectators or players that are unassigned to respawn
    if teamid < 2:
        if repeat.status('gungameRespawnPlayer%s' % userid) != 1:
            repeat.stop('gungameRespawnPlayer%s' % userid)
            hudhint(userid, 'RespawnCountdown_CancelTeam')
        return 1
    # Respawn the player
    repeat.start('gungameRespawnPlayer%s' % userid, 1,
                                                      int(gg_dm_respawn_delay))
    return 1


def player_disconnect(event_var):
    # Get userid
    userid = event_var['userid']

    # Delete the player-specific repeat
    if repeat.find('gungameRespawnPlayer%s' % userid):
        repeat.delete('gungameRespawnPlayer%s' % userid)


def player_death(event_var):
    # Get the userid
    userid = event_var['userid']

    # Respawn the player if the round hasn't ended
    if respawnAllowed:
        # No respawn delay ?
        if int(gg_dm_respawn_delay) == 0:
            gamethread.delayed(0.50, Player(userid).respawn)
        else:
            # If the player does not have a respawn repeat, create one
            respawnPlayer = repeat.find('gungameRespawnPlayer%s' % userid)
            if not respawnPlayer:
                repeat.create('gungameRespawnPlayer%s' % userid,
                                                respawn_count_down, userid)

            repeat.start('gungameRespawnPlayer%s' % userid, 1,
                                                      int(gg_dm_respawn_delay))


# =============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# =============================================================================
def respawn_count_down(userid):
    # Make sure that the repeat exists
    respawnRepeat = repeat.find('gungameRespawnPlayer%s' % userid)
    if not respawnRepeat:
        return

    # Player on server ?
    if not es.exists('userid', userid) and userid != 0:
        respawnRepeat.stop()
        respawnRepeat.delete()
        return

    # Not dead?
    if not getPlayer(userid).isdead:
        respawnRepeat.stop()
        return

    # Round finished?
    if not respawnAllowed:
        # Tell them the round has ended
        hudhint(userid, 'RespawnCountdown_RoundEnded')
        respawnRepeat.stop()
        return

    # More than 1 remaining?
    if respawnRepeat['remaining'] > 1:
        hudhint(userid, 'RespawnCountdown_Plural',
            {'time': respawnRepeat['remaining']})

    # Is the counter 1?
    elif respawnRepeat['remaining'] == 1:
        hudhint(userid, 'RespawnCountdown_Singular')

    # Respawn the player
    elif respawnRepeat['remaining'] == 0:
        if float(gg_dm_respawn_delay) % 1 == 0:
            Player(userid).respawn()
        else:
            gamethread.delayed((float(gg_dm_respawn_delay) % 1),
                                                        Player(userid).respawn)
