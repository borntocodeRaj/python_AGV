#!/usr/bin/python
import collections
import matplotlib.pyplot as plt
import matplotlib.mlab
from math import cos
from math import sin
from math import pi
import numpy

import Track
import LogNavigation
import LogDeltaNP
import LogReperage

OdomModel = collections.namedtuple('OdomModel','t xOdom yOdom thetaOdom xLaser yLaser thetaLaser')


if len(LogDeltaNP.datas)!=0 and len(LogReperage.datas)!= 0:
	print "FileOK with DeltaNP"
	print 'tmin=', max(LogReperage.datas.timestamp[0], LogDeltaNP.datas.timestamp[0])
	print 'tmax=', min(LogReperage.datas.timestamp[-1], LogDeltaNP.datas.timestamp[-1])



''' Model dometrique ave DeltaNP
@param t1 debut de la simulation
@param t2 fin de la simulation
@return tableau de OdomModel'''
def OdomModelNP(t1, t2):
	res = []

	# recherche position initiale
	i = 0
	while LogReperage.datas[i].timestamp < t1 :
		x = LogReperage.datas[i].x
		y = LogReperage.datas[i].y
		theta = LogReperage.datas[i].theta
		i = i + 1

	# recherche debut pour DeltaNP
	j = 0
	while LogDeltaNP.datas[j].timestamp < t1 :
		j=j+1
	
	print 'i=',i,' j=',j

	t=LogDeltaNP.datas[i].timestamp
	xOdom = x
	yOdom = y
	thetaOdom = theta
	xLaser = xOdom
	yLaser = yOdom
	thetaLaser = thetaOdom
		
	while (i < len(LogReperage.datas) 
		and j < len(LogDeltaNP.datas) and
		LogDeltaNP.datas[j].timestamp < t2 ):

		res.append(OdomModel(t,xOdom,yOdom,thetaOdom,xLaser,yLaser,thetaLaser))
		i=i+1
		j=j+1
		t = LogDeltaNP.datas.timestamp[j]
		dx = LogDeltaNP.datas.dx[j]
		dy = LogDeltaNP.datas.dy[j]
		dtheta = LogDeltaNP.datas.dtheta[j]

		xOdom = xOdom + dx*cos(thetaOdom) - dy*sin(thetaOdom)
		yOdom = yOdom + dx*sin(thetaOdom) + dy*cos(thetaOdom)
		thetaOdom =thetaOdom+dtheta
		xLaser = LogReperage.datas[i].x
		yLaser = LogReperage.datas[i].y
		thetaLaser = LogReperage.datas[i].theta
		
	return res

''' Model dometrique tricycle, odometrie sur roue avant
@param t1 debut de la simulation
@param t2 fin de la simulation
@return tableau de OdomModel'''
def OdomModelTrycycle(t1, t2):
	res = []
	i = 0
	xAv= float(Track.dataAgv.xTourelleAv)
	yAv= float(Track.dataAgv.yTourelleAv)
	datas = LogNavigation.datas
	
	while datas[i].timestamp < t1 :
		i=i+1
	
	t=datas[i].timestamp
	xOdom = datas[i].x
	yOdom = datas[i].y
	thetaOdom = datas[i].theta*pi/180.0
	xLaser = xOdom
	yLaser = yOdom
	thetaLaser = thetaOdom
		
	while datas[i].timestamp <= t2 and i<len(datas)-1 :
		res.append(OdomModel(t,xOdom,yOdom,thetaOdom,xLaser,yLaser,thetaLaser))
	
		i=i+1
		vav = datas[i].vav
		dAv= vav*0.03
		phiAv = datas[i].phiav*pi/180.0
		
		dx = dAv*(cos(phiAv)+(yAv/xAv)*sin(phiAv));
		dy = 0.0
		dtheta = dAv*sin(phiAv)/xAv;
		
		xOdom = xOdom + dx*cos(thetaOdom) - dy*sin(thetaOdom)
		yOdom = yOdom + dx*sin(thetaOdom) + dy*cos(thetaOdom)
		thetaOdom =thetaOdom+dtheta
		xLaser = datas[i].x
		yLaser = datas[i].y
		thetaLaser = datas[i].theta*pi/180.0
		
	return res
	
