import csv
import requests
import xml.etree.ElementTree as ET
from supabase import create_client, Client
from datetime import date, datetime

class FetchPlayers:
    def loadXML(self):
        # creating HTTP response object from players high-level url and saving the xml file
        url = 'https://s181-us.ogame.gameforge.com/api/players.xml'
        resp = requests.get(url)
        with open('output/s181PlayersHighLevel.xml', 'wb') as f:
            f.write(resp.content)

        # creating HTTP response object from players total url and saving the xml file
        url = 'https://s181-us.ogame.gameforge.com/api/highscore.xml?category=1&type=0'
        resp = requests.get(url)
        with open('output/s181PlayersTotal.xml', 'wb') as f:
            f.write(resp.content)

    def parseXML(self, highLevelXML, totalScoreXML):
        #Inventorying high level items
        tree = ET.parse(highLevelXML)
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
            playersItems.append(playersDirectory)

        #Inventorying total score items
        tree = ET.parse(totalScoreXML)
        root = tree.getroot()

        for child in root:
            for dict in playersItems:
                if dict.get('playerID') == child.attrib['id']:
                    positionDictUpdate = {'playerTotalPosition': child.attrib['position']}
                    dict.update(positionDictUpdate)
                    scoreDictUpdate = {'playerTotalScore': child.attrib['score']}
                    dict.update(scoreDictUpdate)

        return playersItems

    def writeToDatabase(self, playersItems, filename):
        fields = ['playerID', 'playerName', 'playerStatus', 'playerAlliance', 'fetchDate', 'playerTotalPosition', 'playerTotalScore']
    
        # writing to csv file
        with open(filename, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = fields)
            writer.writeheader()
            writer.writerows(playersItems)
        
        numberOfPlayers = len(playersItems)
        count = 1
        for item in playersItems:
            #Write out data to Supabase
            tableName = 'players'
            supabase_url = "https://euoufmuefdkmihbmcyvp.supabase.co"
            supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV1b3VmbXVlZmRrbWloYm1jeXZwIiwicm9sZSI6ImFub24iLCJpYXQiOjE2NzE1NDQ0MTksImV4cCI6MTk4NzEyMDQxOX0.3ffZfZnbKwPYrJlS-6juaM_tbKCzb8lsDePHI2hndUY"
            supabase: Client = create_client(supabase_url, supabase_key)
            main_list = []
            value = {
                'playerID': item['playerID'],
                'playerName': item['playerName'],
                'playerStatus': item['playerStatus'],
                'playerAlliance': item['playerAlliance'],
                'fetchDate': item['fetchDate'],
                'playerTotalPosition': item['playerTotalPosition'],
                'playerTotalScore': item['playerTotalScore']
            }
            main_list.append(value)
            data = supabase.table(tableName).insert(main_list).execute()  

            #Keep track of progress because this upload takes a while
            print("Working on player " + str(count) + " out of " + str(numberOfPlayers))
            count += 1
        
    def startFetching(self):
        # load from web to update existing xml file
        self.loadXML()
        # parse xml file
        items = self.parseXML('output/s181PlayersHighLevel.xml', 'output/s181PlayersTotal.xml')
        # store players items in a csv file
        self.writeToDatabase(items, 'output/s131PlayersResults.csv')