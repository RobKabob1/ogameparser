from fetchplayers import FetchPlayers
from fetchalliances import FetchAlliances
from fetchplayerplanets import FetchPlayerPlanets
from databasesetup import DatabaseSetup
from createSnapshots import CreateSnapshots
import time

startTime = time.time()

if __name__ == '__main__':
    #Test out database connectino
    bot = DatabaseSetup()
    bot.connect()

    #Fetch Players
    playersTime = time.time()
    bot = FetchPlayers()
    bot.startFetching()
    playersExecutionTime = (time.time() - playersTime)
    print('Players execution time in seconds: ' + str(playersExecutionTime))
    
    #Fetch Alliances
    alliancesTime = time.time()
    bot = FetchAlliances()
    bot.startFetching()
    alliancesExecutionTime = (time.time() - alliancesTime)
    print('Alliances execution time in seconds: ' + str(alliancesExecutionTime))
    
    #Fetch Player Planets
    planetsTime = time.time()
    bot = FetchPlayerPlanets()
    bot.startFetching()
    planetsExecutionTime = (time.time() - planetsTime)
    print('Planets execution time in seconds: ' + str(planetsExecutionTime))
    
    #Snapshot Current Day Players and Alliances for Daily Tables
    snapshotsTime = time.time()
    bot = CreateSnapshots()
    bot.startSnapshots()
    planetsExecutionTime = (time.time() - snapshotsTime)
    print('Snapshot of Players and Alliances execution time in seconds: ' + str(planetsExecutionTime))

    executionTime = (time.time() - startTime)
    print('Total fetch execution time in seconds: ' + str(executionTime))