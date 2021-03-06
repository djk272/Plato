#!/usr/bin/env python3
"""
Random music verse generator originally formed from an excerpt of Plato's metaphysics found on Wikipedia

Author: djk272
Modified by fullsalvo
"""

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from bs4 import BeautifulSoup # Python3 Web Scraper
import numpy as np
import pandas as pd
import re
import requests

_lyric_section_headers = r'\[[^\]]*\]\n'
_remove_lyric_headers = lambda x: re.sub(_lyric_section_headers, '', x)
_remove_special_characters = lambda x: re.sub(r'[\\,\.\?()"]', '', x)

class Scraper:
    """
    Grabs and processes data obtained from the web to be used with the Markov chain generator later.
    """
    def __init__(self, url, album=False, fmt='lxml'):
        source = requests.get(url).text        # downloads the webpage html as plaintext
        self.soup = BeautifulSoup(source, fmt) # loads the lxml parser
        # TODO: Make the scraping method and `fmt' depend on the domain name of the site in question
        if (url == 'https://en.wikipedia.org/wiki/Platonism'):
            self.words = self.plato()
        if (url.startswith('https://genius.com/')):
            if album:
                self.album()
            else:
                self.words = self.genius()

    def plato(self):
        """
        Handles the test parser url.
        """
        # obtains the "blockquote" item
        blockquote = self.soup.find('blockquote')
        # extracts the element of interest from a list of 3 elements, all elements being strings of text. Then removes the first 11 characters from the chosen string becasue they aren't needed.
        glaucon = blockquote.contents[1].text[11:]
        # remove unnecessary special characters and quotation marks, because we only want words.
        glaucon = _remove_special_characters(glaucon)
        # split the string of text into a list of individual words
        words = glaucon.split()
        return words

    def genius(self,url=None):
        if url:
            source = requests.get(url).text
            soup = BeautifulSoup(source, 'lxml')
            lyrics = _remove_lyric_headers(soup.p.get_text())
            lyrics = _remove_special_characters(lyrics)
            words = lyrics.split()
            return words
        else:
            lyrics = _remove_lyric_headers(self.soup.p.get_text())
            lyrics = _remove_special_characters(lyrics)
            words = lyrics.split()
            return words

    def album(self):
        tracklist = self.soup.find('div', {'class': 'track_listing'})
        lyrics = self.genius()
        setattr(self,'words',lyrics)
        for a in tracklist.find_all('a'):
            self.words.extend(self.genius(a['href']))

class Markov:
    """
    Produces Markov chain lyrics from data obtained from the scraper.
    """
    def __init__(self, url, n_words=30, album=False, to_print=True):
        self.scraper = Scraper(url,album)
        self.n_words = n_words
        pairs = self.make_pairs(self.scraper.words)
        self.word_dict = self.form_dict(pairs)
        self.generated = self.generate()
        if to_print:
            print(self.generated)

    def make_pairs(self,words):
        """
        Form word pairs, so that predictions may later be made about what words are reasonable to follow.
        """
        for i in range(len(words)-1):
            yield (words[i], words[i+1])

    def form_dict(self, pairs):
        word_dict = {} # intialize dictionary with empty entries

        for word, next_word in pairs:
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

def _parse_args():
    parser = ArgumentParser(
        description=__doc__,
        formatter_class=RawDescriptionHelpFormatter
    )
    parser.add_argument('-n','--wordcount',
                        help="""
                        The number of words to form the chain from.
                        """,
                        dest='words',
                        type=int,
                        default=30)
    parser.add_argument('url',
                        nargs='?',
                        help="""
                        The url scraped to be used by the Markov chain generator.
                        """,
                        type=str,
                        default="https://en.wikipedia.org/wiki/Platonism")
    parser.add_argument('-a','--album',
                        help="""
                        Rather than only grabbing a song's lyrics, grab the entire album.
                        """,
                        dest='album',
                        action='store_true',
                        default=False)
    return parser.parse_args()

def main():
    _args = _parse_args()
    plato = Markov(_args.url,n_words=_args.words,album=_args.album)
    # TODO: Interactively allow further generated chains to be created before completely exiting
    # (so data doesn't have to be re-downloaded multiple times for the same set)

if __name__ == '__main__':
    main()
