# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 17:31:34 2018

@author: Gabe Freedman
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


BASE_URL = 'http://www.metrolyrics.com/radiohead-albums-list.html'
page = requests.get(BASE_URL)
soup = BeautifulSoup(page.text, 'html.parser')

num_pages = soup.find('span', class_='pages').get_text().replace('\n', 
                     '').replace('\t', '')[-1]


song_list = []
heading_tags = []
albums = []
page_num = 1
df = pd.DataFrame(columns=['Artist', 'Album', 'Track'])

while page_num <= int(num_pages):
    for tag in soup.find_all('div', class_='content song-list compact clearfix'):
        for link in tag.find_all_next('div', class_='metacritic'):
            link.decompose()
        header = tag.find_previous_sibling('header')
        heading_tags.append(header)
    
    for tag in heading_tags:
        song_table = tag.find_next_sibling('div', class_='content song-list compact clearfix')
        song_list.append(song_table.text.replace('\n', '').replace(
                 'Lyrics', 'Lyrics '))
    
    for header in heading_tags:
        album = header.find('span')
        albums.append(album.text)
    
    
    for i in range(len(albums)):
        albums[i] = albums[i].strip()
        for song in song_list[i].split(' Lyrics '):
            song = song.strip()
            df = df.append({'Artist':'Radiohead', 'Album':albums[i], 'Track':song}, 
                            ignore_index=True)
    
    page_num += 1
    time.sleep(2)
    
    BASE_URL = 'http://www.metrolyrics.com/radiohead-albums-list-' + str(page_num) + '.html'
    page = requests.get(BASE_URL)
    soup = BeautifulSoup(page.text, 'html.parser')
    song_list = []
    heading_tags = []
    albums = []

df.to_csv('test.csv', index=False)