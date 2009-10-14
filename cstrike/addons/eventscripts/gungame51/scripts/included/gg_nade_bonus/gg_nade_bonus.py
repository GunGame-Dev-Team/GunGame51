# ../addons/eventscripts/gungame/scripts/included/gg_nade_bonus/gg_nade_bonus.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
# Python Imports


# Eventscripts Imports
import es
import gamethread
from weaponlib import getWeaponNameList
from playerlib import getPlayer

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.players.shortcuts import Player
from gungame51.core.weapons.shortcuts import getLevelWeapon
from gungame51.core.weapons.shortcuts import getLevelMultiKill
from gungame51.core.weapons.shortcuts import getTotalLevels
from gungame51.core.players.shortcuts import setAttribute

# ============================================================================
# >> ADDON REGISTRATION/INFORMATION
# ============================================================================
info = AddonInfo()
info.name = 'gg_nade_bonus'
info.title = 'GG Grenade Bonus' 
info.author = 'GG Dev Team' 
info.version = '0.1'

# ============================================================================
# >> GLOBAL VARIABLES
# ============================================================================
gg_nade_bonus = es.ServerVar('gg_nade_bonus')
list_Weapons = getWeaponNameList('#all')

# ============================================================================
# >> CLASSES
# ============================================================================


# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    # Adding attributes
    createAttributes('#all')
    
    es.dbgmsg(0, 'Loaded: %s' % info.name)
    
def unload():
    es.dbgmsg(0, 'Unloaded: %s' % info.name)
    
# ============================================================================
# >> GAME EVENTS
# ============================================================================
def player_spawn(event_var):
    userid = int(event_var['userid'])
    
    # Checking if player needs a nade bonus
    if not checkBonus(userid):
        return
    
    # Giving bonus (delayed)
    gamethread.delayed(0.15, giveBonus, userid)

def gg_levelup(event_var):
    userid = int(event_var['attacker'])

    # Checking if player needs a nade bonus
    if not checkBonus(userid):
        return

    # Giving bonus
    giveBonus(userid)
    
def player_activate(event_var):
    userid = int(event_var['userid'])
    
    # Adding attributes
    createAttributes(userid)

def gg_start(event_var):
    # Adding attributes
    createAttributes('#all')

def player_death(event_var):
    attacker = int(event_var['attacker'])

    # Checking if player needs a new nade bonus
    if not checkBonus(attacker):
        return
    
    # Getting weapon
    weapon = getNextWeapon(attacker)
    
    # Weapon not from a list ?
    if not weapon[1]:
        return
    
    # Was the kill with the bonus gun ?
    if event_var['weapon'] != weapon[0]:
        return
    
    # Fetch GG player
    ggPlayer = Player(attacker)
    
    # Multikil check
    multiKill = getLevelMultiKill(ggPlayer.nadeBonusLevel, gg_nade_bonus)
    
    # Checking for multikill level
    if multiKill > 1:
        
        # Adding kill
        ggPlayer.nadeBonusMulti += 1
        
        # Level up ?
        if ggPlayer.nadeBonusMulti >= multiKill:
            
            # Reset multikill count
            ggPlayer.nadeBonusMulti = 0
            
            # Level up
            ggPlayer.nadeBonusLevel += 1
            
            # Play sound
            ''' Change this with a sound pack? '''
            ggPlayer.playsound('common/stuck2.wav')
            
            # Give new weapon
            giveBonus(userid, False)
        
        # Add multiKill
        else:
            # Add to multikill count
            ggPlayer.nadeBonusMulti += 1
            
            # Play sound
            ggPlayer.playsound('multikill')
    
    else:
        # Level up
        ggPlayer.nadeBonusLevel += 1
        
        # Give new weapon
        giveBonus(userid, False)

# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
def createAttributes(filter):
    setAttribute(filter, 'nadeBonusLevel', 1)
    setAttribute(filter, 'nadeBonusMulti', 0)

def getNextWeapon(userid):
    '''
        Dev note:
            This returns 2 things (weapon_name, True/False) True if we are 
            using a weapon list; False if we are not.
    '''
    # Checking for nade bonus
    if 'weapon_%s' % gg_nade_bonus in list_Weapons:
        return (str(gg_nade_bonus), False)
    
    # Getting weapon from list
    return (getLevelWeapon(Player(userid).nadeBonusLevel, str(gg_nade_bonus)), True)
    

def giveBonus(userid, spawn=True):
    ggPlayer = Player(userid)

    # Get weapon
    weapon = getNextWeapon(userid)
        
    # Using weapon list?
    if weapon[1]:

        # Player needs a real levelup?
        if getTotalLevels(gg_nade_bonus) < ggPlayer.nadeBonusLevel:
            
            # Level them up
            ggPlayer.levelup(1, userid, 'kill')
                
            # Play the levelup sound
            ggPlayer.playsound('levelup')
            
            # Resetting player's attributes
            ggPlayer.nadeBonusLevel = 1
            ggPlayer.nadeBonusMulti = 0    
            
            return

    # Spawn ?
    es.tell(userid, 'Not spawning? (%s) ' % spawn)
    if not spawn:
        es.tell(userid, 'Not spawning...')
        es.tell(userid, '%s' % getPlayer(userid).primary)
        # Checking player for weapon
        if weapon[0] in [getPlayer(userid).primary, 
            getPlayer(userid).secondary]:
            
            # Knife ?
            if weapon[0] == 'knife':
                es.sexec(userid, 'use weapon_knife')
        
            # Strip player of everything but nade and bonus weapon
            ggPlayer.strip(False, 'weapon_%s' % weapon[0])
            return
            
        # Strip player of everything but a nade
        ggPlayer.strip()
        ''' Turbo type of stripper/give? '''    
    
    # Give player weapon?
    ggPlayer.give(weapon[0])

def checkBonus(userid):
    # Valid team?
    if userid < 2:
        return False
    
    # Dead?
    if getPlayer(userid).isdead:
        return False
    
    # Nade level?
    if Player(userid).weapon != 'hegrenade':
        return False
        
    return True 
    