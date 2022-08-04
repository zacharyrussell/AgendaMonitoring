from distutils.command.upload import upload
import os
import psycopg2
from dotenv import load_dotenv
import sys
from DocumentEntry import DocumentEntry
from keywords import getKeywordString
from keytest import testLength

load_dotenv()
import requests

def setupDB():
    print("Starting request")
    url = "https://agenda-1-agendas.harperdbcloud.com"

    payload = "{\n    \"operation\": \"create_schema\",\n    \"schema\": \"dev\"\n}"
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic emFjaDpwaG9iaWNoaXBwbzQzMQ=='
    }

    response = requests.request("POST", url, headers=headers, data = payload)

    print(response.text.encode('utf8'))
    print("Created Schema")

    payload = "{\n    \"operation\": \"sql\",\n    \"sql\": \"SELECT * FROM dev.dog WHERE id = 1\"\n}"


    payload = "{\n    \"operation\": \"create_table\",\n    \"schema\": \"dev\",\n    \"table\": \"agendas\",\n    \"hash_attribute\": \"id\"\n}"
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic emFjaDpwaG9iaWNoaXBwbzQzMQ=='
    }

    response = requests.request("POST", url, headers=headers, data = payload)

    print(response.text.encode('utf8'))
    print("Created Table")




    def createAttribute(att):
        payload = (f"{{\n    \"operation\": \"create_attribute\",\n    \"schema\": \"dev\",\n    \"table\": \"agendas\",\n    \"attribute\": \"{att}\"\n}}")
        response = requests.request("POST", url, headers=headers, data = payload)
        print(response.text.encode('utf8'))
        print(f"Created attribute {att}")
        return response

    # Date,Location,Meeting,DocTitle,PDF,Link,Keywords
    createAttribute("date")
    createAttribute("location")
    createAttribute("meeting")
    createAttribute("doctitle")
    createAttribute("pdf")
    createAttribute("link")
    createAttribute("keywords")


# https://www.austintexas.gov/edims/document.cfm?id=384455 <-- small doc

# testDoc = DocumentEntry("20220609", "Austin,Texas",
#  "Energy Austin", "Transcript",
#   "https://www.austintexas.gov/edims/document.cfm?id=384184",
#    "https://www.austintexas.gov/edims/document.cfm?id=384184",
#     getKeywordString("https://www.austintexas.gov/edims/document.cfm?id=384184"))



def createAttribute(att):
    url = "https://agenda-1-agendas.harperdbcloud.com"
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic emFjaDpwaG9iaWNoaXBwbzQzMQ=='
    }
    payload = (f"{{\n    \"operation\": \"drop_attribute\",\n    \"schema\": \"dev\",\n    \"table\": \"wholeText\",\n    \"attribute\": \"{att}\"\n}}")
    response = requests.request("POST", url, headers=headers, data = payload)
    print(response.text.encode('utf8'))
    print(f"Created attribute {att}")
    return response

def uploadDocument(documentEntry):
    hash = documentEntry.getHash()
    url = "https://agenda-1-agendas.harperdbcloud.com"
    payload = f"{{\n    \"operation\": \"upsert\",\n    \"schema\": \"dev\",\n    \"table\": \"agendas\",\n    \"records\": [\n        {{\n                      \"date\": \"{documentEntry.date}\",\n            \"doctitle\": \"{documentEntry.doctitle}\",\n            \"keywords\": \"{documentEntry.keywords}\",\n  \"link\": \"{documentEntry.vidlink}\" ,\n \"location\": \"{documentEntry.location}\",\n  \"meeting\": \"{documentEntry.meeting}\",\n \"pdf\": \"{documentEntry.pdf}\",\n \"wholeText\": \"{hash}\"   }}\n    ]\n}}"
    # payload = (f"{{\n    \"operation\": \"sql\",\n    \"sql\": \"INSERT INTO dev.agendas (date, location, meeting, doctitle, pdf, link, keywords) VALUE ('{documentEntry.date}', '{documentEntry.location}', '{documentEntry.meeting}', '{documentEntry.doctitle}', '{documentEntry.pdf}', '{documentEntry.vidlink}', '{documentEntry.keywords}')\"\n}}")
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic emFjaDpwaG9iaWNoaXBwbzQzMQ=='
    }
    # print(payload[178:190])
    response = requests.request("POST", url, headers=headers, data = payload)
    print(f"Agenda: {response.text.encode('utf8')}")

    payload = f"{{\n    \"operation\": \"upsert\",\n    \"schema\": \"dev\",\n    \"table\": \"wholeText\",\n    \"records\": [\n        {{\n                      \"id\": \"{hash}\",\n            \"wholeText\": \"{documentEntry.wholeText}\"   }}\n    ]\n}}"
    response = requests.request("POST", url, headers=headers, data = payload)
    print(f"Text: {response.text.encode('utf8')}")

# uploadDocument(testDoc)


# conn = psycopg2.connect(os.environ["DATABASE_URL"], connect_timeout=60)

# with conn.cursor() as cur:
#     cur.execute("SELECT now()")
#     res = cur.fetchall()
#     conn.commit()
#     print(res)
# print("done")

def deleteTable():
    print("deleting table")
    with conn.cursor() as cur:
        cur.execute("DROP TABLE meetings;")
        #res = cur.fetchall()
        conn.commit()
        #print(res)
        print("Successfully deleted database!!")

def testEntryCreation():
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM meetings")
        res = cur.fetchall()
        conn.commit()
        print(res)
        

# Date,Location,Meeting,DocTitle,PDF,Link,Keywords
def tryCreateTables():
    with conn.cursor() as cur:
        cur.execute("CREATE TABLE IF NOT EXISTS meetings(date DATE, location varchar(50), meeting varchar(50), doctitle varchar(50), pdf varchar(800), link varchar(800), keywords varchar(max));")
        #res = cur.fetchall()
        conn.commit()
        #print(res)
        print("Successfully tried to create database!!")

def uploadMeeting(documentEntry):
    print("Attempting upload")
    with conn.cursor() as cur:
        #cur.execute(f"INSERT INTO meetings VALUES ('Austin, TX',{meeting.date}, {meeting.url}, {meeting.attatchmentsToString()});")
        cur.execute("INSERT INTO meetings (date, location, meeting, doctitle, pdf, link, keywords) VALUES(%s,%s,%s,%s,%s,%s,%s);", 
        (documentEntry.date, documentEntry.location, documentEntry.doctitle, documentEntry.pdf, documentEntry.link, documentEntry.keywords))
        #cur.execute("INSERT INTO meetings (location, date, url, attatchments) VALUES('1','2','3','4');")
        conn.commit()
        #print(res)
        print("Successfully uploaded meeting to Database!")


