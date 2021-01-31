# -*- coding: utf-8 -*-

# Author: Grace Cappella
# Date: 9/23/20
# Purpose: IIPHYS-342 HW1 Solar Wind Data Investigation

#---------- Import Libraries

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import matplotlib.colors as mcolors

#---------- File Directories

filedir = "C:/Users/daugh/OneDrive/Documents/FA2020/IIPHYS-342 Data Analysis for Scientists/Week 4/"
filename = filedir + "SWdata.csv"

#---------- Read in Data Files

data = pd.read_csv(filename, skiprows = 115, skipfooter = 3, usecols = [0,1,2,3,4,5,6], engine = "python")
#change column names for ease
newColumnNames = ["time", "flowspeed", "protondensity", "temp", "NaNpRatio", "plasmabeta", "symH"]
data.columns = newColumnNames
#print(data.columns)


#---------- Get Rid of Bad Data

#notes:
#print statements were used to obtain real max and min values of the data. 
#bad data fill values identified as 9's using https://omniweb.gsfc.nasa.gov/html/ow_data.html

#99999.9 indicates bad flowspeed data
#find the real max flowspeed
FSlist = data.flowspeed.tolist()
FSsize = data.flowspeed.size

max_val = data.flowspeed.max()
real_max = 0
for i in range(0,FSsize):
    if FSlist[i] > real_max and FSlist[i] < max_val:
        real_max = FSlist[i]
#replace bad data values
indx = np.where(data.flowspeed==99999.9)[0]
data.flowspeed[indx]=np.nan
#print(str(real_max))
#print(str(data.flowspeed.min()))
# Real max: 846.7 Real min: 251.7

#999.99 indicates bad protondensity data
#find the real max protondensity
PDlist = data.protondensity.tolist()
PDsize = data.protondensity.size

max_val = data.protondensity.max()
real_max = 0
for i in range(0,PDsize):
    if PDlist[i] > real_max and PDlist[i] < max_val:
        real_max = PDlist[i]
#replace bad data values
indx = np.where(data.protondensity==999.99)[0]
data.protondensity[indx]=np.nan
#print(str(real_max))
#print(str(data.protondensity.min()))
# Real max: 69.36 Real min: 0.14

#10000000 indicates bad temp data
#find the real max temp
Tlist = data.temp.tolist()
Tsize = data.temp.size

max_val = data.temp.max()
real_max = 0
for i in range(0,Tsize):
    if Tlist[i] > real_max and Tlist[i] < max_val:
        real_max = Tlist[i]
#replace bad data values
indx = np.where(data.temp==10000000)[0]
data.temp[indx]=np.nan
#print(str(real_max))
#print(str(data.temp.min()))
# Real max: 3,968,030 Real min: 1067

#9.999 indicates bad NaNpRatio
#find the real max NaNpRatio
NNRlist = data.NaNpRatio.tolist()
NNRsize = data.NaNpRatio.size

max_val = data.NaNpRatio.max()
real_max = 0
for i in range(0,NNRsize):
    if NNRlist[i] > real_max and NNRlist[i] < max_val:
        real_max = NNRlist[i]
#replace bad data values
indx = np.where(data.NaNpRatio==9.999)[0]
data.NaNpRatio[indx]=np.nan
#print(str(real_max))
#print(str(data.NaNpRatio.min()))
# Real max: 0.372 Real min: 0.001

#999.99 indicates bad plasmabeta
#find the real max plasmabeta
PBlist = data.plasmabeta.tolist()
PBsize = data.plasmabeta.size

max_val = data.plasmabeta.max()
real_max = 0
for i in range(0,PBsize):
    if PBlist[i] > real_max and PBlist[i] < max_val:
        real_max = PBlist[i]
#replace bad data values
indx = np.where(data.plasmabeta==999.99)[0]
data.plasmabeta[indx]=np.nan
#print(str(real_max))
#print(str(data.plasmabeta.min()))
# Real max: 998 Real min: 0.01

