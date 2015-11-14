
import numpy as np
import processFile
import matplotlib.pyplot as plt

fileIn = "door1211.csv"
fileOut = "doorOut2.csv"

### if new file, need to process data
# processFile.processFile(fileIn, fileOut)

## extract data from csv file
data = np.genfromtxt(fileOut, delimiter=',')
data = data[580:]
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
print Dtime

## derivative
DX = DaccX / Dtime
DY = DaccY / Dtime
DZ = DaccZ / Dtime

## removes mean
meanX = np.mean(accY[:50])
accX -= meanX
meanY = np.mean(accY[:50])
accY -= meanY
meanZ = np.mean(accZ[:50])
accZ -= meanZ

## velocity
VXi = np.zeros(m-1)
VYi = np.zeros(m-1)
VZi = np.zeros(m-1)
Y = np.zeros(m-1)
Z = np.zeros(m-1)

for i in range(m-1):
    # VXi[i] = ((accX[i]+accX[i+1])/2) * Dtime[i]
    # VZi[i] = ((accZ[i]+accZ[i+1])/2) * Dtime[i]
    # VYi[i] = ((accY[i]+accY[i+1])/2) * Dtime[i]
    VXi[i] = accX[i] * Dtime[i]
    VZi[i] = accZ[i] * Dtime[i]
    VYi[i] = accY[i] * Dtime[i]
VX = np.cumsum(VXi)
VY = np.cumsum(VYi)
VZ = np.cumsum(VZi)

DVZ = np.diff(VZ)
maxDVZ = np.max(np.absolute(DVZ[:50]))
DVY = np.diff(VY)
maxDVY = np.max(np.absolute(DVY[:50]))

maxDerivativeY = np.max(np.absolute(DY[:60]))
maxDerivativeZ = np.max(np.absolute(DZ[:60]))
thresholdMinY = np.min(accY[:30])
thresholdMaxY = np.max(accY[:30])
thresholdMinZ = np.min(accZ[:30])
thresholdMaxZ = np.max(accZ[:30])

booleanY = accY>thresholdMaxY
booleanZ1 = accZ>thresholdMaxZ
booleanZ2 = accZ<thresholdMinZ
booleanZ3 = np.absolute(DZ)>maxDerivativeZ
booleanZ4 = np.absolute(DVZ)>maxDVZ
booleanY4 = np.absolute(DVY)>maxDVY
mvtZ1 = np.where(booleanZ1,1,0)[:m-2]
mvtZ2 = np.where(booleanZ2,1,0)[:m-2]
mvtZ3 = np.where(booleanZ3,1,0)[:m-2]
mvtZ4 = np.where(booleanZ4,1,0)[:m-2]
mvtY4 = np.where(booleanY4,1,0)[:m-2]
mvtY1 = np.where(booleanY,1,0)[:m-2]
mvtY2 = np.where(np.absolute(DY)>maxDerivativeY,1,0)[:m-2]

mvt = mvtY1 | mvtY2 |mvtZ1 | mvtZ2 | mvtZ3 | mvtZ4| mvtY4
i = 0
while i<m-2:
    if mvt[i]==0:
        print i
        t0 = time[i]
        j = i+1
        while j<m-2 :
            if (mvt[j]==0):
                j +=1
            else: break
        print "j: ", j
        timeDiff = time[j] - t0
        if timeDiff < 1:
            mvt[i:j] = 1
        i = j+1
    else:
        i +=1

data = np.zeros((m-1,2))
data[:,0] = time[:m-1]
# data[:,1] = mvt
# np.savetxt("mvt.csv", data, delimiter = ',')

## plot acceleration
# plt.plot(time, accX, color='g')
plt.plot(time, accY, color='b')
plt.plot(time, accZ, color='r')

## plot velocity
# plt.plot(time[:m-1], VX, color='g')
# plt.plot(time[:m-1], VY, color='b')
# plt.plot(time[:m-1], VZ, color='r')


## plot mvt
plt.plot(time[:m-2], mvt[:m-2], color='g')

plt.show()

