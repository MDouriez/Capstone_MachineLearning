## plot acceleration data

import numpy as np
import csv
import matplotlib.pyplot as plt
import processFile


#######################
file = "new.csv"

# time, acc = processFile.openFileAcc(file)
# time, lux = processFile.openFileLux(file)
time, temp = processFile.openFileTemp(file)

#acc = np.genfromtxt(fileOut, delimiter=',', usecols = (2, 3, 4), skip_footer=1)
# print acc
# #time = np.genfromtxt(fileOut, delimiter=',', usecols = (0), skip_footer=1)
# t0 = time[0]
# print t0
# time = time - t0
# # print time

# print acc.shape
#
# accX = acc[:,0]
# accY = acc[:,1]
# accZ = acc[:,2]
#

# plt.plot(time, lux, color='r')
plt.plot(time, temp, color='r')

# plt.plot(time, accX, color='r')
# plt.plot(time, accY, color='b')
# plt.plot(time, accZ, color='g')

plt.show()