''' Model dometrique bi-tourelle, odometrie sur essieu arriere uniquement 
(pour l'ATT)
@param t1 debut de la simulation
@param t2 fin de la simulation
@return tableau de OdomModel'''
def OdomModelATT(t1,t2):
	res = []
	i = 0
	xAv= float(Track.dataAgv.xTourelleAv)
	yAv= float(Track.dataAgv.yTourelleAv)
	xAr= float(Track.dataAgv.xTourelleAr)
	yAr= float(Track.dataAgv.yTourelleAr)
	xrv= xAv - xAr
	datas = LogNavigation.datas
	
	while datas[i].timestamp < t1 :
		i=i+1
	
	t=datas[i].timestamp
	xOdom = datas[i].x
	yOdom = datas[i].y
	thetaOdom = datas[i].theta*pi/180.0
	xLaser = xOdom
	yLaser = yOdom
	thetaLaser = thetaOdom
		
	while datas[i].timestamp <= t2 and i<len(datas)-1 :
		res.append(OdomModel(t,xOdom,yOdom,thetaOdom,xLaser,yLaser,thetaLaser))
	
		i=i+1
		var = datas[i]['var']
		dAr= var*0.02
		phiAv = datas[i].phiav*pi/180.0
		phiAr = datas[i].phiar*pi/180.0
		
		
		dtheta = (dAr*sin(phiAv-phiAr))/(cos(phiAv)*xrv)
		dx = dAr*cos(phiAr);
		dy = dAr*sin(phiAr) - dtheta*xAr;
		
		xOdom = xOdom + dx*cos(thetaOdom) - dy*sin(thetaOdom)
		yOdom = yOdom + dx*sin(thetaOdom) + dy*cos(thetaOdom)
		thetaOdom =thetaOdom+dtheta
		xLaser = datas[i].x
		yLaser = datas[i].y
		thetaLaser = datas[i].theta*pi/180.0
		
	return res
	
	
def PlotSimulOdom(t1, t2):
	plt.figure('XY')
	if len(LogDeltaNP.datas)!=0 and len(LogReperage.datas)!= 0:
			simulOdom=OdomModelNP(t1,t2)
	else:	
		if Track.dataAgv.nbTourelles == 2:
			simulOdom=OdomModelATT(t1,t2)
		else:
			simulOdom=OdomModelTrycycle(t1, t2)
	plt.plot([s.xOdom for s in simulOdom], [s.yOdom for s in simulOdom], color='black')
	#add 20 markers
	for i in range(0,20):
		j=i*(len(simulOdom)/20)
		s=simulOdom[j]
		plt.plot([s.xOdom,s.xLaser],[s.yOdom,s.yLaser])

	t = [ s.t for s in simulOdom ]
	x = [ s.xLaser for s in simulOdom ]

	theta1 = [ numpy.deg2rad(s.thetaLaser) for s in simulOdom ]
	theta2 = [ numpy.deg2rad(s.thetaOdom) for s in simulOdom ]
	diff = [ numpy.deg2rad(s.thetaLaser - s.thetaOdom) for s in simulOdom ]

	plt.figure()
	plt.title('Cap (deg)')
	plt.plot(t, theta1, label ='Reperage')
	plt.plot(t, theta2, label ='Odometrie')
	plt.plot(t, diff, label ='diff')
	plt.grid(True)
	plt.legend()

	plt.figure()
	plt.plot(x, theta1, label ='Reperage')
	plt.plot(x, theta2, label ='Odometrie')
	plt.plot(x, diff, label ='diff')
	plt.grid(True)
	plt.legend()




 
