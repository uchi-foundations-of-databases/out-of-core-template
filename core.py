'''
The core module sets up the data structures and 
and references for this programming assignment.
'''

import platform
import os
import json

def imdb_title_words():
    f = open('title.csv','r', errors='replace')
    line = f.readline()

    while line != "":
        words = line.strip().split(',')[1].split()

        for w in words:
            yield w

        line = f.readline()

    f.close()

def imdb_years():
    f = open('title.csv','r', errors='replace')
    line = f.readline()

    while line != "":
        csvsplit = line.strip().split(',')
        year = csvsplit[len(csvsplit) - 8]
        
        if year.strip() != "":
            yield year

        line = f.readline() 
    f.close()

  





