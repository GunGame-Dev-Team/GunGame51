# ../scripts/included/gg_convert/gg_convert.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
from __future__ import with_statement
import cPickle
from sqlite3 import connect
import time

# Eventscripts Imports
import es
import keyvalues

# GunGame Imports
from gungame51.core import get_game_dir
from gungame51.core.addons.shortcuts import AddonInfo
from gungame51.core.sql import Database
from gungame51.core.sql.shortcuts import insert_winner
from gungame51.core.sql.shortcuts import update_winner

# =============================================================================
# >> ADDON REGISTRATION/INFORMATION
# =============================================================================
info = AddonInfo()
info.name = 'gg_convert'
info.title = 'GG Welcome Message'
info.author = 'GG Dev Team'
info.version = "5.1.%s" % "$Rev$".split('$Rev: ')[1].split()[0]

# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
gg_convert = es.ServerVar('gg_convert')
# The path to the directory from which we convert
convertDir = get_game_dir('cfg/gungame51/converter')
# An instance of the Database() class to adjust the winners database with
ggDB = Database()


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    # Check for files to convert and run the conversion
    run_conversion()


# =============================================================================
# >> GAME EVENTS
# =============================================================================
def es_map_start(event_var):
    # Check for files to convert and run the conversion
    run_conversion()


# =============================================================================
# >> CUSTOM/HELPER FUNCTIONS
# =============================================================================
def run_conversion():
    # List the file names from ../cfg/gungame51/converter/
    for file_path in convertDir.files():

        file_name = file_path.name

        # If the file is the README.txt or an already converted file, skip it
        if file_name == 'README.txt' or file_name[-10:] == '.converted':
            continue

        # --------------------------------------------------------------------
        # GunGame3 Winners Conversion
        # --------------------------------------------------------------------
        if file_name == 'es_gg_winners_db.txt':
            # If gg_convert is set to 2, delete the winners database
            check_delete()

            # Create a new KeyValues instance
            kv = keyvalues.KeyValues(name='gg3_winners')
            # Load the winners database into the KeyValues instance
            kv.load(file_path)

            # For every uniqueid that we will be converting
            for uniqueid in kv:
                uniqueid = str(uniqueid)

                # If it is not a proper uniqueid, skip it
                if not uniqueid.startswith('STEAM_'):
                    continue

                # Add the winner to the current database
                add_winner(kv[uniqueid]['name'], uniqueid,
                    kv[uniqueid]['wins'], int(time.time()))

        # --------------------------------------------------------------------
        # GunGame4 Winners Conversion
        # --------------------------------------------------------------------
        elif file_name == 'es_gg_database.sqldb':
            # If gg_convert is set to 2, delete the winners database
            check_delete()

            # Connect to the sqldb file
            sqldb = connect(file_path)
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
        elif file_name == 'winnersdata.db':
            # If gg_convert is set to 2, delete the winners database
            check_delete()

            # Load the cPickle'd database into the winners dictionary
            with file_path.open() as winnersDataBaseFile:
                winners = cPickle.load(winnersDataBaseFile)

            # For every uniqueid in the winners database
            for uniqueid in winners:
                # Add the winner to the current database
                add_winner(winners[uniqueid]['name'],
                    uniqueid, winners[uniqueid]['wins'],
                    int(winners[uniqueid]['timestamp']))

        # --------------------------------------------------------------------
        # GunGame3 SpawnPoints Conversion
        # --------------------------------------------------------------------
        elif file_name[-7:] == '_db.txt':
            # Create a new KeyValues instance
            kv = keyvalues.KeyValues(name=file_name[3:-7])
            # Load the spawnpoints database into the KeyValues instance
            kv.load(file_path)

            convertedSpawnPoints = []

            # For every spawnpoint in the database, put them in our list
            for point in kv['points']:
                convertedSpawnPoints.append(
                    kv['points'][str(point)].replace(',', ' ') +
                    ' 0.000000 0.000000 0.000000\n')

            # Write the spawnpoints to the spawnpoint file
            write_spawnpoint_file(
                file_name, file_name[3:-7], convertedSpawnPoints)

        # --------------------------------------------------------------------
        # GunGame4 Spawnpoints Conversion
        # --------------------------------------------------------------------
        elif file_name[-6:] == '.sqldb':
            # Connect to the sqldb file
            sqldb = connect(file_path)
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

                convertedSpawnPoints.append(
                    '%s %s %s %s %s 0.000000\n' % tuple(point[2:7]))

            # Write the spawnpoints to the spawnpoint file
            write_spawnpoint_file(
                file_name, file_name[3:-6], convertedSpawnPoints)

        # Store the name which the completed file will be renamed to
        renameTo = file_path + '.converted'

        # Prepare to differentiate the file with a number if it already exists
        x = 1

        # As long as the file already exists
        while renameTo.isfile():

            # Differentiate the file by putting a number in it
            renameTo = (file_path + '[' + str(x) + ']' + '.converted')

            # Increment the number
            x += 1

        # Rename the file
        file_path.rename(renameTo)

    # Commit the queries to the database
    ggDB.commit()


def check_delete():
    # If gg_convert is set to overwrite the current database
    if int(gg_convert) == 2:

        # Delete everything from it
        ggDB._query("DELETE FROM gg_wins")


def write_spawnpoint_file(fileName, mapName, convertedSpawnPoints):
    # The name of the new spawnpoints file
    newFileName = mapName + '.txt'

    # The path to the new spawnpoints file
    newFilePath = get_game_dir('/cfg/gungame51/spawnpoints/' + newFileName)

    # If the spawnpoints are being overwritten, or there are no current
    # spawnpoints, create an empty list for them
    if int(gg_convert) == 2 or not newFilePath.isfile():
        currentSpawnPoints = []

    # If there are current spawnpoints, save them in a list
    else:

        with newFilePath.open() as newFile:
            currentSpawnPoints = newFile.readlines()

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

    # Open the new spawnpoints file
    with newFilePath.open('w') as newFile:

        # Write the spawnpoints to the spawnpoints file
        newFile.writelines(convertedSpawnPoints)


def add_winner(name, uniqueid, wins, timestamp):
    # Store the number of wins that the player currently has, or None if they
    # do not exist
    currentWins = ggDB.select(
        'gg_wins', 'wins', 'where uniqueid = "%s"' % uniqueid)

    # If the uniqueid is not in the database, add it
    if currentWins == None:
        insert_winner(name, uniqueid, wins, timestamp)
    # If the uniqueid is in the database
    else:
        # If gg_convert is set to add the converted and current wins
        if int(gg_convert) == 1:
            totalWins = int(currentWins) + wins
        # If gg_convert is set to replace the current wins
        else:
            totalWins = wins

        # Update the number of wins stored for the uniqueid
        update_winner('wins', totalWins, uniqueid=uniqueid)
