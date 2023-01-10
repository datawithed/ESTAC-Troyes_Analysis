#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 00:18:12 2022

@author: edmorris
"""

### Scrape historic shots for Troyes 2021/22 season ###

# Import modules
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
from mplsoccer import VerticalPitch, add_image
from PIL import Image
import seaborn as sns
from matplotlib import rcParams
rcParams['figure.dpi'] = 750
import matplotlib.pyplot as plt


# Create list of 2021/22 match IDs manually
ly_matches = [17824,17837,17848,17855,17870,17872,17884,17901,17908,17921,17929,17941,17943,17959,17968,17981,17982,17997,18011,18031,18013,18032,18043,18057,18063,18072,18085,18101,18108,18121,18129,18141,18151,18157,18169,18174,18182,18194]
cy_matches = [19653,19665,19673,19687,19688,19707,19714]

base_url = 'https://understat.com/match/'

# Create empty lists to append each dictionary entry to
x = []
y = []
xg = []
team = []
player = []
team_names = []

for i in range(len(ly_matches)):
    # Create url for each match ID
    match_id = str(ly_matches[i])
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

    # Convert string to json format
    data = json.loads(json_data)
    
    data_away = data['a']
    data_home = data['h']
    
    # Loop through dictionary
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
    
# Create dataframe from lists 
col_names = ['x','y','xG','player','team']
shots = pd.DataFrame([x,y,xg,player,team],index=col_names)
# Transpose
shots = shots.T

# Filter for Troyes data
troyes_shots = shots.loc[shots.team == 'Troyes']
troyes_shots['x'] = troyes_shots['x'].astype('float64')
troyes_shots['y'] = troyes_shots['y'].astype('float64')
troyes_shots['xG'] = troyes_shots['xG'].astype('float64')

# Filter for non-Troyes shots
shots_against = shots.loc[shots.team != 'Troyes']
shots_against['x'] = shots_against['x'].astype('float64')
shots_against['y'] = shots_against['y'].astype('float64')
shots_against['xG'] = shots_against['xG'].astype('float64')

# Convert shot locations to StatsBomb pitch coordinates
troyes_shots['sb_x'] = troyes_shots['x']*100*1.2
troyes_shots['sb_y'] = troyes_shots['y']*100*0.8
shots_against['sb_x'] = shots_against['x']*100*1.2
shots_against['sb_y'] = shots_against['y']*100*0.8

# Create empty lists to append each dictionary entry to (current year)
x1 = []
y1 = []
xg1 = []
team1 = []
player1 = []

for i in range(len(cy_matches)):
    # Create url for each match ID
    match_id = str(cy_matches[i])
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

    # Convert string to json format
    data = json.loads(json_data)
    
    data_away = data['a']
    data_home = data['h']
    
    # Loop through dictionary
    for index in range(len(data_home)):
        for key in data_home[index]:
            if key == 'X':
                x1.append(data_home[index][key])
            if key == 'Y':
                y1.append(data_home[index][key])
            if key == 'xG':
                xg1.append(data_home[index][key])
            if key == 'h_team':
                team1.append(data_home[index][key])
            if key == 'player':
                player1.append(data_home[index][key])
                
    for index in range(len(data_away)):
        for key in data_away[index]:
            if key == 'X':
                x1.append(data_away[index][key])
            if key == 'Y':
                y1.append(data_away[index][key])
            if key == 'xG':
                xg1.append(data_away[index][key])
            if key == 'a_team':
                team1.append(data_away[index][key])
            if key == 'player':
                player1.append(data_away[index][key])

# Create dataframe from lists 
shots_cy = pd.DataFrame([x1,y1,xg1,player1,team1],index=col_names)
# Transpose
shots_cy = shots_cy.T

# Filter for Troyes data
troyes_shots_cy = shots_cy.loc[shots_cy.team == 'Troyes']
troyes_shots_cy['x'] = troyes_shots_cy['x'].astype('float64')
troyes_shots_cy['y'] = troyes_shots_cy['y'].astype('float64')
troyes_shots_cy['xG'] = troyes_shots_cy['xG'].astype('float64')

# Filter for non-Troyes shots
shots_against_cy = shots_cy.loc[shots_cy.team != 'Troyes']
shots_against_cy['x'] = shots_against_cy['x'].astype('float64')
shots_against_cy['y'] = shots_against_cy['y'].astype('float64')
shots_against_cy['xG'] = shots_against_cy['xG'].astype('float64')

# Convert shot locations to StatsBomb pitch coordinates
troyes_shots_cy['sb_x'] = troyes_shots_cy['x']*100*1.2
troyes_shots_cy['sb_y'] = troyes_shots_cy['y']*100*0.8
shots_against_cy['sb_x'] = shots_against_cy['x']*100*1.2
shots_against_cy['sb_y'] = shots_against_cy['y']*100*0.8

# Calculate average xG per shot
avg_xg_ly = troyes_shots.xG.sum() / len(troyes_shots.xG)
avg_xg_cy = troyes_shots_cy.xG.sum() / len(troyes_shots_cy.xG)
avg_xg_against_ly = shots_against.xG.sum() / len(shots_against.xG)
avg_xg_against_cy = shots_against_cy.xG.sum() / len(shots_against_cy.xG)

# Two separate plots, ly first
vertical_pitch = VerticalPitch(half=True, pad_top=0.1, pad_right=0.05, pad_bottom=0.05,
                               pad_left=0.05, line_zorder=2)
fig, axs = vertical_pitch.jointgrid(figheight=10, left=None, bottom=0.15,
                                    grid_height=0.7, marginal=0.1,
                                    # plot without endnote/ title axes
                                    endnote_height=0.025, title_height=0.1,
                                    axis=False,  # turn off title/ endnote/ marginal axes
                                    # here we filter out the left and top marginal axes
                                    ax_top=True, ax_bottom=True,
                                    ax_left=True, ax_right=True)
# Plot heatmaps of shot locations for Troyes
ly_plot = vertical_pitch.scatter(troyes_shots.sb_x,troyes_shots.sb_y,ax=axs['pitch'],color='red',edgecolors='#383838',s=150,marker='*',label=f'2021/22 shots\nxG/shot: {round(avg_xg_ly,2)}')
cy_plot = vertical_pitch.scatter(troyes_shots_cy.sb_x,troyes_shots_cy.sb_y,ax=axs['pitch'],edgecolors='#383838',s=150,color='blue',marker='*',label=f'2022/23 shots\nxG/shot: {round(avg_xg_cy,2)}')
troyes_logo1 = add_image(Image.open('ESTAC_Troyes.png'), fig, left = 0.18, bottom = 0.9, height = axs['title'].get_position().height)
legend = axs['pitch'].legend(loc='lower left')
title_string = 'ESTAC Troyes: shotmap for the \n2021/22 and 2022/23 seasons'
axs['title'].text(0.3,0.35,title_string,fontsize=20,fontweight='bold')
#axs['title'].text(0.125,-0.75,'@datawithed',alpha=0.5)
axs['title'].text(0.75,-0.75,'Data via Understat',alpha=0.5)
ly_hist_x = sns.histplot(x=troyes_shots.sb_y,ax=axs['bottom'],linewidth=1,kde=True,color='red')
ly_hist_y = sns.histplot(y=troyes_shots.sb_x,ax=axs['right'],linewidth=1,kde=True,color='red')
cy_hist_x = sns.histplot(x=troyes_shots_cy.sb_y,ax=axs['top'],linewidth=1,kde=True,color='blue',bins=12)
cy_hist_y = sns.histplot(y=troyes_shots_cy.sb_x,ax=axs['left'],linewidth=1,kde=True,color='blue',bins=26)

# Plot shots against
fig, axs = vertical_pitch.jointgrid(figheight=10, left=None, bottom=0.15,
                                    grid_height=0.7, marginal=0.1,
                                    # plot without endnote/ title axes
                                    endnote_height=0.025, title_height=0.1,
                                    axis=False,  # turn off title/ endnote/ marginal axes
                                    # here we filter out the left and top marginal axes
                                    ax_top=True, ax_bottom=True,
                                    ax_left=True, ax_right=True)
ly_plot = vertical_pitch.scatter(shots_against.sb_x,shots_against.sb_y,ax=axs['pitch'],color='red',edgecolors='#383838',s=150,marker='*',label=f'2021/22 shots against\nxG/shot: {round(avg_xg_against_ly,2)}')
cy_plot = vertical_pitch.scatter(shots_against_cy.sb_x,shots_against_cy.sb_y,ax=axs['pitch'],edgecolors='#383838',s=150,color='blue',marker='*',label=f'2022/23 shots against\nxG/shot: {round(avg_xg_against_cy,2)}')
troyes_logo1 = add_image(Image.open('ESTAC_Troyes.png'), fig, left = 0.17, bottom = 0.9, height = axs['title'].get_position().height)
legend = axs['pitch'].legend(loc='lower left')
title_string = 'ESTAC Troyes: shotmap against for \nthe 2021/22 and 2022/23 seasons'
axs['title'].text(0.26,0.35,title_string,fontsize=20,fontweight='bold')
#axs['title'].text(0.125,-0.75,'@datawithed',alpha=0.5)
axs['title'].text(0.75,-0.75,'Data via Understat',alpha=0.5)
ly_hist_x = sns.histplot(x=shots_against.sb_y,ax=axs['bottom'],linewidth=1,kde=True,color='red')
ly_hist_y = sns.histplot(y=shots_against.sb_x,ax=axs['right'],linewidth=1,kde=True,color='red')
cy_hist_x = sns.histplot(x=shots_against_cy.sb_y,ax=axs['top'],linewidth=1,kde=True,color='blue',bins=12)
cy_hist_y = sns.histplot(y=shots_against_cy.sb_x,ax=axs['left'],linewidth=1,kde=True,color='blue',bins=10)


    
    