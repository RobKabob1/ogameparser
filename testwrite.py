import csv, requests, os, logging
import xml.etree.ElementTree as ET
#from supabase import create_client, Client
import psycopg2
from psycopg2 import sql
from datetime import datetime
from databasesetup import DatabaseSetup


def writeToDatabase(self, playersItems):
    logging.info("Writing Data to Supabase")
    
    # Create database connection 
    dbConnection = DatabaseSetup()

    conn = None
    try:
        # read connection parameters & connect to PostgreSQL server
        params = dbConnection.config()
        logging.info('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        
        # create a cursor
        cur = conn.cursor()
        
        #Copy data from the players table into the playersDaily table
        """
        SQL = "DELETE FROM public.\"playersDaily\""
        cur.execute(SQL)
        conn.commit()
        """
        main_list = []
        for item in playersItems:
            value = {
                'playerID': item['playerID'],
                'playerName': item['playerName'],
                'playerStatus': item['playerStatus'],
                'playerAlliance': item['playerAlliance'],
                'fetchDate': item['fetchDate'],
                'playerTotalPosition': item['playerTotalPosition'],
                'playerTotalScore': item['playerTotalScore'],
                'playerEconomyPosition': item['playerEconomyPosition'],
                'playerEconomyScore': item['playerEconomyScore'],
                'playerResearchPosition': item['playerResearchPosition'],
                'playerResearchScore': item['playerResearchScore'],
                'playerMilitaryHighLevelPosition': item['playerMilitaryHighLevelPosition'],
                'playerMilitaryHighLevelScore': item['playerMilitaryHighLevelScore'],
                'playerMilitaryHighLevelShips': item['playerMilitaryHighLevelShips'],
                'playerMilitaryLostPosition': item['playerMilitaryLostPosition'],
                'playerMilitaryLostScore': item['playerMilitaryLostScore'],
                'playerMilitaryBuiltPosition': item['playerMilitaryBuiltPosition'],
                'playerMilitaryBuiltScore': item['playerMilitaryBuiltScore'],
                'playerMilitaryDestroyedPosition': item['playerMilitaryDestroyedPosition'],
                'playerMilitaryDestroyedScore': item['playerMilitaryDestroyedScore'],
                'playerMilitaryHonorPosition': item['playerMilitaryHonorPosition'],
                'playerMilitaryHonorScore': item['playerMilitaryHonorScore'],
                'playerLifeformHighLevelPosition': item['playerLifeformHighLevelPosition'],
                'playerLifeformHighLevelScore': item['playerLifeformHighLevelScore'],
                'playerLifeformEconomyPosition': item['playerLifeformEconomyPosition'],
                'playerLifeformEconomyScore': item['playerLifeformEconomyScore'],
                'playerLifeformTechnologyPosition': item['playerLifeformTechnologyPosition'],
                'playerLifeformTechnologyScore': item['playerLifeformTechnologyScore'],
                'playerLifeformDiscoveriesPosition': item['playerLifeformDiscoveriesPosition'],
                'playerLifeformDiscoveriesScore': item['playerLifeformDiscoveriesScore']           
            }
            main_list.append(value)
        logging.info(main_list)

        # close the communication with the PostgreSQL
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        logging.info(error)
    finally:
        if conn is not None:
            conn.close()
            logging.info('Database connection closed.')