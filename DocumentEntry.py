class DocumentEntry:
    def __init__(self, date, location, meeting, doctitle, pdf, vidlink, wholeText, keywords):
        self.date = date
        self.location = location
        self.meeting = meeting
        self.doctitle = doctitle 
        self.vidlink = vidlink
        self.pdf = pdf
        self.wholeText = wholeText
        self.keywords = keywords


    def getHash(self):
        tupleVal = (self.date, self.location, self.meeting, self.doctitle, self.vidlink, self.pdf)
        return (str(hash(tupleVal)))

