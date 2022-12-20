from fetchplayers import FetchPlayers

if __name__ == '__main__':
    
    """
    #Make table for new user if it doesnt exist
    bot = DatabaseSetup(parameters)
    bot.connect()

    #Begin Applying
    bot = LinkedinEasyApply(parameters, browser)
    bot.login()
    bot.security_check()
    bot.start_applying()
    """
    bot = FetchPlayers()
    bot.startFetching()
