import numpy as np

def computeDerivative (accX, accY, accZ, time):
    m= accX.shape[0]
    DaccX = np.diff(accX)
    DaccY = np.diff(accY)
    DaccZ = np.diff(accZ)
    Dtime = np.diff(time)
    # print Dtime

    ## derivative of acceleration
    DX = DaccX / Dtime
    DY = DaccY / Dtime
    DZ = DaccZ / Dtime

    return DX, DY, DZ

def computeVelocity (accX, accY, accZ, time):
    m= accX.shape[0]
    Dtime = np.diff(time)
    VXi = np.zeros(m-1)
    VYi = np.zeros(m-1)
    VZi = np.zeros(m-1)

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

    return VX, VY, VZ

def detectMvt (accX, accY, accZ, time, p, timeInterval0, timeInterval1):
    m = accX.shape[0]
    DX, DY, DZ = computeDerivative (accX, accY, accZ, time)

    maxDX = np.max(np.absolute(DX[:p]))
    maxDY = np.max(np.absolute(DY[:p]))
    maxDZ = np.max(np.absolute(DZ[:p]))
    MaxX = np.max(np.absolute(accX[:p]))
    MaxY = np.max(np.absolute(accY[:p]))
    MaxZ = np.max(np.absolute(accZ[:p]))

    ## define booleans
    bX1 = np.absolute(accX)> 1.5 * MaxX
    bY1 = np.absolute(accY)>1.5 * MaxY
    bZ1 = np.absolute(accZ)>1.5 * MaxZ
    bX2 = np.absolute(DX)>1.5 * maxDX
    bY2 = np.absolute(DY)>1.5 * maxDY
    bZ2 = np.absolute(DZ)>1.5 * maxDZ

    mvtX1 = np.where(bX1,1,0)[:m-2]
    mvtX2 = np.where(bX2,1,0)[:m-2]
    mvtY1 = np.where(bY1,1,0)[:m-2]
    mvtY2 = np.where(bY2,1,0)[:m-2]
    mvtZ1 = np.where(bZ1,1,0)[:m-2]
    mvtZ2 = np.where(bZ2,1,0)[:m-2]


    mvt = mvtX1 | mvtX2 | mvtY1 | mvtY2 |mvtZ1 | mvtZ2

    ## loop to handle gaps in data aquisition

    i = 0
    while i<m-2:
        if mvt[i]==1:
            print i
            t0 = time[i]
            j = i+1
            while j<m-2 :
                if (mvt[j]==1):
                    j +=1
                else: break
            print "j: ", j
            timeDiff = time[j] - t0
            if timeDiff < timeInterval1:
                mvt[i:j] = 0
            i = j+1
        else:
            i +=1

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
            if timeDiff < timeInterval0:
                mvt[i:j] = 1
            i = j+1
        else:
            i +=1

    return mvt