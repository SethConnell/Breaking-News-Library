#!/usr/bin/python
# -*- coding: utf-8 -*-

# Made some imports I'll need later on.
import os
import time
import facepy
import requests
import ast
import unicodedata
from TaskThreaderModule import *
from bs4 import BeautifulSoup
from six.moves import urllib
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


# Setting global variables for Facebook share function.
token = os.environ.get('facebook_token')
graph = facepy.GraphAPI(token, version=2.9)

# A simple function to get number of shares on Facebook of a url using social shares module.
def facebookShares(url):
    global token
    global graph
    response = graph.get('?og_object&share_count&id=' + str(link) + '&fields=og_object,engagement&access_token=' + str(token))
    return response["engagement"]["share_count"]

# The 'stories' list will store all news stories once scraping is complete.
stories = []


# Using this function to display data saved as dicts to the list 'stories'.
def displayStories():
    global stories
    for i in range(0, len(stories)):
        print
        print stories[i]['headline']
        print stories[i]['url']
        print stories[i]['shares']
        print ''


# A clean function that scrapes Fox News.com
def scrapeFoxNews():
    source = "Fox News"
    global foxnewslist
    foxnewslist = []
    foxnews = 'http://www.foxnews.com/'
    r = requests.get(foxnews)
    data = r.text
    soup = BeautifulSoup(data, 'lxml')
    for i in range(0, 15):
        foundstories = soup.find_all('article', class_='article story-'
                + str(i))
        for data in foundstories:
            htmlatag = data.find('h2', class_='title').find('a')
            headline = htmlatag.getText()
            url = htmlatag.get('href')
            d = {"source": source, 'headline': headline, 'url': url}
            foxnewslist.append(d)


# A function that scrapes the Daily Wire.
def scrapeDailyWire():
    source = "Daily Wire"
    global dailywirelist
    dailywirelist = []
    dailywire = 'https://www.dailywire.com/'
    result = urllib.request.urlopen(dailywire)
    data = response.read()
    soup = BeautifulSoup(data, 'lxml')
    for h3 in soup.find_all('article',
                            class_='article-teaser f-deflate-1-s fx ai-c mb-3-s mb-4-ns'
                            ):
        blah = h3.find('a', text=True)
        headline = blah.text
        url = 'https://www.dailywire.com' + blah['href']
        d = {"source": source, 'headline': headline, 'url': url}
        dailywirelist.append(d)


# A function that scrapes The Gateway Pundit.
def scrapeTheGatewayPundit():
    source = "Gateway Pundit"
    global gatewaypunditlist
    gatewaypunditlist = []
    thegatewaypundit = 'https://www.thegatewaypundit.com/'
    user_agent = \
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers = {'User-Agent': user_agent}
    request = urllib.request.Request(thegatewaypundit, None, headers)  # The assembled request
    response = urllib.request.urlopen(request)
    data = response.read()
    soup = BeautifulSoup(data, 'lxml')
    for h3 in soup.find_all('h3', class_='post-title'):
        blah = h3.find('a', text=True)
        headline = blah.text
        url = blah['href']
        d = {"source": source, 'headline': headline, 'url': url}
        gatewaypunditlist.append(d)


# This function scrapes WND's political frontpage only.
def scrapeWND():
    source = "WND"
    global wndlist
    wndlist = []
    wnd = 'http://www.wnd.com/category/front-page/politics/'
    user_agent = \
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers = {'User-Agent': user_agent}
    request = urllib.request.Request(wnd, None, headers)  # The assembled request
    response = urllib.request.urlopen(request)
    data = response.read()
    soup = BeautifulSoup(data, 'lxml')
    for i in soup.find_all('a', class_='cat-feature', href=True):
        headline = i.find('h1', class_='posttitle').text
        url = i['href']
        d = {"source": source, 'headline': headline, 'url': url}
        wndlist.append(d)


