# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 17:31:34 2018

@author: Gabe Freedman
"""

import lyrics
import vocab-scrape

def main():
    artist = 'Radiohead'.lower()

    disc = lyrics.get_unique_discography(artist)
    disc = lyrics.clean_discography(disc)

if __name__ == '__main__':
    main()
