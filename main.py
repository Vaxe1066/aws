import requests
import json
from bs4 import BeautifulSoup
import string
import re

def countWords(words, parsedHTML):
    wordsLst = words.split(', ')
    parsedCleansed = re.sub(r'[^A-Za-z. ]+', '', parsedHTML)

    print(parsedCleansed)

def validUrl(url):
        #check whether the url is valid
    try:
        response = requests.get(url)
        return True
    except requests.ConnectionError as exception:
        return False

#test = validUrl("https://en.wikdia.org/wiki/Arsenal_F.C.") 

#if(test==True):
#    print(test)
#else:
    #output = json.loads(test)
#    print(type(test))




def getDataFromUrl(url, wordString):
    #wordString = 'ball, cup, football, beautiful'

    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    #print(soup.prettify())

    page = soup.get_text()


    # split into words by white space
    words = page.split()
    # remove punctuation from each word
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in words]
    # convert to lower case
    stripped = [word.lower() for word in stripped]
    #remove numbers
    stripped = [re.sub(r'[^A-Za-z ]+', '', word) for word in stripped]
    #print(stripped)

    wordsLst = wordString.split(', ')
    # convert to lower case
    wordsLst = [word.lower() for word in wordsLst]
    #print(wordsLst)


    outputDict = {key: 0 for key in wordsLst}
    for word in stripped:
        if word in wordsLst:
            curCount = outputDict[word]
            outputDict[word] = curCount + 1

    return outputDict