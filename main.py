# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 17:31:34 2018

@author: Gabe Freedman
"""

import lyrics
import vocab_scrape

def main():
    artist = 'Radiohead'.lower()

    disc = lyrics.get_unique_discography()
    disc = lyrics.clean_discography(disc)
    disc['Lyrics'] = [lyrics.get_lyrics(row.Track) for row in disc.itertuples()]
    print('done')
    disc.to_csv(r'C:\Users\Gabe Freedman\Desktop\Projects\music_vocab\test.csv', index=False)


if __name__ == '__main__':
    main()
