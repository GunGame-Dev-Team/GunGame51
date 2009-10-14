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
    
    # We using a weapon list ?
    if not usingWeaponList():
        return
        
    # Getting weapon
    weapon = getWeapon(attacker)    
    
    # Was the kill with the bonus gun ?
    if event_var['weapon'] != weapon[0]:
        return
    
    # Fetch GG player
    ggPlayer = Player(attacker)
    
    # Multikil check
    multiKill = getLevelMultiKill(ggPlayer.nadeBonusLevel, str(gg_nade_bonus))
    
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
            
            # Give new weapon
            giveBonus(attacker, True)
        
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
        giveBonus(attacker, True)

# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
def createAttributes(filter):
    setAttribute(filter, 'nadeBonusLevel', 1)
    setAttribute(filter, 'nadeBonusMulti', 0)

def usingWeaponList():
    # Does gg_nade_bonus contain a regular weapon?
    _format = str(gg_nade_bonus).split(',')[0].replace(' ', '')
    if 'weapon_' + _format in list_Weapons:
        return False
    
    # Assuming weaponlist
    return True  

def getWeapon(userid):
    # Using a weapon list ?
    if usingWeaponList():
        return [getLevelWeapon(Player(userid).nadeBonusLevel, str(gg_nade_bonus))]
        
    # Getting regular weapon(s)
    weap = str(gg_nade_bonus).split(',')
    
    # Cleaning up list
    for index in range(len(weap)):
        
        # Removing spaces
        weap[index] = str(weap[index]).replace(' ', '')
        
        # Valid weapon(s)?
        if ('weapon_' + weap[index]) not in list_Weapons:
            
            # Send error
            es.dbgmsg(0, 'GunGame5.1 ERROR :: (%s) ' % weap[index] + 
                         'is not a valid weapon!')    
            
            # Remove invalid weapon
            del weap[index]   
    
    # Sending weapon(s)        
    return weap

def giveBonus(userid, sound=False):
    ggPlayer = Player(userid)

    # Using weapon list?
    if usingWeaponList():
        # Player needs a real levelup?
        if getTotalLevels(str(gg_nade_bonus)) < ggPlayer.nadeBonusLevel:
            
            # Level them up
            ggPlayer.levelup(1, userid, 'kill')
                
            # Play the levelup sound
            ggPlayer.playsound('levelup')
            
            # Resetting player's attributes
            ggPlayer.nadeBonusLevel = 1
            ggPlayer.nadeBonusMulti = 0    
            
            es.tell(userid, 'LEVEL UP!!!')
            
            return
            
    # Play sound ?
    ''' Change this with a sound pack? '''
    if sound:
        ggPlayer.playsound('common/stuck2.wav')
  
    # Get weapon
    weapons = getWeapon(userid)
    
    # Strip player
    ggPlayer.strip(False, weapons)
    
    # All you get is a knife?
    if len(weapons) == 1 and weapons[0] == 'knife':
        
        # Not carrying a nade?
        if int(getPlayer(userid).get('he')) == 0:    
            
            # Pull out knife
            es.sexec(userid, 'use weapon_knife')
        
        return
    
    # Give weapons
    for weapon in weapons:
        gamethread.delayed(0, ggPlayer.give, weapon)

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
    