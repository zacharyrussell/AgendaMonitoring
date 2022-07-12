from datetime import date, timedelta

from Webscraper import createMeetingObject


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)



def findMeetingsForDateRange(startY, startM, endY, endM):
    start_date = date(startY, startM, 1)
    end_date = date(endY, endM, 2)
    for single_date in daterange(start_date, end_date):
        date = single_date.strftime("%Y%m%d")
        createMeetingObject(str(date))
        print(date)