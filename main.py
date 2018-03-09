# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 17:31:34 2018

@author: Gabe Freedman
"""

import lyrics
import vocab-scrape

artist = 'Radiohead'.lower()

disc = lyrics.get_unique_discography(artist)
disc = lyrics.clean_discography(disc)
