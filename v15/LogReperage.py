#!/usr/bin/python
import matplotlib.pyplot
import matplotlib.mlab
from scipy import interpolate
from math import *
import numpy
import pylab
import Utils

import LogDeltaNP


datas=[]
continuousTheta=[]
psiNav = []
easyTrack = []

def RotationMatrix2D(theta):
	c = cos(theta)
	s = sin(theta)
	return numpy.array([ [ c, -s], [s, c] ])

def Import(filename):
	return matplotlib.mlab.csv2rec(filename,delimiter='\t') 

def PlotXY():
	matplotlib.pyplot.figure('XY')
	#adds N time markers
	N=20
	for i in range(0,N):
		j=i*(len(datas.x)/N)
		x=datas.x[j]
		y=datas.y[j]
		matplotlib.pyplot.annotate("t="+str(datas.timestamp[j]),[x,y], color='blue')
		'''
		if j+1 < len(datas.x):
			dx=datas.x[j+1]-datas.x[j]
			dy=datas.y[j+1]-datas.y[j]
			ax.quiver(x,y, dx, dy, width=0.01, angles='xy', scale_units='xy', scale= 1000, color='blue')
			print j
		'''
	matplotlib.pyplot.plot(datas.x, datas.y, marker='+', label='Reperage')
	if datas.dtype.fields.has_key("psix"):
		matplotlib.pyplot.plot(datas.psix, datas.psiy, marker='+', label='Psi')
	if datas.dtype.fields.has_key("inex"):
		matplotlib.pyplot.plot(datas.inex, datas.iney, marker='+', label='Ine')
	if datas.dtype.fields.has_key("psix"):
		matplotlib.pyplot.plot(datas.psix, datas.psiy, marker='+', label='Psi')
	if datas.dtype.fields.has_key("reperagetargetsx"):
		matplotlib.pyplot.plot(datas.reperagetargetsx, datas.reperagetargetsy, marker='+', label='reperagetargets')

def PlotRTK():
    matplotlib.pyplot.figure('XY')
    matplotlib.pyplot.plot(reperageRTK.xgps, reperageRTK.ygps, 'o', label='GPS')
   
def PlotDiff(scale = 1000):
    matplotlib.pyplot.figure('XY')
    mr, psi = Utils.TimeRescale([datas, psiNav])
    n = len(mr)
    I = numpy.multiply(range(0,n/20),20)
    x = [ mr.x[i] for i in I ]
    y = [ mr.y[i] for i in I ]
    rx = [ mr.x[i]-psi.x[i] for i in I ]
    ry = [ mr.y[i]-psi.y[i] for i in I ]
    matplotlib.pyplot.quiver(x,y, numpy.multiply(rx,scale), numpy.multiply(ry,scale), width=0.0025, angles='xy', scale_units='xy', scale= 1,label="Diff")

def PlotWheelTraj(dataAgv):
    matplotlib.pyplot.figure('XY')
    voie = dataAgv.voie
    # arD
    xD = datas.x + numpy.multiply( voie/2.0, numpy.sin(datas.theta))
    yD = datas.y - numpy.multiply( voie/2.0, numpy.cos(datas.theta))
    xG = datas.x - numpy.multiply( voie/2.0, numpy.sin(datas.theta))
    yG = datas.y + numpy.multiply( voie/2.0, numpy.cos(datas.theta))
    matplotlib.pyplot.plot(xD, yD)
    matplotlib.pyplot.plot(xG, yG)

def PlotTheta():
	matplotlib.pyplot.figure()
	ax1 = matplotlib.pyplot.subplot(1,1,1)
	ax1.plot(datas.timestamp, numpy.rad2deg(datas.theta), marker='+', label='Reperage')
	if datas.dtype.fields.has_key("psitheta"):
		ax1.plot(datas.timestamp, numpy.rad2deg(datas.psitheta), marker='+', label='Psi')
	if datas.dtype.fields.has_key("inex"):
		ax1.plot(datas.timestamp, numpy.rad2deg(datas.inetheta), marker='+', label='Ine')
	if datas.dtype.fields.has_key("psix"):
		ax1.plot(datas.timestamp, numpy.rad2deg(datas.psitheta), marker='+', label='psi')
	if datas.dtype.fields.has_key("reperagetargetsx"):
		ax1.plot(datas.timestamp, numpy.rad2deg(datas.psitheta), marker='+', label='reperagetargets')

	Utils.FormatAxe(ax1, "yaw", "t(s)", "deg")
	matplotlib.pyplot.legend()
	matplotlib.pyplot.grid(True)
	matplotlib.pyplot.show()

def PlotT():
    matplotlib.pyplot.figure()
    ax1 = matplotlib.pyplot.subplot(3,1,1)
    ax1.plot(datas.timestamp, datas.x, marker='+', label='x-Reperage')
    ax1.plot(datas.timestamp, datas.y, marker='+', label='y-Reperage')
    if len(psiNav) != 0 :
        ax1.plot(psiNav.timestamp, psiNav.x, marker='x', label='psiNav')
    if len(easyTrack) != 0 :
        ax1.plot(easyTrack.timestamp, easyTrack.x, marker='x', label='easyTrack')
    Utils.FormatAxe(ax1, "x-y", "t(s)", "mm")
    if len(LogDeltaNP.datas) > 0:
    	ax2 = matplotlib.pyplot.subplot(3,1,2, sharex=ax1)
        ax2.plot(LogDeltaNP.datas.timestamp, LogDeltaNP.datas.dx, label='dx')
        ax2.plot(LogDeltaNP.datas.timestamp, LogDeltaNP.datas.dy, label='dy')
        Utils.FormatAxe(ax2, "dx-dy", "t(s)", "mm")

    	ax3 = matplotlib.pyplot.subplot(3,1,3, sharex=ax1)
        ax3.plot(LogDeltaNP.datas.timestamp, LogDeltaNP.datas.dtheta, label='dtheta')
        Utils.FormatAxe(ax2, "dtheta", "t(s)", "rad")

def Courbure():
    dx = datas.x[1:]-datas.x[0:-1]
    dy = datas.y[1:]-datas.y[0:-1]
    dtheta = datas.x[1:]-datas.x[0:-1]
    ds = numpy.sqrt( numpy.square(dx) + numpy.square(dy) )
    c = numpy.divide(dtheta, ds)
    return c    

matplotlib.pyplot.ion()
try:
	datas=Import("MultiReperage.txt")
	print 'LogReperage:Import datas OK len=', len(datas)
	continuousTheta=Utils.ContinuousAngle(datas.theta)
	
	def fx(t):
		return Utils.InterpolateValue(datas.timestamp, datas.x, t)
	def fy(t):
		return Utils.InterpolateValue(datas.timestamp, datas.y, t)
	def ftheta(t):
		theta=Utils.InterpolateValue(datas.timestamp, continuousTheta, t)
		return Utils.Mod2Pi(theta)

except IOError:
	datas=[]
	print 'LogReperage:Could not import datas'


try:
	psiNav = Import("ReperagePsiNav.txt")
except IOError:
	print 'no "ReperagePsiNav.txt"'

try:
	easyTrack = Import("ReperageEasyTrack.txt")
except IOError:
	print 'no "ReperageEasyTrack.txt"'


try:
    reperageRTK = Import("ReperageRTK")
except IOError:
	print 'no "ReperageRTK"'




