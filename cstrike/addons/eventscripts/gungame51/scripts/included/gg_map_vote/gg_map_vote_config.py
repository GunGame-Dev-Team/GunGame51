# ../addons/eventscripts/gungame51/scripts/cfg/included/gg_map_vote.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
# EventScripts Imports
import es
import cfglib

# GunGame Imports
from gungame51.core.cfg import generate_header

# ============================================================================
# >> GLOBAL VARIABLES
# ============================================================================
config = cfglib.AddonCFG('%s/cfg/' %es.ServerVar('eventscripts_gamedir') +
    'gungame51/included_addon_configs/gg_map_vote.cfg')

# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================

def load():
    generate_header(config)

    config.text('+'*76)
    config.text('|' + ' '*28 + 'MAP VOTE SETTINGS' + ' '*29 + '|')
    config.text('+'*76)
    config.text('')
    config.text('')

    # gg_map_vote
    config.text('='*76)
    config.text('>> GUNGAME MAP VOTE')
    config.text('='*76)
    config.text('Description:')
    config.text('   Allows players to vote for the next map.')
    config.text('Notes:')
    config.text('   * This does not require any additional plug-ins.')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not use voting.')
    config.text('   1 = (Enabled) Use GunGame\'s map voting system.')
    config.text('   2 = (Enabled) Use a 3rd-party voting system.')
    config.text('Default Value: 0')
    config.cvar('gg_map_vote', 0, 'Controls GunGame\'s map ' +
        'voting.').addFlag('notify')
    config.text('')

    # gg_map_vote_command
    config.text('='*76)
    config.text('>> 3RD PARTY VOTE COMMAND')
    config.text('='*76)
    config.text('Description:')
    config.text('   If gg_map_vote is set to 2, this is the command that ' + 
                    'will be issued when.') 
    config.text('   the vote is triggered.')
    config.text('Examples:')
    config.text(' Mani:        gg_map_vote_command "ma_voterandom end 4"')
    config.text(' BeetlesMod:  gg_map_vote_command "admin_votemaps"')
    config.text(' SourceMod:   gg_map_vote_command "sm_mapvote" (with ' +
                'mapchooser.smx enabled)')
    config.text('Default Value: "ma_voterandom end 4"')
    config.cvar('gg_map_vote_command', "ma_voterandom end 4", 
                                        'Triggers 3rd party voting.')
    config.text('')

    # gg_map_vote_size
    config.text('='*76)
    config.text('>> MAP VOTE SIZE')
    config.text('='*76)
    config.text('Description:')
    config.text('   This variable controls the number of maps that will be ' + 
                    'displayed as') 
    config.text('   options in the vote menu.')
    config.text('Notes:')
    config.text('   * It is recommended not to set this too high.')
    config.text('Options:')
    config.text('   0 = (Enabled) Use entire map list.')
    config.text('   # = (Enabled) Use # amount of options.')
    config.text('Default Value: 6')
    config.cvar('gg_map_vote_size', 6, 'Controls GunGame\'s map vote size.')
    config.text('')

    # gg_map_vote_trigger
    config.text('='*76)
    config.text('>> MAP VOTE TRIGGER LEVEL')
    config.text('='*76)
    config.text('Description:')
    config.text('   This variable controls what level the GunGame Vote is ' +
                    'fired on.') 
    config.text('   The value will be subtracted from the total ' + 
                    'number of levels.')
    config.text('Notes:')
    config.text('   * If there are 23 levels, and "gg_vote_trigger" is set ' +
                      'to "3", voting') 
    config.text('     will start on level 20.')
    config.text('Options:')
    config.text('   # = (Enabled) # from the last level to start the voting.')
    config.text('Default Value: 4')
    config.cvar('gg_map_vote_trigger', 4, 
                            'Which level to trigger GunGame\'s map voting.')
    config.text('')

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
    config.text('')

    # gg_map_vote_dont_show_last_maps
    config.text('='*76)
    config.text('>> EXCLUDE RECENTLY PLAYED MAPS')
    config.text('='*76)
    config.text('Description:')
    config.text('   This variable will exclude the selected number of ' +
                    'recently') 
    config.text('   played maps from the vote menu.')
    config.text('Notes:')
    config.text('   * Make sure you have enough maps listed in your source.')
    config.text('Options:')
    config.text('   0 = (Disabled) Do not exclude recent maps.')
    config.text('   # = (Enabled) # of last maps to exclude.')
    config.text('Default Value: 0')
    config.cvar('gg_map_vote_dont_show_last_maps', 0, 
                            'Exclude recent maps from GunGame\'s map voting.')
    config.text('')

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
    config.text('')

    # gg_map_vote_list_source
    config.text('='*76)
    config.text('>> MAP LIST SOURCE')
    config.text('='*76)
    config.text('Description:')
    config.text('   Controls which map list will be used ' +
                    'to build the vote menu.')
    config.text('Notes:')
    config.text('   * You may only filter maps with option 3. See ' + 
                        'below for more information.')
    config.text('Options:')
    config.text('   1 = mapcycle.txt')
    config.text('   2 = maplist.txt')
    config.text('   3 = "gg_map_list_file" variable')
    config.text('   4 = All maps in the "maps" folder')    
    config.text('Default Value: 1')
    config.cvar('gg_map_vote_list_source', 1,
                                'Source of maps for GunGame\'s map voting.')
    config.text('')

    # gg_map_vote_file
    config.text('='*76)
    config.text('>> MAP LIST FILE')
    config.text('='*76)
    config.text('Description:')
    config.text('   This variable is not used, unless the above variable ' + 
                            'is set to 3.')
    config.text('Notes:')
    config.text('   * You may filter out maps by player count.')
    config.text('   * See "/cfg/gungame51/gg_vote_list.txt" for examples and' +
                        ' information.')
    config.text('   * You can NOT add filters to "maplist.txt" and '
                        '"mapcycle.txt"')                        
    config.text('Examples:')
    config.text('   gg_map_vote_file "cfg/gungame51/my_list.txt"')
    config.text('   gg_map_vote_file "cfg/my_other_list.txt"')
    config.text('Default Value: cfg/gungame51/gg_vote_list.txt')
    config.cvar('gg_map_vote_file', 'cfg/gungame51/gg_vote_list.txt', 
                                    'Map list for GunGame\'s map voting.')
    config.text('')
        
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
    config.text('')
        
    # gg_map_vote_after_death
    config.text('='*76)
    config.text('>> DEAD FILTER')
    config.text('='*76)
    config.text('Description:')
    config.text('   * This will only send the vote menu to dead players. ')
    config.text('   * Players will receive the menu once they die.')
    config.text('Notes:')
    config.text('   * Players can use the player vote command to load the ' +
                        'menu if they') 
    config.text('     wish to vote while alive.')
    config.text('Options:')
    config.text('   0 = (Disabled) Send the vote menu to everyone.')
    config.text('   1 = (Enabled) Only send the vote menu to dead players.')
    config.text('Default Value: 0')
    config.cvar('gg_map_vote_after_death', 0, 
                    'Only the dead get popups during GunGame\'s map voting.')
    config.text('')
    config.text('')

    config.text('+'*76)
    config.text('|' + ' '*26 + 'ROCK THE VOTE SETTINGS' + ' '*26 + '|')
    config.text('+'*76)
    config.text('')
    config.text('')
    
    # gg_map_vote_rtv
    config.text('='*76)
    config.text('>> ROCK THE VOTE')
    config.text('='*76)
    config.text('Description:')
    config.text('   Allows players to request a map vote in the middle of' +
                ' a map.')
    config.text('Note:')
    config.text('   * Only takes effect with "gg_map_vote 1" set.')
    config.text('Examples:')
    config.text('   0 = (Disabled)')
    config.text('   1 = (Enabled)')
    config.text('Default Value: 1')
    config.cvar('gg_map_vote_rtv', 1,
                            'Allow rocking the vote.')
    config.text('')

    # gg_map_vote_rtv_command
    config.text('='*76)
    config.text('>> ROCK THE VOTE COMMAND')
    config.text('='*76)
    config.text('Description:')
    config.text('   Allows players to rock the vote.')
    config.text('Examples:')
    config.text('   gg_map_vote_rtv_command "rtv"')
    config.text('Default Value: "!rtv"')
    config.cvar('gg_map_vote_rtv_command', "!rtv", 
                            'Player say command for GunGame\'s RTV.')
    config.text('')

    # gg_map_vote_rtv_disable_level
    config.text('='*76)
    config.text('>> ROCK THE VOTE DISABLE LEVEL')
    config.text('='*76)
    config.text('Description:')
    config.text('   The percentage of total number of levels which, when the' +
                ' leader reaches')
    config.text('   it, disables RTV for that map.')
    config.text('Examples:')
    config.text('   60 = (If there are 24 total levels, when the leader hits' +
                ' level')
    config.text('           15 (we round down), RTV is disabled)')
    config.text('Default Value: 50')
    config.cvar('gg_map_vote_rtv_levels_required', 60, 
                            'Level percentage when RTV gets disabled.')
    config.text('')

    # gg_map_vote_rtv_percent
    config.text('='*76)
    config.text('>> ROCK THE VOTE PERCENTAGE')
    config.text('='*76)
    config.text('Description:')
    config.text('   The percentage of total players required to rtv before ' +
                'the vote gets')
    config.text('   rocked.')
    config.text('Examples:')
    config.text('   60 = 60% of players (rounded down) on the server need ' +
                'to RTV.')
    config.text('Default Value: 60')
    config.cvar('gg_map_vote_rtv_percent', 60, 
                            'Player say command for GunGame\'s rtv.')
    config.text('')
    config.text('')

    config.text('+'*76)
    config.text('|' + ' '*28 + 'NOMINATION SETTINGS' + ' '*29 + '|')
    config.text('+'*76)
    config.text('')
    config.text('')
    
    # gg_map_vote_nominate
    config.text('='*76)
    config.text('>> NOMINATE FOR VOTE')
    config.text('='*76)
    config.text('Description:')
    config.text('   Allows players to request a map to be in the next vote.')
    config.text('Notes:')
    config.text('   * Only takes effect with "gg_map_vote 1" set.')
    config.text('   * Only gg_map_vote_size nominations can be made.')
    config.text('   * gg_map_vote_dont_show_last_maps can\'t be nominated.')
    config.text('Examples:')
    config.text('   0 = (Disabled)')
    config.text('   1 = (Enabled)')
    config.text('Default Value: 1')
    config.cvar('gg_map_vote_nominate', 1,
                            'Allow vote nominations.')
    config.text('')

    # gg_map_vote_nominate_command
    config.text('='*76)
    config.text('>> ROCK THE VOTE COMMAND')
    config.text('='*76)
    config.text('Description:')
    config.text('   Allows players to nominate.')
    config.text('Examples:')
    config.text('   gg_map_vote_nominate_command "!nominate"')
    config.text('Default Value: "!nominate"')
    config.cvar('gg_map_vote_nominate_command', "!nominate", 
                            'Player say command for GunGame\'s nominate.')
    config.text('')

    # Write
    config.write()
    es.dbgmsg(0, '\tgg_map_vote.cfg')
       
def unload():
    global config
    
    # Remove the "notify" flags as set by addFlag('notify')
    for cvar in config.getCvars().keys():
        es.flags('remove', 'notify', cvar)
    
    # Delete the cfglib.AddonCFG instance
    del config