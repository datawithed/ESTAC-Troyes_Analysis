#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 22:35:28 2022

@author: edmorris
"""

# Defensive actions analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['figure.dpi'] = 750

# import data
press_22 = pd.read_csv('Pressures 2022-23.csv')
press_21 = pd.read_csv('Pressures 2021-22.csv')
possession_22 = pd.read_csv('Possession 22-23.csv')[:7]
possession_21 = pd.read_csv('Possession 21-22.csv')

# Total presses comparison (scaled)
press_21_p90 = press_21.Press.sum() / 38
press_22_p90 = press_22.Press.sum() / 7 # scale up from 7 games played to 38
# Pressures p90 has decreased this season

# Compare this to average possession this season
avg_pos_p90_22 = possession_22.Poss.mean()
avg_pos_p90_21 = possession_21.Poss.mean()

# Avg possession has decreased from last season, but so have pressures
    # Would expect pressures to increase
dict_for_plot = {'Troyes Possession':[avg_pos_p90_21,avg_pos_p90_22],'Opposition Possession':[100-avg_pos_p90_21,100-avg_pos_p90_22]}
df_for_plot = pd.DataFrame(dict_for_plot)
df_for_plot.index = ['Season: 2021/22','Season: 2022/23']

plt.style.use('ggplot')

fig, ax = plt.subplots()
ax.bar(df_for_plot.index,df_for_plot['Troyes Possession'],label='Troyes Avg',color='royalblue')
ax.bar(df_for_plot.index,df_for_plot['Opposition Possession'],bottom=df_for_plot['Troyes Possession'],label='Opposition Avg',color='tomato')
ax.legend(loc=9,prop={'size':8})
ax.set_ylabel('Possesion (%)')
y_offset = -7
for bar in ax.patches:
    ax.text(bar.get_x()+bar.get_width()/2,
            bar.get_height()+bar.get_y()+y_offset,
            str(round(bar.get_height()))+'%',
            ha='center',
            weight='bold')
ax.set_title('Possession comparison for 2021/22 and 2022/23 seasons',fontsize=12)