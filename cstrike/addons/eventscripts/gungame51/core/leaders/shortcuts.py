# ../addons/eventscripts/gungame/core/leaders/shortcuts.py

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

# GunGame Imports
from gungame51.core import removeReturnChars
from gungame51.core.leaders import leaders

# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
def is_leader(userid):
    return leaders.is_leader(userid)
    
def get_leader_count():
    """Returns the amount of leaders."""
    return len(leaders.current)
    
def get_old_leader_list():
    """Returns the userids of the old/previous leader(s)."""
    # Remove disconnected userids from the previous leaders and return the list
    return leaders.previous
    
def get_leader_list():
    """Returns the userids of the current leader(s)."""
    # Remove disconnected userids from the current leaders and return the list
    return leaders.current
    
def get_leader_names():
    """Returns the names of the current leader(s)."""
    return [removeReturnChars(es.getplayername(x)) for x in get_leader_list()]
    
def get_leader_level():
    """Returns the current leader level."""
    return leaders.leaderlevel