#there doesn't appear to be bad symH
#print(str(data.symH.max()))
#print(str(data.symH.min()))
# Real max: 78 Real min: -205

#********** Handling DateTimes

#***combine dates and times into one string
# note: this MUST be run for program to work correctly

#find how many points there are
numpts = data.time.shape[0]
#make an empty array to hold the datetimes
date_dt = [0 for i in range(numpts)]
#loop to combine dates and times
for i in range(0,numpts):
    #combine date & time into 1 string
    tempdate = data.time[i]
    #turn into a datetime, save in the ith location of the array
    date_dt[i] = dt.datetime.strptime(tempdate,"%Y-%m-%dT%H:%M:%S.000Z") 
    
#make a new column in the data to store the datetimes
data["datetime"] = date_dt

#***grab just hours, day and month instead of entire datetime
#   and save as columns in data

data["hours"] = data.datetime.dt.hour + data.datetime.dt.minute/60. + data.datetime.dt.second/3600.
data["day"] = data.datetime.dt.day
data["month"] = data.datetime.dt.month
data["year"] = data.datetime.dt.year

#---------- Find high and low flowspeeds

indxHi = np.where((data.flowspeed>=500))[0]
indxLo = np.where((data.flowspeed<500))[0]

#---------- Find specific time periods of data

indx2016 = np.where((data.year==2016))[0]
indx2016_10 = np.where(((data.year==2016)&(data.month==10)))[0]
indx2016_8 = np.where(((data.year==2016)&(data.month==8)))[0]
indx2017_4 = np.where(((data.year==2017)&(data.month==4)))[0]

#---------- Rolling Average for Data Smoothing

symHrollAvg = data.symH.rolling(500,center=True).mean()

#---------- Plot ICMEs with symH vs time

# 2016 ICMEs
'''
plt.figure(figsize=(10,5))
plt.plot(data.datetime, data.symH)
plt.plot(data.datetime, symHrollAvg)
plt.xlim(pd.Timestamp("2016-07-31"),pd.Timestamp("2016-08-15"))
plt.xlabel("Time")
plt.ylabel("symH, nT (<-50 nT means storms)")
plt.title("August 2-3, 2016 ICME")

plt.figure(figsize=(10,5))
plt.plot(data.datetime, data.symH)
plt.plot(data.datetime, symHrollAvg)
plt.xlim(pd.Timestamp("2016-10-07"),pd.Timestamp("2016-10-21"))
plt.xlabel("Time")
plt.ylabel("symH, nT (<-50 nT means storms)")
plt.title("October 13-14, 2016 ICME")

plt.figure(figsize=(10,5))
plt.plot(data.datetime, data.symH)
plt.plot(data.datetime, symHrollAvg)
plt.xlim(pd.Timestamp("2016-10-28"),pd.Timestamp("2016-11-11"))
plt.xlabel("Time")
plt.ylabel("symH, nT (<-50 nT means storms)")
plt.title("November 4-5, 2016 ICME")

plt.figure(figsize=(10,5))
plt.plot(data.datetime, data.symH)
plt.plot(data.datetime, symHrollAvg)
plt.xlim(pd.Timestamp("2016-11-04"),pd.Timestamp("2016-11-18"))
plt.xlabel("Time")
plt.ylabel("symH, nT (<-50 nT means storms)")
plt.title("November 10, 2016 ICME")
'''

