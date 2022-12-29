from fetchplayers import FetchPlayers
#from fetchalliances import FetchAlliances
#from fetchplayerplanets import FetchPlayerPlanets
from databasesetup import DatabaseSetup
from createSnapshots import CreateSnapshots
import logging, time

def main():
    #Build Logger
    startTime = time.time()
    logging.basicConfig(filename='ogameparser.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(name)s:%(message)s')    

    #Test out database connection
    logging.info('Testing out database connections')
    bot = DatabaseSetup()
    bot.connect()

    #Fetch Players
    playersTime = time.time()
    bot = FetchPlayers()
    bot.startFetching()
    playersExecutionTime = (time.time() - playersTime)
    logging.info('Players execution time in seconds: ' + str(playersExecutionTime))
    """
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
    """
    executionTime = (time.time() - startTime)
    logging.info('Finish running script. Total fetch execution time in seconds: ' + str(executionTime))

if __name__ == '__main__':
    main()