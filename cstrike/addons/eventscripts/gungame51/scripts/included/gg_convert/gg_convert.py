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
from sqlite3 import connect
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
gg_convert = es.ServerVar('gg_convert')
# The path to the directory from which we convert
convertDir = es.ServerVar('eventscripts_gamedir') + '/cfg/gungame51/converter/'
# An instance of the Database() class to adjust the winners database with
ggDB = Database()

# ============================================================================
# >> LOAD & UNLOAD
# ============================================================================
def load():
    es.dbgmsg(0, 'Loaded: %s' % info.name)
    # Check for files to convert and run the conversion
    run_conversion()

def unload():
    es.dbgmsg(0, 'Unloaded: %s' % info.name)

# ============================================================================
# >> GAME EVENTS
# ============================================================================
def es_map_start(event_var):
    # Check for files to convert and run the conversion
    run_conversion()

# ============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# ============================================================================
def run_conversion():
    # List the file names from ../cfg/gungame51/converter/
    for fileName in os.listdir(convertDir):
        # If the file is the README.txt or an already converted file, skip it
        if fileName == 'README.txt' or fileName[-10:] == '.converted':
            continue

        # --------------------------------------------------------------------
        # GunGame3 Winners Conversion
        # --------------------------------------------------------------------
        if fileName == 'es_gg_winners_db.txt':
            # If gg_convert is set to 2, delete the winners database
            check_delete()

            # Create a new KeyValues instance
            kv = keyvalues.KeyValues(name='gg3_winners')
            # Load the winners database into the KeyValues instance
            kv.load(convertDir + fileName)

            # For every uniqueid that we will be converting
            for uniqueid in kv:
                uniqueid = str(uniqueid)

                # If it is not a proper uniqueid, skip it
                if not uniqueid.startswith('STEAM_'):
                    continue

                # Add the winner to the current database
                add_winner(kv[uniqueid]['name'], uniqueid, \
                kv[uniqueid]['wins'], int(time.time()))

        # --------------------------------------------------------------------
        # GunGame4 Winners Conversion
        # --------------------------------------------------------------------
        elif fileName == 'es_gg_database.sqldb':
            # If gg_convert is set to 2, delete the winners database
            check_delete()

            # Connect to the sqldb file
            sqldb = connect(convertDir + fileName)
            # Create the cursor
            cursor = sqldb.cursor()
            # Prepare the query
            cursor.execute('select * from gg_players')
            # Store the output in a list
            gg_players = cursor.fetchall()
            # Close the connection
            sqldb.close()

            # For every player in the database
            for player in gg_players:
                # Get their wins
                wins = player[2]

                # If the player has on wins, skip them
                if not wins:
                    continue

                # Add the winner to the current database
                add_winner(player[0], player[1], wins, player[-1])

        # --------------------------------------------------------------------
        # GunGame5 Winners Conversion
        # --------------------------------------------------------------------
        elif fileName == 'winnersdata.db':
            # If gg_convert is set to 2, delete the winners database
            check_delete()

            # Load the cPickle'd database into the winners dictionary
            winnersDataBaseFile = open(convertDir + 'winnersdata.db', 'r')
            winners = cPickle.load(winnersDataBaseFile)
            winnersDataBaseFile.close()

            # For every uniqueid in the winners database
            for uniqueid in winners:
                # Add the winner to the current database
                add_winner(winners[uniqueid]['name'], uniqueid, \
                winners[uniqueid]['wins'], int(winners[uniqueid] \
                ['timestamp']))

        # --------------------------------------------------------------------
        # GunGame3 SpawnPoints Conversion
        # --------------------------------------------------------------------
        elif fileName[-7:] == '_db.txt':
            # Create a new KeyValues instance
            kv = keyvalues.KeyValues(name=fileName[3:-7])
            # Load the spawnpoints database into the KeyValues instance
            kv.load(convertDir + fileName)

            convertedSpawnPoints = []

            # For every spawnpoint in the database, put them in our list
            for point in kv['points']:
                convertedSpawnPoints.append(kv['points'][str(point)] \
                .replace(',', ' ') + ' 0.000000 0.000000 0.000000\n')

            # Write the spawnpoints to the spawnpoint file
            write_spawnpoint_file(fileName, fileName[3:-7], \
            convertedSpawnPoints)

        # --------------------------------------------------------------------
        # GunGame4 Spawnpoints Conversion
        # --------------------------------------------------------------------
        elif fileName[-6:] == '.sqldb':
            # Connect to the sqldb file
            sqldb = connect(convertDir + fileName)
            # Create the cursor
            cursor = sqldb.cursor()
            # Prepare the query
            cursor.execute('select * from spawnpoints')
            # Store the output in a list
            spawnPoints = cursor.fetchall()
            # Close the connection
            sqldb.close()

            convertedSpawnPoints = []

            # For every spawnpoint in the database, put them in our list
            for point in spawnPoints:

                # If the spawnpoint is not valid, skip it
                if float(x) == 0 and float(y) == 0 and float(z) == 0:
                    continue

                convertedSpawnPoints.append('%s %s %s %s %s 0.000000\n' \
                % (point[2], point[3], point[4], point[5], point[6]))

            # Write the spawnpoints to the spawnpoint file
            write_spawnpoint_file(fileName, fileName[3:-6], \
            convertedSpawnPoints)

        # Store the name which the completed file will be renamed to
        renameTo = convertDir + fileName + '.converted'
        # Prepare to differentiate the file with a number if it already exists
        x = 1

        # As long as the file already exists
        while path.isfile(renameTo):
            # Differentiate the file by putting a number in it
            renameTo = convertDir + fileName + '[' + str(x) + ']' + \
            '.converted'
            # Increment the number
            x += 1

        # Rename the file
        os.rename(convertDir + fileName, renameTo)

    # Commit the queries to the database
    ggDB.commit()

