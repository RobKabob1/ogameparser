from fetchplayers import FetchPlayers
from fetchalliances import FetchAlliances
from databasesetup import DatabaseSetup
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

    executionTime = (time.time() - startTime)
    print('Total fetch execution time in seconds: ' + str(executionTime))
