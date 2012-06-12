# ../core/cfg/files/__init__.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame Imports
from gungame51.core.cfg.dictionary import ConfigTypeDictionary


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Declare all config *.py files located in the "core.cfg.files" directory
__all__ = ConfigTypeDictionary._get_config_list('main')
