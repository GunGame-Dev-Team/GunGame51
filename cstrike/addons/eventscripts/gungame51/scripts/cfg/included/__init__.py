# ../cstrike/addons/eventscripts/gungame/scripts/config/included/__init__.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
# GunGame Imports
from gungame51.core.cfg import getConfigList

# ============================================================================
# >> GLOBAL VARIABLES
# ============================================================================
# Declare all config *.py files located in the "core.cfg.files" directory
__all__ = getConfigList('included')