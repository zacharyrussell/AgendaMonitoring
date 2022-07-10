

class Meeting:
    def __init__(self, date, url, attatchments):
        self.date = date
        self.attatchments = attatchments
        self.url = url 
    
    def __str__(self):
        print(f"This meeting occured on {self.date} and has {len(self.attatchments)} documents linked")