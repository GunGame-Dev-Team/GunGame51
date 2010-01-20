# ../addons/eventscripts/gungame/scripts/included/gg_final_fight/gg_final_fight.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
# Eventscripts Imports
import es
import gamethread
import repeat
import votelib
from weaponlib import getWeaponNameList
from playerlib import getPlayer
from playerlib import getUseridList

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.messaging.shortcuts import msg
from gungame51.core.messaging.shortcuts import saytext2
from gungame51.core.players.shortcuts import Player
from gungame51.core.players.shortcuts import setAttribute
from gungame51.core.weapons.shortcuts import get_level_weapon


# ============================================================================
# >> ADDON REGISTRATION/INFORMATION
# ============================================================================
info = AddonInfo()
info.name = 'gg_final_fight'
info.title = 'GG Final Fight'
info.author = 'GG Dev Team'
info.version = '0.1'
info.translations = ['gg_final_fight']

# ============================================================================
# >> GLOBAL VARIABLES
# ============================================================================
# Server Vars
gg_final_fight = es.ServerVar('gg_final_fight')
gg_final_fight_bots = es.ServerVar('gg_final_fight_bots') # 0 = no, 1 = w/ human, 2 = no worries
gg_knife_pro = es.ServerVar('gg_knife_pro')
gg_deadstrip = es.ServerVar('gg_dead_strip')


# Misc
winnerId = []
fightRunning = False
fighters = []
fightVote = None

# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    setAttribute('#all', 'inFinalFight', False)

    # Create vote
    createVote()

    # Load message
    es.dbgmsg(0, 'Loaded: %s' % info.name)

def unload():
    # Delete the vote
    deleteVote()
    
    # Unload message
    es.dbgmsg(0, 'Unloaded: %s' % info.name)

# ============================================================================
# >> GAME EVENTS
# ============================================================================
def player_death(event_var):
    # Allready in a fight ?
    if fightRunning:

        # One left standing ?
        alive = getUseridList('#alive')
        if len(alive) != 1:
            return

        # Winner !
        es.msg('%s won!' % alive[0])

    # 1 Player on terrorist ?
    t_list = getUseridList('#t, #alive')
    if len(t_list) != 1:
        return

    # 1 Player on counter-terrorist ?
    ct_list = getUseridList('#ct, #alive')
    if len(ct_list) != 1:
        return

    # Check for bots ?
    if int(gg_final_fight_bots) < 2:

        # All bots ?
        if all([es.isbot(x) for x in ct_list + t_list]):
            return
            
    # Start vote
    startVote()

def item_pickup(event_var):
    # Fight running ?
    if not fightRunning:
        return

    # Let dead strip do it?
    if int(gg_dead_strip):
        return

    userid = int(event_var['userid'])

    # Make them use the knife ?
    if getPlayer(userid).weapon != 'weapon_knife':
        es.sexec(userid, 'use weapon_knife')

    # Strip them of everything, but a knife
    Player(userid).strip(True)

def player_activate(event_var):
    userid = int(event_var['userid'])
    setAttribute(userid, 'inFinalFight', False)

def player_spawn(event_var):
    userid = int(event_var['userid'])

    # Fight going ?
    if fightRunning:
        # Slay or something ?
        pass

    #if userid == winnerId[0]:
    #    # Send winner menu

        # Delete winner
        #del winnerId{:}
    
# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
def createVote():
    global fightVote

    # Create vote
    fightVote = votelib.create('gungameFinalFight', voteFinish, voteSubmit)
    # Set question and answers
    fightVote.setquestion('Do you want to knife-fight?')
    fightVote.addoption('Yes!')
    fightVote.addoption('No.')

def deleteVote():
    # Delete the vote (if it exists, should not)
    if votelib.exists('gungameFinalFight'):
        votelib.delete('gungameFinalFight')

def startVote():
    # Create vote
    createVote()
    # Start the vote for 30 seconds
    fightVote.start(30)
    # Make bots vote yes
    for bot in getUseridList('#bot, #alive'):
        voteSubmit(bot.userid, 'gungameFinalFight', 1, 'Yes!') #not sure
    
def voteSubmit(userid, votename, choice, choicename):
    # Did the player answer no?
    if choice == 2:
        fightVote.stop(1)
        saytext2('#human', Player(userid).index, 'PlayerDenied',
            {'player':es.getplayername(userid)}, False)
        return
    
def voteFinish(votename, win, winname, winvotes, winpercent, total, tie, 
  cancelled):
    # Vote cancelled? (if somebody voted no)
    if cancelled:
        return

    # Nobody voted?
    if not total:
        msg('#human', 'NoVotesReceived', {}, False)
        return

    # A tie vote? (Yes and no, occurs when the second player denies)
    if tie:
        msg('#human', 'FightVoteTied', {}, False)
        return

    # Delete old winner
    #if winnerId:
    #    del winnerId[:]

    # Both yes ?

    #for userid in getPlayerList('#alive'):
    #    pass

    # Delete vote
    deleteVote()
    
def startFight():

    pass
