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
