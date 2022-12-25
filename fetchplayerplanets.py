import csv, requests, os, time
import xml.etree.ElementTree as ET
from supabase import create_client, Client
from datetime import date, datetime

class FetchPlayerPlanets:

    def loadPlayerIDs(self):
        print("Grabbing player information from Supabase")
        #get playerIDs from Supabase
        supabase_url = "https://euoufmuefdkmihbmcyvp.supabase.co"
        supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV1b3VmbXVlZmRrbWloYm1jeXZwIiwicm9sZSI6ImFub24iLCJpYXQiOjE2NzE1NDQ0MTksImV4cCI6MTk4NzEyMDQxOX0.3ffZfZnbKwPYrJlS-6juaM_tbKCzb8lsDePHI2hndUY"
        supabase: Client = create_client(supabase_url, supabase_key)
        queryRunTime = datetime.now().strftime("%Y-%m-%d 00:00:00")
        playerIDDict = supabase.table("players").select("playerID").gte('fetchDate', queryRunTime).execute()

        return playerIDDict.data           
    
    def searchXMLs(self, playersToParse):
        print("Parsing Planet information from players and grabbing XML information from API")
        #loop through each URL based on ID (https://s181-us.ogame.gameforge.com/api/playerData.xml?id=100654) and store those planet values (16 planets)
        URL = 'https://s181-us.ogame.gameforge.com/api/playerData.xml?id='
        planetItems = []

        inventoryCount = 0
        numberOfPlayers = len(playersToParse)
        for individualPlayer in playersToParse:
            for playerID in individualPlayer.values():
                #get info from XML
                XML = URL + str(playerID)
                resp = requests.get(XML)
                outFile = "output/s181" + str(playerID) + ".xml"
                with open(outFile, 'wb') as f:
                    f.write(resp.content)
                
                #Inventorying planets and construct return object
                tree = ET.parse(outFile)
                root = tree.getroot()
                applicationRunTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                listOfPlanets = {}
                listOfPlanets['playerID'] = root.attrib['id']
                listOfPlanets['fetchDate'] = applicationRunTime

                planetCount = 1
                for child in root[1]:
                    listOfPlanets['planet' + str(planetCount) + 'ID'] = child.attrib['id']
                    listOfPlanets['planet' + str(planetCount) + 'Name'] = child.attrib['name']
                    listOfPlanets['planet' + str(planetCount) + 'Coords'] = child.attrib['coords']
                    planetCount += 1    

                while planetCount <= 9:
                    listOfPlanets['planet' + str(planetCount) + 'ID'] = None
                    listOfPlanets['planet' + str(planetCount) + 'Name'] = None
                    listOfPlanets['planet' + str(planetCount) + 'Coords'] = None
                    planetCount += 1  

                planetItems.append(listOfPlanets)

                print("Inventoried planets on player " + str(inventoryCount) + " out of " + str(numberOfPlayers))
                inventoryCount += 1

                #delete the working XML file
                os.remove(outFile)    

                #sleep so XML calls dont break
                time.sleep(0.5)

        return planetItems

    def writeToDatabase(self, planetItems, filename):
        print("Writing Data to Supabase")
        #write all to new planets table
        fields = [
            'playerID',
            'planet1ID',
            'planet1Name',
            'planet1Coords',
            'planet2ID',
            'planet2Name',
            'planet2Coords',
            'planet3ID',
            'planet3Name',
            'planet3Coords',
            'planet4ID',
            'planet4Name',
            'planet4Coords',
            'planet5ID',
            'planet5Name',
            'planet5Coords',
            'planet6ID',
            'planet6Name',
            'planet6Coords',
            'planet7ID',
            'planet7Name',
            'planet7Coords',
            'planet8ID',
            'planet8Name',
            'planet8Coords',
            'planet9ID',
            'planet9Name',
            'planet9Coords',
            'fetchDate'         
            ]
    
        """
        # writing to csv file
        with open(filename, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = fields)
            writer.writeheader()
            writer.writerows(planetItems)
        """
        
        #Write out data to Supabase
        tableName = 'planets'
        supabase_url = "https://euoufmuefdkmihbmcyvp.supabase.co"
        supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV1b3VmbXVlZmRrbWloYm1jeXZwIiwicm9sZSI6ImFub24iLCJpYXQiOjE2NzE1NDQ0MTksImV4cCI6MTk4NzEyMDQxOX0.3ffZfZnbKwPYrJlS-6juaM_tbKCzb8lsDePHI2hndUY"
        supabase: Client = create_client(supabase_url, supabase_key)
        main_list = []
        for item in planetItems:
            value = {
                'playerID': item['playerID'],
                'planet1ID': item['planet1ID'],
                'planet1Name': item['planet1Name'],
                'planet1Coords': item['planet1Coords'],
                'planet2ID': item['planet2ID'],
                'planet2Name': item['planet2Name'],
                'planet2Coords': item['planet2Coords'],
                'planet3ID': item['planet3ID'],
                'planet3Name': item['planet3Name'],
                'planet3Coords': item['planet3Coords'],
                'planet4ID': item['planet4ID'],
                'planet4Name': item['planet4Name'],
                'planet4Coords': item['planet4Coords'],
                'planet5ID': item['planet5ID'],
                'planet5Name': item['planet5Name'],
                'planet5Coords': item['planet5Coords'],
                'planet6ID': item['planet6ID'],
                'planet6Name': item['planet6Name'],
                'planet6Coords': item['planet6Coords'],
                'planet7ID': item['planet7ID'],
                'planet7Name': item['planet7Name'],
                'planet7Coords': item['planet7Coords'],
                'planet8ID': item['planet8ID'],
                'planet8Name': item['planet8Name'],
                'planet8Coords': item['planet8Coords'],
                'planet9ID': item['planet9ID'],
                'planet9Name': item['planet9Name'],
                'planet9Coords': item['planet9Coords'],
                'fetchDate': item['fetchDate']       
            }
            main_list.append(value)

        data = supabase.table(tableName).insert(main_list).execute()  

    def startFetching(self):
        # load from web to update existing xml file
        playersToParse = self.loadPlayerIDs()
        # parse xml file
        items = self.searchXMLs(playersToParse)
        # store players items in a csv file
        self.writeToDatabase(items, 'output/s131PlanetsResults.csv')
            
        