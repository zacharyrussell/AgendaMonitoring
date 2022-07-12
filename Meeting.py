

class Meeting:
    def __init__(self, location, title, date, url, attatchments, videos, transcripts):
        self.location = location
        self.title = title
        self.date = date
        self.attatchments = attatchments
        self.url = url 
        self.videos = videos
        self.transcripts = transcripts
    

    def attatchmentsToString(self):
        attatchmentsString = ""
        numOfAttatchments = len(self.attatchments)
        for i in range(numOfAttatchments -1):
            attatchmentsString = attatchmentsString + self.attatchments[i] + " | "
        attatchmentsString = attatchmentsString + self.attatchments[numOfAttatchments - 1]
        return attatchmentsString

    def printMeeting(self):
        print(f"Title: {self.title}")
        print(f"Date: {self.date}")
        print(f"URL: {self.url}")
        print("Agendas:")
        for agenda in self.attatchments:
            print(agenda.title)
            print(agenda.url)
        print("Videos:")
        for video in self.videos:
            print(video.title)
            print(video.url)
        print("Transcripts:")
        for transcript in self.transcripts:
            print(transcript.title)
            print(transcript.url)
