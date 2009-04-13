# ../cstrike/addons/eventscripts/gungame/scripts/config/included/__init__.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate: 2009-04-06 20:23:27 -0400 (Mon, 06 Apr 2009) $
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
# GunGame Imports
from gungame51.core.cfg import __configs__
from gungame51.core.cfg import getConfigList

# ============================================================================
# >> GLOBAL VARIABLES
# ============================================================================
# Declare all config *.py files located in the "core.cfg.files" directory
__all__ = getConfigList('included')

# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
for config in __all__:
    # Load and execute all configs in the "core.cfg.files" directory
    __configs__.load(config)