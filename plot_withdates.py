
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import processFile
import datetime


# enter sensor type (pressure, accelerometer, humidity, magnetometer, temperature, luxometer)
value_type = "magnetometer"

# indicate if file type is new (with sensor id) or old (first version of the csv files): True or False
new = False

# enter file name
file = 'sensortag_debug_20160110101356 - Bathroom.csv'

unit = {}
unit['temperature'] = 'C'
unit['accelerometer'] = 'G'
unit['humidity'] = 'rH'
unit['magnetometer'] = 'uT'
unit['pressure'] = 'mbar'

time, data = processFile.openFile(file, value_type, new, True)
print 'data.shape: ' , data.shape

print 'Plotting...'

# print np.ndiff(time)


if value_type == "luxometer":
    m = data.shape[0]
    for i in range(m):
        if data[i] > 100000:
            data[i] = 200

# print data
# print type(time)

time = time.values()
# print time.shape

fig, ax = plt.subplots(1)

if value_type in {"accelerometer", "magnetometer"}:
    dataX = data[:,0]
    dataY = data[:,1]
    dataZ = data[:,2]

    # plt.plot(time, dataX, color='r', label=value_type[:3]+'X')
    plt.plot(time, dataY, color='c', label=value_type[:3]+'Y')
    # plt.plot(time, dataZ, color='g', label=value_type[:3]+'Z')

elif value_type == "temperature":
    ambient_temp = data[:,0]
    object_temp = data[:,1]

    plt.plot(time, ambient_temp, color='b', label='Ambient_temp')
    # plt.plot(time, object_temp, color='r', label='Object_temp')

else:
   ax.plot(time, data, color='r', label=value_type)

# size: enables to modify front size
# labelpad: distances the ticks from the labels
plt.xlabel('Time', size=15, labelpad=10)
plt.ylabel(value_type.capitalize() + ' (' + unit[value_type] + ')', size=15,  labelpad=10)
plt.legend(loc='best')

# title of the plot, size: changes frontsize
plt.title('Magnetic field on the button-type flush', size=20)

ax.xaxis.set_major_locator(mdates.HourLocator(np.arange(0, 25, 1)))
# ax.xaxis.set_minor_locator(mdates.HourLocator(np.arange(0, 25, 12)))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
# ax.xaxis.set_minor_formatter(mdates.DateFormatter(' %H:%M'))

plt.xticks(size=14, rotation=90)
plt.yticks(size=14)

ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d %H:%M:%S')
# fig.autofmt_xdate()
plt.gcf().subplots_adjust(bottom=0.30)


plt.show()