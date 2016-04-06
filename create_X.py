'''
Author: Ludovic
Takes in argument the names of the files to merge
Returns a matrix with columns: (date, sensor1_feature1, sensor1_feature2, ..., sensorN_featureD, ...)

The only thing that needs to be changed manually is the time_reference and the duration
'''

import sys
#import featurize
import pandas as pd
import numpy as np
import datetime as dt
import csv

# datetime of reference
time_reference = dt.datetime(2016,2,25,0,01,00,000000)
duration = dt.timedelta(14) # 14 days

files = sys.argv[1:]

#files = ['sensor.csv','sensor0.csv']

# read the files and store in global var data
data =[]
for file in files:
    foo = pd.read_csv(file)
    data.append(foo)
    
# rename the columns for each file:

for i in xrange(len(data)):
    features_names = list(data[i].columns)
    features_new_names = ['Time_stamp']
    for j in xrange(len(features_names)-1):
        features_new_names.append(files[i]+"_"+features_names[j+1])
    data[i].columns = features_new_names

# for each file:
#    see the gaps between time reference and beginning of file
#    create an array of (#difference) rows and (1(time) + #features) columns
#    vstack
#    see the gaps between the end of time window and the end of file
#    create an array of (#difference) rows and (1(time) + #features) columns
#    vstack

for i in xrange(len(data)):
    # see gap between time ref and beginning of file
    min_time = dt.datetime.strptime(np.min(data[i].Time_stamp), '%Y-%m-%d %H:%M:%S')
    max_time = dt.datetime.strptime(np.max(data[i].Time_stamp), '%Y-%m-%d %H:%M:%S')

    # create an array of min_time- time_reference rows and (1(time) + #features) columns
    features_names = list(data[i].columns)
    index = pd.date_range(start = time_reference, end = min_time- dt.timedelta(0,0,60), freq='Min')
    foo = pd.DataFrame(index = index,columns = features_names)
    foo.Time_stamp = index
    
    #vstack
    bar = data[i]
    data[i] = pd.concat([foo,bar])

    # create an array of time_reference + duration - max_time rows and (1(time) + #features) columns
    features_names = list(data[i].columns)
    index = pd.date_range(start = max_time + dt.timedelta(0,60), end = time_reference + duration, freq='Min')
    foo = pd.DataFrame(index = index,columns = features_names)
    foo.Time_stamp = index
    
    #vstack
    bar = data[i]
    data[i] = pd.concat([bar,foo])

X = pd.DataFrame(data[0].Time_stamp)
for i in xrange(len(data)):
    X = pd.concat([X, data[i].ix[:, data[i].columns != 'Time_stamp']], axis=1, join_axes=[X.index])
    
# export final instances as csv    
export = open("X.csv", "wb")
open_file_object = csv.writer(export)
open_file_object.writerow(X.columns)
open_file_object.writerows(np.asarray(X))
export.close()