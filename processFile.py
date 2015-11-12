import csv
from StringIO import StringIO
import numpy as np


def processFile(fileIn, fileOut):

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