# 2017 ICMEs
'''
plt.figure(figsize=(10,5))
plt.plot(data.datetime, data.symH)
plt.plot(data.datetime, symHrollAvg)
plt.xlim(pd.Timestamp("2017-03-28"),pd.Timestamp("2017-04-11"))
plt.xlabel("Time")
plt.ylabel("symH, nT (<-50 nT means storms)")
plt.title("April 4, 2017 ICME")

plt.figure(figsize=(10,5))
plt.plot(data.datetime, data.symH)
plt.plot(data.datetime, symHrollAvg)
plt.xlim(pd.Timestamp("2017-04-02"),pd.Timestamp("2017-04-17"))
plt.xlabel("Time")
plt.ylabel("symH, nT (<-50 nT means storms)")
plt.title("April 9-10, 2017 ICME")

plt.figure(figsize=(10,5))
plt.plot(data.datetime, data.symH)
plt.plot(data.datetime, symHrollAvg)
plt.xlim(pd.Timestamp("2017-04-07"),pd.Timestamp("2017-04-21"))
plt.xlabel("Time")
plt.ylabel("symH, nT (<-50 nT means storms)")
plt.title("April 14-15, 2017 ICME")

plt.figure(figsize=(10,5))
plt.plot(data.datetime, data.symH)
plt.plot(data.datetime, symHrollAvg)
plt.xlim(pd.Timestamp("2017-05-20"),pd.Timestamp("2017-06-06"))
plt.xlabel("Time")
plt.ylabel("symH, nT (<-50 nT means storms)")
plt.title("May 27-29, 2017 ICME")

plt.figure(figsize=(10,5))
plt.plot(data.datetime, data.symH)
plt.plot(data.datetime, symHrollAvg)
plt.xlim(pd.Timestamp("2017-07-09"),pd.Timestamp("2017-07-24"))
plt.xlabel("Time")
plt.ylabel("symH, nT (<-50 nT means storms)")
plt.title("July 16-17, 2017 ICME")

plt.figure(figsize=(10,5))
plt.plot(data.datetime, data.symH)
plt.plot(data.datetime, symHrollAvg)
plt.xlim(pd.Timestamp("2017-08-15"),pd.Timestamp("2017-08-30"))
plt.xlabel("Time")
plt.ylabel("symH, nT (<-50 nT means storms)")
plt.title("August 22-23, 2017 ICME")

plt.figure(figsize=(10,5))
plt.plot(data.datetime, data.symH)
plt.plot(data.datetime, symHrollAvg)
plt.xlim(pd.Timestamp("2017-09-01"),pd.Timestamp("2017-09-15"))
plt.xlabel("Time")
plt.ylabel("symH, nT (<-50 nT means storms)")
plt.title("September 7-8, 2017 ICME")

plt.figure(figsize=(10,5))
plt.plot(data.datetime, data.symH)
plt.plot(data.datetime, symHrollAvg)
plt.xlim(pd.Timestamp("2017-09-01"),pd.Timestamp("2017-09-17"))
plt.xlabel("Time")
plt.ylabel("symH, nT (<-50 nT means storms)")
plt.title("September 8-10, 2017 ICME")

plt.figure(figsize=(10,5))
plt.plot(data.datetime, data.symH)
plt.plot(data.datetime, symHrollAvg)
plt.xlim(pd.Timestamp("2017-12-18"),pd.Timestamp("2018-01-02"))
plt.xlabel("Time")
plt.ylabel("symH, nT (<-50 nT means storms)")
plt.title("December 25-26, 2017 ICME")
'''

