# ../core/leaders/shortcuts.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# EventScripts Imports
#   ES
from es import getplayername

# GunGame Imports
from gungame51.core import remove_return_chars
#   Leaders
from gungame51.core.leaders import LeaderManager


# =============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# =============================================================================
def is_leader(userid):
    return LeaderManager().is_leader(userid)


def get_leader_count():
    """Returns the amount of leaders."""
    return len(LeaderManager().current)


def get_leader_list():
    """Returns the userids of the current leader(s)."""
    # Remove disconnected userids from the current leaders and return the list
    return LeaderManager().current


def get_leader_names():
    """Returns the names of the current leader(s)."""
    return [
        remove_return_chars(getplayername(x)) for x in get_leader_list()]


def get_leader_level():
    """Returns the current leader level."""
    return LeaderManager().leaderlevel


def reset_leaders():
    """Resets the internal leader lists."""
    LeaderManager().reset()
