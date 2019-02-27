#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 16:32:56 2019

@author: ubuntu
"""
# =============================================================================
# 
# =============================================================================

import sys
sys.path.insert(0, '/home/ubuntu/Desktop/News_Output_Test/Code')
import api
import ZeeNewsSearcher

# =============================================================================
# 
# =============================================================================

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen, Request
import re
import time
from selenium import webdriver
import json
import random
from fake_useragent import UserAgent

geckodriver = '/home/ubuntu/Desktop/News_Output_Test/geckodriver/geckodriver'
count = 1
Total = 0

# =============================================================================
# 
# =============================================================================

def Scrapper(url, 
             name, 
             title = '', 
             total = 0, 
             author = 'NA', 
             urlToImage = 'NA',
             publishedAt = 'NA',
             userAgent = UserAgent()):

    webpage = ''
    print(name)
    OutputZeeNews=[]
    OutputTimesOfIndia=[]
    global count

    user_agent_list = [
            userAgent.msie,
            userAgent.chrome,
            userAgent.google,
            userAgent.firefox,
            userAgent.ff,
            userAgent.safari,
            userAgent.random
            ]
    
    user_agent = random.choice(user_agent_list)
    

    if name == 'The Hindu':
        driver = webdriver.Firefox(executable_path = geckodriver)
        driver.get(url)
        webpage = driver.page_source

    elif name == 'Zee News':
        print(user_agent)
        req = Request(
                url, 
                data=None, 
                headers={
                        'User-Agent': user_agent
                        })
        webpage = urlopen(req).read()

    elif name == 'The Times of India':
        print(user_agent)
        req = Request(
                url, 
                data=None, 
                headers={
                        'User-Agent': user_agent
                        })
        webpage = urlopen(req).read()
        
        
    page_soup = soup(webpage, features="lxml")
    output = page_soup.prettify()

# =============================================================================
# #The hindu
# =============================================================================
    
    if name == 'The Hindu':
        
        print('Article Number -->', count)
        
        outputTheHindu = page_soup.find('div', {'class': '_yeti_done'})
        outputTheHindu = soup(str(outputTheHindu))
        print(outputTheHindu)
        count = count + 1
        
        data = {
                'totalResults': str(total),
                'source': {
                        'id': 'the-hindu',
                        'name': name
                        },
                'author' : author,
                'title': title,
                'description': 'Summary Goes Here',
                'url': url,
                'urlToImage': urlToImage,
                'publishedAt': publishedAt,
                'content': str(outputTheHindu)
                }
                
        with open('NewsJsonOutput.json', 'a') as f:
            json.dump(data, f, indent=4)
                
# =============================================================================
# #Zee News
# =============================================================================
        
    elif name == 'Zee News':
        
        print('Article Number -->', count)
        
        publishedAtZeeNews = page_soup.find_all('div', {'class': 'write-block margin-bt20px'})
        publishedAtZeeNews = soup(str(publishedAtZeeNews))
        publishedAtZeeNews = re.sub(r'<.*?>', '', str(publishedAtZeeNews()))
        publishedAtZeeNews = re.split(",", publishedAtZeeNews)
        publishedAtZeeNews = str(publishedAtZeeNews[0]) + str(publishedAtZeeNews[1]) + str(publishedAtZeeNews[2])
        publishedAtZeeNews = re.sub('[/[[/]', '', publishedAtZeeNews)
        
        #authorZeeNews = page_soup('meta', {'name': 'news_keywords'})
        #authorZeeNews = re.sub('^(.*content=")', '', str(authorZeeNews))
        #authorZeeNews = re.split(',', authorZeeNews)[0]
    
    
        outputZeeNews = page_soup('div', {'class': 'field-item even'})
        outputZeeNews = soup(str(outputZeeNews))
        if len(outputZeeNews('p')) > 3:
            OutputText = re.sub('<p>', '', str(outputZeeNews('p')))
            OutputText = re.sub('[[]', '', OutputText)
            OutputText = re.sub('[]]', '', OutputText)
            OutputText = re.sub(r', \xa0', '', OutputText)
            OutputText = re.sub(r'\xa0', '', OutputText)
            OutputText = re.split('</p>', OutputText)
            
            for InternalIterator in range(0, len(OutputText)):
                if len(OutputText[InternalIterator]) > 4:
                    text = re.sub(r'[^\w\s]','', OutputText[InternalIterator])
                    OutputZeeNews.append(text)
                    
            print(OutputZeeNews)
            count = count + 1
            
            data = {'totalResults': str(total),
                    'source': {
                            'id': 'zee-news',
                            'name': name
                            },
                    'author' : author,
                    'title': title,
                    'description': 'Summary Goes Here',
                    'url': url,
                    'urlToImage': urlToImage,
                    'publishedAt': publishedAtZeeNews,
                    'content': OutputZeeNews
                    }
                
            with open('NewsJsonOutput.json', 'a') as f:  
                json.dump(data, f, indent=4)


# =============================================================================
#     #The times of India
# =============================================================================
        
    elif name == 'The Times of India':
        
        print('Article Number -->', count)
        
        outputTimesOfIndia = page_soup('div', {'class': 'Normal'})
        outputTimesOfIndia = soup(str(outputTimesOfIndia))
        
        OutputText = re.sub(r'<.*?>', '', str(outputTimesOfIndia('div', {'class': 'Normal'})))
        OutputText = re.sub("\'s", "", OutputText)
        OutputText = re.sub("\n", "", OutputText)
        OutputText = re.sub("[/]/]", "", OutputText)
        OutputText = re.sub("[[/]", "", OutputText)
        OutputText = re.split("[.]", OutputText)
        print(OutputText)
            
        for InternalIterator in range(0, len(OutputText)):
            if len(OutputText[InternalIterator]) > 4:
                text = re.sub(r'[[/]','', OutputText[InternalIterator])
                text = re.sub(r'\u201c','', text)
                OutputTimesOfIndia.append(text)
            
        print(OutputTimesOfIndia)
        count = count + 1

        data = {
                'totalResults': str(total),
                'source': {
                        'id': 'the-times-of-india',
                        'name': name
                        },
                'author' : author,
                'title': title,
                'description': 'Summary Goes Here',
                'url': url,
                'urlToImage': urlToImage,
                'publishedAt': publishedAt,
                'content': OutputTimesOfIndia
                }

        with open('NewsJsonOutput.json', 'a') as f:  
            json.dump(data, f, indent=4)        
        
    with open('Beautiful2.txt', 'a') as f:
        f.write(output)
        
# =============================================================================
#         
# =============================================================================
    
def StartFunction(Keyword):
    
    ua = UserAgent()
    
    global count
    global Total
    global total
    count = 1
    Total = 0
    limit = 0
    TopicsList = api.callAPI(Keyword)
    TopicsListZeeNews = ZeeNewsSearcher.CallZeeNews(Keyword)
    Total = len(TopicsList) + len(TopicsListZeeNews)
    
    for Iterator in range(0, len(TopicsList)):

        Url = TopicsList[Iterator]['url']
        Name = TopicsList[Iterator]['name']
        Title = TopicsList[Iterator]['title']
        Author = TopicsList[Iterator]['author']
        UrlToImage = TopicsList[Iterator]['urlToImage']
        PublishedAt = TopicsList[Iterator]['publishedAt']
        
        Scrapper(Url, Name, 
                 title = Title, total = Total, 
                 author = Author, urlToImage = UrlToImage,
                 publishedAt = PublishedAt, userAgent = ua)
        limit = random.randint(5, 14)
        print("Sleeping for --> ", limit)
        print('')
        time.sleep(limit)

        
    for IteratorZee in range(0, len(TopicsListZeeNews)):
        Url = TopicsListZeeNews[IteratorZee]['url']
        Name = TopicsListZeeNews[IteratorZee]['name']
        Title = TopicsListZeeNews[IteratorZee]['title']
        
        Scrapper(Url, Name, 
                 title = Title, total = Total,
                 userAgent = ua)
        limit = random.randint(6, 14)
        print("Sleeping for --> ", limit)
        print('')
        time.sleep(limit)