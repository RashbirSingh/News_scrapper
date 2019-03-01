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
# Importing library
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
ArticlesList = []

# =============================================================================
# Defining the scrapped class and defualt ardguments
# =============================================================================

def Scrapper(url, 
             name = "not available", 
             title = "not available", 
             total = 0, 
             author = "not available", 
             urlToImage = "not available",
             publishedAt = "not available",
             userAgent = UserAgent()):

    webpage = ''
    print(name)
    OutputZeeNews=[]
    OutputTimesOfIndia=[]
    global count
    global ArticlesList

# =============================================================================
# User agent list to scrap different usrs and spoof various browsers 
# imported using fake_useragent
# =============================================================================

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
    
# =============================================================================
# Using if else to handle different webpages
# =============================================================================

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
    #output = page_soup.prettify()

# =============================================================================
# #The hindu
# =============================================================================
    
    if name == 'The Hindu':
        
        print('Article Number -->', count)
        
        outputTheHindu = page_soup.find('div', {'class': '_yeti_done'})
        outputTheHindu = soup(str(outputTheHindu))
        print(outputTheHindu)
        count = count + 1
  
################### Creating data dict ########################################    
        data = {
                #'totalResults': str(total),
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
                
        ArticlesList.append(data)
                
        #with open('NewsJsonOutput.json', 'a') as f:
            #json.dump(data, f, indent=4)
                
# =============================================================================
# #Zee News
# =============================================================================
        
    elif name == 'Zee News':
        
        print('Article Number -->', count)
        
########## Getting publised date and time information #################################
        publishedAtZeeNews = page_soup.find_all('div', {'class': 'write-block margin-bt20px'})
        publishedAtZeeNews = soup(str(publishedAtZeeNews))
        publishedAtZeeNews = re.sub(r'<.*?>', '', str(publishedAtZeeNews()))
        publishedAtZeeNews = re.split(",", publishedAtZeeNews)
        publishedAtZeeNews = str(publishedAtZeeNews[0]) + str(publishedAtZeeNews[1]) + str(publishedAtZeeNews[2])
        publishedAtZeeNews = re.sub('[/[[/]', '', publishedAtZeeNews)
        
        #authorZeeNews = page_soup('meta', {'name': 'news_keywords'})
        #authorZeeNews = re.sub('^(.*content=")', '', str(authorZeeNews))
        #authorZeeNews = re.split(',', authorZeeNews)[0]
    
############### Processing the content body data #######################################    
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

################### Creating data dict ########################################           
            data = {
                    #'totalResults': str(total),
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
                    
            ArticlesList.append(data)
                
            #with open('NewsJsonOutput.json', 'a') as f:  
                #json.dump(data, f, indent=4)


# =============================================================================
#     #The times of India
# =============================================================================
        
    elif name == 'The Times of India':
        
        print('Article Number -->', count)
        
        outputTimesOfIndia = page_soup('div', {'class': 'Normal'})
        outputTimesOfIndia = soup(str(outputTimesOfIndia))


############### Processing the content body data #######################################        
        OutputText = re.sub(r'<.*?>', '', str(outputTimesOfIndia('div', {'class': 'Normal'})))
        OutputText = re.sub("\'s", "", OutputText)
        OutputText = re.sub("\n", "", OutputText)
        OutputText = re.sub("[/]/]", "", OutputText)
        OutputText = re.sub("[[/]", "", OutputText)
        OutputText = re.split("[.]", OutputText)
        print(OutputText)
            
        for InternalIterator in range(0, len(OutputText)):
            if len(OutputText[InternalIterator]) > 0:
                text = re.sub(r'[[/]','', OutputText[InternalIterator])
                text = re.sub(r'\u201c','', text)
                OutputTimesOfIndia.append(text)
            
        print(OutputTimesOfIndia)
        count = count + 1

################### Creating data dict ########################################
        data = {
                #'totalResults': str(total),
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
                
        ArticlesList.append(data)

        #with open('NewsJsonOutput.json', 'a') as f:  
            #json.dump(data, f, indent=4)        
        
    #with open('Beautiful2.txt', 'a') as f:
        #f.write(output)
        
# =============================================================================
# CAll this function to implement this python file
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

# =============================================================================
# Iterating News API
# =============================================================================
    
    try :
        
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
            
# =============================================================================
# Iterating Zee news
# =============================================================================
        
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
        
            JsonData = {
                    "status": "ok",
                    "totalResults": Total,
                    "articles": ArticlesList
                    }

# =============================================================================
# Dunping final articles into json format
# =============================================================================
    
    finally: 
        with open('NewsJsonOutput.json', 'a') as f:
            json.dump(JsonData, f, indent=4)