# 2018 ICMEs
'''
plt.figure(figsize=(10,5))
plt.plot(data.datetime, data.symH)
plt.plot(data.datetime, symHrollAvg)
plt.xlim(pd.Timestamp("2018-03-02"),pd.Timestamp("2018-03-18"))
plt.xlabel("Time")
plt.ylabel("symH, nT (<-50 nT means storms)")
plt.title("March 9-11, 2018 ICME")

plt.figure(figsize=(10,5))
plt.plot(data.datetime, data.symH)
plt.plot(data.datetime, symHrollAvg)
plt.xlim(pd.Timestamp("2018-05-06"),pd.Timestamp("2018-05-21"))
plt.xlabel("Time")
plt.ylabel("symH, nT (<-50 nT means storms)")
plt.title("May 13, 2018 ICME")

plt.figure(figsize=(10,5))
plt.plot(data.datetime, data.symH)
plt.plot(data.datetime, symHrollAvg)
plt.xlim(pd.Timestamp("2018-05-31"),pd.Timestamp("2018-06-14"))
plt.xlabel("Time")
plt.ylabel("symH, nT (<-50 nT means storms)")
plt.title("June 6-7, 2018 ICME")

plt.figure(figsize=(10,5))
plt.plot(data.datetime, data.symH)
plt.plot(data.datetime, symHrollAvg)
plt.xlim(pd.Timestamp("2018-06-18"),pd.Timestamp("2018-07-03"))
plt.xlabel("Time")
plt.ylabel("symH, nT (<-50 nT means storms)")
plt.title("June 25-26, 2018 ICME")

plt.figure(figsize=(10,5))
plt.plot(data.datetime, data.symH)
plt.plot(data.datetime, symHrollAvg)
plt.xlim(pd.Timestamp("2018-06-23"),pd.Timestamp("2018-07-09"))
plt.xlabel("Time")
plt.ylabel("symH, nT (<-50 nT means storms)")
plt.title("June 30-July 2, 2018 ICME")

plt.figure(figsize=(10,5))
plt.plot(data.datetime, data.symH)
plt.plot(data.datetime, symHrollAvg)
plt.xlim(pd.Timestamp("2018-07-03"),pd.Timestamp("2018-07-18"))
plt.xlabel("Time")
plt.ylabel("symH, nT (<-50 nT means storms)")
plt.title("July 10-11, 2018 ICME")

plt.figure(figsize=(10,5))
plt.plot(data.datetime, data.symH)
plt.plot(data.datetime, symHrollAvg)
plt.xlim(pd.Timestamp("2018-08-18"),pd.Timestamp("2018-09-02"))
plt.xlabel("Time")
plt.ylabel("symH, nT (<-50 nT means storms)")
plt.title("August 25-26, 2018 ICME")

plt.figure(figsize=(10,5))
plt.plot(data.datetime, data.symH)
plt.plot(data.datetime, symHrollAvg)
plt.xlim(pd.Timestamp("2018-09-16"),pd.Timestamp("2018-10-01"))
plt.xlabel("Time")
plt.ylabel("symH, nT (<-50 nT means storms)")
plt.title("September 23-24, 2018 ICME")
'''

# 2019 ICMEs
'''
plt.figure(figsize=(10,5))
plt.plot(data.datetime, data.symH)
plt.plot(data.datetime, symHrollAvg)
plt.xlim(pd.Timestamp("2019-04-30"),pd.Timestamp("2019-05-16"))
plt.xlabel("Time")
plt.ylabel("symH, nT (<-50 nT means storms)")
plt.title("May 7-9, 2019 ICME")

plt.figure(figsize=(10,5))
plt.plot(data.datetime, data.symH)
plt.plot(data.datetime, symHrollAvg)
plt.xlim(pd.Timestamp("2019-05-04"),pd.Timestamp("2019-05-20"))
plt.xlabel("Time")
plt.ylabel("symH, nT (<-50 nT means storms)")
plt.title("May 11-13, 2019 ICME")

plt.figure(figsize=(10,5))
plt.plot(data.datetime, data.symH)
plt.plot(data.datetime, symHrollAvg)
plt.xlim(pd.Timestamp("2019-05-07"),pd.Timestamp("2019-05-23"))
plt.xlabel("Time")
plt.ylabel("symH, nT (<-50 nT means storms)")
plt.title("May 14-15, 2019 ICMEs")

plt.figure(figsize=(10,5))
plt.plot(data.datetime, data.symH)
plt.plot(data.datetime, symHrollAvg)
plt.xlim(pd.Timestamp("2019-05-09"),pd.Timestamp("2019-05-25"))
plt.xlabel("Time")
plt.ylabel("symH, nT (<-50 nT means storms)")
plt.title("May 16-18, 2019 ICME")

plt.figure(figsize=(10,5))
plt.plot(data.datetime, data.symH)
plt.plot(data.datetime, symHrollAvg)
plt.xlim(pd.Timestamp("2019-05-20"),pd.Timestamp("2019-06-04"))
plt.xlabel("Time")
plt.ylabel("symH, nT (<-50 nT means storms)")
plt.title("May 27-28, 2019 ICME")

plt.figure(figsize=(10,5))
plt.plot(data.datetime, data.symH)
plt.plot(data.datetime, symHrollAvg)
plt.xlim(pd.Timestamp("2019-10-22"),pd.Timestamp("2019-11-10"))
plt.xlabel("Time")
plt.ylabel("symH, nT (<-50 nT means storms)")
plt.title("October 29-30, November 2-3, 2019 ICME")

plt.figure(figsize=(10,5))
plt.plot(data.datetime, data.symH)
plt.plot(data.datetime, symHrollAvg)
plt.xlim(pd.Timestamp("2019-10-26"),pd.Timestamp("2019-11-10"))
plt.xlabel("Time")
plt.ylabel("symH, nT (<-50 nT means storms)")
plt.title("November 2-3, 2019 ICME")

plt.figure(figsize=(10,5))
plt.plot(data.datetime, data.symH)
plt.plot(data.datetime, symHrollAvg)
plt.xlim(pd.Timestamp("2019-11-04"),pd.Timestamp("2019-11-19"))
plt.xlabel("Time")
plt.ylabel("symH, nT (<-50 nT means storms)")
plt.title("November 11-12, 2019 ICME")
'''

