# importing required modules
from bz2 import compress
from ctypes import sizeof
# creating a pdf file object
import io
import pdfplumber
import requests
import string
import time
import zlib
import sys
def getKeywordString(PDF_URL):
    r = requests.get(PDF_URL)
    f = io.BytesIO(r.content)
    all_text = ''
    with pdfplumber.open(f) as pdf:
        for pdf_page in pdf.pages:
            single_page_text = pdf_page.extract_text()
            #print( single_page_text )
            # separate each page's text with newline
            all_text = all_text + ' ' + single_page_text
        #print (all_text
        # initializing punctuations string
        punc = '''á• –”“’!()-[]{};:'"\,<>./?@#$%^&*_~`¡¢£¤¥¦§¨©ª«¬®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ'''
        
        
        # Removing punctuations in string
        # Using loop + punctuation string

        for ele in all_text:
            if ele in punc:
                all_text = all_text.replace(ele, "")
        
        # printing result
        all_text = all_text.replace("\n", "").lower()
        #print(all_text)
        #example.replace( /\n/g, " " )
        unique_words = set(all_text.split(' '))
        #print(unique_words)
        omittedWords = ['a', 'the', 'of', 'is', 'or', '']
        returnString = ''
        count = 0
        for word in unique_words:
            if word not in omittedWords:
                if count == 0:
                    returnString = returnString + word
                else:
                    returnString = returnString + '|' + word
                count = count + 1

        # print(returnString)
        print(f"Num words: {len(all_text)}")
        compressed = zlib.compress(returnString.encode())
        return returnString


if __name__ == '__main__':
    tic = time.perf_counter()
    # getKeywordString('https://www.austintexas.gov/edims/document.cfm?id=383785')
    
    # getKeywordString("https://www.austintexas.gov/edims/document.cfm?id=385572")
    getKeywordString("https://www.austintexas.gov/edims/document.cfm?id=383786")
    toc = time.perf_counter()
    print(f"Found keywords in {toc - tic:0.4f} seconds")
    





# reader = PyPDF2.PdfFileReader(f)

# contents = reader.getPage(0).extractText().split('\n')
# unique_words = set(contents.split(' '))

# print(contents)