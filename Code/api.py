#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 13:04:49 2019

@author: ubuntu
"""

from newsapi import NewsApiClient
import json
# Init
newsapi = NewsApiClient(api_key='1ed8aaa997a44e97b014450d99ed1edb')
TopicsList = []
TitleNumber = []


def callAPI(Keyword):
    global TitleNumber
    TitleNumber = []
    global TopicsList
    TopicsList = []
    for i in range(1, 11):
        print("On NewsAPI's Page --> ", i)
        TitleNumber.append(newsapi.get_everything(q = Keyword,
                                                  sources='the-hindu,the-times-of-india,google-news-in',
                                                  sort_by='relevancy',
                                                  language='en',
                                                  page = int(i)))
        if TitleNumber[0]['totalResults'] <= 20:
            break

    for Itertaor in range(0, len(TitleNumber)):
        for URLIterator in range(len(TitleNumber[Itertaor]['articles'])):
            #print('+++', TitleNumber[Itertaor]['articles'][URLIterator]['source']['name'])
            #print('>>> ', TitleNumber[Itertaor]['articles'][URLIterator]['url'])
            #print('')
            TopicsList.append({
                    'name': TitleNumber[Itertaor]['articles'][URLIterator]['source']['name'],
                    'author' : TitleNumber[Itertaor]['articles'][URLIterator]['author'],
                    'title': TitleNumber[Itertaor]['articles'][URLIterator]['title'],
                    'description': TitleNumber[Itertaor]['articles'][URLIterator]['description'],
                    'url': TitleNumber[Itertaor]['articles'][URLIterator]['url'],
                    'urlToImage': TitleNumber[Itertaor]['articles'][URLIterator]['urlToImage'],
                    'publishedAt': TitleNumber[Itertaor]['articles'][URLIterator]['publishedAt'],
                    'content': TitleNumber[Itertaor]['articles'][URLIterator]['content']
                    })
            
    with open('NewsAPIJSONFile.json', 'w') as f:  
        json.dump(TitleNumber, f, indent=4)
        
    return TopicsList