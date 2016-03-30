############## README ######### 
#to change: value_type, file_name, time_reference, name of the output file, 


####### script
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import processFile
import datetime as dt
import pandas as pd
import csv

# enter sensor type (pressure, accelerometer, humidity, magnetometer, temperature)
value_type = "accelerometer"

# indicate if file type is new (with sensor id) or old (first version of the csv files): True or False
new = True

# enter file name
file = 'C:\Users\Ludovic\Documents\Capstone\Capstone_MachineLearning\example.csv'

# reference
time_reference = dt.datetime(2016,2,20,0,44,50,265999)

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

def update_time_window_start(time):
    return time + dt.timedelta(0,60)


########### initialization

temp = list(zip(time,dataN))  #temporary list to prepare for the data frame (using pandas)
df = pd.DataFrame(data = temp, columns = ['Time', 'Data']) #data frame (using pandas)
time_window_start = time_reference 
feature_list = []
# number of data points
n = data.shape[0]
# counter, to determine how many data points from the file have been processed (so that we know if we should stop or not)
count = 0

######### create feature for each time window
while count < n:    
    temp = df[(df['Time'] >= time_window_start) & (df['Time'] < (time_window_start + dt.timedelta(0,60)))]  #select only data in time window
    count = count + len(temp.Data) # update to have a terminating condition
    #append features
    feature_list.append([time_window_start,mean(temp.Data),maxi(temp.Data),mini(temp.Data), max_minus_min(temp.Data), std(temp.Data), variance(temp.Data), RMS(temp.Data), hour_of_day(time_window_start)])
    # update time window
    time_window_start = update_time_window_start(time_window_start)

######## export features in a new csv file
export = open("sensor.csv", "wb")
open_file_object = csv.writer(export)
open_file_object.writerow(["Time_stamp","Mean","Max","Min","Max-Min","Std","Variance","RMS","hour"])
open_file_object.writerows(np.asarray(feature_list))
export.close()