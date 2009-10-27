# ../addons/eventscripts/gungame/scripts/cfg/included/gg_map_vote.py

'''
$Rev: $
$LastChangedBy: $
$LastChangedDate: $
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
# EventScripts Imports
import es
import cfglib

# ============================================================================
# >> GLOBAL VARIABLES
# ============================================================================
config = cfglib.AddonCFG('%s/cfg/' %es.ServerVar('eventscripts_gamedir') +
    'gungame51/included_addon_configs/gg_map_vote.cfg')

# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================

def load():
    config.text('*'*76)
    config.text('*' + ' '*15 + 'gg_map_vote.cfg -- Map Vote ' +
                'Configuration' + ' '*16 + '*')
    config.text('*' + ' '*74 + '*')
    config.text('*' + ' '*17 + 'This file defines GunGame Addon settings.' +
                ' '*16 + '*')
    config.text('*' + ' '*74 + '*')
    config.text('*  Note: Any alteration of this file requires a server ' +
                'restart or a' + ' '*8 + '*')
    config.text('*' + ' '*11 + 'reload of GunGame.' + ' '*45 + '*')
    config.text('*'*76)
    config.text('')
    config.text('')
    
    # gg_map_vote
    config.text('='*76)
    config.text('>> GUNGAME MAP VOTE')
    config.text('='*76)
    config.text('Description:')
    config.text('   Allows players to vote for the next map.')
    config.text('Notes:')
    config.text('   * This does not require any additional plugins.')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not use voting.')
    config.text('   1 = (Enabled) Use GunGame\'s map voting system.')
    config.text('   2 = (Enabled) Use a 3rd-party voting system.')
    config.text('Default Value: 0')
    config.cvar('gg_map_vote', 0, 'Controls GunGame\'s map voting.')

    # gg_map_vote_command
    config.text('='*76)
    config.text('>> 3RD PARTY VOTE COMMAND')
    config.text('='*76)
    config.text('Description:')
    config.text('   If gg_map_vote is set to 2, this is the command that ' + 
                    'will be issued when the vote is triggered.')
    config.text('Examples:')
    config.text('   Mani: gg_map_vote_command "ma_voterandom end 4"')
    config.text('   BeetlesMod: gg_map_vote_command "admin_votemaps"')
    config.text('   SourceMod: gg_map_vote_command "sm_map_vote"')
    config.text('Default Value: "ma_voterandom end 4"')
    config.cvar('gg_map_vote_command', "ma_voterandom end 4", 
                                        'Triggers 3rd party voting.')
    
    # gg_map_vote_size
    config.text('='*76)
    config.text('>> MAP VOTE SIZE')
    config.text('='*76)
    config.text('Description:')
    config.text('   This variable controls the number of maps that will be ' + 
                    'displayed as options in the vote menu.')
    config.text('Notes:')
    config.text('   * It is recommended not to set this too high.')
    config.text('Options:')
    config.text('   0 = (Enabled) Use entire map list.')
    config.text('   # = (Enabled) Use # amount of options.')
    config.text('Default Value: 6')
    config.cvar('gg_map_vote_size', 6, 'Controls GunGame\'s map vote size.')
    
    # gg_map_vote_trigger
    config.text('='*76)
    config.text('>> MAP VOTE TRIGGER LEVEL')
    config.text('='*76)
    config.text('Description:')
    config.text('   This variable controls what level the GunGame Vote is ' +
                    'fired on. The value will be subtracted from the total ' + 
                    'number of levels.')
    config.text('Notes:')
    config.text('   * If there are 23 levels, and "gg_vote_trigger" is set ' +
                      'to "3", voting will start on level 20.')
    config.text('Options:')
    config.text('   # = (Enabled) # from the last level to start the voting.')
    config.text('Default Value: 4')
    config.cvar('gg_map_vote_trigger', 4, 
                            'Which level to trigger GunGame\'s map voting.')
    
    # gg_map_vote_time
    config.text('='*76)
    config.text('>> MAP VOTE TIME')
    config.text('='*76)
    config.text('Description:')
    config.text('   This variable controls how long the vote will last for.')
    config.text('Notes:')
    config.text('   * It is recommended not to set this too high.')
    config.text('   * If nobody votes, it will default to the "mapcycle.txt".')
    config.text('Options:')
    config.text('   # = (Enabled) Time in seconds to allow voting.')
    config.text('Default Value: 30')
    config.cvar('gg_map_vote_time', 30, 'GunGame\'s map voting time limit.')
    
    # gg_map_vote_dont_show_last_maps
    config.text('='*76)
    config.text('>> EXCLUDE RECENTLY PLAYED MAPS')
    config.text('='*76)
    config.text('Description:')
    config.text('   This variable will exclude the selected number of ' +
                    'recently played maps from the vote menu.')
    config.text('Notes:')
    config.text('   * Make sure you have enough maps listed in your source.')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not exclude recent maps.')
    config.text('   # = (Enabled) # of last maps to exclude.')
    config.text('Default Value: 0')
    config.cvar('gg_map_vote_dont_show_last_maps', 0, 
                            'Exclude recent maps from GunGame\'s map voting.')
    
    # gg_map_vote_show_player_vote
    config.text('='*76)
    config.text('>> SHOW PLAYER VOTES')
    config.text('='*76)
    config.text('Description:')
    config.text('   This variable controls if votes will be publically ' +
                    'announced.')
    config.text('Examples:')
    config.text('   * Monday voted for gg_funtimes.')
    config.text('   * XE_ManUp voted for gg_hello_kitty_island_adventure.')
    config.text('   * Warren voted for aim_shotty.')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not use display player votes.')
    config.text('   1 = (Enabled) Display player votes.')
    config.text('Default Value: 0')
    config.cvar('gg_map_vote_show_player_vote', 0, 
                        'Shows player feedback from GunGame\'s map voting.')
    
    # gg_map_vote_list_source
    config.text('='*76)
    config.text('>> MAP LIST SOURCE')
    config.text('='*76)
    config.text('Description:')
    config.text('   This variable controls which map list will be used ' +
                    'to build the vote menu.')
    config.text('Notes:')
    config.text('   * You may only filter maps with option 3.  See ' + 
                        'below for more information.')
    config.text('Options:')
    config.text('   1 = mapcycle.txt')
    config.text('   2 = maplist.txt')
    config.text('   3 = "gg_map_list_file" variable')
    config.text('   4 = All maps in the "maps" folder')    
    config.text('Default Value: 0')
    config.cvar('gg_map_vote_list_source', 0, 
                                'Source of maps for GunGame\'s map voting.')
                                
    # gg_map_vote_file
    config.text('='*76)
    config.text('>> MAP LIST FILE')
    config.text('='*76)
    config.text('Description:')
    config.text('   This variable is not used, unless the above variable ' + 
                            'is set to 3.')
    config.text('Notes:')
    config.text('   * You may filter out maps by player count.')
    config.text('   * See "/cfg/gg_vote_list.txt" for examples and ' +
                        'information.')
    config.text('   * You can NOT add filters to "maplist.txt" and '
                        '"mapcycle.txt"')                        
    config.text('Examples:')
    config.text('   gg_map_vote_file "cfg/gungame/my_list.txt"')
    config.text('   gg_map_vote_file "cfg/my_other_list.txt"')
    config.text('Default Value: cfg/gungame51/gg_vote_list.txt')
    config.cvar('gg_map_vote_file', 'cfg/gungame51/gg_vote_list.txt', 
                                    'Map list for GunGame\'s map voting.')
    
    # gg_map_vote_player_command
    config.text('='*76)
    config.text('>> PLAYER VOTE COMMAND')
    config.text('='*76)
    config.text('Description:')
    config.text('   Allows players to vote for the next map.')
    config.text('Notes:')
    config.text('   * Players can vote or revote using this say command.')
    config.text('Examples:')
    config.text('   gg_map_vote_player_command "!ggvote"')
    config.text('   gg_map_vote_player_command "!vote"')
    config.text('Default Value: "!vote"')
    config.cvar('gg_map_vote_player_command', "!vote", 
                            'Player say command for GunGame\'s map voting.')
    
    # gg_map_vote_after_death
    config.text('='*76)
    config.text('>> DEAD FILTER')
    config.text('='*76)
    config.text('Description:')
    config.text('   This will only send the vote menu to dead players. ' + 
                    'Players will automatically receive the menu once they ' +
                    'die.')
    config.text('Notes:')
    config.text('   * Players can use the player vote command to load the ' +
                        'menu if they wish to vote while alive.')
    config.text('Options:')
    config.text('   0 = (Disabled) Send the vote menu to everyone.')
    config.text('   1 = (Enabled) Only send the vote menu to dead players.')
    config.text('Default Value: 0')
    config.cvar('gg_map_vote_after_death', 0, 
                        'Filter sending popups during GunGame\'s map voting.')
   
def unload():
    global config
    
    # Remove the "notify" flags as set by addFlag('notify')
    for cvar in config.getCvars().keys():
        es.flags('remove', 'notify', cvar)
    
    # Delete the cfglib.AddonCFG instance
    del config
'''
//----------------------------------------------------------------------------
// gg_map_vote.cfg -- Holds map voting options.
//
// This file contains the settings for "gg_map_vote".
//
// Note: Any alteration of this file requires a server restart or a reload of
//       GunGame.
//----------------------------------------------------------------------------

