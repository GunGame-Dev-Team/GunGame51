# ../addons/eventscripts/gungame/scripts/included/gg_convert/gg_convert.py

'''
$Rev: 206 $
$LastChangedBy: Monday $
$LastChangedDate: 2009-10-28 15:35:41 -0400 (Wed, 28 Oct 2009) $
'''

# ============================================================================
# >> IMPORTS
# ============================================================================
# Python Imports
import cPickle
import os
from os import path
import time

# Eventscripts Imports
import es
import keyvalues

# GunGame Imports
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.sql import Database

# ============================================================================
# >> ADDON REGISTRATION/INFORMATION
# ============================================================================
info = AddonInfo()
info.name = 'gg_convert'
info.title = 'GG Welcome Message' 
info.author = 'GG Dev Team' 
info.version = '0.1'

# ============================================================================
# >> GLOBAL VARIABLES
# ============================================================================
convertDir = es.ServerVar('eventscripts_gamedir') + '/cfg/gungame51/converter/'
gg_convert = es.ServerVar('gg_convert')
ggDB = Database()

# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    es.dbgmsg(0, 'Loaded: %s' % info.name)
    run_conversion()

def unload():
    es.dbgmsg(0, 'Unloaded: %s' % info.name)

# ============================================================================
# >> GAME EVENTS
# ============================================================================
def es_map_start(event_var):
    run_conversion()

# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
def run_conversion():
    if int(gg_convert) == 2:
        ggDB.query("DELETE FROM gg_wins")

    for fileName in os.listdir(convertDir):
        if fileName == 'README.txt' or fileName[-10:] == '.converted':
            continue

        # GunGame3 Winners
        if fileName == 'es_gg_winners_db.txt':
            kv = keyvalues.KeyValues(name='gg3_winners')
            kv.load(convertDir + fileName)

            for uniqueid in kv:
                uniqueid = str(uniqueid)

                if not uniqueid.startswith('STEAM_'):
                    continue

                add_winner(kv[uniqueid]['name'], uniqueid, kv[uniqueid]['wins'], int(time.time()))

        # GunGame4 Winners
        elif fileName == 'es_gg_database.sqldb':
            es.sql('open', 'gg_database', 'gungame51/converter/')
            es.sql('query', 'gg_database', 'gg4_conversion_db', 'SELECT * FROM gg_players')
            es.sql('close', 'gg_database')

            kv = keyvalues.getKeyGroup('gg4_conversion_db')

            for player in kv:
                player = str(player)
                wins = int(kv[player]['wins'])

                if not wins:
                    continue

                add_winner(kv[player]['name'], kv[player]['steamid'], wins, int(time.time()))

            es.keygroupdelete('gg4_conversion_db')

        # GunGame5 Winners
        elif fileName == 'winnersdata.db':
            winnersDataBaseFile = open(convertDir + 'winnersdata.db', 'r')
            winners = cPickle.load(winnersDataBaseFile)
            winnersDataBaseFile.close()

            for uniqueid in winners:
                add_winner(winners[uniqueid]['name'], uniqueid, winners[uniqueid]['wins'], int(winners[uniqueid]['timestamp']))

        renameTo = convertDir + fileName + '.converted'
        x = 1

        while path.isfile(renameTo):
            renameTo = convertDir + fileName + '[' + str(x) + ']' + '.converted'
            x += 1

        os.rename(convertDir + fileName, renameTo)

    ggDB.commit()

def add_winner(name, uniqueid, wins, timestamp):
    currentWins = ggDB.select('gg_wins', 'wins', "where uniqueid = '%s'" % uniqueid)

    if currentWins == None:
        ggDB.query("INSERT INTO gg_wins " + "(name, uniqueid, wins, timestamp) " + "VALUES ('%s', '%s', '%s', %d)" % (name, uniqueid, wins, timestamp))
    else:
        if int(gg_convert) == 1:
            totalWins = int(currentWins) + wins
        else:
            totalWins = wins

        ggDB.query("UPDATE gg_wins SET wins=%s " % totalWins + "WHERE uniqueid = '%s'" % uniqueid)