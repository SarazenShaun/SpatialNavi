# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 16:08:52 2020

@author: Shaun Ganju
"""


import os
import pandas as pd
import os, csv
import geopandas
import matplotlib.pyplot as plt
dataframe_collection = []
files_to_open = []
basepath = 'C:/Users/Shaun Ganju/Desktop/Coding/Spatial Navigation/csv_files'
for entry in os.listdir(basepath):
    if os.path.isfile(os.path.join(basepath, entry)):
        files_to_open.append(entry)
for i in range(len(files_to_open)):
    df = pd.read_csv(basepath+ '/' + files_to_open[i])
    plt.plot(df['LongitudeDegrees'],df['LatitudeDegrees'])
    plt.show()
     