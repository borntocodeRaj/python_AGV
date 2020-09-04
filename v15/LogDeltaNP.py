#!/usr/bin/python
import matplotlib.pyplot
import matplotlib.mlab

tractionAv=[]
filename = "DeltaNP.txt"

def Import(filename):
	datas=matplotlib.mlab.csv2rec(filename,delimiter='\t')
	print "LogDeltaNP:", filename, "OK n=", len(datas)
	return datas


try:
	datas = Import(filename)
	t = datas.timestamp
	dt = t[1:]-t[0:-1]
except:
	print "Could not read file:", filename
	datas = []

