# -*- coding: utf-8 -*-
"""
Created on Sun Jul 27 14:35:53 2014

@author: blancosilva
"""

from urllib2 import urlopen
from json import loads

def no_repeats(word):
    new_word = ""
    for letter in word:
        if letter not in new_word:
            new_word += letter
    return new_word == word

file = open("words.txt", 'r')
words = file.read().split("\n")
file.close()
words = filter(lambda x: len(x)>0, words)
words = filter(no_repeats, words)

file = open("bing.txt")
bing = loads(file.read())
file.close()

for word in words:
    if word not in bing.keys():
        print word
        search_string = "http://www.bing.com/search?q=site:en.wikipedia.org+"+word
        print search_string
        file = urlopen(search_string)
        source = file.read()
        file.close()
        source = source.split('<span class="sb_count">')
        source = source[1]
        print source[:30]
        score = int(source[:source.index(" results</span>")].strip().replace(",",""))
        print score
        bing[word]= score

