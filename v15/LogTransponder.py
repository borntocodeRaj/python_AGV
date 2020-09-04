#!/usr/bin/python
import matplotlib.pyplot
import matplotlib.mlab
import collections
import numpy
from math import *
from matplotlib.colors import LinearSegmentedColormap
import Utils

tractionAv=[]

def square(x):
	return x*x

def Import(filename):
	datas=matplotlib.mlab.csv2rec(filename,delimiter='\t')
	print "Transpondeur", filename, "OK n=", len(datas)
	print datas[0]
	return datas

Adjust=collections.namedtuple("Adjust", "timestamp x y theta rx ry rtheta consistency confidence dA dO")
cmap=LinearSegmentedColormap.from_list('cmap', [(1,0,0),(1,0,0),(1,0.75,0),(1,0.75,0),(1,1,0),(1,1,0),(0,1,0),(0,1,0)])

def ComputeAdjust():
	res=[]
	sel=[data for data in datas if data['available']==1]
	for data in sel:
		rtheta = Utils.Mod2Pi(data.theta-data.thetaodom)
		res.append(Adjust(data.timestamp,
			data.x, data.y, data.theta, 
			data.x-data.xodom, data.y-data.yodom, rtheta,
			data.consistency, data.confidence, data.da, data.do))
	return res

def PlotQ():
	dodomax=13000
	color=[]
	for dodom in datas.dodom:
		color.append(dodomax-dodom)
	matplotlib.pyplot.figure('XY')
	matplotlib.pyplot.scatter(datas.x, datas.y, c=color, cmap=cmap, marker='+', vmin=0, vmax=dodomax)
	matplotlib.pyplot.axes().set_aspect('equal')

def PlotAdjust(scale=100):
	x=[]
	y=[]
	rx=[]
	ry=[]
	thetaox=[]
	thetaoy=[]
	thetatx=[]
	thetaty=[]
	confidence=[]
	consistency=[]
	for adjust in adjusts:
		x.append(adjust.x)
		y.append(adjust.y)
		rx.append(adjust.rx*scale)
		ry.append(adjust.ry*scale)
		thetaox.append(cos(adjust.theta)*500)
		thetaoy.append(sin(adjust.theta)*500)
		thetatx.append(cos(adjust.theta+adjust.rtheta*90)*1000)
		thetaty.append(sin(adjust.theta+adjust.rtheta*90)*1000)
		confidence.append(adjust.confidence)
		consistency.append(adjust.consistency)
	matplotlib.pyplot.figure('XY')
	matplotlib.pyplot.quiver(x ,y, thetatx, thetaty, consistency, width=0.003, angles='xy', scale_units='xy', scale= 1,label="Recalage", cmap=cmap)
	matplotlib.pyplot.quiver(x ,y, thetaox, thetaoy, confidence, width=0.006, angles='xy', scale_units='xy', scale= 1,label="Recalage", cmap=cmap)
	matplotlib.pyplot.quiver(x ,y, rx, ry, width=0.001, angles='xy', scale_units='xy', scale= 1,label="Recalage", color='black')
	matplotlib.pyplot.axes().set_aspect('equal')


def PlotT():
	matplotlib.pyplot.figure()
	t = [ adjust.timestamp for adjust in adjusts ]
	rx = [ adjust.rx for adjust in adjusts ]
	ry = [ adjust.ry for adjust in adjusts ]
	rtheta = [ numpy.rad2deg(adjust.rtheta) for adjust in adjusts ] 
	consistency = [ adjust.consistency for adjust in adjusts ] 
	matplotlib.pyplot.quiver(t ,numpy.zeros(len(t)), rx, ry, consistency, width=0.003, angles='xy', scale_units='xy', scale= 1,label="Recalage", cmap=cmap)
	matplotlib.pyplot.axis('equal')

def Plot2():
	matplotlib.pyplot.figure('XY')	
	x=[]
	y=[]
	y2=[]

	#deltaY calibration
	list_dy=[]

	for i in range(1,len(sel2)):
		a=sel2[i-1]
		b=sel2[i]
		dist=sqrt(square(b.x-a.x)+square(b.y-a.y))
		x.append(dist)
		y.append(-b.rx*sin(b.theta)+b.ry*cos(b.theta))
		y2.append(b.rx*cos(b.theta)+b.ry*sin(b.theta))

		if x[-1] > 3000 and x[-1] < 4000:
			list_dy.append(y)

	matplotlib.pyplot.figure('XY')
	matplotlib.pyplot.plot(x,y,'.', label='lat')
	#matplotlib.pyplot.plot(x,y2,'.', label='long')
	matplotlib.pyplot.grid(True)
	matplotlib.pyplot.legend()

	print 'Calibration, DeltaY antenne AV: ajouter', -numpy.average(list_dy)*2.0

def PlotTheta():
	matplotlib.pyplot.figure()	
	x=[]
	y=[]
	y2=[]

	#deltaY calibration
	list_dy=[]

	for i in range(1,len(sel2)):
		a=sel2[i-1]
		b=sel2[i]
		dist=sqrt(square(b.x-a.x)+square(b.y-a.y))
		x.append(dist)
		y.append(b.rtheta)

	matplotlib.pyplot.plot(x,numpy.rad2deg(y),'.', label='rtheta(deg)')
	#matplotlib.pyplot.plot(x,y2,'.', label='long')
	matplotlib.pyplot.grid(True)
	matplotlib.pyplot.legend()

try:
	try:
		print("len(datas)=",len(datas),"(already loaded)")
	except NameError:
		datas=Import('Transpondeur.txt')
except:
	print "No transponder at all..."
	datas=[]

matplotlib.pyplot.ion()
adjusts=ComputeAdjust()
sel2=[]
for i in range(1,len(adjusts)):
	a=adjusts[i]
	b=adjusts[i-1]
	if fabs(a.x-b.x)>1000 or fabs(a.y-b.y)>1000:
		sel2.append(a)

print 'Stats:'
rx = [ a.rx for a in sel2 ]
print "rx moyen:", numpy.average(rx)
print "rx stddev:", numpy.std(rx)

ry = [ a.ry for a in sel2 ]
print "ry moyen:", numpy.average(ry)
print "ry stddev:", numpy.std(ry)

rthetas = [ a.rtheta for a in sel2 ]
print "rtheta moyen:", numpy.average(rthetas), 'rad ', numpy.rad2deg(numpy.average(rthetas)) 
print "rtheta stddev:", numpy.std(rthetas), ' rad ', numpy.rad2deg(numpy.std(rthetas))
 





