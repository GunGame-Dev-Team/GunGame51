# ../core/players/fields/__init__.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> Imports
# =============================================================================
from fields import *

def make_fields(**kwargs):
    for k, v in kwargs.items():
        if not isinstance(v, PlayerField):
            raise ValueError('Fields must be a PlayerField instance.')
    return kwargs