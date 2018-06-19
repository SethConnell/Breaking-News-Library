#Made some imports I'll need later on.
import socialshares
import requests
import ast
import unicodedata
from bs4 import BeautifulSoup
from six.moves import urllib
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

#A simple function to get number of shares on Facebook of a url using social shares module.
def facebookShares(url):
    counts = socialshares.fetch(url, ['facebook'])
    return int(counts['facebook']['share_count'])

stories = []

# Using this function to display data saved as dicts to the list 'stories'.
def displayStories():
    global stories
    for i in range(0, len(stories)):
        print stories[i]["headline"]
        print stories[i]['url']
        print stories[i]['shares']
        print ""

#A clean function that scrapes Fox News.com        
def scrapeFoxNews():
    global stories
    foxnews = "http://www.foxnews.com/"
    r  = requests.get(foxnews)
    data = r.text
    soup = BeautifulSoup(data,"lxml")
    for i in range(0, 15):
        foundstories = soup.find_all("article", class_="article story-" + str(i))
        for data in foundstories:
            htmlatag = data.find("h2", class_="title").find("a")
            headline = htmlatag.getText()
            url = htmlatag.get("href")
            shares = facebookShares(url)
            d = {"headline" : headline,
                 "url" : url,
                 "shares" : shares}
            stories.append(d)

# A function that scrapes the Daily Wire.
def scrapeDailyWire():
    global stories
    dailywire = "https://www.dailywire.com/"
    page = urllib.urlopen(dailywire)
    r = requests.get(dailywire)
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    for h3 in soup.find_all("article", class_="article-teaser f-deflate-1-s fx ai-c mb-3-s mb-4-ns"):
         blah = h3.find('a', text=True)
         headline = blah.text
         url = "https://www.dailywire.com" + blah['href']
         shares = facebookShares(url)
         print ""
         d = {"headline" : headline,
             "url" : url,
             "shares" : shares}
         stories.append(d)

# A function that scrapes The Gateway Pundit.
def scrapeTheGatewayPundit():
    global stories
    thegatewaypundit = "https://www.thegatewaypundit.com/"
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers={'User-Agent':user_agent,} 
    request=urllib.request.Request(thegatewaypundit,None,headers) #The assembled request
    response = urllib.request.urlopen(request)
    data = response.read()
    soup = BeautifulSoup(data, "lxml")
    for h3 in soup.find_all("h3", class_="post-title"):
        blah = h3.find("a", text=True)
        headline = blah.text
        url = blah['href']
        shares = facebookShares(url)
        d = {"headline" : headline,
             "url" : url,
             "shares" : shares}
        stories.append(d)

#This function scrapes WND's political frontpage only.
def scrapeWND(): 
    global stories
    wnd = "http://www.wnd.com/category/front-page/politics/"
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers={'User-Agent':user_agent,} 
    request=urllib.request.Request(wnd,None,headers) #The assembled request
    response = urllib.request.urlopen(request)
    data = response.read()
    soup = BeautifulSoup(data, "lxml")
    for i in soup.find_all("a", class_="cat-feature", href=True):
        headline = i.find("h1", class_="posttitle").text
        url = i['href']
        shares = facebookShares(url)
        d = {"headline" : headline,
             "url" : url,
             "shares" : shares}
        stories.append(d)

