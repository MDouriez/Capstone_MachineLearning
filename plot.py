
import numpy as np
import matplotlib.pyplot as plt
import processFile

# enter sensor type (pressure, accelerometer, humidity, magnetometer, temperature)
value_type = "pressure"

# enter file name
file = 'trial bathroom 12 hours sensortag_output_20160106230013 Pressure().csv'

time, data = processFile.openFile(file, value_type)

print data
print time

print data.shape

if value_type in {"accelerometer", "magnetometer"}:
    dataX = data[:,0]
    dataY = data[:,1]
    dataZ = data[:,2]

    plt.plot(time, dataX, color='r', label = value_type+'X')
    plt.plot(time, dataY, color='b', label = value_type+'Y')
    plt.plot(time, dataZ, color='g', label = value_type+'Z')

elif value_type == "temperature":
    ambient_temp = data[:,0]
    object_temp = data[:,1]

    plt.plot(time, ambient_temp, color='r', label = 'ambient_temp')
    plt.plot(time, object_temp, color='b', label = 'object_temp')

else:
   plt.plot(time, data, color='r', label = value_type)


plt.xlabel('Time (seconds)')
plt.ylabel(value_type.capitalize())
plt.show()
