# ../core/addons/__init__.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame Imports
#   Addons
from priority import PriorityAddon
from manager import AddonManager


# =============================================================================
# >> FUNCTIONS
# =============================================================================
'''
This wrapper makes it possible to use key addon functions
without interacting with the AddonManager directly
'''

def load(*a, **kw):
    AddonManager()._load_addon(*a, **kw)
load.__doc__ = AddonManager._load_addon.__doc__


def unload(*a, **kw):
    AddonManager()._unload_addon(*a, **kw)
unload.__doc__ = AddonManager._unload_addon.__doc__
