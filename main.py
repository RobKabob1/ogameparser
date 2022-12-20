from fetchplayers import FetchPlayers
from databasesetup import DatabaseSetup
import time

startTime = time.time()

if __name__ == '__main__':
    #Test out database connectino
    bot = DatabaseSetup()
    bot.connect()
    """
    #Begin Applying
    bot = LinkedinEasyApply(parameters, browser)
    bot.login()
    bot.security_check()
    bot.start_applying()
    """
    bot = FetchPlayers()
    bot.startFetching()

    executionTime = (time.time() - startTime)
    print('Execution time in seconds: ' + str(executionTime))
