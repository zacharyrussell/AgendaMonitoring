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
        


def tryCreateTables():
    with conn.cursor() as cur:
        cur.execute("CREATE TABLE IF NOT EXISTS meetings(location varchar(8000), date varchar(8000), url varchar(8000), attatchments varchar(8000));")
        #res = cur.fetchall()
        conn.commit()
        #print(res)
        print("Successfully tried to create database!!")

def uploadMeeting(meeting):
    with conn.cursor() as cur:

        #cur.execute(f"INSERT INTO meetings VALUES ('Austin, TX',{meeting.date}, {meeting.url}, {meeting.attatchmentsToString()});")
        cur.execute("INSERT INTO meetings (location, date, url, attatchments) VALUES(%s,%s,%s,%s);", 
        ('Austin, TX', meeting.date, meeting.url, meeting.attatchmentsToString()))
        #cur.execute("INSERT INTO meetings (location, date, url, attatchments) VALUES('1','2','3','4');")
        conn.commit()
        #print(res)
        print("Successfully uploaded meeting to Database!")


