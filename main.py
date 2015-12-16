
import numpy as np
import processFile
import matplotlib.pyplot as plt
import utils

fileIn = "doorOC.csv"
fileOut = "doorOut2.csv"
# fileOut = "doorOCOut.csv"

## extract data from csv file
data = np.genfromtxt(fileOut, delimiter=',')
data = data[580:]
time = data[:,0]
acc = data[:,1:4]
accX = acc[:,0]
accY = acc[:,1]
accZ = acc[:,2]
m,n = acc.shape

## removes mean with first values (up to index)
index = 50
meanX = np.mean(accY[:index])
accX -= meanX
meanY = np.mean(accY[:index])
accY -= meanY
meanZ = np.mean(accZ[:index])
accZ -= meanZ

###
VX, VY, VZ = utils.computeVelocity (accX, accY, accZ, time)
DX, DY, DZ = utils.computeDerivative (accX, accY, accZ, time)

p = 10
timeInterval0 = 0.7
timeInterval1 = 0.5
mvt = utils.detectMvt (accX, accY, accZ, time, p, timeInterval0, timeInterval1)

data = np.zeros((m-1,2))
data[:,0] = time[:m-1]
# data[:,1] = mvt
# np.savetxt("mvt.csv", data, delimiter = ',')

## plot acceleration
# plt.plot(time, accX, color='g')
plt.plot(time, accY, color='b')
plt.plot(time, accZ, color='r')
#
# plt.plot(time0, acc0X, color='g')
# plt.plot(time0, acc0Y, color='b')
# plt.plot(time0, acc0Z, color='r')

## plot velocity
# plt.plot(time[:m-1], VX, color='g')
# plt.plot(time[:m-1], VY, color='b')
# plt.plot(time[:m-1], VZ, color='r')


## plot mvt
plt.plot(time[:m-2], mvt[:m-2], color='g')

plt.show()

