// 
//=========== (C) Copyright 2008 GunGame 5 All rights reserved. ===========
//
// Events triggered by GunGame mod version 1.0.432
//
// No spaces in event names, max length 32
// All strings are case sensitive
// total game event byte length must be < 1024
//
// valid data key types are:
//   none   : value is not networked
//   string : a zero terminated string
//   bool   : unsigned int, 1 bit
//   byte   : unsigned int, 8 bit
//   short  : signed int, 16 bit
//   long   : signed int, 32 bit
//   float  : float, 32 bit

"gungame_events"
{
	"gg_levelup"
	{
        "attacker"  "short"     // The userid of the player that leveled up
        "leveler"   "short"     // The userid of the player that is leveling
        "userid"	"short"     // The userid of victim
        "old_level" "byte"      // The old level of the player that leveled up
        "new_level" "byte"      // The new level of the player that leveled up
        "reason"    "string"    // The reason for the level up
	}
	"gg_leveldown"
	{
        "userid"    "short"     // The userid of player that is leveling down
        "leveler"   "short"     // The userid of the player that is leveling
        "attacker"  "short"     // The userid of the attacker
        "old_level" "byte"      // The old level of the player that leveled down
        "new_level" "byte"      // The new level of the player that leveled down
        "reason"    "string"    // The reason for the level down
	}
	"gg_knife_steal"
	{
        "attacker"          "short" // The userid of the player that stole the level
        "attacker_level"    "byte"  // The new level of the player that stole the level
        "userid"            "short" // The userid of victim
        "userid_level"      "byte"  // The new level of the victim
	}
    "gg_multi_level"
    {
        "userid"    "short" // The userid of the leader that lost a level
        "leveler"   "short" // The userid of the player that is leveling
    }
    "gg_new_leader"
    {
        "userid"        "short"     // The userid of the player that became the new leader
        "leveler"       "short"     // The userid of the player that leveled up to become the new leader
        "leaders"       "string"    // String of current leaders' userids separated by "," e.g. "2,7,9"
        "old_leaders"   "string"    // String of old userids separated by "," e.g. "2,7,9"
        "leader_level"  "short"     // The current leader's level
    }
    "gg_tied_leader"
    {
        "userid"        "short"     // The userid of the player that tied the leader(s)
        "leveler"       "short"     // The userid of the player that leveled up to tie then leaders
        "leaders"       "string"    // String of current leaders' userids separated by "," e.g. "2,7,9"
        "old_leaders"   "string"    // String of old leaders' userids separated by "," e.g. "2,7,9"
        "leader_level"  "short"     // The current leader's level
    }
    "gg_leader_lostlevel"
    {
        "userid"        "short"     // The userid of the leader that lost a level
        "leveler"       "short"     // The userid of the player that is leveling
        "leaders"       "string"    // String of current leaders' userids separated by "," e.g. "2,7,9"
        "old_leaders"   "string"    // String of old leaders' userids separated by "," e.g. "2,7,9"
        "leader_level"  "short"     // The current leader's level
    }
    "gg_start"
    {
        // Fires at the end of the warmup round
        // Fires on es_map_start if there is no warmup round
    }
    "gg_vote"
    {
        // Fires when a vote starts
    }
    "gg_win"
    {
        "attacker"  "short"     // The userid of the player that won
        "winner"    "short"     // The userid of the player that won
        "userid"    "short"     // The userid of the victim that "gave up" the win
        "loser"     "short"     // The userid of the victim that "gave up" the win
        "round"     "bool"      // 1 if the winner of the round, 0 if the winner of the map
    }
    "gg_map_end"
    {
        // Fires at the end of a map when there is no winner
    }
    "gg_load"
    {
        // Fires when gungame is successfully loaded
    }
    "gg_unload"
    {
        // Fires when gungame is successfully unloaded
    }
    "gg_addon_loaded"
    {
        "addon"     "string"    // The name of the addon that was loaded
        "type"      "string"    // The type of addon that was loaded (included or custom)
    }
    "gg_addon_unloaded"
    {
        "addon"     "string"    // The name of the addon that was unloaded
        "type"      "string"    // The type of addon that was unloaded (included or custom)
    }
}