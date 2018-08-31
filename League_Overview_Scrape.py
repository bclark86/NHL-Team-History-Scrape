"""
Created on Wed Aug 15 01:42:58 2018

@author: BryanClark
"""
from bs4 import BeautifulSoup
import requests
import pandas as pd
#import numpy as np

# create function to get table of Champions by season
def getLeagueChampions(url):
    ''' 
    This function creates a dataframe from the NHL league overview with
    Champions and runners up
    '''
    # get table from website
    url = url
    html = requests.get(url).content.decode('utf-8')
    bsObj = BeautifulSoup(html, "lxml")
    leage_table = bsObj.find("table",{"id": "league_index"})
    league = pd.read_html(str(leage_table), header = 1)[0]
    
    return league

# url of page
url = "https://www.hockey-reference.com/leagues/"

# get data and save to file
NHL_leagues = getLeagueChampions(url)
NHL_leagues.to_csv("Data/NHLChampionsAllTime.csv", index = False)

del NHL_leagues
del url