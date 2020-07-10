#!/usr/bin/env python
# coding: utf-8

# In[5]:


import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt


# In[6]:


xlsxFiles = []

# Gets all .xlsx files from a target directory
for file in os.listdir("./csv_files/"):
    if file.endswith(".csv"):
        xlsxFiles.append(os.path.join("./csv_files/", file))

#print(xlsxFiles)

xlsxContents = {}
tempFileContents = 0

for xlsxFile in xlsxFiles:
    tempFileContents = pd.read_csv(xlsxFile)
    formattedContents = []
    for i in range(len(tempFileContents["TimeSeconds"].values)):
        rowContent = []
        rowContent.append(tempFileContents["LatitudeDegrees"].values[i])
        rowContent.append(tempFileContents["LongitudeDegrees"].values[i])
        rowContent.append(tempFileContents["Time"].values[i])
        rowContent.append(tempFileContents["Delta_Distance(km)"].values[i])
        rowContent.append(tempFileContents["Delta_Time"].values[i])
        rowContent.append(tempFileContents["TimeSeconds"].values[i])
        
        formattedContents.append(rowContent)
        
    xlsxContents[xlsxFile] = formattedContents


# In[7]:


print(np.array(xlsxContents[xlsxFiles[0]]))


# In[8]:


'''
print(xlsxContents[0].columns)
print(xlsxContents[0]["LatitudeDegrees"].values)
print(xlsxContents[0]["LongitudeDegrees"].values)
print(xlsxContents[0]["TimeSeconds"].values)
'''


# In[67]:


def getAvgPath(listOfXlsxFiles, xlsxContentDict):
    pathAvg = []
    lowestCommonPathLength = min([len(xlsxContentDict[file]) for file in listOfXlsxFiles])
    
    for i in range(lowestCommonPathLength):
        coords = [0, 0]
        for file in listOfXlsxFiles:
            coords[0] += xlsxContentDict[file][i][0]
            coords[1] += xlsxContentDict[file][i][1]
        
        coords[0] /= len(listOfXlsxFiles)
        coords[1] /= len(listOfXlsxFiles)
        pathAvg.append(coords)
    
    return pathAvg

secondPath = [1,3,4,5,6,7,8,9,10,11,12,13,14,16,17,18,19]
exceptions = [2, 15, 20]
firstPath = list(set(range(0,20)) - set(secondPath) - set(exceptions))

print(firstPath)

# First Path
#averagedList = [xlsxFiles[i] for i in firstPath]

# Second Path
averagedList = [xlsxFiles[i] for i in secondPath]

avgPath = np.array(getAvgPath(averagedList, xlsxContents)[:])


# In[68]:


x = [coords[0] for coords in avgPath]
y = [coords[1] for coords in avgPath]

secondPath = set([1, 3, 4, 7, 9, 10, 12, 14, 15, 19])
exceptions = set([8, 11, 18, 20])

plt.scatter(y, x)
plt.show()


# In[ ]:




