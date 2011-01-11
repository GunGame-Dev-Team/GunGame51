# ../scripts/included/gg_afk_punish/gg_afk_punish.py

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
import popuplib
from playerlib import getUseridList

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.players.shortcuts import Player

# =============================================================================
# >> ADDON REGISTRATION/INFORMATION
# =============================================================================
info = AddonInfo()
info.name = 'gg_afk_punish'
info.title = 'GG AFK Punish'
info.author = 'GG Dev Team'
info.version = "5.1.%s" % "$Rev$".split('$Rev: ')[1].split()[0]
info.translations = ['gg_afk_punish']

# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Get the es.ServerVar() instance of "gg_afk_punish"
gg_afk_punish = es.ServerVar('gg_afk_punish')

# Get the es.ServerVar() instance of "gg_afk_rounds"
gg_afk_rounds = es.ServerVar('gg_afk_rounds')


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    es.dbgmsg(0, 'Loaded: %s' % info.name)


def unload():
    es.dbgmsg(0, 'Unloaded: %s' % info.name)


# =============================================================================
# >> GAME EVENTS
# =============================================================================
def player_death(event_var):
    # Set player ids
    userid = int(event_var['userid'])
    attacker = int(event_var['attacker'])

    # =========================================================================
    # BOT CHECK (Bots are never AFK)
    # =========================================================================
    if es.isbot(userid):
        return
    # =========================================================================
    # SUICIDE CHECK (Do not count suicides due to the "kill" console command)
    # =========================================================================
    if (attacker == 0 or attacker == userid):
        return

    # =========================================================================
    # TEAM-KILL CHECK (TKs can happen before the player has a chance to move)
    # =========================================================================
    if (event_var['es_userteam'] == event_var['es_attackerteam']):
        return

    # =========================================================================
    # AFK CHECK
    # =========================================================================
    # See if the player was AFK
    if Player(userid).afk():
        # Check AFK punishment
        afkPunishCheck(userid)


def round_end(event_var):
    # Was a ROUND_DRAW or GAME_COMMENCING?
    if int(event_var['reason']) in [10, 16]:
        return

    # Now, we will loop through the userid list and run the AFK Punishment
    #   checks on them
    for userid in getUseridList('#alive,#human'):
        # See if the player was AFK
        if Player(userid).afk():
            # Check AFK punishment
            afkPunishCheck(userid)


def afkPunishCheck(userid):
    ggPlayer = Player(userid)

    # Is AFK punishment enabled?
    if int(gg_afk_rounds) > 0:
        # Increment the afk round attribute
        ggPlayer.afk.rounds += 1

        # Have been AFK for too long
        if ggPlayer.afk.rounds > int(gg_afk_rounds):
            punish(userid)
    else:
        punish(userid)


def punish(userid):
    ggPlayer = Player(userid)

    # Kick Punishment
    if int(gg_afk_punish) == 1:
        es.server.queuecmd('kickid %d %s' % (userid,
                           ggPlayer.langstring('KickedForAFK')))

    # Spectate Punishment
    elif int(gg_afk_punish) == 2:
        # Send them to spectator
        es.server.queuecmd('es_xfire %d !self SetTeam 1' % userid)

        # Send a popup saying they were switched
        popuplib.quicksend(0, userid,
                           ggPlayer.langstring('SwitchedToSpectator'))

    # Reset the AFK rounds back to 0
    ggPlayer.afk.rounds = 0