# 2020 ICMEs (through April; later data not available)
'''
plt.figure(figsize=(10,5))
plt.plot(data.datetime, data.symH)
plt.plot(data.datetime, symHrollAvg)
plt.xlim(pd.Timestamp("2019-12-28"),pd.Timestamp("2020-01-12"))
plt.xlabel("Time")
plt.ylabel("symH, nT (<-50 nT means storms)")
plt.title("January 4-5, 2020 ICME")

plt.figure(figsize=(10,5))
plt.plot(data.datetime, data.symH)
plt.plot(data.datetime, symHrollAvg)
plt.xlim(pd.Timestamp("2020-02-11"),pd.Timestamp("2020-02-26"))
plt.xlabel("Time")
plt.ylabel("symH, nT (<-50 nT means storms)")
plt.title("February 18-19, 2020 ICME")

plt.figure(figsize=(10,5))
plt.plot(data.datetime, data.symH)
plt.plot(data.datetime, symHrollAvg)
plt.xlim(pd.Timestamp("2020-04-13"),pd.Timestamp("2020-04-28"))
plt.xlabel("Time")
plt.ylabel("symH, nT (<-50 nT means storms)")
plt.title("April 20-21, 2020 ICME")
'''



#---------- ICMEs with at least -50 nT drop in symH
#colorbar labels must be changed as well as vmin and vmax

# flowspeed colorbar--scatterplot: vmin = 200, vmax = 900
'''
colors1 = plt.cm.Spectral(np.linspace(1,.55,128))
colors2 = plt.cm.Spectral(np.linspace(.45,0,128))
colors = np.vstack((colors1, colors2))
mymap = mcolors.LinearSegmentedColormap.from_list('my_colormap', colors)
clrs = data.flowspeed
'''
# protondensity colorbar--scatterplot: vmin = 0, vmax = 70
'''
colors1 = plt.cm.Spectral(np.linspace(1,.55,128))
colors2 = plt.cm.Spectral(np.linspace(.45,0,128))
colors = np.vstack((colors1, colors2))
mymap = mcolors.LinearSegmentedColormap.from_list('my_colormap', colors)
clrs = data.protondensity
'''
# temperature colorbar--scatterplot: vmin = 0; vmax = 4,000,000
'''
colors1 = plt.cm.Spectral(np.linspace(1,.55,64))
colors2 = plt.cm.Spectral(np.linspace(.45,0,192))
colors = np.vstack((colors1, colors2))
mymap = mcolors.LinearSegmentedColormap.from_list('my_colormap', colors)
clrs = data.temp
'''
# plasmabeta colorbar--scatterplot: vmin = 0, vmax = 40
'''
colors1 = plt.cm.Spectral(np.linspace(1,.55,128))
colors2 = plt.cm.Spectral(np.linspace(.45,0,128))
colors = np.vstack((colors1, colors2))
mymap = mcolors.LinearSegmentedColormap.from_list('my_colormap', colors)
clrs = data.plasmabeta
'''