# This function scrapes all stories from Conservative Tribune.
def CT():
    source = "Conservative Tribune"
    global ctlist
    ctlist = []
    ct = 'https://www.westernjournal.com/ct/'
    r = requests.get(ct)
    data = r.text
    soup = BeautifulSoup(data, 'lxml')
    for article in soup.find_all('article', class_='post'):
        headline = article.find('h3', class_='entry-title').text
        url = article.find('a', attrs={'data-type': 'Internal link'},
                           href=True)['href']
        d = {"source": source, 'headline': headline, 'url': url}
        ctlist.append(d)


# This function takes the front stories from Fox News Insider.
def InsiderFoxNews():
    source = "Fox News Insider"
    global insiderfoxlist
    insiderfoxlist = []
    fox = 'http://insider.foxnews.com/'
    options = Options()
    options.set_headless(headless=True)
    driver = webdriver.Firefox(firefox_options=options,
                               executable_path=r'/usr/local/bin/geckodriver'
                               )
    driver.get(fox)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    for i in soup.find_all('h2')[0:40]:
        headline = i.find('a').text
        url = i.find('a', href=True)['href']
        d = {"source": source, 'headline': headline, 'url': url}
        insiderfoxlist.append(d)
    driver.quit()


# This function scrapes TheHill.com.
def TheHill():
    source = "The Hill"
    global thehilllist
    thehilllist = []
    hill = 'http://thehill.com/'
    r = requests.get(hill)
    data = r.text
    soup = BeautifulSoup(data, 'lxml')
    for story in soup.find_all('h2'):
        headline = story.find('a').text
        url = 'http://thehill.com' + story.find('a', href=True)['href']
        d = {"source": source, 'headline': headline, 'url': url}
        thehilllist.append(d)

#This function scrapes IJ Review.
def ijr():
    source = "IJ Review"
    global soup
    global ijrlist
    ijrlist = []
    ijr = 'https://ijr.com/'
    options = Options()
    options.set_headless(headless=True)
    driver = webdriver.Firefox(firefox_options=options,
                               executable_path=r'/usr/local/bin/geckodriver'
                               )
    driver.get(ijr)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    soup = soup.find('div', class_='infinite-scroll-component')
    for story in soup.find_all('a', attrs={'rel': 'post'}, href=True):
        headline = story.text
        url = "https://ijr.com" + story['href']
        d = {"source": source, 'headline': headline, 'url': url}
        ijrlist.append(d)
    driver.quit()

# This function scrapes Breitbart's website.
def Breitbart():
    source = "Breitbart"
    global soup
    global breitbartlist
    breitbartlist = []
    breitbart = 'http://www.breitbart.com/'
    r = requests.get(breitbart)
    data = r.text
    soup = BeautifulSoup(data, 'lxml')
    soup = soup.find("ul", id="BBTrendUL")
    for story in soup.find_all('li'):
        headline = story.find('a').text
        url = story.find("a", href=True)["href"]
        d = {"source": source, 'headline': headline, 'url': url}
        breitbartlist.append(d)

# This function scrapes FreeBeacon.com
def FreeBeacon():
    source = "Free Beacon"
    global freebeaconlist
    freebeaconlist = []
    fb = 'http://freebeacon.com/'
    r = requests.get(fb)
    data = r.text
    soup = BeautifulSoup(data, 'lxml')
    soup = soup.find("div", class_="show-for-large-up")
    for story in soup.find_all("article",class_="post"):
        headline = story.find("a", {"rel":"bookmark"})['title']
        url = story.find("a", href=True)["href"]
        d = {"source": source, 'headline': headline, 'url': url}
        freebeaconlist.append(d)

# This function finds stories from dennismichaellynch.com
def Dennis():
    source = "Dennis Michael Lynch"
    global dennislist
    dennislist = []
    link = "http://dennismichaellynch.com/"
    user_agent = \
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers = {'User-Agent': user_agent}
    request = urllib.request.Request(link, None, headers)  # The assembled request
    response = urllib.request.urlopen(request)
    data = response.read()
    soup = BeautifulSoup(data, 'lxml')
    soup = soup.find("div", class_="trending-stories")
    for story in soup.find_all("article", class_="latestPost excerpt grid-2"):
        headline = story.find("a")["title"]
        url  = story.find("a", href=True)["href"]
        d = {"source": source, 'headline': headline, 'url': url}
        dennislist.append(d)

