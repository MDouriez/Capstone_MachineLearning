import numpy as np
import csv
from StringIO import StringIO

# Removes the 118.99 values of the humidity

# enter sensor type (pressure, accelerometer, humidity, magnetometer, temperature, luxometer)
value_type = "humidity"

# indicate if file type is new (with sensor id) or old (first version of the csv files): True or False
new = False

# enter file name
file = 'sensortag_output_20160117180352 Humidity(rH).csv'

# Open file but keep time as a string
f = open(file, "rb")
r = csv.reader(f)
o = StringIO()
w = csv.writer(o)
w.writerows(r)
o.seek(0)

data = np.genfromtxt(o, delimiter=',', usecols=(2), skip_footer=1)
o.seek(0)
time = np.genfromtxt(o, dtype=str, usecols = (0), delimiter=',', skip_footer=1)



# time, data = processFile.openFile(file, value_type, new)
# print data

m = time.shape[0]
# print m

to_be_deleted = []
i = 0
while i < m:
    count = 0
    if data[i] > 118.99 :
        count +=1
        j = i+1
        while j<m:
            if (data[j] > 118.99) :
                count +=1
                j+=1
            else: break
        if count <= 6:
            for k in range(count):
                to_be_deleted.append(i+k)
        i += count
    else:
        i+=1

print to_be_deleted

data = np.delete(data, to_be_deleted, 0)
time = np.delete(time, to_be_deleted, 0)
m = time.shape[0]
print m

empty = np.ones(m)
a = np.vstack((time, empty))
a = np.vstack((a, data))
print a

with open("rm env "+file, 'wb') as fp:
    output = csv.writer(fp)
    for i in range(m):
        output.writerow(a[:,i])

print "File 'rm env " +file+ "' created"

# plt.plot(time, data, color='r', label=value_type)
# plt.show()