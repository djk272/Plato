### Random musical verse generator using an excerpt from Plato's middle period metaphyics from wikipedia ###


### First, scrape wikipedia for the excerpt

### Second, use those words to randomly generate exsistential phrases for the verse of a song
##########################################################################################

###~~Web scraper in Python 3~~###
from bs4 import BeautifulSoup
import requests
import pandas as pd 

source = requests.get('https://en.wikipedia.org/wiki/Platonism').text #loads the website html in text form

soup = BeautifulSoup(source, 'lxml') #loads the lxml parser

blockquote = soup.find('blockquote') #parses through finding the "blockquote" item


glaucon = blockquote.contents[1].text[11:] #extracts the element of interest from a list of 3 elements, all elements being strings of text. Then removes the first 11 characters from the chosen string becasue they aren't needed.


glaucon = glaucon.replace("\"","").replace("?", "").replace(",", "").replace(".","").replace("-","") #removing unessecary special characters and quotation marks, because we only want words.

words = glaucon.split() #spliting the string of text into a list of individual words

print(words)
##########################################################################################

###~~Random Word Generator~~###