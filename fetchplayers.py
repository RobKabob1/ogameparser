import csv, requests, os
import xml.etree.ElementTree as ET
from supabase import create_client, Client
from datetime import date, datetime

class FetchPlayers:
    def loadXML(self):
        print("Grabbing Players XML information from API")
        #Inventory the list of URLs to go through
        urls = {
            'playerHighLevel':'https://s181-us.ogame.gameforge.com/api/players.xml',
            'playerTotal':'https://s181-us.ogame.gameforge.com/api/highscore.xml?category=1&type=0',
            'playerEconomy':'https://s181-us.ogame.gameforge.com/api/highscore.xml?category=1&type=1',
            'playerResearch':'https://s181-us.ogame.gameforge.com/api/highscore.xml?category=1&type=2',
            'playerMilitaryHighLevel':'https://s181-us.ogame.gameforge.com/api/highscore.xml?category=1&type=3',
            'playerMilitaryLost':'https://s181-us.ogame.gameforge.com/api/highscore.xml?category=1&type=4',
            'playerMilitaryBuilt':'https://s181-us.ogame.gameforge.com/api/highscore.xml?category=1&type=5',
            'playerMilitaryDestroyed':'https://s181-us.ogame.gameforge.com/api/highscore.xml?category=1&type=6',
            'playerMilitaryHonor':'https://s181-us.ogame.gameforge.com/api/highscore.xml?category=1&type=7',
            'playerLifeformHighLevel':'https://s181-us.ogame.gameforge.com/api/highscore.xml?category=1&type=8',
            'playerLifeformEconomy':'https://s181-us.ogame.gameforge.com/api/highscore.xml?category=1&type=9',
            'playerLifeformTechnology':'https://s181-us.ogame.gameforge.com/api/highscore.xml?category=1&type=10',
            'playerLifeformDiscoveries':'https://s181-us.ogame.gameforge.com/api/highscore.xml?category=1&type=11'
        }
        
        #Grab the XML files for each of the URLs and return the XML files for parsing later
        listOfXMLs = {}
        for name, url in urls.items():
            resp = requests.get(url)
            outFile = "output/s181" + name + ".xml"
            listOfXMLs[name] = outFile
            with open(outFile, 'wb') as f:
                f.write(resp.content)

        return listOfXMLs

    def parseXML(self, XMLList):
        print("Parsing XMLs")
        #Inventorying high level items
        tree = ET.parse(XMLList.get('playerHighLevel'))
        root = tree.getroot()
        playersItems = []
        applicationRunTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for child in root:
            playersDirectory = {}
            playersDirectory['playerID'] = child.attrib['id']
            playersDirectory['playerName'] = child.attrib['name']
            if 'status' in child.attrib:
                playersDirectory['playerStatus'] = child.attrib['status']
            else:
                playersDirectory['playerStatus'] = None
            if 'alliance' in child.attrib:
                playersDirectory['playerAlliance'] = child.attrib['alliance']
            else:
                playersDirectory['playerAlliance'] = None
            playersDirectory['fetchDate'] = applicationRunTime

            #Create Null values that we can update later. Null values are required for our Supabase insert.
            playersDirectory['playerTotalPosition'] = None
            playersDirectory['playerTotalScore'] = None
            playersDirectory['playerEconomyPosition'] = None
            playersDirectory['playerEconomyScore'] = None
            playersDirectory['playerResearchPosition'] = None
            playersDirectory['playerResearchScore'] = None
            playersDirectory['playerMilitaryHighLevelPosition'] = None
            playersDirectory['playerMilitaryHighLevelScore'] = None
            playersDirectory['playerMilitaryHighLevelShips'] = None
            playersDirectory['playerMilitaryLostPosition'] = None
            playersDirectory['playerMilitaryLostScore'] = None
            playersDirectory['playerMilitaryBuiltPosition'] = None
            playersDirectory['playerMilitaryBuiltScore'] = None
            playersDirectory['playerMilitaryDestroyedPosition'] = None
            playersDirectory['playerMilitaryDestroyedScore'] = None
            playersDirectory['playerMilitaryHonorPosition'] = None
            playersDirectory['playerMilitaryHonorScore'] = None
            playersDirectory['playerLifeformHighLevelPosition'] = None
            playersDirectory['playerLifeformHighLevelScore'] = None
            playersDirectory['playerLifeformEconomyPosition'] = None
            playersDirectory['playerLifeformEconomyScore'] = None
            playersDirectory['playerLifeformTechnologyPosition'] = None
            playersDirectory['playerLifeformTechnologyScore'] = None
            playersDirectory['playerLifeformDiscoveriesPosition'] = None
            playersDirectory['playerLifeformDiscoveriesScore'] = None
                        
            playersItems.append(playersDirectory)
        
        #remove the HighLevelXML before we iterate on each of them below
        os.remove(XMLList['playerHighLevel'])
        XMLList.pop('playerHighLevel')

        #Loop through the rest of the items containing all individual player score and position items
        for XMLName, XMLLocation in XMLList.items():
            
            tree = ET.parse(XMLLocation)
            root = tree.getroot()

            for child in root:
                for dict in playersItems:
                    if dict.get('playerID') == child.attrib['id']:
                        positionName = XMLName + "Position"
                        positionDictUpdate = {positionName: child.attrib['position']}
                        dict.update(positionDictUpdate)
                        positionName = XMLName + "Score"
                        scoreDictUpdate = {positionName: child.attrib['score']}
                        dict.update(scoreDictUpdate)
                        if 'ships' in child.attrib:
                            positionName = XMLName + "Ships"
                            scoreDictUpdate = {positionName: child.attrib['ships']}
                            dict.update(scoreDictUpdate)
        
        # delete working files
        for file in XMLList.values():
            os.remove(file)

        #return all data
        return playersItems

    def writeToDatabase(self, playersItems, filename):
        print("Writing Data to Supabase")
        fields = [
            'playerID', 
            'playerName', 
            'playerStatus', 
            'playerAlliance', 
            'fetchDate', 
            'playerTotalPosition',
            'playerTotalScore',
            'playerEconomyPosition',
            'playerEconomyScore',
            'playerResearchPosition',
            'playerResearchScore',
            'playerMilitaryHighLevelPosition',
            'playerMilitaryHighLevelScore',
            'playerMilitaryHighLevelShips',
            'playerMilitaryLostPosition',
            'playerMilitaryLostScore',
            'playerMilitaryBuiltPosition',
            'playerMilitaryBuiltScore',
            'playerMilitaryDestroyedPosition',
            'playerMilitaryDestroyedScore',
            'playerMilitaryHonorPosition',
            'playerMilitaryHonorScore',
            'playerLifeformHighLevelPosition',
            'playerLifeformHighLevelScore',
            'playerLifeformEconomyPosition',
            'playerLifeformEconomyScore',
            'playerLifeformTechnologyPosition',
            'playerLifeformTechnologyScore',
            'playerLifeformDiscoveriesPosition',
            'playerLifeformDiscoveriesScore',           
            ]
    
        """
        # writing to csv file
        with open(filename, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = fields)
            writer.writeheader()
            writer.writerows(playersItems)
        """
        
        #Write out data to Supabase
        tableName = 'players'
        supabase_url = "https://euoufmuefdkmihbmcyvp.supabase.co"
        supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV1b3VmbXVlZmRrbWloYm1jeXZwIiwicm9sZSI6ImFub24iLCJpYXQiOjE2NzE1NDQ0MTksImV4cCI6MTk4NzEyMDQxOX0.3ffZfZnbKwPYrJlS-6juaM_tbKCzb8lsDePHI2hndUY"
        supabase: Client = create_client(supabase_url, supabase_key)
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
        
        data = supabase.table(tableName).insert(main_list).execute()  
        
    def startFetching(self):
        # load from web to update existing xml file
        XMLsToParse = self.loadXML()
        # parse xml file
        items = self.parseXML(XMLsToParse)
        # store players items in a csv file
        self.writeToDatabase(items, 'output/s131PlayersResults.csv')