# CURRENTLY SET FOR PLASMABETA
#*** 2016 symH drop ICMEs
'''
plt.figure(figsize=(10,5))
plt.scatter(data.datetime, data.symH, c=clrs, vmin=0, vmax=40, cmap=mymap)
cbar = plt.colorbar()
cbar.set_label("Plasma Beta", rotation=270)
plt.xlim(pd.Timestamp("2016-07-31"),pd.Timestamp("2016-08-05"))
plt.xlabel("Time")
plt.ylabel("symH, nT (<-50 nT means storms)")
plt.title("August 2-3, 2016 ICME")

plt.figure(figsize=(10,5))
plt.scatter(data.datetime, data.symH, c=clrs, vmin=0, vmax=40, cmap=mymap)
cbar = plt.colorbar()
cbar.set_label("Plasma Beta", rotation=270)
plt.xlim(pd.Timestamp("2016-10-11"),pd.Timestamp("2016-10-16"))
plt.xlabel("Time")
plt.ylabel("symH, nT (<-50 nT means storms)")
plt.title("October 13-14, 2016 ICME")

plt.figure(figsize=(10,5))
plt.scatter(data.datetime, data.symH, c=clrs, vmin=0, vmax=40, cmap=mymap)
cbar = plt.colorbar()
cbar.set_label("Plasma Beta", rotation=270)
plt.xlim(pd.Timestamp("2016-11-08"),pd.Timestamp("2016-11-12"))
plt.xlabel("Time")
plt.ylabel("symH, nT (<-50 nT means storms)")
plt.title("November 10, 2016 ICME")
'''

#*** 2017 symH drop ICMEs
'''
plt.figure(figsize=(10,5))
plt.scatter(data.datetime, data.symH, c=clrs, vmin=0, vmax=40, cmap=mymap)
cbar = plt.colorbar()
cbar.set_label("Plasma Beta", rotation=270)
plt.xlim(pd.Timestamp("2017-04-02"),pd.Timestamp("2017-04-04"))
plt.xlabel("Time")
plt.ylabel("symH, nT (<-50 nT means storms)")
plt.title("April 4, 2017 ICME")

plt.figure(figsize=(10,5))
plt.scatter(data.datetime, data.symH, c=clrs, vmin=0, vmax=40, cmap=mymap)
cbar = plt.colorbar()
cbar.set_label("Plasma Beta", rotation=270)
plt.xlim(pd.Timestamp("2017-05-25"),pd.Timestamp("2017-05-31"))
plt.xlabel("Time")
plt.ylabel("symH, nT (<-50 nT means storms)")
plt.title("May 27-29, 2017 ICME")

plt.figure(figsize=(10,5))
plt.scatter(data.datetime, data.symH, c=clrs, vmin=0, vmax=40, cmap=mymap)
cbar = plt.colorbar()
cbar.set_label("Plasma Beta", rotation=270)
plt.xlim(pd.Timestamp("2017-07-14"),pd.Timestamp("2017-07-19"))
plt.xlabel("Time")
plt.ylabel("symH, nT (<-50 nT means storms)")
plt.title("July 16-17, 2017 ICME")

plt.figure(figsize=(10,5))
plt.scatter(data.datetime, data.symH, c=clrs, vmin=0, vmax=40, cmap=mymap)
cbar = plt.colorbar()
cbar.set_label("Plasma Beta", rotation=270)
plt.xlim(pd.Timestamp("2017-09-06"),pd.Timestamp("2017-09-11"))
plt.xlabel("Time")
plt.ylabel("symH, nT (<-50 nT means storms)")
plt.title("September 7-8 and 8-10, 2017 ICMEs")
'''