//=========================================================
// MAP VOTING
//=========================================================
// A map vote will be triggered once a player reaches a preset level below
// the highest level.
//
// Once all human players have voted, the vote is stopped and the winning
// map is displayed to the players.
//
// Note: This vote does not require any other plugin except EventScripts.
// Note: More map vote options in gg_map_vote.cfg
//
// Example: If "gg_vote_trigger" is set to 3, once a player is 3 levels
//          below the highest level, the vote will trigger.
//
// Options: 0 = Disabled
//          1 = Enabled (GunGame Map Voting)
//          2 = Third-party voting system (Uses gg_map_vote_command)

gg_map_vote 0

//=========================================================
// MAP VOTE COMMAND
//=========================================================
// If gg_map_vote is set to 2, this is the command that will be issued
// when the vote is triggered.
//
// Examples: Mani: gg_map_vote_command "ma_voterandom end 4"
//           BeetlesMod: gg_map_vote_command "admin_votemaps"
//           SourceMod: gg_map_vote_command "sm_map_vote"

gg_map_vote_command "ma_voterandom end 4"

//=========================================================
// MAP VOTE SIZE
//=========================================================
// This variable controls the number of maps that will be displayed as options
// in the vote menu.
//
// Options: 0 = Entire map list.
//          <options> = Show <options>.

