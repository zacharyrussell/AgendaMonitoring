# coding=utf-8
# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import requests
# import pdfplumber
from bs4 import BeautifulSoup
from PDFReader import downloadPdf, parsePDF
from Meeting import Meeting 

# Finds all links to meetings on Austin website. Then appends requested date
# to URL, giving new web page that contains agendas 
def get_Paragraphs(url, date):
    year = date[0:4]
    baseURL = "https://www.austintexas.gov"
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")
    for link in soup.find_all('a', href=True):
        # Append urlExt to base url to navigate to meeting page
        urlExt = link.get('href')
        # only search city council links in specified year
        cityCouncilLink = f"/department/city-council/{year}/"
        if cityCouncilLink in str(link):
            if date in str(link):
                return baseURL + str(urlExt)


# Finds all attribute (a) sections of html and filters out those that contain
# href properties 
def findEntryData(address):
    agendas = []
    res = requests.get(address)
    soup = BeautifulSoup(res.content, "html.parser")
    for link in soup.find_all('a', href=True):
        if "Agenda" in str(link):
            #Austin website contains alot of redundant links flagged as "backup"
            if not "Backup" in str(link):
                agenda = link.get('href')
                agendas.append(agenda)
    return agendas


def createMeetingObject(date):
    year = date[0:4]
    url = get_Paragraphs(f"https://www.austintexas.gov/department/city-council/{year}/{year}_master_index.htm", str(date))

    if not url:
        print(f"No meeting found on {date}")
        return 
        
    agendas = findEntryData(url)
    meeting = Meeting(date, url, agendas)
    for agenda in meeting.attatchments:
        print(agenda)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    date = input("Enter date to find agenda")
    createMeetingObject(date)