#*** 2018 symH drop ICMEs
'''
plt.figure(figsize=(10,5))
plt.scatter(data.datetime, data.symH, c=clrs, vmin=0, vmax=40, cmap=mymap)
cbar = plt.colorbar()
cbar.set_label("Plasma Beta", rotation=270)
plt.xlim(pd.Timestamp("2018-03-07"),pd.Timestamp("2018-03-13"))
plt.xlabel("Time")
plt.ylabel("symH, nT (<-50 nT means storms)")
plt.title("March 9-11, 2018 ICME")

plt.figure(figsize=(10,5))
plt.scatter(data.datetime, data.symH, c=clrs, vmin=0, vmax=40, cmap=mymap)
cbar = plt.colorbar()
cbar.set_label("Plasma Beta", rotation=270)
plt.xlim(pd.Timestamp("2018-08-23"),pd.Timestamp("2018-08-28"))
plt.xlabel("Time")
plt.ylabel("symH, nT (<-50 nT means storms)")
plt.title("August 25-26, 2018 ICME")
'''

#*** 2019 symH drop ICMEs
'''
plt.figure(figsize=(10,5))
plt.scatter(data.datetime, data.symH, c=clrs, vmin=0, vmax=40, cmap=mymap)
cbar = plt.colorbar()
cbar.set_label("Plasma Beta", rotation=270)
plt.xlim(pd.Timestamp("2019-05-09"),pd.Timestamp("2019-05-17"))
plt.xlabel("Time")
plt.ylabel("symH, nT (<-50 nT means storms)")
plt.title("May 11-13 and 14-15, 2019 ICME")
'''

#*** 2020 symH drop ICMEs
'''
plt.figure(figsize=(10,5))
plt.scatter(data.datetime, data.symH, c=clrs, vmin=0, vmax=40, cmap=mymap)
cbar = plt.colorbar()
cbar.set_label("Plasma Beta", rotation=270)
plt.xlim(pd.Timestamp("2020-02-16"),pd.Timestamp("2020-02-21"))
plt.xlabel("Time")
plt.ylabel("symH, nT (<-50 nT means storms)")
plt.title("February 18-19, 2020 ICME")
'''
'''
plt.figure(figsize=(10,5))
plt.scatter(data.datetime, data.symH, c=clrs, vmin=0, vmax=40, cmap=mymap)
cbar = plt.colorbar()
cbar.set_label("Plasma Beta", rotation=270)
plt.xlim(pd.Timestamp("2020-04-18"),pd.Timestamp("2020-04-23"))
plt.xlabel("Time")
plt.ylabel("symH, nT (<-50 nT means storms)")
plt.title("April 20-21, 2020 ICME")
'''



#---------- Plot Data
'''
#---plot each variable against time

#flowspeed
plt.figure(figsize=(8,10))

plt.subplot(6,1,1).xaxis.set_visible(False) #hides tick labels for that subplot so they don't peek out the side
plt.plot(data.datetime, data.flowspeed)
plt.ylabel("Flow Speed,\nkm/s", labelpad = 20)

#proton density
plt.subplot(6,1,2).xaxis.set_visible(False)
plt.plot(data.datetime, data.protondensity)
plt.ylabel("Proton Density,\n$cm^-3$", labelpad = 25)

#temperature
plt.subplot(6,1,3).xaxis.set_visible(False)
plt.plot(data.datetime, data.temp)
plt.ylabel("Temperature, K")

#He nuclei to protons (NaNpRatio)
plt.subplot(6,1,4).xaxis.set_visible(False)
plt.plot(data.datetime, data.NaNpRatio)
plt.ylabel("NaNpRatio", labelpad = 30)

#plasma beta: >1 means more thermal pressure, <1 means more magnetic pressure
plt.subplot(6,1,5).xaxis.set_visible(False)
plt.plot(data.datetime, data.plasmabeta)
plt.ylabel("Plasma Beta", labelpad = 20)

#SymH: -50nT means small storms; the smaller the value, the larger the storm
plt.subplot(6,1,6)
plt.plot(data.datetime, data.symH)
plt.ylabel("SymH, nT", labelpad = 15)
plt.xlabel("Time")

#eliminate space between subplots so they share an x axis
plt.subplots_adjust(hspace = 0)
'''

