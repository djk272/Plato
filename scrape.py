### Random musical verse generator using an excerpt from Plato's middle period metaphysics from wikipedia ###


### First, scrape wikipedia for the excerpt

### Second, use those words to randomly generate exsistential phrases for the verse of a song
##########################################################################################

###~~Web scraper in Python 3~~###
from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd 
#################################

source = requests.get('https://en.wikipedia.org/wiki/Platonism').text #loads the website html in text form

soup = BeautifulSoup(source, 'lxml') #loads the lxml parser

blockquote = soup.find('blockquote') #parses through finding the "blockquote" item


glaucon = blockquote.contents[1].text[11:] #extracts the element of interest from a list of 3 elements, all elements being strings of text. Then removes the first 11 characters from the chosen string becasue they aren't needed.


glaucon = glaucon.replace("\"","").replace("?", "").replace(",", "").replace(".","").replace("-","") #removing unessecary special characters and quotation marks, because we only want words.

words = glaucon.split() #spliting the string of text into a list of individual words

#print(words)
##########################################################################################

###~~Markov Chain Random Word Generator~~###

## Building a function to make the words in the string into pairs of words, so we can predict which word should come after any given word ##

def make_pairs(words):

	for i in range(len(words)-1):
		yield (words[i], words[i+1]) # all of this in the function creates a list which pairs adjecent words together, excluding the first word of the previous pair, so you create unique pairs


pairs = make_pairs(words) # word pairs are now equal to the previous function

## building the dictionary ##

word_dict = {} # intialize dictionary with empty entries


for word, next_word in pairs:
	if word in word_dict.keys():
		word_dict[word].append(next_word) # create a dictionary to store a list of all the intances a word appears directly after a particular word.
	else:
		word_dict[word] = [next_word] #if not then they must be the same word

#print(word_dict["the"])# prints all of the words that come after the word "the" in the text


first_word = np.random.choice(words) # the first word is randomly chosen from the text

while first_word.islower():
	first_word = np.random.choice(words) # all this does is when the first word chosen from the text is lower case it will chose the first word randomly again until it isn't. This prevents a word being chosen mid sentence in the text that is probably awkward to use at the begining of a new sentence.

chain = [first_word] # we start the chain of words we want to generate with the first word randomly chosen

n_words = 30 # the number of words the chain will be in length

for i in range(n_words):
	chain.append(np.random.choice(word_dict[chain[-1]])) # add 30 random words from the dictonary, the next word is chosen based on the last element or word in the chain.

' '.join(chain) # joins the words in the list made in the generated chain of words in to a string, with all the words connected by a space

print(' '.join(chain)) # prints the output so you can read it