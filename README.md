# Plato

A random musical verse generator written in Python

Scrapes [a wikipedia article on Platonism](https://en.wikipedia.org/wiki/Platonism), using the blockquotes as the source for the lyric generation. Phrases are unique and are chosen via Markov chains.

## Dependencies

All dependencies are available via PyPI:
* BeautifulSoup
* lxml
* numpy
* pandas
* requests

## Usage

    usage: plato.py [-h] [-n words] [url]

    random music verse generator originally formed from an excerpt of plato's metaphysics found on wikipedia

    author: djk272
    modified by fullsalvo

    positional arguments:
      url                   the url scraped to be used by the markov chain
                            generator.

    optional arguments:
      -h, --help            show this help message and exit
      -n words, --wordcount words
                            the number of words to form the chain from.