def check_delete():
    # If gg_convert is set to overwrite the current database
    if int(gg_convert) == 2:
        # Delete everything from it
        ggDB.query("DELETE FROM gg_wins")

def write_spawnpoint_file(fileName, mapName, convertedSpawnPoints):
    # The name of the new spawnpoints file
    newFileName = mapName + '.txt'
    # The path to the new spawnpoints file
    newFilePath = es.ServerVar('eventscripts_gamedir') + '/cfg/gungame51/' + \
    'spawnpoints/' + newFileName

    # If the spawnpoints are being overwritten, or there are no current
    # spawnpoints, create an empty list for them
    if int(gg_convert) == 2 or not path.isfile(newFilePath):
        currentSpawnPoints = []
    # If there are current spawnpoints, save them in a list
    else:
        newFile = open(newFilePath, 'r')
        currentSpawnPoints = newFile.readlines()
        newFile.close()

    # Open the new spawnpoints file
    newFile = open(newFilePath, 'w')

    # Copy the converted spawnpoints so that we can remove the original
    # converted spawnpoints during the for loop iteration
    convertedSpawnPoints_copy = convertedSpawnPoints[:]

    # For every current spawnpoint
    for currentPoint in currentSpawnPoints:
        # For every converted spawnpoint
        for convertedPoint in convertedSpawnPoints_copy:
            # If the x, y and z are equal, remove the converted spawnpoint
            # and keep the current spawnpoint
            if currentPoint.split(' ')[0:3] == convertedPoint.split(' ')[0:3]:
                convertedSpawnPoints.remove(convertedPoint)

    # Combine the converted spawnpoints with the current ones
    convertedSpawnPoints.extend(currentSpawnPoints)

    # Write the spawnpoints to the spawnpoints file
    newFile.writelines(convertedSpawnPoints)

    # Close the file
    newFile.close()

def add_winner(name, uniqueid, wins, timestamp):
    # Store the number of wins that the player currently has, or None if they
    # do not exist
    currentWins = ggDB.select('gg_wins', 'wins', "where uniqueid = '%s'" % \
    uniqueid)

    # If the uniqueid is not in the database, add it
    if currentWins == None:
        ggDB.query("INSERT INTO gg_wins " + "(name, uniqueid, wins, " +
        "timestamp) " + "VALUES ('%s', '%s', '%s', %d)" % (name, uniqueid, \
        wins, timestamp))
    # If the uniqueid is in the database
    else:
        # If gg_convert is set to add the converted and current wins
        if int(gg_convert) == 1:
            totalWins = int(currentWins) + wins
        # If gg_convert is set to replace the current wins
        else:
            totalWins = wins

        # Update the number of wins for the uniqueid
        ggDB.query("UPDATE gg_wins SET wins=%s " % totalWins + "WHERE " + \
        "uniqueid = '%s'" % uniqueid)