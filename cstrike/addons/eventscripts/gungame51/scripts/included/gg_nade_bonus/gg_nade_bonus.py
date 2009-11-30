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
from gungame51.core.weapons.shortcuts import get_total_levels
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
# Server Vars
gg_nade_bonus = es.ServerVar('gg_nade_bonus')
gg_nade_bonus_mode = es.ServerVar('gg_nade_bonus_mode')
gg_nade_bonus_reset = es.ServerVar('gg_nade_bonus_reset')

# Weapon list
list_Weapons = getWeaponNameList('#all')

# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    # Adding attributes
    create_attributes('#all')
    
    es.dbgmsg(0, 'Loaded: %s' % info.name)
    
def unload():
    es.dbgmsg(0, 'Unloaded: %s' % info.name)
    
# ============================================================================
# >> GAME EVENTS
# ============================================================================
def player_spawn(event_var):
    userid = int(event_var['userid'])
    
    # Checking if player needs a nade bonus
    if not check_bonus(userid):
        return
    
    # Reset the player's bonus level ?
    if int(gg_nade_bonus_reset) and using_weapon_list():
        Player(userid).nadeBonusMulti = 0
        Player(userid).nadeBonusLevel = 1
    
    # Giving bonus (delayed)
    gamethread.delayed(0.10, give_bonus, userid)

def gg_levelup(event_var):
    userid = int(event_var['attacker'])

    # Checking if player needs a nade bonus
    if not check_bonus(userid):
        return
    
    # Using a weapon list ?
    if using_weapon_list():
        Player(userid).nadeBonusMulti = 0
        Player(userid).nadeBonusLevel = 1        
    
    # Giving bonus (delayed)
    gamethread.delayed(0.10, give_bonus, userid)

def gg_leveldown(event_var):       
    userid = int(event_var['userid'])
    
    # Player leveled down to nade ?
    if not check_bonus(userid):
        return    
    
    # Using weapon list ?
    if not using_weapon_list():
        return

    oldlevel = int(event_var['old_level'])
    
    # Was Player on nade ?
    if getLevelWeapon(oldlevel) == 'hegrenade':
        
        # Reset bonus levels
        Player(userid).nadeBonusMulti = 0
        Player(userid).nadeBonusLevel = 1        

    # Give bonus weapon(s)
    gamethread.delayed(0.10, give_bonus, userid)
    
def player_activate(event_var):
    userid = int(event_var['userid'])
    
    # Adding attributes
    create_attributes(userid)

def gg_start(event_var):
    # Adding attributes
    create_attributes('#all')

def player_death(event_var):
    attacker = int(event_var['attacker'])

    # Checking if player needs a new nade bonus
    if not check_bonus(attacker):
        return
    
    # We using a weapon list ?
    if not using_weapon_list():
        return
        
    weapon = get_weapon(attacker)

    # Was the kill with the bonus gun ?
    if event_var['weapon'] != weapon[0]:
        return
    
    ggPlayer = Player(attacker)
    
    # Stop Player at last level ?
    if int(gg_nade_bonus_mode) == 0:
        
        # Player on last level ?
        if get_total_levels(str(gg_nade_bonus)) == ggPlayer.nadeBonusLevel:
            return
    
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
            give_bonus(attacker, True, True)
        
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
        give_bonus(attacker, True, True)

# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
def create_attributes(filter):
    setAttribute(filter, 'nadeBonusLevel', 1)
    setAttribute(filter, 'nadeBonusMulti', 0)

def using_weapon_list():
    # Does gg_nade_bonus contain a regular weapon?
    nade_bonus = str(gg_nade_bonus).split(',')[0].replace(' ', '')
    if 'weapon_' + nade_bonus in list_Weapons:
        return False
    
    # Assuming weaponlist
    return True  

def get_weapon(userid):
    # Using a weapon list ?
    if using_weapon_list():
        return [getLevelWeapon(Player(userid).nadeBonusLevel, 
                                                str(gg_nade_bonus))]
     
    # Getting regular weapon(s)
    weap = str(gg_nade_bonus).split(',')
    
    # Cleaning up list
    for index in range(len(weap)):
    
        # We know the first one is clean
        if index == 0:
            continue
        
        # Removing spaces
        weap[index] = str(weap[index]).replace(' ', '')
        
        # Valid weapon(s)?
        if ('weapon_' + weap[index]) not in list_Weapons:
            
            # Send error
            raise ValueError('gg_nade_bonus (%s) contains ' % gg_nade_bonus +
                'the invalid weapon "%s"' % weap[index])
    
    # Sending weapon(s)        
    return weap

def give_bonus(userid, sound=False, turboCheck=False):
    ggPlayer = Player(userid)

    # Using weapon list?
    if using_weapon_list():
        
        # Player needs a real levelup?
        totalLevels = get_total_levels(str(gg_nade_bonus))
        if totalLevels < ggPlayer.nadeBonusLevel:
            
            # Reset bonus multi kills
            ggPlayer.nadeBonusMulti = 0                
            
            # Player stuck on last gun ?
            if int(gg_nade_bonus_mode) == 0:
                ggPlayer.nadeBonusLevel = totalLevels
                return
            
            # Resetting player's bonus level
            ggPlayer.nadeBonusLevel = 1
                
            # Put the player back on level 1 ?
            if int(gg_nade_bonus_mode) == 1:               
            
                # Recall the function to give level 1 weapon
                give_bonus(userid, sound, turboCheck)
                return
            
            # Level them up
            ggPlayer.levelup(1, userid, 'kill')
                
            # Play the levelup sound
            ggPlayer.playsound('levelup')

            return
            
    # Play sound ?
    if sound:
        ggPlayer.playsound('nadebonuslevel')

    # gg_turbo is loaded ?
    if turboCheck and not int(es.ServerVar('gg_turbo')):
        return
  
    # Get weapon
    weapons = get_weapon(userid)
    
    # All you get is a knife?
    if len(weapons) == 1 and weapons[0] == 'knife':
        
        # Not carrying a nade?
        if int(getPlayer(userid).get('he')) == 0:    
            
            # Pull out knife
            es.sexec(userid, 'use weapon_knife')
        
        return
    
    # Give weapons
    for weapon in weapons:
        ggPlayer.give(weapon, False, True, True)

def check_bonus(userid):
    # Valid userid?
    if userid < 1:
        return False

    # Valid team?
    if getPlayer(userid).teamid < 2:
        return False
    
    # Dead?
    if getPlayer(userid).isdead:
        return False
    
    # Nade level?
    if Player(userid).weapon != 'hegrenade':
        return False
        
    return True 
    