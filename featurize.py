'''
Author: Ludovic
Input: sensor_type, csv_file_name, output_name
To change: time_reference, name of the output file

'''

####### script
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import processFile
import datetime as dt
import pandas as pd
import csv

# reference
time_reference = dt.datetime(2016,2,20,0,01,00,000000)

# enter sensor type (pressure, accelerometer, humidity, magnetometer, temperature)
value_type = sys.argv[1]

# indicate if file type is new (with sensor id) or old (first version of the csv files): True or False
new = True

# enter file name
#file = 'C:\Users\Ludovic\Documents\Capstone\Capstone_MachineLearning\example.csv'
file = sys.argv[2]

time, data = processFile.openFile(file, value_type, new, True)
print 'data.shape: ' , data.shape


if value_type in {"accelerometer", "magnetometer"}:
    dataX = data[:,0]
    dataY = data[:,1]
    dataZ = data[:,2]
    dataN = np.sqrt(dataX*dataX+dataY*dataY+dataZ*dataZ)
    
elif value_type == "temperature":
    dataN = data[:,0] # ambient_temp
    #object_temp = data[:,1]
    
elif value_type == "humidity":
    dataN = data[:,0] 
    
else:
    print "invalid value_type"


########## define features

def mean(vector):
    return np.mean(vector)

def maxi(vector):
    return np.max(vector)

def mini(vector):
    return np.min(vector)

def max_minus_min(vector):
    return np.max(vector) - np.min(vector)

def std(vector):
    return np.std(vector)

def variance(vector):
    return np.var(vector)

def RMS(vector):
    # returns Root Mean Square
    return np.sqrt(np.mean(np.square(vector)))

def hour_of_day(time_stamp):
    # returns the hour of the day of the time window
    return time_stamp.hour

def end_minus_start(vector):
    # returns the last element of the vector minus the first element of the vector
    # useful for slow evolutions (eg temperature
    if len(vector) >0:
    	return vector.iloc[-1]-vector.iloc[0]
    else:
    	return 0 

def update_time_window_start(time):
    return time + dt.timedelta(0,60)


########### initialization

print "Initializing..."

temp = list(zip(time,dataN))  #temporary list to prepare for the data frame (using pandas)
df = pd.DataFrame(data = temp, columns = ['Time', 'Data']) #data frame (using pandas)
time_window_start = time_reference 
feature_list = []
# number of data points
n = data.shape[0]
# counter, to determine how many data points from the file have been processed (so that we know if we should stop or not)
count = 0

######### create feature for each time window
print "Creating features..."

tracker_25 = 0

while count < n:    
    temp = df[(df['Time'] >= time_window_start) & (df['Time'] < (time_window_start + dt.timedelta(0,60)))]
    count = count + len(temp.Data)
    temp2 = temp[temp['Data'] !=0]
    feature_list.append([time_window_start,mean(temp2.Data),maxi(temp2.Data),mini(temp2.Data), max_minus_min(temp2.Data), std(temp2.Data), variance(temp2.Data), RMS(temp2.Data),end_minus_start(temp2.Data), hour_of_day(time_window_start)])
    # update time window
    time_window_start = update_time_window_start(time_window_start)
    if ((count/float(n) > .25) and (tracker_25 == 0)): 
    	tracker_25 = 1
    	print "25 percent reached"

    
######## export features in a new csv file
print "Exporting..."

output_name = sys.argv[3]

export = open(output_name, "wb")
open_file_object = csv.writer(export)
open_file_object.writerow(["Time_stamp","Mean","Max","Min","Max-Min","Std","Variance","RMS","End-Start","hour"])
open_file_object.writerows(np.asarray(feature_list))
export.close()

print "Done"
