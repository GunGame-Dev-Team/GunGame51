# ../addons/eventscripts/gungame/core/sql/__init__.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
# Python Imports
from sqlite3 import connect

# GunGame Imports
from gungame51.core import getGameDir

# ============================================================================
# >> GLOBALS
# ============================================================================

# ============================================================================
# >> CLASSES
# ============================================================================
class Database(object):
    '''
    Database class:
        You can assign this class to an object, or execute it directly.

        Example ussage:
            x = Database()
            x.select('tbl_name', ('name', 'age'), 'where city="dallas"')
            x.query('create table zomg_i_has_table')
        
        returnDict will return the information back in dictionary form:
            [{'name': 'luke', 'age': 24}, {name: 'michael', 'age': 90}]
    '''
    def __new__(cls, *p, **k):
        if not '_gg_database' in cls.__dict__:
            cls._gg_database = object.__new__(cls)
        return cls._gg_database

    def __init__(self):
        # Connection
        self.connect()

        # Initilize the Database
        self._ggSQL.text_factory = str
        self.query("CREATE TABLE IF NOT EXISTS gg_wins(name " +
                     "varchar(31), uniqueid varchar(20), wins int " +
                     "DEFAULT 0, timestamp int, PRIMARY KEY(uniqueid DESC))")
        self.query("PRAGMA auto_vacuum = 1")
        self.commit()

    def select(self, table, fields=None, conditions=None, returnDict=False,
                                                                    limit=50):
        try:
            if self._ggSQL.total_changes:
                pass
        except:
            self.connect()
            
        if conditions:
            table = '%s %s' % (str(table), conditions)
        if limit:
            table = '%s limit %s' % (str(table), int(limit))

        if isinstance(fields, list) or isinstance(fields, tuple):
            f = str(fields)[1:-1].replace('"', '').replace("'", '')
        elif fields:
            f = fields
            fields = [fields]
        else:
            f = '*'
            if returnDict:
                fields = [z[1] for z in [y for y in
                           self.query('PRAGMA table_info(%s)' % table, True)]]

        self.curs.execute('select %s from %s' % (f, table))

        selected = self.curs.fetchall()

        for i in range(len(selected)):
            # Convert to list ?
            if isinstance(selected[i], tuple):
                selected[i] = list(selected[i])

            # Convert to dict ?
            if returnDict:
                selected[i] = dict(zip(fields, selected[i]))

        # Return simple queries
        if len(selected) == 1:
            if len(selected[0]) == 1:
                return selected[0][0]
            return selected[0]

        if not selected:
            selected = None

        return selected

    def query(self, _query, getReturn=False):
        try:
            if self._ggSQL.total_changes:
                pass
        except:
            self.connect()

        self.curs.execute(_query)
        if getReturn:
            return self.curs.fetchall()

    def close(self):
        try:
            self.commit()
            self._ggSQL.close()
        except:
            pass

    def commit(self):
        try:
            if self._ggSQL.total_changes:
                self._ggSQL.commit()
        except:
            pass

    def connect(self):
        self._ggSQL = connect(getGameDir(
                    'addons/eventscripts/gungame51/core/sql/gg_database.db'))
        self.curs = self._ggSQL.cursor()