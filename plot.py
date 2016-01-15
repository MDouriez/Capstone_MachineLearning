
import numpy as np
import matplotlib.pyplot as plt
import processFile

# enter sensor type (pressure, accelerometer, humidity, magnetometer, temperature, luxometer)
value_type = "accelerometer"

# indicate if file type is new (with sensor id) or old (first version of the csv files): True or False
new = True

unit = {}
unit['temperature'] = 'C'
unit['accelerometer'] = 'G'
unit['humidity'] = 'rH'
unit['magnetometer'] = 'uT'
unit['pressure'] = 'mbar'


# enter file name
file = 'sensortag_debug_20160110101356_1000lines B0:B4:48:BF:66:85 Accelerometer(G).csv'

time, data = processFile.openFile(file, value_type, new)

if value_type == "luxometer":
    m = data.shape[0]
    for i in range(m):
        if data[i] > 100000:
            data[i] = 200

print data
print time

print data.shape

if value_type in {"accelerometer", "magnetometer"}:
    dataX = data[:,0]
    dataY = data[:,1]
    dataZ = data[:,2]

    plt.plot(time, dataX, color='r', label=value_type[:3]+'X')
    plt.plot(time, dataY, color='b', label=value_type[:3]+'Y')
    plt.plot(time, dataZ, color='g', label=value_type[:3]+'Z')

elif value_type == "temperature":
    ambient_temp = data[:,0]
    object_temp = data[:,1]

    plt.plot(time, ambient_temp, color='r', label='Ambient_temp')
    plt.plot(time, object_temp, color='b', label='Object_temp')

else:
   plt.plot(time, data, color='r', label=value_type)


plt.xlabel('Time (hours)')
plt.ylabel(value_type.capitalize() + ' (' + unit[value_type] + ')')
plt.legend(loc='best')
plt.show()
