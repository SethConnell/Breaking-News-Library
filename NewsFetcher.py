#!/usr/bin/python
# -*- coding: utf-8 -*-

# Made some imports I'll need later on.
import time
import socialshares
import requests
import ast
import unicodedata
from bs4 import BeautifulSoup
from six.moves import urllib
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


# A simple function to get number of shares on Facebook of a url using social shares module.
def facebookShares(url):
    try:
        counts = socialshares.fetch(url, ['facebook'])
        return int(counts['facebook']['share_count'])
    except KeyError:
        time.sleep(15)
        counts = socialshares.fetch(url, ['facebook'])
        return int(counts['facebook']['share_count'])


stories = []


# Using this function to display data saved as dicts to the list 'stories'.
def displayStories():
    global stories
    for i in range(0, len(stories)):
        print stories[i]['headline']
        print stories[i]['url']
        print stories[i]['shares']
        print ''


# A clean function that scrapes Fox News.com
def scrapeFoxNews():
    global stories
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
            shares = facebookShares(url)
            d = {'headline': headline, 'url': url, 'shares': shares}
            stories.append(d)


# A function that scrapes the Daily Wire.
def scrapeDailyWire():
    global stories
    dailywire = 'https://www.dailywire.com/'
    page = urllib.urlopen(dailywire)
    r = requests.get(dailywire)
    data = r.text
    soup = BeautifulSoup(data, 'lxml')
    for h3 in soup.find_all('article',
                            class_='article-teaser f-deflate-1-s fx ai-c mb-3-s mb-4-ns'
                            ):
        blah = h3.find('a', text=True)
        headline = blah.text
        url = 'https://www.dailywire.com' + blah['href']
        shares = facebookShares(url)
        print ''
        d = {'headline': headline, 'url': url, 'shares': shares}
        stories.append(d)


# A function that scrapes The Gateway Pundit.
def scrapeTheGatewayPundit():
    global stories
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
        shares = facebookShares(url)
        d = {'headline': headline, 'url': url, 'shares': shares}
        stories.append(d)


# This function scrapes WND's political frontpage only.
def scrapeWND():
    global stories
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
        shares = facebookShares(url)
        d = {'headline': headline, 'url': url, 'shares': shares}
        stories.append(d)


# This function scrapes all stories from Conservative Tribune.
def CT():
    global stories
    ct = 'https://www.westernjournal.com/ct/'
    r = requests.get(ct)
    data = r.text
    soup = BeautifulSoup(data, 'lxml')
    for article in soup.find_all('article', class_='post'):
        headline = article.find('h3', class_='entry-title').text
        url = article.find('a', attrs={'data-type': 'Internal link'},
                           href=True)['href']
        shares = facebookShares(url)
        d = {'headline': headline, 'url': url, 'shares': shares}
        stories.append(d)


# This function takes the front stories from Fox News Insider.
def InsiderFoxNews():
    global stories
    fox = 'http://insider.foxnews.com/'
    options = Options()
    options.set_headless(headless=True)
    driver = webdriver.Firefox(firefox_options=options,
                               executable_path=r'/usr/local/bin/geckodriver'
                               )
    driver.get(fox)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    for i in var.find_all('h2')[0:40]:
        headline = i.find('a').text
        url = i.find('a', href=True)['href']
        shares = facebookShares(url)
        d = {'headline': headline, 'url': url, 'shares': shares}
        stories.append(d)
    driver.quit()


# This function scrapes TheHill.com.
def TheHill():
    global stories
    hill = 'http://thehill.com/'
    r = requests.get(hill)
    data = r.text
    soup = BeautifulSoup(data, 'lxml')
    for story in soup.find_all('h2'):
        headline = story.find('a').text
        url = 'http://thehill.com' + story.find('a', href=True)['href']
        shares = facebookShares(url)
        d = {'headline': headline, 'url': url, 'shares': shares}
        stories.append(d)

#This function scrapes IJ Review.
def ijr():
    global stories
    global soup
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
        shares = facebookShares(url)
        d = {'headline': headline, 'url': url, 'shares': shares}
        stories.append(d)
    driver.quit()

# This function scrapes Breitbart's website.
def Breitbart():
    global soup
    global stories
    breitbart = 'http://www.breitbart.com/'
    r = requests.get(breitbart)
    data = r.text
    soup = BeautifulSoup(data, 'lxml')
    soup = soup.find("ul", id="BBTrendUL")
    for story in soup.find_all('li'):
        headline = story.find('a').text
        url = story.find("a", href=True)["href"]
        shares = facebookShares(url)
        d = {'headline': headline, 'url': url, 'shares': shares}
        stories.append(d)

# This function scrapes FreeBeacon.com
def FreeBeacon():
    global stories
    fb = 'http://freebeacon.com/'
    r = requests.get(fb)
    data = r.text
    soup = BeautifulSoup(data, 'lxml')
    soup = soup.find("div", class_="show-for-large-up")
    for story in soup.find_all("article",class_="post"):
        headline = story.find("a", {"rel":"bookmark"})['title']
        url = story.find("a", href=True)["href"]
        shares = facebookShares(url)
        d = {'headline': headline, 'url': url, 'shares': shares}
        stories.append(d)

# This function finds stories from dennismichaellynch.com
def Dennis():
    global stories
    link = "http://dennismichaellynch.com/"
    user_agent = \
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers = {'User-Agent': user_agent}
    request = urllib.request.Request(link, None, headers)  # The assembled request
    response = urllib.request.urlopen(request)
    data = response.read()
    soup = BeautifulSoup(data, 'lxml')
    print soup
    soup = soup.find("div", class_="trending-stories")
    for story in soup.find_all("article", class_="latestPost excerpt grid-2"):
        headline = story.find("a")["title"]
        url  = story.find("a", href=True)["href"]
        shares = facebookShares(url)
        d = {'headline': headline, 'url': url, 'shares': shares}
        stories.append(d)

# This function extracts stories from Western Journal.
def WesternJournal():
    global stories
    link = "https://www.westernjournal.com/"
    r = requests.get(link)
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    soup = soup.find("div", id="fhe-section-0")
    for story in soup.find_all("div", class_="fhe-headline"):
        headline = story.find("a").text
        url = story.find("a", href=True)["href"]
        shares = facebookShares(url)
        d = {'headline': headline, 'url': url, 'shares': shares}
        stories.append(d)

# This function gets news from JudicialWatch.com
def JudicialWatch():
    global stories
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
            shares = facebookShares(url)
            d = {'headline': headline, 'url': url, 'shares': shares}
            stories.append(d)
            print headline
            print url
            print ""
            time.sleep(.3)
        
# This function gets news from the daily caller.
def DailyCaller():
    global stories
    link = "http://dailycaller.com/"
    r = requests.get(link)
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    soup = soup.find("div", "articles trending")
    for story in soup.find_all("a", href=True):
        headline = story.find("h4").text
        url = "http://dailycaller.com" + story["href"]
        shares = facebookShares(url)
        d = {'headline': headline, 'url': url, 'shares': shares}
        stories.append(d)
