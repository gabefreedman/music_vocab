# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 18:40:10 2018

@author: Gabe Freedman
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

def get_unique_discography():
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
        time.sleep(1)
        
        BASE_URL = 'http://www.metrolyrics.com/radiohead-albums-list-' + str(page_num) + '.html'
        page = requests.get(BASE_URL)
        soup = BeautifulSoup(page.text, 'html.parser')
        song_list = []
        heading_tags = []
        albums = []

    return df

def clean_discography(df):
    
    df = df.dropna()

    df['Track'] = df['Track'].str.lower()

    df['Track'] = df['Track'].apply(lambda x: re.sub(r'[^a-zA-Z0-9\s\']',' ', str(x)))

    df['Track'] = df['Track'].apply(lambda x: re.sub(' +', '-', str(x)))
    
    df['Track'] = df['Track'].str.replace("\'", '')

    df['Track'] = df['Track'].apply(lambda x: x.rstrip('-'))

    df = df[~(df['Track'].str.endswith(('-remix', '-rework', '-rmx', '-live', '-version')))]

    df = df.drop_duplicates(subset=['Track'], keep='last')
    
    df = df.dropna()
    
    return df


def get_lyrics(track):
    
    BASE_URL = 'http://www.metrolyrics.com/' + track + '-lyrics-radiohead.html'
    
    page = requests.get(BASE_URL)
    time.sleep(1)
    if page.history:
        return [resp.status_code for resp in page.history]
    else:
        soup = BeautifulSoup(page.text, 'html.parser')
    
        raw_lyric = []
        for tag in soup.find_all('p', class_='verse'):
            raw_lyric.append(tag.text)
        
        raw_lyric = ' '.join(raw_lyric).split()
        return raw_lyric
    
def clean_lyrics(df):
    
    df = df[df['Lyrics'].map(len) > 1]

def get_status_code(track):
    
    BASE_URL = r'http://www.metrolyrics.com/' + track + '-lyrics-radiohead.html'
    
    page = requests.get(BASE_URL)
    if page.history:
        return [resp.status_code for resp in page.history]
    else:
        return page.status_code

    

#df = get_unique_discography()
#df = clean_discography(df)
#df['Lyrics'] = [get_lyrics(row.Track) for row in df.itertuples()]
#print('done')
#df.to_csv(r'C:\Users\Gabe Freedman\Desktop\Projects\music_vocab\test.csv', index=False)