gg_map_vote_size 4

//=========================================================
// TRIGGER LEVEL
//=========================================================
// This variable controls what level the GunGame Vote is fired on. The value
// will be subtracted from the total number of levels.
//
// Therefore, if there are 23 levels, and "gg_vote_trigger" is set to "3",
// voting will start on level 20.

gg_vote_trigger 3

//=========================================================
// MAP LIST SOURCE
//=========================================================
// This variable controls which map list that will be used to build the vote
// menu.
//
// Options: 1 = mapcycle.txt
//          2 = maplist.txt
//          3 = "gg_map_list_file" variable
//          4 = "maps" folder

gg_map_list_source 1

//=========================================================
// MAP LIST FILE
//=========================================================
// This variable does not need to changed, unless the above variable is set to
// 3.
//
// This variable will hold a custom maplist that you would like to use with
// gg_map_vote.

gg_map_list_file "cfg/gungame5/gg_maplist.txt"

//=========================================================
// VOTE TIME
//=========================================================
// This variable controls how long the vote will last for.
//
// Note: If no votes are taken within the set time, the next map will be the
//       next one in the map list file.

gg_vote_time 30

//=========================================================
// EXCLUDE RECENTLY PLAYED MAPS
//=========================================================
// This variable will exclude the selected number of recently played maps
// from the vote menu.

gg_dont_show_last_maps 1

//=========================================================
// SHOW PLAYER VOTES
//=========================================================
// This variable controls if votes will be publically announced.
//
// Example: Saul voted for cs_office
//          RideGuy voted for de_dust2
//
// Options: 0 = Off
//          1 = On

gg_show_player_vote 1

//=========================================================
// BOTS VOTE
//=========================================================
// This variable controls whether or not bots will randomly vote for a map.
//
// Options: 0 = Off
//          1 = On

gg_vote_bots_vote 0
'''