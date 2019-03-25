#!/usr/bin/env python3
"""
Random music verse generator formed from an excerpt of Plato's metaphysics, found on Wikipedia

Author: djk272
Modified by fullsalvo
"""

from bs4 import BeautifulSoup # Python3 Web Scraper
import requests
import numpy as np
import pandas as pd

class Scraper:
    """
    Grabs and processes data obtained from the web to be used with the Markov chain generator later.
    """
    def __init__(self, url, fmt='lxml'):
        source = requests.get(url).text        # downloads the webpage html as plaintext
        self.soup = BeautifulSoup(source, fmt) # loads the lxml parser
        # TODO: Make the scraping method and `fmt' depend on the domain name of the site in question
        if (url == 'https://en.wikipedia.org/wiki/Platonism'):
            self.words = self.plato()

    def plato(self):
        """
        Handles the test parser url.
        """
        # obtains the "blockquote" item
        blockquote = self.soup.find('blockquote')
        # extracts the element of interest from a list of 3 elements, all elements being strings of text. Then removes the first 11 characters from the chosen string becasue they aren't needed.
        glaucon = blockquote.contents[1].text[11:]
        # remove unnecessary special characters and quotation marks, because we only want words.
        glaucon = glaucon.replace("\"","").replace("?", "").replace(",", "").replace(".","").replace("-","")
        # split the string of text into a list of individual words
        words = glaucon.split()
        return words

class Markov:
    """
    Produces Markov chain lyrics from data obtained from the scraper.
    """
    def __init__(self, url, n_words=30, to_print=True):
        self.scraper = Scraper(url)
        self.n_words = n_words
        self.pairs = self.make_pairs(self.scraper.words)
        self.word_dict = self.form_dict()
        self.generated = self.generate()
        if to_print:
            print(self.generated)

    def make_pairs(self,words):
        """
        Form word pairs, so that predictions may later be made about what words are reasonable to follow.
        """
        for i in range(len(words)-1):
            yield (words[i], words[i+1])

    def form_dict(self):
        word_dict = {} # intialize dictionary with empty entries

        for word, next_word in self.pairs:
            if word in word_dict.keys():
                word_dict[word].append(next_word) # create a dictionary to store a list of all the intances a word appears directly after a particular word.
            else:
                word_dict[word] = [next_word] #if not then they must be the same word
        return word_dict

    def generate(self):
        # pick the first word of the generated chain, ensuring that the word chosen is also a word that starts a line in the source
        first_word = np.random.choice(self.scraper.words) # the first word is randomly chosen from the text
        while first_word.islower():
            first_word = np.random.choice(self.scraper.words)

        chain = [first_word]

        for i in range(self.n_words):
            chain.append(np.random.choice(self.word_dict[chain[-1]]))

        return ' '.join(chain) # joins the words in the list made in the generated chain of words in to a string, with all the words connected by a space

def main():
    plato = Markov('https://en.wikipedia.org/wiki/Platonism')
    # TODO: Interactively allow further generated chains to be created before completely exiting
    # (so data doesn't have to be re-downloaded multiple times for the same set)

if __name__ == '__main__':
    main()
