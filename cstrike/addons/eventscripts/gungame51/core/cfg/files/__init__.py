# ../cstrike/addons/eventscripts/gungame/core/cfg/files/__init__.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
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
__all__ = getConfigList('main')

# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
for config in __all__:
    # Load and execute all configs in the "core.cfg.files" directory
    __configs__.load(config)