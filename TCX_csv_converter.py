# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 22:21:07 2020

@author: Shaun Ganju
"""
from math import radians, cos, sin, asin, sqrt
import io
import os
from lxml import objectify
import pandas as pd
from datetime import *

def reformat(df):
    x = 0
    r = 6371
    distances = [0]
    total_distance = [0]
    total = 0;
    for x in range(len(df.index)):
        string = df.at[x,'Time'].replace("T", " ")
        string = string.replace("+00:00", "")
        df.at[x,'Time'] = string
        df.at[x,'LatitudeDegrees'] = float(df.at[x,'LatitudeDegrees'])
        df.at[x,'LongitudeDegrees'] = float(df.at[x,'LongitudeDegrees'])
    for i in range(len(df.index)-1):
        long_1 = radians(df.at[i,'LongitudeDegrees'])
        lat_1 = radians( df.at[i,'LatitudeDegrees'])
        long_2  = radians(df.at[i+1,'LongitudeDegrees'])
        lat_2 = radians( df.at[i+1,'LatitudeDegrees'])
        distances.append(distance(lat_1,lat_2,long_1,long_2))
        total = total + distance(lat_1,lat_2,long_1,long_2)
        total_distance.append(total)
    df['Delta_Distance(km)'] = distances  
    df['Distance_Travelled(km)'] = total_distance
    return(df) 
def deltatime_format(df):
    deltatimes = [0]
    TotalTimeSeconds = [0]
    total = 0
    for x in range(1,len(df.index)):
        time_1 =  datetime.strptime(df.loc[x-1]['Time'],'%Y-%m-%d %H:%M:%S.%f')
        time_2 =  datetime.strptime(df.loc[x]['Time'],'%Y-%m-%d %H:%M:%S.%f')
        delta_t = time_2-time_1
        total = total+delta_t.total_seconds()
        TotalTimeSeconds.append(total)
        deltatimes.append(delta_t.total_seconds())
    df['Delta_Time'] = deltatimes
    df['TimeSeconds'] = TotalTimeSeconds
    return df
def tcx_reformat(name_of_file):
    
    namespaces={'ns': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2'}
    tree = objectify.parse(name_of_file)
    root = tree.getroot()
    trackpoints = []
    activity = root.Activities.Activity
    for trackpoint in activity.xpath('.//ns:Trackpoint', namespaces=namespaces):
        latitude_degrees = add_trackpoint(trackpoint, 'ns:Position/ns:LatitudeDegrees', namespaces)
        longitude_degrees = add_trackpoint(trackpoint, 'ns:Position/ns:LongitudeDegrees', namespaces)
        times = trackpoint.find('.//' + 'ns:Time', namespaces=namespaces).text
        trackpoints.append((latitude_degrees,longitude_degrees,times))
    activity_data = pd.DataFrame(trackpoints, columns=['LatitudeDegrees', 'LongitudeDegrees','Time'])
    activity_data = activity_data.dropna()
    activity_data = activity_data.reset_index(drop=True)
    activity_data = AddNewRun(activity_data)
    return activity_data
def AddNewRun(df):
    df = deltatime_format(reformat(df))
    return df

    return gdf 
def add_trackpoint(element, subelement, namespaces, default=None):
    in_str = './/' + subelement
    try:
        return float(element.find(in_str, namespaces=namespaces).text)
    except AttributeError:
        return default
def convert_csv(df):
    df.to_csv(r"C:\Users\Shaun Ganju\Desktop\Coding\Spatial Navigation\csv_files\Track_data_"+datetime.strftime(datetime.strptime(df.loc[0]['Time'],'%Y-%m-%d %H:%M:%S.%f'),'%m_%d_%Y')+".csv")
    return("Track_data_"+datetime.strftime(datetime.strptime(df.loc[0]['Time'],'%Y-%m-%d %H:%M:%S.%f'),'%m_%d_%Y')+".csv")
def distance(lat1, lat2, lon1, lon2): 
      
    # The math module contains a function named 
    # radians which converts from degrees to radians. 
    # Haversine formula  
    dlon = lon2 - lon1  
    dlat = lat2 - lat1 
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
  
    c = 2 * asin(sqrt(a))  
     
    # Radius of earth in kilometers. Use 3956 for miles 
    r = 6371
       
    # calculate the result 
    return(c * r)  
files_to_open = []
basepath = 'C:/Users/Shaun Ganju/Desktop/Coding/Spatial Navigation/tcx_files'
for entry in os.listdir(basepath):
    if os.path.isfile(os.path.join(basepath, entry)):
        files_to_open.append(entry)
csv_files = []
for i in range(len(files_to_open)):
    df = tcx_reformat(basepath+ '/' + files_to_open[i])
    csv_files.append(convert_csv(df).replace('.csv', ''))