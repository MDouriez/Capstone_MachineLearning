
import numpy as np
import processFile
import matplotlib.pyplot as plt

fileIn = "door2.csv"
fileOut = "doorOut2.csv"
# processFile.processFile(fileIn, fileOut)

data = np.genfromtxt(fileOut, delimiter=',')
time = data[:,0]
acc = data[:,1:4]
accX = acc[:,0]
accY = acc[:,1]
accZ = acc[:,2]
m,n = acc.shape


DaccX = np.diff(accX)
DaccY = np.diff(accY)
DaccZ = np.diff(accZ)
Dtime = np.diff(time)
# maxDtime = np.argmax(Dtime)
# print maxDtime
# time[maxDtime:m] = time[maxDtime:m] - (np.max(Dtime) - 1)
# Dtime = np.diff(time)
# print Dtime

## derivative
DX = DaccX / Dtime
DY = DaccY / Dtime
DZ = DaccZ / Dtime

## removes mean
meanY = np.mean(accY[:100])
print meanY
accY -= meanY

meanZ = np.mean(accZ[:100])
print meanZ
accZ -= meanZ

## velocity
VY = np.zeros(m-1)
VZ = np.zeros(m-1)
Y = np.zeros(m-1)
Z = np.zeros(m-1)
indexVY = 0
indexVZ = 0
for i in range(m-2):
    VZi = ((accZ[i]+accZ[i+1])/2) * Dtime[i]
    VYi = ((accY[i]+accY[i+1])/2) * Dtime[i]
    indexVY += VYi
    indexVZ += VZi
    VZ[i] = indexVZ
    VY[i] = indexVY

maxDerivativeY = np.max(np.absolute(DY[:60]))
maxDerivativeZ = np.max(np.absolute(DZ[:60]))
thresholdMinY = np.min(accY[:70])
thresholdMaxY = np.max(accY[:70]) + 0.008
thresholdMinZ = np.min(accZ[:70]) - 0.008
thresholdMaxZ = np.max(accZ[:70]) + 0.008

booleanY = accY>thresholdMaxY
booleanZ1 = accZ>thresholdMaxZ
booleanZ2 = accZ<thresholdMinZ
booleanZ3 = np.absolute(DZ)>maxDerivativeZ
mvtZ1 = np.where(booleanZ1,1,0)
mvtZ2 = np.where(booleanZ2,1,0)
mvtZ3 = np.where(booleanZ3,1,0)
mvtY1 = np.where(booleanY,1,0)
mvtY2 = np.where(np.absolute(DY)>maxDerivativeY,1,0)
mvt = mvtY1[:m-1] | mvtY2 |mvtZ1[:m-1] | mvtZ2[:m-1] | mvtZ3
for j in range(4):
    for i in range(m-3):
        if mvt[i+1] == mvt[i-1] and mvt[i+1] == 1:
            mvt[i] = 1

data = np.zeros((m-1,2))
data[:,0] = time[:m-1]
data[:,1] = mvt
np.savetxt("mvt.csv", data, delimiter = ',')


# plt.plot(time[600:m-2], VZ[600:m-2], color='g')
# plt.plot(time[:550], Y[:550], color='r')
plt.plot(time[922:965], mvt[922:965], color='r')
# plt.plot(time[:550], accY[:550], color='b')
# plt.plot(time[600:m-1], acc[600:m-1,2], color='r')
plt.show()

