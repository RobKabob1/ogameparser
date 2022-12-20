import csv
import requests
import xml.etree.ElementTree as ET
from supabase import create_client, Client

class FetchPlayers:
    def loadXML(self):
        # url of feed
        url = 'https://s181-us.ogame.gameforge.com/api/players.xml'
        # creating HTTP response object from given url
        resp = requests.get(url)
        # saving the xml file
        with open('output/s181Players.xml', 'wb') as f:
            f.write(resp.content)

    def parseXML(self, xmlfile):
        tree = ET.parse(xmlfile)
        root = tree.getroot()
        # create empty list for players items
        playersItems = []
        
        for child in root:
            playersDirectory = {}

            #get each attribute from players XML
            playersDirectory['playerID'] = child.attrib['id']
            playersDirectory['playerName'] = child.attrib['name']
            if 'status' in child.attrib:
                playersDirectory['playerStatus'] = child.attrib['status']
            else:
                playersDirectory['playerStatus'] = ''
            if 'alliance' in child.attrib:
                playersDirectory['playerAlliance'] = child.attrib['alliance']
            else:
                playersDirectory['playerAlliance'] = ''

            # append players dictionary to players items list
            playersItems.append(playersDirectory)
        return playersItems

    def writeToDatabase(self, playersItems, filename):
        fields = ['playerID', 'playerName', 'playerStatus', 'playerAlliance']
    
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
        items = self.parseXML('output/s181Players.xml')
        # store players items in a csv file
        self.writeToDatabase(items, 'output/s131PlayersResults.csv')