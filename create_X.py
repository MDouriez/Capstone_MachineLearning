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

X = pd.DataFrame(data[0].Time_stamp)
for i in xrange(len(data)):
    X = pd.merge(X,data[i], how ='outer', on = 'Time_stamp')
    
# export final instances as csv    
export = open("X_fixed.csv", "wb")
open_file_object = csv.writer(export)
open_file_object.writerow(X.columns)
open_file_object.writerows(np.asarray(X))
export.close()
