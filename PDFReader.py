import requests


def downloadPdf(pdf):
    r = requests.get(pdf, stream= True)
    with open("agenda.pdf", "wb") as pdf:
        for chunk in r.iter_content(chunk_size=1024):
            '''
            writing one chunk at a time to pdf file
            '''
            if chunk:
                pdf.write(chunk)
                # print(chunk)
        pdf.close()


def parsePDF(link):
    pass 