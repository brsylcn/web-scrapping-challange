#!/usr/bin/env python
# coding: utf-8

# # MISSION TO MARS




# get_ipython().system('pip install GetOldTweets3')





from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime
import pymongo
import time



def init_browser():
    
    # executable_path = {'executable_path': 'chromedriver.exe'}

    # browser = Browser('chrome', **executable_path, headless=False)

    executable_path = {'executable_path': '/app/.chromedriver/bin/chromedriver'}
    
    return Browser('chrome', headless=True, **executable_path)

info = {}

def scrape_news():
    
    try:

        browser = init_browser()
    
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)
        # time.sleep(3)


        html = browser.html


        soup = BeautifulSoup(html, 'html.parser')
        # soup





        news_title = soup.find('div', class_='content_title').text

        news_p = soup.find('div', class_='article_teaser_body').text


        # print(news_title)

        # print(news_p)

        info['title'] = news_title
        info['paragraph'] = news_p
        
        return info
    
    finally:
        
        browser.quit()


def scrape_image():
    
    try:
        
        browser = init_browser()

        url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        
        browser.visit(url2)

        html2 = browser.html

        soup2 = BeautifulSoup(html2, 'html.parser')

        image_url = soup2.find('article')['style'][23:-3]

        featured_image_url = f'{url2[0:24]}{image_url}'

        # print(featured_image_url)
        
        info['featured_image_url'] = featured_image_url

        return info
    
    finally:
        
        browser.quit()


def scrape_weather():
    
    try:
        
        browser = init_browser()

        url3 = 'https://twitter.com/marswxreport'
        browser.visit(url3)
        # time.sleep(3)

        html3 = browser.html

        soup3 = BeautifulSoup(html3, 'html.parser')
        # soup3




# mars_weather = soup3.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').find()

# print(mars_weather) #------> try




        url_ex = "https://twitter.com/marswxreport?lang=en"

        tweet_html_content = requests.get(url_ex).text

        soup = BeautifulSoup(tweet_html_content, "lxml")
        tweet_list = soup.find_all('div', class_="js-tweet-text-container")

        tweety = []

        for tweets in tweet_list: 
    
            body = tweets.find('p').text
    
            if 'InSight' and 'sol' in body:
        
                tweety.append(body)

                break
            else: 

                pass
    

        mars_weather = ([tweety[0]][0][:-26])
        tweet_img_link = ([tweety[0]][0][-26:])
        # print(f"{mars_weather}: {tweet_img_link}")
        
        info['mars_weather'] = mars_weather

        return info
    
    finally:
        
        browser.quit()
        




#import GetOldTweets3 as got
#tweetCriteria = got.manager.TweetCriteria().setUsername("MarsWxReport").setMaxTweets(5)
#tweet = got.manager.TweetManager.getTweets(tweetCriteria)[3]
#print(tweet.text)


def scrape_facs():

    url4 = 'http://space-facts.com/mars/'

    facts = pd.read_html(url4)

    df = facts[0]

    df.columns = ['Description','Value']

    df.set_index('Description', inplace=True)

    df.to_html()

    data = df.to_dict(orient='records')  
    #df
    
    info['facts'] = data
    
    return info



def scrape_hem():
    
    try:
        
        browser = init_browser()

        url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

        browser.visit(url5)

        html5 = browser.html

        soup5 = BeautifulSoup(html5, 'html.parser')

        everything = soup5.find_all('div', class_='item')

        list_urls = []

        url6 = 'https://astrogeology.usgs.gov'

        for hemisphere in everything: 
    
            title = hemisphere.find('h3').get_text()
    
            image_url = hemisphere.find('a', class_='itemLink product-item')['href']
    
            browser.visit(url6 + image_url)
    
            image_html = browser.html
    
            soup6 = BeautifulSoup(image_html, 'html.parser')
    
            finale = url6 + soup6.find('img', class_='wide-image')['src']
    
            list_urls.append({"title" : title, "img_url" : finale})
    
        return info
    
    finally:
        
        browser.quit()

        # list_urls






