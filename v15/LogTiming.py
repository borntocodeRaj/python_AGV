#!/usr/bin/python
import matplotlib.pyplot as plt
import matplotlib.mlab

tractionAv=[]
filename = "ba-timing"

def Import(filename):
	datas=matplotlib.mlab.csv2rec(filename,delimiter='\t')
	print "LogTiming:", filename, "OK n=", len(datas)
	return datas


def Plot():
    plt.figure('timing')
    plt.plot(datas.date_hour, datas.timedebut, label='timedebut')
    plt.plot(datas.date_hour, datas.timelock, label='timelock')
    plt.plot(datas.date_hour, datas.timefin, label='timefin')
    plt.grid(True)
    plt.legend()

try:
	datas = Import(filename)
	t = datas.timestamp
	dt = t[1:]-t[0:-1]
except:
	print "Could not read file:", filename
	datas = []

