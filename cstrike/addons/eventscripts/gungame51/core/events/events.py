# ../core/events/events.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# Imports
# =============================================================================
from gungame51.core.events.eventlib import ESEvent
from gungame51.core.events.eventlib.fields import BooleanField
from gungame51.core.events.eventlib.fields import ByteField
from gungame51.core.events.eventlib.fields import ShortField
from gungame51.core.events.eventlib.fields import StringField


# =============================================================================
# Global Variables
# =============================================================================
# from events import * will only import from __all__
__all__ = ['GG_LevelUp', 'GG_LevelDown', 'GG_Knife_Steal', 'GG_Multi_Level',
           'GG_New_Leader', 'GG_Tied_Leader', 'GG_Leader_LostLevel',
           'GG_Leader_Disconnect', 'GG_Start', 'GG_Vote', 'GG_Win',
           'GG_Map_End', 'GG_Load', 'GG_Unload', 'GG_Addon_Loaded',
           'GG_Addon_Unloaded']


# =============================================================================
# Classes (Events)
# =============================================================================
class GG_LevelUp(ESEvent):
    """Fires when a player levels up"""
    attacker = ShortField(min_value=2, comment='The userid of the player ' +
                          'that leveled up')
    leveler = ShortField(min_value=2, comment='The userid of the player ' +
                         'that is leveling up')
    userid = ShortField(min_value=0, comment='The userid of victim')
    old_level = ByteField(min_value=1, comment='The old level of the player ' +
                          'that leveled up')
    new_level = ByteField(min_value=1, comment='The new level of the player ' +
                          'that leveled up')
    reason = StringField(comment='The reason for the level up')


class GG_LevelDown(ESEvent):
    """Fires when a player levels down"""
    attacker = ShortField(min_value=0, comment='The userid of the player ' +
                          'that is leveling down')
    leveler = ShortField(min_value=2, comment='The userid of the player ' +
                         'that is leveling down')
    userid = ShortField(min_value=2, comment='The userid of attacker')
    old_level = ByteField(min_value=1, comment='The old level of the player ' +
                          'that leveled down')
    new_level = ByteField(min_value=1, comment='The new level of the player ' +
                          'that leveled down')
    reason = StringField(comment='The reason for the level down')


class GG_Knife_Steal(ESEvent):
    """Fires when a player steals a level by knifing"""
    attacker = ShortField(min_value=2, comment='The userid of the player ' +
                          'that stole the level')
    attacker_level = ByteField(min_value=1, comment='The new level of the ' +
                               'player that stole the level')
    userid = ShortField(min_value=2, comment='The userid of the victim')
    userid_level = ByteField(min_value=1, comment='The new level of the ' +
                             'victim')


class GG_Multi_Level(ESEvent):
    """Fires when a player achieves a multi-level bonus"""
    userid = ShortField(min_value=2, comment='The userid of the player that ' +
                        'multi-leveled')
    leveler = ShortField(min_value=2, comment='The userid of the player that' +
                         ' is leveling')


class GG_New_Leader(ESEvent):
    """Fires when a player becomes the new leader"""
    userid = ShortField(min_value=2, comment='The userid of the player that ' +
                        'became the new leader')
    leveler = ShortField(min_value=2, comment='The userid of the player that' +
                         ' leveled up to become the new leader')
    leaders = StringField(comment="String of current leaders' userids " +
                          'separated by "," e.g. "2,7,9"')
    leader_level = ByteField(comment="The current leader's level")


class GG_Tied_Leader(ESEvent):
    """Fires when a player ties the leader"""
    userid = ShortField(min_value=2, comment='The userid of the player that ' +
                        'tied the leader(s)')
    leveler = ShortField(min_value=2, comment='The userid of the player that' +
                         ' leveled up to tie the leader(s)')
    leaders = StringField(comment="String of current leaders' userids " +
                          'separated by "," e.g. "2,7,9"')
    leader_level = ByteField(comment="The current leader's level")


class GG_Leader_LostLevel(ESEvent):
    """Fires when a leader loses a level"""
    userid = ShortField(min_value=2, comment='The userid of the leader that ' +
                        'lost a level')
    leveler = ShortField(min_value=2, comment='The userid of the player that' +
                         ' is leveling')
    leaders = StringField(comment="String of current leaders' userids " +
                          'separated by "," e.g. "2,7,9"')
    leader_level = ByteField(comment="The current leader's level")


class GG_Leader_Disconnect(ESEvent):
    """Fires when a leader disconnects"""
    userid = ShortField(min_value=2, comment='The userid of the leader that ' +
                        'disconnected')
    leaders = StringField(comment="String of current leaders' userids " +
                          'separated by "," e.g. "2,7,9"')
    leader_level = ByteField(comment="The current leader's level")


class GG_Start(ESEvent):
    """Fires at the end of warmup round or on es_map_start if there is no
    warmup round

    """
    pass


class GG_Vote(ESEvent):
    """Fires when a vote starts"""
    pass


class GG_Win(ESEvent):
    """Fires when a player wins the game"""
    attacker = ShortField(min_value=2, comment='The userid of the player ' +
                          'that won')
    winner = ShortField(min_value=2, comment='The userid of the player ' +
                        'that won')
    userid = ShortField(min_value=2, comment='The userid of the victim that ' +
                        '"gave up" the win')
    loser = ShortField(min_value=2, comment='The userid of the victim that ' +
                       '"gave up" the win')


class GG_Map_End(ESEvent):
    """Fires at the end of a map when there is no winner"""
    pass


class GG_Load(ESEvent):
    """Fires when gungame is successfully loaded"""
    pass


class GG_Unload(ESEvent):
    """Fires when gungame is successfully unloaded"""
    pass


class GG_Addon_Loaded(ESEvent):
    """Fires when an included or custom addon is loaded"""
    addon = StringField(comment='The name of the addon that was loaded')
    type = StringField(comment='The type of addon that was loaded (included ' +
                       'or custom)')


class GG_Addon_Unloaded(ESEvent):
    """Fires when an included or custom addon is unloaded"""
    addon = StringField(comment='The name of the addon that was unloaded')
    type = StringField(comment='The type of addon that was loaded (included ' +
                       'or custom)')
