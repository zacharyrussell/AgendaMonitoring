# coding=utf-8
# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from cgi import test
import dryscrape
from bs4 import BeautifulSoup
import threading
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv
from requests.exceptions import ConnectionError
from datetime import date, timedelta
from distutils.command.upload import upload
import requests
import concurrent.futures
# import pdfplumber
from bs4 import BeautifulSoup
from Attatchment import Attatchment
from Meeting import Meeting 
from CSVWriter import addToCSV


skipUrls = []
# Finds all links to meetings on Austin website. Then appends requested date
# to URL, giving new web page that contains agendas 
def getMeetingFromMaster(url, date, meetingArray):
    
    driver = webdriver.Chrome('./chromedriver') 
    driver.get(url) 
    time.sleep(5) 
    html = driver.page_source
    print (html)
    # res = driver.page_source
    # baseURL = "https://www.arlingtontx.gov/cms/one.aspx?objectId=15052707"
    # soup = BeautifulSoup(res, "lxml")
    # #soup.find(id="intro-text")
    # #print(soup.contents)
    # year = date[0:4]
    # print(res)
    if "Evening" in html:
        print("AAAAAAAAAYEAH")
    else:
        print("No")
    # for link in soup.find_all('table'):
        # print(str(link))
        # return
        # Append urlExt to base url to navigate to meeting page
        # urlExt = link.get('href')
        # only search city council links in specified year
        # cityCouncilLink = f"/department/city-council/{year}/"
        # if cityCouncilLink in str(link):
        #     if date in str(link) and str(link) not in skipUrls:
        #         skipUrls.append(str(link))
        #         createMeetingObject(date, meetingArray)
        #         return baseURL + str(urlExt)


# Finds all attribute (a) sections of html and filters out those that contain
# href properties 
def collectAttatchments(address):
    agendas = []
    videos = []
    transcripts = []
    dupCheck = []
    res = requests.get(address)
    soup = BeautifulSoup(res.content, "html.parser")
    titleText = soup.find("title").string
    titleText = titleText.replace("| AustinTexas.gov", "")
    for link in soup.find_all('a', href=True):
        if "Agenda" in str(link):
            #Austin website contains alot of redundant links flagged as "backup"
            if not "Backup" in str(link):
                agenda = link.get('href')
                title = link.string
                attatchment = Attatchment(title, agenda)
                if agenda not in dupCheck:
                    dupCheck.append(agenda)
                    agendas.append(attatchment)
        elif "Transcript" in str(link):
            transcript = link.get('href')
            title = "Transcript"
            attatchment = Attatchment(title, transcript)
            if transcript not in dupCheck:
                dupCheck.append(transcript)
                transcripts.append(attatchment)
        elif "swagit" in str(link):
            video = link.get('href')
            title = "Video"
            attatchment = Attatchment(title, video)
            if video not in dupCheck:
                dupCheck.append(video)
                videos.append(attatchment)

    return titleText, agendas, videos, transcripts

def createMeetingObject(date, meetingArray):
    year = date[0:4]
    url = getMeetingFromMaster(f"https://www.arlingtontx.gov/cms/one.aspx?objectId=15052707", str(date), meetingArray)
    if not url:
        #zprint(f"No meeting found on {date}")
        return 
    (titleText, agendas, videos, transcripts) = collectAttatchments(url)
    meeting = Meeting("Austin", titleText, date, url, agendas, videos, transcripts)
    # for agenda in meeting.attatchments:
    #     print(agenda)
    print(f"Successfuly created meeting object for date {date}!")
    # meeting.printMeeting()
    addMeetingToMeetingArray(meeting, meetingArray)
    return meeting

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

def mThread_findMeetingsForDateRange(startY, startM, endY, endM):
    start_date = date(startY, startM, 1)
    end_date = date(endY, endM, 2)
    meetingArray = []
    futures = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(createMeetingObject, str(single_date.strftime("%Y%m%d")), meetingArray) 
        for single_date in daterange(start_date, end_date)]
    addToCSV(meetingArray)
    print("Successfully added all meetings to CSV!")
    print(f"There were {len(meetingArray)} agendas since {startM}-{startY}!")

def addMeetingToMeetingArray(meeting, meetingArray):
    if meeting: 
        for attatchment in meeting.attatchments:
            csvEntry = [meeting.date, meeting.location, meeting.title, attatchment.title, attatchment.url]
            meetingArray.append(csvEntry)
        for transcript in meeting.transcripts:
            video = meeting.videos[0]
            csvEntry = [meeting.date, meeting.location, meeting.title, transcript.title, attatchment.url, video.title, video.url]
            meetingArray.append(csvEntry)

def addToCSV(meetings):
    with open('./csvTest', 'w') as f:
        # create the csv writer
        writer = csv.writer(f)
        # write a row to the csv file
        writer.writerows(meetings)

    
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    date = input("Enter date to find agenda")
    #findMeetingsForDateRange(2022, 1, 2022, 7)
    meetingArray = []
    createMeetingObject(date, meetingArray)
    #mThread_findMeetingsForDateRange(2021, 1, 2022, 7)
