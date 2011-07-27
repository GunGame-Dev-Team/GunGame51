# ../core/players/winners.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# EventScripts Imports
import es as _es
from . import _PlayerMeta
from fields import make_fields as _make_fields
from fields import IntegerField as _IntegerField
from gungame51.core.sql import Database as _Database
from gungame51.core.sql.shortcuts import insert_winner as _insert_winner
from gungame51.core.sql.shortcuts import update_winner as _update_winner


# =============================================================================
# >> GLOBALS
# =============================================================================

# =============================================================================
# >> CLASSES
# =============================================================================
class PlayerWins(_PlayerMeta):
    # Declare the default attribute fields
    _fields = _make_fields(wins=_IntegerField(min_value=0))

    # =========================================================================
    # Class Properties and Property Methods
    # =========================================================================
    def _get_wins(self):
        """Retrieves the number wins."""
        # Query the wins database
        winsQuery = _Database().select('gg_wins', 'wins',
                                       'where uniqueid' +
                                       ' = "%s"' % self.steamid)

        if winsQuery:
            return int(winsQuery)
        return 0

    def _set_wins(self, value):
        """Sets the number wins."""
        # Bots can't win
        if _es.isbot(self.userid):
            return

        # Has won before
        if self.wins:
            _update_winner('wins', value, uniqueid=self.steamid)
        # New entry
        else:
            name = es.getplayername(self.userid)
            if not name:
                name = "unnamed"
            _insert_winner(name, self.steamid, value)

    wins = property(fget=_get_wins, fset=_set_wins)

    # =========================================================================
    # Methods
    # =========================================================================
    def database_update(self):
        '''
        Updates the time and the player's name in the database
        '''
        if self.wins:
            _update_winner(('name', 'timestamp'), (_es.getplayername(
                self.userid), 'strftime("%s","now")'), uniqueid=self.steamid)
