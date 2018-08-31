"""
Created on Mon Aug 13 22:09:44 2018
Last Edited on 
@author: BryanClark
"""

from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import numpy as np

# create function to get single-season standings
def getNHLSeason(url):
    ''' 
    This function creates a dataframe from the NHL team standings table listed
    for the season listed in the URL
    '''
    # get table from website
    url = url
    html = requests.get(url).content.decode('utf-8')
    bsObj = BeautifulSoup(re.sub("<!--|-->","", html), "lxml")
    stats_table = bsObj.find("table",{"id": "stats"})
    
    # extract season from URL string
    season = re.sub("\D", "", url)
    
    # dataframe operations
    team_stats = pd.read_html(str(stats_table), header = 1)[0]
    team_stats = team_stats.rename(columns = {"Unnamed: 1": "Team"})
    team_stats["Season"] = season                               
    
    # set columns for the dataframe
    cols = ['Season', 'Rk', 'Team', 'AvAge', 'GP', 'W', 'L', 'OL', 'PTS', 
            'PTS%', 'GF', 'GA', 'SOW', 'SOL', 'SRS', 'SOS', 'TG/G', 'EVGF', 
            'EVGA', 'PP', 'PPO', 'PP%', 'PPA', 'PPOA', 'PK%', 'SH', 'SHA', 
            'PIM/G', 'oPIM/G', 'S', 'S%', 'SA', 'SV%', 'PDO']
    
    # check if columns are present for season and add N/As if missing
    for col in team_stats.columns.tolist():
        if col in cols:
            continue
        else:
            team_stats[col] = np.nan
    
    # re-order columns
    team_stats = team_stats.reindex(columns = cols)
    
    return team_stats
 
# initialize empty dataframe for all seasons
full_team_stats = pd.DataFrame()

# starting season
season_counter = 2018

while season_counter > 1917:
    try:
        year = str(season_counter)
        print("Working on " + year + "...")
        url = "https://www.hockey-reference.com/leagues/NHL_" + year + ".html"
        stats = getNHLSeason(url = url)
        full_team_stats = full_team_stats.append(stats, ignore_index = True)
        season_counter -= 1
    except Exception as e: print(e)

print("All done!")

# remove any duplicate values for QA
full_team_stats = full_team_stats.drop_duplicates()

# add column for made playoffs based on * presence
full_team_stats["Playoffs"] = full_team_stats.apply(
                                lambda x: "*" in x.Team, axis=1)
    
# remove * from Team column
full_team_stats["Team"] = full_team_stats["Team"].str.replace("*", "")

full_team_stats.to_csv("Data/NHLStandingsAllTime.csv", index = False)


# remove enviroment variables
del full_team_stats
del season_counter
del stats
del url
del year
