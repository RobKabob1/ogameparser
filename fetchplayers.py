import csv
import requests
import xml.etree.ElementTree as ET

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

    def savetoCSV(self, playersItems, filename):
        fields = ['playerID', 'playerName', 'playerStatus', 'playerAlliance']
        # writing to csv file
        with open(filename, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = fields)
            writer.writeheader()
            writer.writerows(playersItems)

    def startFetching(self):
        # load from web to update existing xml file
        self.loadXML()
        # parse xml file
        items = self.parseXML('output/s181Players.xml')
        # store players items in a csv file
        self.savetoCSV(items, 'output/s131PlayersResults.csv')