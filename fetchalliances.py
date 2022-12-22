import csv
import requests
import xml.etree.ElementTree as ET
from supabase import create_client, Client
from datetime import date, datetime

class FetchAlliances:
    def loadXML(self):
        # url of feed
        url = 'https://s181-us.ogame.gameforge.com/api/alliances.xml'
        # creating HTTP response object from given url
        resp = requests.get(url)
        # saving the xml file
        with open('output/s181Alliances.xml', 'wb') as f:
            f.write(resp.content)

        #Inventory the list of URLs to go through
        urls = {
            'allianceHighLevel':'https://s181-us.ogame.gameforge.com/api/alliances.xml',
            'allianceTotal':'https://s181-us.ogame.gameforge.com/api/highscore.xml?category=2&type=0',
            'allianceEconomy':'https://s181-us.ogame.gameforge.com/api/highscore.xml?category=2&type=1',
            'allianceResearch':'https://s181-us.ogame.gameforge.com/api/highscore.xml?category=2&type=2',
            'allianceMilitaryHighLevel':'https://s181-us.ogame.gameforge.com/api/highscore.xml?category=2&type=3',
            'allianceMilitaryLost':'https://s181-us.ogame.gameforge.com/api/highscore.xml?category=2&type=4',
            'allianceMilitaryBuilt':'https://s181-us.ogame.gameforge.com/api/highscore.xml?category=2&type=5',
            'allianceMilitaryDestroyed':'https://s181-us.ogame.gameforge.com/api/highscore.xml?category=2&type=6',
            'allianceMilitaryHonor':'https://s181-us.ogame.gameforge.com/api/highscore.xml?category=2&type=7',
            'allianceLifeformHighLevel':'https://s181-us.ogame.gameforge.com/api/highscore.xml?category=2&type=8',
            'allianceLifeformEconomy':'https://s181-us.ogame.gameforge.com/api/highscore.xml?category=2&type=9',
            'allianceLifeformTechnology':'https://s181-us.ogame.gameforge.com/api/highscore.xml?category=2&type=10',
            'allianceLifeformDiscoveries':'https://s181-us.ogame.gameforge.com/api/highscore.xml?category=2&type=11'
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
        #Inventorying high level items
        tree = ET.parse(XMLList.get('allianceHighLevel'))
        root = tree.getroot()
        alliancesItems = []
        applicationRunTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for child in root:
            alliancesDirectory = {}
            alliancesDirectory['allianceID'] = child.attrib['id']
            alliancesDirectory['allianceName'] = child.attrib['name']
            alliancesDirectory['allianceTag'] = child.attrib['tag']
            alliancesDirectory['founderID'] = child.attrib['founder']
            alliancesDirectory['foundDate'] = child.attrib['foundDate']
            if 'open' in child.attrib:
                alliancesDirectory['allianceOpen'] = child.attrib['open']
            else:
                alliancesDirectory['allianceOpen'] = None
            alliancesDirectory['fetchDate'] = applicationRunTime

            #Create Null values that we can update later. Null values are required for our Supabase insert.
            alliancesDirectory['allianceTotalPosition'] = None
            alliancesDirectory['allianceTotalScore'] = None
            alliancesDirectory['allianceEconomyPosition'] = None
            alliancesDirectory['allianceEconomyScore'] = None
            alliancesDirectory['allianceResearchPosition'] = None
            alliancesDirectory['allianceResearchScore'] = None
            alliancesDirectory['allianceMilitaryHighLevelPosition'] = None
            alliancesDirectory['allianceMilitaryHighLevelScore'] = None
            alliancesDirectory['allianceMilitaryLostPosition'] = None
            alliancesDirectory['allianceMilitaryLostScore'] = None
            alliancesDirectory['allianceMilitaryBuiltPosition'] = None
            alliancesDirectory['allianceMilitaryBuiltScore'] = None
            alliancesDirectory['allianceMilitaryDestroyedPosition'] = None
            alliancesDirectory['allianceMilitaryDestroyedScore'] = None
            alliancesDirectory['allianceMilitaryHonorPosition'] = None
            alliancesDirectory['allianceMilitaryHonorScore'] = None
            alliancesDirectory['allianceLifeformHighLevelPosition'] = None
            alliancesDirectory['allianceLifeformHighLevelScore'] = None
            alliancesDirectory['allianceLifeformEconomyPosition'] = None
            alliancesDirectory['allianceLifeformEconomyScore'] = None
            alliancesDirectory['allianceLifeformTechnologyPosition'] = None
            alliancesDirectory['allianceLifeformTechnologyScore'] = None
            alliancesDirectory['allianceLifeformDiscoveriesPosition'] = None
            alliancesDirectory['allianceLifeformDiscoveriesScore'] = None
                        
            alliancesItems.append(alliancesDirectory)
        
        #remove the HighLevelXML before we iterate on each of them below
        XMLList.pop('allianceHighLevel')

        #Loop through the rest of the items containing all individual alliance score and position items
        for XMLName, XMLLocation in XMLList.items():
            
            tree = ET.parse(XMLLocation)
            root = tree.getroot()

            for child in root:
                for dict in alliancesItems:
                    if dict.get('allianceID') == child.attrib['id']:
                        positionName = XMLName + "Position"
                        positionDictUpdate = {positionName: child.attrib['position']}
                        dict.update(positionDictUpdate)
                        positionName = XMLName + "Score"
                        scoreDictUpdate = {positionName: child.attrib['score']}
                        dict.update(scoreDictUpdate)

        #return all data
        return alliancesItems

    def writeToDatabase(self, alliancesItems, filename):
        fields = [
            'allianceID', 
            'allianceName', 
            'allianceTag', 
            'founderID', 
            'foundDate', 
            'allianceOpen',
            'fetchDate', 
            'allianceTotalPosition',
            'allianceTotalScore',
            'allianceEconomyPosition',
            'allianceEconomyScore',
            'allianceResearchPosition',
            'allianceResearchScore',
            'allianceMilitaryHighLevelPosition',
            'allianceMilitaryHighLevelScore',
            'allianceMilitaryLostPosition',
            'allianceMilitaryLostScore',
            'allianceMilitaryBuiltPosition',
            'allianceMilitaryBuiltScore',
            'allianceMilitaryDestroyedPosition',
            'allianceMilitaryDestroyedScore',
            'allianceMilitaryHonorPosition',
            'allianceMilitaryHonorScore',
            'allianceLifeformHighLevelPosition',
            'allianceLifeformHighLevelScore',
            'allianceLifeformEconomyPosition',
            'allianceLifeformEconomyScore',
            'allianceLifeformTechnologyPosition',
            'allianceLifeformTechnologyScore',
            'allianceLifeformDiscoveriesPosition',
            'allianceLifeformDiscoveriesScore',           
            ]
    
        # writing to csv file
        with open(filename, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = fields)
            writer.writeheader()
            writer.writerows(alliancesItems)
        
        numberOfalliances = len(alliancesItems)
        count = 1
        for item in alliancesItems:
            #Write out data to Supabase
            tableName = 'alliances'
            supabase_url = "https://euoufmuefdkmihbmcyvp.supabase.co"
            supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV1b3VmbXVlZmRrbWloYm1jeXZwIiwicm9sZSI6ImFub24iLCJpYXQiOjE2NzE1NDQ0MTksImV4cCI6MTk4NzEyMDQxOX0.3ffZfZnbKwPYrJlS-6juaM_tbKCzb8lsDePHI2hndUY"
            supabase: Client = create_client(supabase_url, supabase_key)
            main_list = []
            value = {
                'allianceID': item['allianceID'],
                'allianceName': item['allianceName'],
                'allianceTag': item['allianceTag'],
                'founderID': item['founderID'],
                'foundDate': item['foundDate'],
                'allianceOpen': item['allianceOpen'],
                'fetchDate': item['fetchDate'],
                'allianceTotalPosition': item['allianceTotalPosition'],
                'allianceTotalScore': item['allianceTotalScore'],
                'allianceEconomyPosition': item['allianceEconomyPosition'],
                'allianceEconomyScore': item['allianceEconomyScore'],
                'allianceResearchPosition': item['allianceResearchPosition'],
                'allianceResearchScore': item['allianceResearchScore'],
                'allianceMilitaryHighLevelPosition': item['allianceMilitaryHighLevelPosition'],
                'allianceMilitaryHighLevelScore': item['allianceMilitaryHighLevelScore'],
                'allianceMilitaryLostPosition': item['allianceMilitaryLostPosition'],
                'allianceMilitaryLostScore': item['allianceMilitaryLostScore'],
                'allianceMilitaryBuiltPosition': item['allianceMilitaryBuiltPosition'],
                'allianceMilitaryBuiltScore': item['allianceMilitaryBuiltScore'],
                'allianceMilitaryDestroyedPosition': item['allianceMilitaryDestroyedPosition'],
                'allianceMilitaryDestroyedScore': item['allianceMilitaryDestroyedScore'],
                'allianceMilitaryHonorPosition': item['allianceMilitaryHonorPosition'],
                'allianceMilitaryHonorScore': item['allianceMilitaryHonorScore'],
                'allianceLifeformHighLevelPosition': item['allianceLifeformHighLevelPosition'],
                'allianceLifeformHighLevelScore': item['allianceLifeformHighLevelScore'],
                'allianceLifeformEconomyPosition': item['allianceLifeformEconomyPosition'],
                'allianceLifeformEconomyScore': item['allianceLifeformEconomyScore'],
                'allianceLifeformTechnologyPosition': item['allianceLifeformTechnologyPosition'],
                'allianceLifeformTechnologyScore': item['allianceLifeformTechnologyScore'],
                'allianceLifeformDiscoveriesPosition': item['allianceLifeformDiscoveriesPosition'],
                'allianceLifeformDiscoveriesScore': item['allianceLifeformDiscoveriesScore']           
            }
            main_list.append(value)
            data = supabase.table(tableName).insert(main_list).execute()  

            #Keep track of progress because this upload takes a while
            print("Working on alliance " + str(count) + " out of " + str(numberOfalliances))
            count += 1

    def startFetching(self):
        # load from web to update existing xml file
        XMLsToParse = self.loadXML()
        # parse xml file
        items = self.parseXML(XMLsToParse)
        # store alliances items in a csv file
        self.writeToDatabase(items, 'output/s131AlliancesResults.csv')