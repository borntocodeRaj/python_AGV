#!/usr/bin/python
import matplotlib.pyplot
import matplotlib.mlab
import scipy
import pylab
import numpy
import scipy.signal
import Utils

from math import *

import LogReperage

tb=[]
thetab=[]

def Import(filename):
	print "LogXsens reading", filename, "..."
	datas=matplotlib.mlab.csv2rec(filename,delimiter='\t')
	print "LogXsens:", filename, "OK n=", len(datas)
	return datas


def PlotT():
	matplotlib.pyplot.figure()

	ax1 = matplotlib.pyplot.subplot(1,1,1)
	ax1.plot(t, numpy.rad2deg(datas.instantbias), '.', label="instantBias")
	ax1.plot(t, numpy.rad2deg(datas.bias), '-', label="bias")
	Utils.FormatAxe(ax1, "bias", "t(s)", "deg/s")

def PlotTheta():
	matplotlib.pyplot.figure()
	ax1 = matplotlib.pyplot.subplot(1,1,1)
	ax1.plot(t, numpy.rad2deg(Utils.ContinuousAngle(datas.theta)), '-+', label="theta")
	ax1.plot(t, numpy.rad2deg(Utils.ContinuousAngle(theta2)), '-x', label="theta2")
	ax1.plot(LogReperage.datas.timestamp, numpy.rad2deg(Utils.ContinuousAngle(LogReperage.datas.psitheta)), '-', label="psi.theta")
	ax1.plot(tb, numpy.rad2deg(thetab), '*-', label="ref")
	Utils.FormatAxe(ax1, "yaw", "t(s)", "deg")

def Theta2():
	res = []
	prevInstantbias = datas[0].instantbias
	prevt = datas[0].timestamp
	dt = 0
	corr = 0

	memt=0
	memtheta=0

	for data in datas:
		theta = data.theta
		instantbias=data.instantbias
		if ( instantbias == prevInstantbias ):
			dt = dt + data.timestamp - prevt
			theta = theta - data.bias*dt
			corr = data.bias*dt
			if memt==0:
				memt=data.timestamp
				memtheta=data.theta
		else:
			if dt >= 0.03:
				print 't=',data.timestamp,"\tcorr:", numpy.rad2deg(corr),"deg \tdt:",dt,"s"
				tb.append(memt)
				thetab.append(memtheta)	
				tb.append(data.timestamp)
				thetab.append(data.theta)	
				memt=0
				memtheta=0
			dt = 0
		res.append(theta)
		prevt = data.timestamp
		prevInstantbias = instantbias
	return res

matplotlib.pyplot.ion()

print "ReperageInertiel Log Analyzer"
#matplotlib.pyplot.close("all")


datas=Import("ReperageInertiel.txt")
t = datas.timestamp
theta2=Theta2()