# This function extracts stories from Western Journal.
def WesternJournal():
    source = "Western Journal"
    global westernjournallist
    westernjournallist = []
    link = "https://www.westernjournal.com/"
    r = requests.get(link)
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    soup = soup.find("div", id="fhe-section-0")
    for story in soup.find_all("div", class_="fhe-headline"):
        headline = story.find("a").text
        url = story.find("a", href=True)["href"]
        d = {"source": source, 'headline': headline, 'url': url}
        westernjournallist.append(d)

# This function gets news from JudicialWatch.com
def JudicialWatch():
    source = "Judicial Watch"
    global judicialwatchlist
    judicialwatchlist = []
    link = "http://www.judicialwatch.org/"
    r = requests.get(link)
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    soup = soup.find("ul", id="tslinks")
    for story in soup.find_all("li"):
        headline = story.find("a").text
        url = story.find("a", href=True)["href"]
        if url[0:8] != "https://":
            print "not a valid url"
        else:
            d = {"source": source, 'headline': headline, 'url': url}
            judicialwatchlist.append(d)
            time.sleep(.3)
        
# This function gets news from the daily caller.
def DailyCaller():
    source = "Daily Caller"
    global dailycallerlist
    dailycallerlist = []
    link = "http://dailycaller.com/"
    r = requests.get(link)
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    soup = soup.find("div", "articles trending")
    for story in soup.find_all("a", href=True):
        headline = story.find("h4").text
        url = "http://dailycaller.com" + story["href"]
        d = {"source": source, 'headline': headline, 'url': url}
        dailycallerlist.append(d)

# This function searches Weasel Zippers for stories.
def WeaselZippers():
    source = "Weasel Zippers"
    global weaselzipperslist
    weaselzipperslist = []
    link = "https://www.weaselzippers.us/"
    r = requests.get(link)
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    for story in soup.find_all("div","post")[0:10]:
        headline = story.find("a").text
        url = story.find("a",href=True)['href']
        d = {"source": source, 'headline': headline, 'url': url}
        weaselzipperslist.append(d)

# This function gets as many share-counts from Facebook's API as it safely can.
def getshares(linklist):
    global stories
    for i in range(0,85):
        shares = facebookShares(linklist[i]['url'])
        stories[i]["shares"] = str(shares)
        time.sleep(22)

# This function appends all scraped data to the global stories list.
def connectNewsLists():
    global stories
    data = [foxnewslist, dailywirelist, gatewaypunditlist, wndlist, ctlist, insiderfoxlist, thehilllist, ijrlist, breitbartlist, freebeaconlist, westernjournallist, judicialwatchlist, dailycallerlist, weaselzipperslist]
    length = len(data)
    for site in range(0, length):
        length2 = len(data[site])
        for i in range(0,length2):
            stories.append(data[site][i])
    print "finished!"
                
# The 'scrapingfunctions' list contains all functions that search for news stories.
scrapingfunctions = [scrapeFoxNews, scrapeDailyWire, scrapeTheGatewayPundit, scrapeWND, CT, InsiderFoxNews, TheHill, ijr, Breitbart, FreeBeacon, Dennis, WesternJournal, JudicialWatch, DailyCaller, WeaselZippers]

# This function prints all items from the global 'stories' list.
def printStories():
    global stories
    for story in stories:
        print story["source"]
        print story["headline"]
        print story["url"]
        print ""
    print "Complete!"

# This functions runs the storyfinding processes.
def start():
    global scrapingfunctions
    print "Starting Processes"
    runTasks(scrapingfunctions)
    print "Complete!"
    time.sleep(2)
    connectNewsLists()
    print "Printing Results:"
    printStories()

    
