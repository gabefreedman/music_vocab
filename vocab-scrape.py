# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 21:40:41 2018

@author: Gabe Freedman
"""

import requests
from bs4 import BeautifulSoup


def get_vocab():
    
    BASE_URL = 'https://satvocabulary.us/'
    
    page = requests.get(BASE_URL)
    if page.status_code == 200:
        soup = BeautifulSoup(page.text, 'html.parser')
        
        vocab_tag_list = soup.find_all('b')
        vocab_list = []
        
        for word in vocab_tag_list:
            vocab_list.append(word.contents[0])
        
        return vocab_list
    else:
        return 'Error Code:' + str(page.status_code)


def clean_vocab(words):
    
    cleaned_words = []
    
    for word in words:
        if word.isalpha():
            cleaned_words.append(word)
        elif '(' in word and ' (' not in word:
            cleaned_words.append(word.partition('(')[0])
        elif ' (' in word:
            cleaned_words.append(word.partition(' (')[0])
        elif ', ' in word:
            cleaned_words.append(word.partition(', ')[0])
            cleaned_words.append(word.partition(', ')[2])
    return cleaned_words

