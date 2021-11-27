import requests
from bs4 import BeautifulSoup
import string
import re


def validUrl(url):
        #check whether the url is valid
    try:
        response = requests.get(url)
        return True
    except requests.ConnectionError as exception:
        return False



def getDataFromUrl(url, wordString):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')

    page = soup.get_text()
    # split into words by white space
    words = page.split()
    # remove punctuation from each word
    mapping = str.maketrans('', '', string.punctuation) #create mapping of punc to be removed
    stripped = [w.translate(mapping) for w in words]
    # convert to lower case
    stripped = [word.lower() for word in stripped]
    #remove numbers
    stripped = [re.sub(r'[^A-Za-z ]+', '', word) for word in stripped] #using regex keep only alphabet chars

    wordsLst = wordString.split(', ')
    # convert to lower case
    wordsLst = [word.lower() for word in wordsLst]


    outputDict = {key: 0 for key in wordsLst} #initialise the dictionary with keys from list of words
    for word in stripped:
        if word in wordsLst:
            curCount = outputDict[word]
            outputDict[word] = curCount + 1 #incremenet the count each time word is found

    return outputDict