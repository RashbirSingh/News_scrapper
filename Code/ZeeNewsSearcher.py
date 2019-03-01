#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 13:23:32 2019

@author: ubuntu
"""
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import re
import json

ReapiredLinksList = []
TopicsList = []

def CallZeeNews(Keyword):
    ReapiredLinksList = []
    TopicsList = []
    url = 'https://zeenews.india.com/tags/'+str(Keyword)+'.html'
    webpage = urlopen(url)

    
    page_soup = soup(webpage, features="lxml")
    
    Links = page_soup.find_all('div', {'class': 'sec-con-box'})
    Links = soup(str(Links), features="lxml")
    Links = Links('h3', {'class': 'margin-bt10px'})
    Links = soup(str(Links), features="lxml")
    Links = Links('a')
    Links = re.sub('<a href="', '', str(Links))
    Links = re.sub('[[, ]', '', str(Links))
    Links = re.sub('[]]', '', str(Links))
    Links = re.sub(r'">', '', str(Links))
    LinksList = re.split('</a>', str(Links))

    for iterator in range(0, len(LinksList)):
        if iterator%2 == 0:
            ReapiredLinksList.append('https://zeenews.india.com'+LinksList[iterator])

    ReapiredLinksList.pop()       

    #with open('ZeeNewsJSONFile.json', 'w') as f:  
        #json.dump(ReapiredLinksList, f, indent=4)
        
    for TopicIterator in range(0, len(ReapiredLinksList)):
        Nameurl = re.sub('[/]', ' ', ReapiredLinksList[TopicIterator])
        Nameurl = re.sub('https: | zeenews.india.com', '', Nameurl)
        Nameurl = re.sub('-11-', ' eleven ', Nameurl)
        Nameurl = re.sub('-26-', ' twenty six ', Nameurl)
        Nameurl = re.sub('-4-', ' four ', Nameurl)
        Nameurl = re.sub('.html', '', Nameurl)
        Nameurl = re.sub(' bihar |  news |  cricket | news  bihar| cricket | bihar |', '', Nameurl)
        Nameurl = re.sub(r'-', ' ', Nameurl)
        Nameurl = re.sub(r'_', '', Nameurl)
        Nameurl = re.sub('[0-9]', '', Nameurl)
        TopicsList.append(
                {'title': Nameurl,
                 'name': 'Zee News',
                 'url': ReapiredLinksList[TopicIterator]
                 }
                )
    
    return TopicsList