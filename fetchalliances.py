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

    def parseXML(self, xmlfile):
        tree = ET.parse(xmlfile)
        root = tree.getroot()
        # create empty list for alliance items
        allianceItems = []

        #Get current application run time
        applicationRunTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        for child in root:
            allianceDirectory = {}

            #get each attribute from alliance XML
            allianceDirectory['allianceID'] = child.attrib['id']
            allianceDirectory['allianceName'] = child.attrib['name']
            allianceDirectory['allianceTag'] = child.attrib['tag']
            allianceDirectory['founderID'] = child.attrib['founder']
            allianceDirectory['foundDate'] = child.attrib['foundDate']
            if 'open' in child.attrib:
                allianceDirectory['allianceOpen'] = child.attrib['open']
            else:
                allianceDirectory['allianceOpen'] = ''
            allianceDirectory['fetchDate'] = applicationRunTime

            # append alliances dictionary to alliances items list
            allianceItems.append(allianceDirectory)
        return allianceItems

    def writeToDatabase(self, allianceItems, filename):
        fields = ['allianceID', 'allianceName', 'allianceTag', 'founderID', 'foundDate', 'allianceOpen', 'fetchDate']
    
        # writing to csv file
        with open(filename, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = fields)
            writer.writeheader()
            writer.writerows(allianceItems)

        #Write out data to Supabase
        numberOfAlliances = len(allianceItems)
        count = 1
        for item in allianceItems:
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
                'fetchDate': item['fetchDate']
            }
            main_list.append(value)
            data = supabase.table(tableName).insert(main_list).execute()  

            #Keep track of progress because this upload takes a while
            print("Working on alliance " + str(count) + " out of " + str(numberOfAlliances))
            count += 1

    def startFetching(self):
        # load from web to update existing xml file
        self.loadXML()
        # parse xml file
        items = self.parseXML('output/s181Alliances.xml')
        # store alliances items in a csv file
        self.writeToDatabase(items, 'output/s131AllianceResults.csv')