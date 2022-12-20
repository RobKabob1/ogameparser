#Python code to illustrate parsing of XML files
# importing the required modules
import csv
import requests
import xml.etree.ElementTree as ET

def loadRSS():

    # url of rss feed
    url = 'https://s181-us.ogame.gameforge.com/api/players.xml'
    # creating HTTP response object from given url
    resp = requests.get(url)
    # saving the xml file
    with open('s181Players.xml', 'wb') as f:
        f.write(resp.content)

def parseXML(xmlfile):
    # create element tree object
    tree = ET.parse(xmlfile)
    # get root element
    root = tree.getroot()
    # create empty list for news items
    playersItems = []

    
    for child in root:
        # empty players dictionary
        playersDirectory = {}

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

        # append news dictionary to news items list
        playersItems.append(playersDirectory)
    # return news items list
    return playersItems

def savetoCSV(playersItems, filename):
    # specifying the fields for csv file
    fields = ['playerID', 'playerName', 'playerStatus', 'playerAlliance']
    # writing to csv file
    with open(filename, 'w') as csvfile:
        # creating a csv dict writer object
        writer = csv.DictWriter(csvfile, fieldnames = fields)
        # writing headers (field names)
        writer.writeheader()
        # writing data rows
        writer.writerows(playersItems)

def main():
    # load rss from web to update existing xml file
    loadRSS()
    # parse xml file
    items = parseXML('s181Players.xml')
    # store news items in a csv file
    savetoCSV(items, 's131PlayersResults.csv')

if __name__ == "__main__":
    # calling main function
    main()