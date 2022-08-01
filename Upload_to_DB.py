import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(os.environ["DATABASE_URL"])


def deleteTable():
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
    with conn.cursor() as cur:
        #cur.execute(f"INSERT INTO meetings VALUES ('Austin, TX',{meeting.date}, {meeting.url}, {meeting.attatchmentsToString()});")
        cur.execute("INSERT INTO meetings (date, location, meeting, doctitle, pdf, link, keywords) VALUES(%s,%s,%s,%s,%s,%s,%s);", 
        (documentEntry.date, documentEntry.location, documentEntry.doctitle, documentEntry.pdf, documentEntry.link, documentEntry.keywords))
        #cur.execute("INSERT INTO meetings (location, date, url, attatchments) VALUES('1','2','3','4');")
        conn.commit()
        #print(res)
        print("Successfully uploaded meeting to Database!")


