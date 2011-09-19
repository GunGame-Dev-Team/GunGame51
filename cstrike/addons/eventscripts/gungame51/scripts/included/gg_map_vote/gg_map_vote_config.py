# ../scripts/included/gg_map_vote/gg_map_vote_config.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
from __future__ import with_statement
from path import path

# GunGame Imports
from gungame51.core.cfg import ConfigContextManager


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():

    # Create the cfg file
    with ConfigContextManager(
      path(__file__).parent.split('scripts')[~0][1:]) as config:

        # Create the Map Vote section
        config.cfg_section('MAP VOTE SETTINGS')

        # Create the gg_map_vote instance
        with config.cfg_cvar('gg_map_vote') as cvar:

            cvar.name = 'GUNGAME MAP VOTE'
            cvar.description.append('Allows players to vote for the next map.')
            cvar.notes.append('This does not require any additional plug-ins.')
            cvar.options.append('0 = (Disabled) Do not use voting.')
            cvar.options.append(
                '1 = (Enabled) Use GunGame\'s map voting system.')
            cvar.options.append('2 = (Enabled) Use a 3rd-party voting system.')
            cvar.default = 0
            cvar.text = "Controls GunGame's map voting."

        # Create the gg_map_vote_command instance
        with config.cfg_cvar('gg_map_vote_command') as cvar:

            cvar.name = '3RD PARTY VOTE COMMAND'
            cvar.description.append('If gg_map_vote is set to 2, this is ' +
                'the command that will be issued when the vote is triggered.')
            cvar.examples.append('Mani:        gg_map_vote_command ' +
                '"ma_voterandom end 4"')
            cvar.examples.append('BeetlesMod:  gg_map_vote_command ' +
                '"admin_votemaps"')
            cvar.examples.append('SourceMod:   gg_map_vote_command ' +
                '"sm_mapvote" (with mapchooser.smx enabled)')
            cvar.default = 'ma_voterandom end 4'
            cvar.text = 'Triggers 3rd party voting.'

        # Create the gg_map_vote_size instance
        with config.cfg_cvar('gg_map_vote_size') as cvar:

            cvar.name = 'MAP VOTE SIZE'
            cvar.description.append('This variable controls the number of ' +
                'maps that will be displayed as options in the vote menu.')
            cvar.notes.append('It is recommended not to set this too high.')
            cvar.options.append('0 = (Enabled) Use entire map list.')
            cvar.options.append('# = (Enabled) Use # amount of options.')
            cvar.default = 6
            cvar.text = "Controls GunGame's map vote size."

        # Create the gg_map_vote_trigger instance
        with config.cfg_cvar('gg_map_vote_trigger') as cvar:

            cvar.name = 'MAP VOTE TRIGGER LEVEL'
            cvar.description.append('This variable controls what ' +
                'level the GunGame Vote is fired on.')
            cvar.description.append('The value will be subtracted ' +
                'from the total number of levels.')
            cvar.notes.append(
                'If there are 23 levels, and "gg_vote_trigger" ' +
                'is set to "3", voting will start on level 20.')
            cvar.options.append(
                '# = (Enabled) # from the last level to start the voting.')
            cvar.default = 4
            cvar.text = "Which level to trigger GunGame's map voting."

        # Create the gg_map_vote_time instance
        with config.cfg_cvar('gg_map_vote_time') as cvar:

            cvar.name = 'MAP VOTE TIME'
            cvar.description.append(
                'This variable controls how long the vote will last for.')
            cvar.notes.append('It is recommended not to set this too high.')
            cvar.notes.append(
                'If nobody votes, it will default to the "mapcycle.txt".')
            cvar.options.append(
                '# = (Enabled) Time in seconds to allow voting.')
            cvar.default = 30
            cvar.text = "GunGame's map voting time limit."

        # Create the gg_map_vote_dont_show_last_maps instance
        with config.cfg_cvar('gg_map_vote_dont_show_last_maps') as cvar:

            cvar.name = 'EXCLUDE RECENTLY PLAYED MAPS'
            cvar.description.append('This variable will exclude the ' +
                'selected number of recently played maps from the vote menu.')
            cvar.notes.append(
                'Make sure you have enough maps listed in your source.')
            cvar.options.append('0 = (Disabled) Do not exclude recent maps.')
            cvar.options.append('# = (Enabled) # of last maps to exclude.')
            cvar.default = 0
            cvar.text = "Exclude recent maps from GunGame's map voting."

        # Create the gg_map_vote_show_player_vote instance
        with config.cfg_cvar('gg_map_vote_show_player_vote') as cvar:

            cvar.name = 'SHOW PLAYER VOTES'
            cvar.description.append('This variable controls ' +
                'if votes will be publically announced.')
            cvar.examples.append('Monday voted for gg_funtimes.')
            cvar.examples.append('XE_ManUp voted for ' +
                'gg_hello_kitty_island_adventure.')
            cvar.examples.append('Warren voted for aim_shotty.')
            cvar.options.append(
                '0 = (Disabled) Do not use display player votes.')
            cvar.options.append('1 = (Enabled) Display player votes.')
            cvar.default = 0
            cvar.text = "Shows player feedback from GunGame's map voting."

        # Create the gg_map_vote_list_source instance
        with config.cfg_cvar('gg_map_vote_list_source') as cvar:

            cvar.name = 'MAP LIST SOURCE'
            cvar.description.append('Controls which map list ' +
                'will be used to build the vote menu.')
            cvar.notes.append('You may only filter maps with ' +
                'option 3. See below for more information.')
            cvar.options.append('1 = mapcycle.txt')
            cvar.options.append('2 = maplist.txt')
            cvar.options.append('3 = "gg_map_vote_file" variable')
            cvar.options.append('4 = All maps in the "maps" folder')
            cvar.default = 1
            cvar.text = "Source of maps for GunGame's map voting."

        # Create the gg_map_vote_file instance
        with config.cfg_cvar('gg_map_vote_file') as cvar:

            cvar.name = 'MAP LIST FILE'
            cvar.description.append('This variable is not used, ' +
                'unless the above variable is set to 3.')
            cvar.notes.append('You may filter out maps by player count.')
            cvar.notes.append('See "/cfg/gungame51/gg_vote_list.txt" ' +
                'for examples and information.')
            cvar.notes.append('You can NOT add filters to ' +
                '"maplist.txt" and "mapcycle.txt"')
            cvar.examples.append(
                'gg_map_vote_file "cfg/gungame51/my_list.txt"')
            cvar.examples.append('gg_map_vote_file "cfg/my_other_list.txt"')
            cvar.default = 'cfg/gungame51/gg_vote_list.txt'
            cvar.text = "Map list for GunGame's map voting."

        # Create the gg_map_vote_player_command instance
        with config.cfg_cvar('gg_map_vote_player_command') as cvar:

            cvar.name = 'PLAYER VOTE COMMAND'
            cvar.description.append('Allows players to vote for the next map.')
            cvar.notes.append(
                'Players can vote or revote using this say command.')
            cvar.examples.append('gg_map_vote_player_command "!ggvote"')
            cvar.examples.append('gg_map_vote_player_command "!vote"')
            cvar.default = '!vote'
            cvar.text = "Player say command for GunGame's map voting."

        # Create the gg_map_vote_after_death instance
        with config.cfg_cvar('gg_map_vote_after_death') as cvar:

            cvar.name = 'DEAD FILTER'
            cvar.description.append(
                'This will only send the vote menu to dead players.')
            cvar.description.append(
                'Players will receive the menu once they die.')
            cvar.notes.append('Players can use the player vote command ' +
                'to load the menu if they wish to vote while alive.')
            cvar.options.append(
                '0 = (Disabled) Send the vote menu to everyone.')
            cvar.options.append(
                '1 = (Enabled) Only send the vote menu to dead players.')
            cvar.default = 0
            cvar.text = "Only the dead get popups during GunGame's map voting."

        # Create the RTV section
        config.cfg_section('ROCK THE VOTE SETTINGS')

        # Create the gg_map_vote_rtv instance
        with config.cfg_cvar('gg_map_vote_rtv') as cvar:

            cvar.name = 'ROCK THE VOTE'
            cvar.description.append('Allows players to request a ' +
                'map vote in the middle of a map.')
            cvar.notes.append('Only takes effect with "gg_map_vote 1" set.')
            cvar.examples.append('0 = (Disabled)')
            cvar.examples.append('1 = (Enabled)')
            cvar.default = 1
            cvar.text = 'Allow rocking the vote.'

        # Create the gg_map_vote_rtv_command instance
        with config.cfg_cvar('gg_map_vote_rtv_command') as cvar:

            cvar.name = 'ROCK THE VOTE COMMAND'
            cvar.description.append('Allows players to rock the vote.')
            cvar.examples.append('gg_map_vote_rtv_command "rtv"')
            cvar.default = '!rtv'
            cvar.text = "Player say command for GunGame's RTV."

        # Create the gg_map_vote_rtv_levels_required instance
        with config.cfg_cvar('gg_map_vote_rtv_levels_required') as cvar:

            cvar.name = 'ROCK THE VOTE DISABLE LEVEL'
            cvar.description.append(
                'The percentage of total number of levels which, when ' +
                'the leader reaches it, disables RTV for that map.')
            cvar.examples.append('60 = (If there are 24 total levels, when ' +
                'the leader hits level 15 (we round down), RTV is disabled)')
            cvar.default = 60
            cvar.text = 'Level percentage when RTV gets disabled.'

        # Create the gg_map_vote_rtv_percent instance
        with config.cfg_cvar('gg_map_vote_rtv_percent') as cvar:

            cvar.name = 'ROCK THE VOTE PERCENTAGE'
            cvar.description.append('The percentage of total ' +
                'players required to rtv before the vote gets rocked.')
            cvar.examples.append('60 = 60% of players ' +
                '(rounded down) on the server need to RTV.')
            cvar.default = 60
            cvar.text = "Player say command for GunGame's rtv."

        # Create the Nomination section
        config.cfg_section('NOMINATION SETTINGS')

        # Create the gg_map_vote_nominate instance
        with config.cfg_cvar('gg_map_vote_nominate') as cvar:

            cvar.name = 'NOMINATE FOR VOTE'
            cvar.description.append(
                'Allows players to request a map to be in the next vote.')
            cvar.notes.append('Only takes effect with "gg_map_vote 1" set.')
            cvar.notes.append('Only gg_map_vote_size nominations can be made.')
            cvar.notes.append(
                'gg_map_vote_dont_show_last_maps can\'t be nominated.')
            cvar.options.append('0 = (Disabled)')
            cvar.options.append('1 = (Enabled)')
            cvar.default = 1
            cvar.text = 'Allow vote nominations.'

        # Create the gg_map_vote_nominate_command instance
        with config.cfg_cvar('gg_map_vote_nominate_command') as cvar:

            cvar.name = 'ROCK THE VOTE COMMAND'
            cvar.description.append('Allows players to nominate.')
            cvar.options.append('gg_map_vote_nominate_command "!nominate"')
            cvar.default = '!nominate'
            cvar.text = "Player say command for GunGame's nominate."