#*** plot flow speed vs. proton density
'''
plt.figure()
plt.plot(data.flowspeed, data.protondensity, "m.")
plt.xlabel("Flow Speed, km/s")
plt.ylabel("Proton Density, $cm^-3$")

#*** plot flow speed vs time

plt.figure(figsize=(10,5))
plt.plot(data.datetime, data.flowspeed)
plt.xlabel("Time")
plt.ylabel("Proton Density, $cm^-3$")
'''
'''
#*** plot proton density vs flow speed for "high" flowspeeds

plt.figure()
plt.plot(data.protondensity[indxHi], data.flowspeed[indxHi], "m.")
plt.ylim(490,900)
plt.xlim(-2,70)
plt.ylabel("Flow Speed, km/s")
plt.xlabel("Proton Density, $cm^-3$")

'''
'''
#*** plot high flowspeeds vs time

plt.figure()
plt.plot(data.datetime[indxHi], data.flowspeed[indxHi], marker=".", linestyle='')
plt.xlabel("Time")
plt.ylabel("Flow Speed, km/s")
'''

#*** plot low flowspeeds and high flowspeeds against protondensity
'''
plt.figure()

plt.subplot(2,1,1)
plt.plot(data.datetime[indxHi], data.flowspeed[indxHi])
plt.ylabel("Flowspeed, km/s")

plt.subplot(2,1,2)
plt.plot(data.datetime[indxLo], data.flowspeed[indxLo])
plt.ylabel("Flowspeed, km/s")
plt.xlabel("Time")

plt.subplots_adjust(hspace = 0)
'''

#*** plot low and hi flowspeeds vs other variables
'''
# low flowspeed vs proton density
plt.figure()
plt.plot(data.protondensity[indxLo],data.flowspeed[indxLo], marker=".", linestyle="")
plt.ylabel("Flowspeed, km/s")
plt.xlabel("Proton Density, %cm^'2%")

# high flowspeed vs proton density
plt.figure()
plt.plot(data.protondensity[indxHi],data.flowspeed[indxHi], marker=".", linestyle="")
plt.ylabel("Flowspeed, km/s")
plt.xlabel("Proton Density, %cm^'2%")
'''
'''
# low flowspeed vs temperature
plt.figure()
plt.plot(data.temp[indxLo], data.flowspeed[indxLo], marker=".", linestyle="")
plt.ylabel("Flowspeed, km/s")
plt.xlabel("Temperature, K")

# high flowspeed vs temperature
plt.figure()
plt.plot(data.temp[indxHi], data.flowspeed[indxHi], marker=".", linestyle="")
plt.ylabel("Flowspeed, km/s")
plt.xlabel("Temperature, K")


# low flowspeed vs NaNpRatio
plt.figure()
plt.plot(data.NaNpRatio[indxLo],data.flowspeed[indxLo], marker=".", linestyle="")
plt.ylabel("Flowspeed, km/s")
plt.xlabel("NaNp Ratio")

# low flowspeed vs plasmabeta
plt.figure()
plt.plot(data.plasmabeta[indxLo], data.flowspeed[indxLo], marker=".", linestyle="")
plt.ylabel("Flowspeed, km/s")
plt.xlabel("Plasma Beta")

# low flowspeed vs. symH
plt.figure()
plt.plot(data.symH[indxLo], data.flowspeed[indxLo], marker=".", linestyle="")
plt.ylabel("Flowspeed, km/s")
plt.xlabel("SymH, nT")
'''

#*** plot symH over SMALL time intervals
'''
plt.figure(figsize=(12,8))
plt.plot(data.datetime[indx2016_10],data.symH[indx2016_10])

plt.figure(figsize=(12,8))
plt.plot(data.datetime[indx2016_8],data.symH[indx2016_8])
'''
'''
plt.figure(figsize=(12,8))
plt.plot(data.datetime[indx2017_4],data.symH[indx2017_4])
plt.xlabel("Time")
plt.ylabel("symH, nT")
'''

