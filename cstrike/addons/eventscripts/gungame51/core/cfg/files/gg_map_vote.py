# ../addons/eventscripts/gungame/core/cfg/files/gg_map_vote.py

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

# ============================================================================
# >> GLOBAL VARIABLES
# ============================================================================
config = cfglib.AddonCFG('%s/cfg/gungame51/gg_map_vote.cfg'
        %es.ServerVar('eventscripts_gamedir'))

# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================

def load():
    config = cfglib.AddonCFG('%s/cfg/gungame51/gg_map_vote.cfg' %es.ServerVar('eventscripts_gamedir'))

    config.text('*'*70)
    config.text('*               gg_map_vote.cfg -- Map Voting Options                *')
    config.text('*                                                                    *')
    config.text('*         This file contains the settings for "gg_map_vote".         *')
    config.text('*                                                                    *')
    config.text('*  Note: Any alteration of this file requires a server restart or a  *')
    config.text('*        reload of GunGame.                                          *')
    config.text('*'*70)
    config.text('')
    config.text('')
    
    # Error Logging
    config.text('='*76)
    config.text('>> GG MAP VOTE')
    config.text('='*76)
    config.text('Description:')

    config.text('Notes:')

    config.text('Options:')
    config.text('   0 = (Disabled) Do not use voting.')
    config.text('   1 = (Enabled) Use GunGame\'s map voting system.')
    config.text('   2 = (Enabled) Use a 3rd-party voting system.')
    config.text('Default Value: 0')
    config.cvar('gg_map_vote', 0, 'Controls GunGame\'s map voting.')
    
    config.write()
    es.dbgmsg(0, '\tgg_map_vote.cfg')
    
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