#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 11 22:58:17 2022

@author: edmorris
"""

### Scrape historic shots for Troyes 2021/22 season ###

# Import modules
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json

# Scrape one game
base_url = 'https://understat.com/match/'
match_id = str(17824)
url = base_url + match_id

res = requests.get(url)
soup = BeautifulSoup(res.content,'lxml')
scripts = soup.find_all('script')

# Get shots data only
strings = scripts[1].text

# Strip unnecessary symbols so we only have json data
index_start = strings.index("('")+2
index_end = strings.index("')")

json_data = strings[index_start:index_end]
json_data = json_data.encode('utf8').decode('unicode_escape')

# convert string to json format
data = json.loads(json_data)

# Create empty lists to append each dictionary entry to
x = []
y = []
xg = []
team = []
data_away = data['a']
data_home = data['h']
player = []

# loop through dictionary
for index in range(len(data_home)):
    for key in data_home[index]:
        if key == 'X':
            x.append(data_home[index][key])
        if key == 'Y':
            y.append(data_home[index][key])
        if key == 'xG':
            xg.append(data_home[index][key])
        if key == 'h_team':
            team.append(data_home[index][key])
        if key == 'player':
            player.append(data_home[index][key])
            
for index in range(len(data_away)):
    for key in data_away[index]:
        if key == 'X':
            x.append(data_away[index][key])
        if key == 'Y':
            y.append(data_away[index][key])
        if key == 'xG':
            xg.append(data_away[index][key])
        if key == 'a_team':
            team.append(data_away[index][key])
        if key == 'player':
            player.append(data_away[index][key])

# Create dataframe
col_names = ['x','y','xG','player','team']
df = pd.DataFrame([x,y,xg,player,team],index=col_names)
df = df.T

