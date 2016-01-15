import csv
from StringIO import StringIO
import numpy as np


def openFile(file, type, new):
    # extract data from file.
    # type = 'accelerometer' or 'temperature' or 'pressure' or 'magnetometer' or 'humidity' or 'luxometer'

    # remove quotation marks
    f = open(file, "rb")
    r = csv.reader(f)
    o = StringIO()
    w = csv.writer(o)
    w.writerows(r)
    o.seek(0)

    i=0
    if new:
        i = 1

    # extract sensor values
    if type == 'accelerometer':
        data = np.genfromtxt(o, delimiter=',', usecols=(2+i, 3+i, 4+i), skip_footer=1)
    elif type == 'magnetometer':
        data = np.genfromtxt(o, delimiter=',', usecols=(10+i,11+i,12+i), skip_footer=1)
    elif type == 'luxometer':
        data = np.genfromtxt(o, delimiter=',', usecols=(2+i), skip_footer=1)
    elif type == 'temperature': #temperature (object + ambient!)
        data = np.genfromtxt(o, delimiter=',', usecols=(2+i,4+i), skip_footer=1)
    elif type == 'pressure':
        data = np.genfromtxt(o, delimiter=',', usecols=(2+i), skip_footer=1)
    elif type == 'humidity':
        data = np.genfromtxt(o, delimiter=',', usecols=(2+i), skip_footer=1)

    # extract time
    o.seek(0)
    time = np.genfromtxt(o, dtype=str, usecols = (0), delimiter=',', skip_footer=1)

    # convert time from a date to a number
    m = time.shape[0]
    year = np.zeros(m)
    month= np.zeros(m)
    day= np.zeros(m)
    hour= np.zeros(m)
    sec= np.zeros(m)
    minu= np.zeros(m)
    for i in range(m):
        lhs, rhs = time[i].split(" ")
        year[i], month[i], day[i] = lhs.split("-")
        hour[i], minu[i], sec[i] = rhs.split(":")
    t = day*86400 + hour*3600 + minu*60 + sec
    t = t/3600
    # print t

    # put t0 to 0
    t0 = t[0]
    # print t0
    t = t - t0

    return t, data


def processFile(fileIn, fileOut):
    # remove quotation marks from a file

    ## remove quotation marks
    f = open(fileIn, "rb")
    r = csv.reader(f)
    o = StringIO()
    w = csv.writer(o)
    w.writerows(r)
    o.seek(0)
    ## acceleration data
    acc = np.genfromtxt(o, delimiter=',', usecols = (2, 3, 4), skip_footer=1)
    o.seek(0)
    ## time data
    time = np.genfromtxt(o, dtype=str, usecols = (0), delimiter=',', skip_footer=1)

    ## convert time from a date to a number
    m = time.shape[0]
    year = np.zeros(m)
    month= np.zeros(m)
    day= np.zeros(m)
    hour= np.zeros(m)
    sec= np.zeros(m)
    minu= np.zeros(m)
    for i in range(m):
        lhs, rhs = time[i].split(" ")
        year[i], month[i], day[i] = lhs.split("-")
        hour[i], minu[i], sec[i] = rhs.split(":")
    t = hour*3600 + minu*60 + sec
    print t
    t0 = t[0]
    print t0
    t = t - t0
    print t.shape
    print acc.shape
    m, n = acc.shape

    ## save time and acceleration into a new csv file fileOut
    data = np.zeros((m,n+1))
    data[:,0] = t
    data[:,1:4] = acc
    np.savetxt(fileOut, data, delimiter = ',')