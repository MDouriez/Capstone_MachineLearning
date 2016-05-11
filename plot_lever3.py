'''
Script used to detect the usage of a toilet flush 

'''


import numpy as np
import matplotlib.pyplot as plt
import processFile
import math
import pandas as pd


# enter sensor type (pressure, accelerometer, humidity, magnetometer, temperature)
value_type = "magnetometer"

# enter file name
file = 'C:\Users\Ludovic\Documents\Capstone\mesures\_flush_lever_phoenix.csv'

# indicate if file type is new (with sensor id) or old (first version of the csv files): True or False
new = True

unit = {}
unit['temperature'] = 'C'
unit['accelerometer'] = 'G'
unit['humidity'] = 'rH'
unit['magnetometer'] = 'uT'
unit['pressure'] = 'mbar'
unit['gyroscope'] = 'deg/s'

time, data = processFile.openFile(file, value_type, new, False)


if value_type in {"magnetometer"}:
    dataX = data[:,0]
    dataY = data[:,1]
    dataZ = data[:,2]
    dataN = np.sqrt(dataX*dataX+dataY*dataY+dataZ*dataZ)
    plt.plot(time, dataN, color='r', label = 'Norm of magnetic field')  #absolute value of the Y axis of magnetometer
    
elif value_type == "accelerometer":
    accelerometerX = data[:,0]
    accelerometerY = data[:,1]
    accelerometerZ = data[:,2]
    #    plt.plot(time, accelerometerX, color='r', label = value_type+'X')
    #   plt.plot(time, accelerometerY, color='b', label = value_type+'Y')
    #  plt.plot(time, accelerometerZ, color='g', label = value_type+'Z')

    dataN = np.sqrt(accelerometerX*accelerometerX+accelerometerY*accelerometerY+accelerometerZ*accelerometerZ)
    plt.plot(time, dataN, color='r', label = value_type+'Norm')

elif value_type == "gyroscope":
    gX = data[:,0]
    gY = data[:,1]
    gZ = data[:,2]
    #    plt.plot(time, accelerometerX, color='r', label = value_type+'X')
    #   plt.plot(time, accelerometerY, color='b', label = value_type+'Y')
    #  plt.plot(time, accelerometerZ, color='g', label = value_type+'Z')

    dataN = np.sqrt(gX*gX+gY*gY+gZ*gZ)
    plt.plot(time, dataN, color='r', label = value_type+'Norm')

elif value_type == "temperature":
    ambient_temp = data[:,0]
    object_temp = data[:,1]

    plt.plot(time, ambient_temp, color='r', label = 'ambient_temp')
    plt.plot(time, object_temp, color='b', label = 'object_temp')

else:
   plt.plot(time, data, color='r', label = value_type)


plt.xlabel('Time (minutes)')
plt.ylabel(value_type.capitalize() + ' (' + unit[value_type] + ')')
plt.legend(loc='best')
plt.title('Simulations of pillbox usage')
plt.show()  


'''
# event recognition based on threshold comparison

print dataX[:10]
print dataY[:10]
print dataZ[:10]
print dataN[:10]


temp = list(zip(time,dataN))  #temporary list to prepare for the data frame (using pandas)
df = pd.DataFrame(data = temp, columns = ['Time', 'Data']) #data frame (using pandas)

#print len(df)
#print df[:10]
#print df.Data[:10]
#define time window
#print df
print max(time)


count = 0 # used to count the number of openings detected

timer_temp = 0 # used for comparison with timer, to determine false positives
threshold = 150 # threshold used to for comparison with the readings, to detect openings

foo = [0]
print int(math.floor(max(time))/window)
for i in range(1,int(math.floor(max(time))/window)):
    #the loop goes through the entire file
    #temp contains the data for only one time window
    temp = df[(df['Time'] > timer) & (df['Time'] < timer + window)]
    print temp
    if len(temp) >0:
        print temp[:5]
        if max(temp.Data) > threshold: #compares the max of each time window to threshold
            count = count + 1 
            #print temp[:5]
            #print "length temp", len(temp)
            #print "max temp", max(temp.Data)
            #print "count", count
            #print "timer", timer
            if timer_temp == timer - window :  #avoids double counts
                foo.append(timer) 
            timer_temp = timer 
    timer = timer + window 

print count
print foo

'''


temp = list(zip(time,dataN))  #temporary list to prepare for the data frame (using pandas)
df = pd.DataFrame(data = temp, columns = ['Time', 'Data']) #data frame (using pandas)

window = 1  #define time window
timer = 0 # used in the for loop

temp = [{'time': 0, 'value': 0, 'event': 0}]
results = pd.DataFrame(temp)  # will contain 3 columns; time = time of the time window, value = max value in the time window, event = dummy variable (1 if event, 0 otherwise)


for i in range(1,int(math.floor(max(time))/window)):
    # the loop goes through the entire file
    # temp contains the data for only one time window
    temp = df[(df['Time'] > timer) & (df['Time'] < timer + window)]
    if len(temp) >0:
        results.loc[i] = [0,max(temp.Time), max(temp.Data)]
    timer = timer + window 


print 'foo'
percent = 1.2

print 'max range', int(math.floor(max(time))/window)

count = 0 #counter for the loop to avoid out of array types errors
for index,row in results.iterrows():
    if count == 1:
        temp1 = results.value[index]
    if count == 2:
        temp2 = results.value[index]
    if count == 3:
        temp3 = results.value[index]
    if count == 4:
        temp4 = results.value[index]
    if count > 4:
        if (temp1*percent < results.value[index]) and (temp2*percent < results.value[index]) and (temp3*percent < results.value[index]) and (temp4*percent < results.value[index]):
            results.event[index] = 1
        temp1 = temp2
        temp2 = temp3
        temp3 = temp4
        temp4 = results.value[index]
    count = count + 1


print results[results['event'] == 1]
