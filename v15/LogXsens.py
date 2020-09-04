#!/usr/bin/python
import matplotlib.pyplot
import matplotlib.mlab
import scipy
import pylab
import numpy
import scipy.signal
from scipy import interpolate

from math import *

import Utils
import LogReperage
import Track
import LogDeltaNP
import ConfigAgv
import LogNavigation

try:
    tcycle = 0.001* ConfigAgv.configAgv['Parameters']['Application.DataConfig']['TempsCycle']
    print "Tcycle=", tcycle, ' s'
except:
    print "Could not find time cycle from configAgv"
    tcycle = ( (int)(100*(LogReperage.datas[1].timestamp-LogReperage.datas[0].timestamp)))/100.0
    print "Tcycle=", tcycle, ' s'

drift_a=0
drift_b=0

#Date Hour	TimeStamp	Cycle	Roll	Pitch	Yaw	AccX	AccY	AccZ	VitX	VitY	VitZ	

def Import(filename):
	print "LogXsens reading", filename, "..."
	datas=matplotlib.mlab.csv2rec(filename,delimiter='\t')
	print "LogXsens:", filename, "OK n=", len(datas)
	return datas

def Extract():
	acc=numpy.array([])
	w=[]
	angle=[]
	mag = []
	q = []
	has_mag = datas.dtype.fields.has_key("magx")
	acc    = numpy.array([[data.accx, data.accy, data.accz] for data in datas])
	w      = numpy.array([[data.vitx, data.vity, data.vitz] for data in datas])
	angle  = numpy.deg2rad(numpy.array([[data.yaw, data.pitch, data.roll] for data in datas]))
	if has_mag:
		mag  = numpy.array( [ [data.magx, data.magy, data.magz] for data in datas ] ) 

	if datas.dtype.fields.has_key("q0"):
		q = numpy.array([[data.q0, data.q1, data.q2, data.q3] for data in datas])

	return angle, acc, w, mag,q
		
def PlotT():
	matplotlib.pyplot.figure()

	ax1 = matplotlib.pyplot.subplot(3,1,1)
	ax1.plot(t, acc[:,0], '-', label="AccX")
	ax1.plot(t, acc[:,1], '-', label="AccY")
	ax1.plot(t, acc[:,2], '-', label="AccZ")
	ax1.plot(t, ac2[:,0], '-', label="Acc2X")
	ax1.plot(t, ac2[:,1], '-', label="Acc2Y")
	ax1.plot(t, ac2[:,2], '-', label="Acc2Z")
	Utils.FormatAxe(ax1, "Accelerations", "t(s)", "m/s^2")


	ax2 = matplotlib.pyplot.subplot(3,1,2, sharex=ax1)
	ax2.plot(t, numpy.rad2deg(w[:,0]), '-', label="WX")
	ax2.plot(t, numpy.rad2deg(w[:,1]), '-', label="WY")
	ax2.plot(t, numpy.rad2deg(w[:,2]), '-', label="WZ")
	ax2.plot(t, numpy.rad2deg(w2[:,0]), '-', label="W2X")
	ax2.plot(t, numpy.rad2deg(w2[:,1]), '-', label="W2Y")
	ax2.plot(t, numpy.rad2deg(w2[:,2]), '-', label="W2Z")

	ax2.plot(t, numpy.rad2deg(odomYawVelocity), '-+', label="WZ-Encoders")
	Utils.FormatAxe(ax2, "angular velocity", "t(s)", "deg/s")

	ax3 = matplotlib.pyplot.subplot(3,1,3, sharex=ax1)
	ax3.plot(t, numpy.rad2deg(angle[:,0]), '-', label="Yaw")
	ax3.plot(t, numpy.rad2deg(angle[:,1]), '-', label="RollY")
	ax3.plot(t, numpy.rad2deg(angle[:,2]), '-', label="Pitch")
	Utils.FormatAxe(ax3, "Euler angles", "t(s)", "deg")


def PlotRollDy():
    matplotlib.pyplot.figure()
    ax1 = matplotlib.pyplot.subplot(3,1,1)
    ax1.plot(LogNavigation.datas.timestamp, LogNavigation.datas.dy)
    Utils.FormatAxe(ax1, "dy", "t(s)", "ml")

    ax2 = matplotlib.pyplot.subplot(3,1,2, sharex=ax1)
    ax2.plot(t, numpy.rad2deg(w[:,0]), '.', label="WX")
    ax2.plot(t, Utils.low_pass_filter(numpy.rad2deg(w[:,0]), fe=1.0/tcycle, fc=0.5),
         '-', label="WX-filtered", linewidth=4)
    ax2.plot(t, numpy.rad2deg(w[:,1]), '.', label="WY")
    ax2.plot(t, Utils.low_pass_filter(numpy.rad2deg(w[:,1]), fe=1.0/tcycle, fc=0.5),
         '-', label="WY-filtered", linewidth=4)
    Utils.FormatAxe(ax1, "wx", "t(s)", "deg/s")

    ax3 = matplotlib.pyplot.subplot(3,1,3, sharex=ax1)
    ax3.plot(datas.timestamp, datas.roll, label='roll')
    ax3.plot(datas.timestamp, datas.pitch, label='pitch')
    ax3.legend()
    Utils.FormatAxe(ax2, "roll/pitch", "t(s)", "deg")

    idTrcPrec = -1
    sPrec = 0
    for data in LogNavigation.datas:
        idTrc = data.idtrc
        s = data.d
        #if idTrc != idTrcPrec:
        if s <= sPrec or idTrcPrec != idTrc:
            ax1.plot([data.timestamp, data.timestamp], [-100,100], color='black')
            ax3.plot([data.timestamp, data.timestamp], [-100,100], color='black')
            lbl = 'T'+str(idTrc)
            ax1.text(data.timestamp, 100, lbl, rotation=45)
            idTrcPrec = idTrc
            sPrec = s

    matplotlib.pyplot.figure()
    matplotlib.pyplot.plot(t, Utils.low_pass_filter(100.0*numpy.rad2deg(w[:,0]), fe=1.0/tcycle, fc=0.5),
         '-', label="WX-filtered", linewidth=4)
    matplotlib.pyplot.plot(LogNavigation.datas.timestamp, LogNavigation.datas.dy)


def PlotCorrelationDyWx():
    #y = Utils.low_pass_filter(numpy.rad2deg(w[:,0]), fe=1.0/tcycle, fc=0.5)
    y = numpy.rad2deg(w[:,0])
    t = datas.timestamp
    t2 = LogNavigation.datas.timestamp
    y2 = LogNavigation.datas.dy
    f=interpolate.interp1d(t2, y2, bounds_error=False, fill_value=0, copy=False)
    y3 = [ f(ti) for ti in t]
    fig = matplotlib.pyplot.figure()
    ax = matplotlib.pyplot.subplot(1,1,1)
    ax.plot(y, y3, '.')
    Utils.FormatAxe(ax, "dy", "wx filtered (deg/s)", "mm")
    
    
def PlotYawVelocity():
	matplotlib.pyplot.figure()
	ax1 = matplotlib.pyplot.subplot(1,1,1)
	#ax1.plot(t, numpy.rad2deg(w[:,2]), '-', label="WZ")
	ax1.plot(t, numpy.rad2deg(w2[:,2]), '-', label="W2Z")
	ax1.plot(t, numpy.rad2deg(odomYawVelocity), '-+', label="WZ-Encoders")
	#ax1.plot(t, numpy.rad2deg(odomYawVelocity-w[:,2]), '-+', label="err1")

	err2 = odomYawVelocity-w2[:,2]
	ax1.plot(t, numpy.rad2deg(err2), '-+', label="err2")
	
	err3 = Utils.low_pass_filter(err2, 1/tcycle, 2.0)
	ax1.plot(t, numpy.rad2deg(err3), '-+', label="err3(filtre)")

	Utils.FormatAxe(ax1, "angular velocity", "t(s)", "deg/s")

# Yaw compultations

def XsensYaw():
	return [ realYaw[n2] - angle[n2,0] + theta for theta in angle[:,0] ]	

'''
def IntegratedYaw():
	res = []
	#initialze integration correctly
	theta = realYaw[0]
	res.append(theta)
	for i in range(0,len(dt)):
		theta=theta+w[i,2]*dt[i]
		theta = ((theta+pi)%(2*pi))-pi
		res.append(theta)
	return numpy.array(res)
'''

def IntegratedYaw():
	res = []
	#initialze integration correctly
	theta = realYaw[0]
	res.append(theta)
	for i in range(0,len(dt)):
		m = EulerRotationMatrix(0,angle[i,1],angle[i,2])
		w2 = pylab.dot(m,w[i,:])
		theta=theta+w2[2]*dt[i]
		theta = ((theta+pi)%(2*pi))-pi
		res.append(theta)
	return numpy.array(res)

def OdomYawVelocity():
	res = numpy.multiply(deltaNP.dtheta, 1.0/ tcycle); 
	return pylab.array(res)

def OdomYaw():	
	theta = realYaw[0]
	# odometry rear wheels
	yaw = [theta]
	for i in range(0,len(dt)):
		if t[i]>t2:
			#theta = Utils.Mod2Pi(theta + dt[i]*(arD.vitesseinst[i]-arG.vitesseinst[i])/Track.dataAgv.voie)
			theta = theta + odomYawVelocity[i]*dt[i]
		else:
			theta = realYaw[i]
		yaw.append(theta)
	return numpy.array(yaw)

def ComputePositionYaw(t0):
	x = []
	y = []
	theta = []

	for i in range(0,len(t)):
		if t[i]<=t0 or i==0:
			xi = real.x[i]
			yi = real.y[i]
			thetai = real.theta[i]
		else:
			thetai = thetai + xsensYaw[i] - xsensYaw[i-1]
			xi = xi + deltaNP[i].dx * cos(thetai) - deltaNP[i].dy * sin(thetai) 
			yi = yi + deltaNP[i].dx * sin(thetai) + deltaNP[i].dy * cos(thetai) 

		x.append(xi)
		y.append(yi)
		theta.append(thetai)
	return x, y, theta

def ComputePositionOdom(t0):
	x = []
	y = []
	theta = []

	for i in range(0,len(t)):
		if t[i]<=t0 or i==0:
			xi = real.x[i] 
			yi = real.y[i]
			thetai = real.theta[i]
		else:
			thetai = thetai + deltaNP[i].dtheta
			xi = xi + deltaNP[i].dx * cos(thetai) - deltaNP[i].dy * sin(thetai) 
			yi = yi + deltaNP[i].dx * sin(thetai) + deltaNP[i].dy * cos(thetai) 

		x.append(xi)
		y.append(yi)
		theta.append(thetai)
	return x, y, theta

def ComputePositionMagnet(distAntenne, useYaw):
	x = []
	y = []
	theta = []
	d = 0

	recalTheta=[]
	recalY=[]

	previousMagnet=numpy.array([real.x[0], real.y[0]])

	for i in range(0,len(t)):
		if i == 0:
			xi = real.x[0] 
			yi = real.y[0]
			thetai = real.theta[0]
		elif d < 2000:
			if useYaw:
				thetai = thetai + xsensYaw[i] -  xsensYaw[i-1]
			else:
				thetai = thetai + deltaNP[i].dtheta

			xi = xi + deltaNP[i].dx * cos(thetai) - deltaNP[i].dy * sin(thetai) 
			yi = yi + deltaNP[i].dx * sin(thetai) + deltaNP[i].dy * cos(thetai) 


			d = d +  numpy.linalg.norm( [deltaNP[i].dx,deltaNP[i].dy] ,2)
		else:
			thetai = thetai + deltaNP[i].dtheta
			xi = xi + deltaNP[i].dx * cos(thetai) - deltaNP[i].dy * sin(thetai) 
			yi = yi + deltaNP[i].dx * sin(thetai) + deltaNP[i].dy * cos(thetai) 

			posMagnetReel = numpy.array( [real.x[i]+distAntenne*cos(real.theta[i]), real.y[i]+distAntenne*sin(real.theta[i]) ])
			posMagnetEstime = numpy.array( [xi+distAntenne*cos(thetai), yi+distAntenne*sin(thetai) ])
			dMagnet = numpy.linalg.norm( posMagnetReel - previousMagnet)
			if dMagnet > 1000:
				a = posMagnetReel - previousMagnet
				b = posMagnetEstime - previousMagnet
				dy = numpy.cross(a,b)/numpy.linalg.norm(a)
				dtheta = dy/dMagnet

				recalTheta.append(dtheta)
				recalY.append(dy)

				thetai = thetai - dtheta
				xi = real.x[i] 
				yi = real.y[i]
				previousMagnet = posMagnetReel
				d = 0

		x.append(xi)
		y.append(yi)
		theta.append(thetai)
	print "Resultat. std dev, y=", numpy.std(recalY), ", theta=", numpy.std(recalTheta)*180/pi
	print "Resultat. MAX, y=", numpy.max(recalY), ", theta=", numpy.max(recalTheta)*180/pi
	print "Resultat. MIN, y=", numpy.min(recalY), ", theta=", numpy.min(recalTheta)*180/pi
	print "Resultat. AVG, y=", numpy.average(recalY), ", theta=", numpy.average(recalTheta)*180/pi
	return x, y, theta


def DerivePos():
	distance=[]
	di = 0
	for dx in deltaNP:
		di = di + dx
		distance.append(di)
	do = []
	for i in range(0,len(t)):
		do.append( sqrt((real.x-xo)*(real.x-xo)+(real.y-xo)*(real.y-xo)) )
	matplotlib.pyplot.figure()

	matplotlib.pyplot.plot(d, do, label='do')
	matplotlib.pyplot.plot(d, numpy.multiply(0.01,d), label='lim+')
	matplotlib.pyplot.plot(d, numpy.multiply(-0.01,d), label='lim-')

	matplotlib.pyplot.grid(True)
	#matplotlib.pyplot.axis('equal')
	matplotlib.pyplot.legend()


def PlotPosition():
	matplotlib.pyplot.figure()

	matplotlib.pyplot.plot(real.x, real.y, label='real')
	matplotlib.pyplot.plot(x, y, label='yaw')
	matplotlib.pyplot.plot(x2, y2, label='I yaw')
	matplotlib.pyplot.plot(xo, yo, label='odom')
	"""
	matplotlib.pyplot.plot(xm, ym, label='magnet 0')
	matplotlib.pyplot.plot(xm2, ym2, label='magnet 2000')
	matplotlib.pyplot.plot(xm_, ym_, label='magnet 0')
	matplotlib.pyplot.plot(xm2_, ym2_, label='magnet 2000')
	"""
	matplotlib.pyplot.grid(True)
	matplotlib.pyplot.legend()

	matplotlib.pyplot.figure()
	ax1 = matplotlib.pyplot.subplot(2,1,1)
	ax2 = matplotlib.pyplot.subplot(2,1,2,sharex=ax1)
	ax1.plot(t, real.x, label='real.x')
	ax2.plot(t, real.y, label='real.y')
	ax1.plot(t, x, label='yaw.x')
	ax2.plot(t, y, label='yaw.y')
	ax1.plot(t[0:-1], x2, label='Iyaw.x')
	ax2.plot(t[0:-1], y2, label='Iyaw.y')
	ax1.plot(t, xo, label='odomAR.x')
	ax2.plot(t, yo, label='odomAR.y')

	"""
	ax1.plot(t, xm, label='m.x')
	ax2.plot(t, ym, label='m.y')
	ax1.plot(t, xm2, label='m2.x')
	ax2.plot(t, ym2, label='m2.y')

	ax1.plot(t, xm_, label='m_.x')
	ax2.plot(t, ym_, label='m_.y')
	ax1.plot(t, xm2_, label='m2_.x')
	ax2.plot(t, ym2_, label='m2_.y')
	"""

	ax1.grid(True)
	ax1.legend()
	ax2.grid(True)
	ax2.legend()

	matplotlib.pyplot.figure()
	ax1 = matplotlib.pyplot.subplot(2,1,1)
	ax2 = matplotlib.pyplot.subplot(2,1,2,sharex=ax1)
	ax1.plot(t, x-real.x, label='yaw.x')
	ax2.plot(t, y-real.y, label='yaw.y')
	ax1.plot(t[0:-1], x2-real.x[0:-1], label='Iyaw.x')
	ax2.plot(t[0:-1], y2-real.y[0:-1], label='Iyaw.y')
	ax1.plot(t, xo-real.x, label='odomAR.x')
	ax2.plot(t, yo-real.y, label='odomAR.y')
	ax1.plot(t[0:-1], xo2-real.x[0:-1], label='odomAV.x')
	ax2.plot(t[0:-1], yo2-real.y[0:-1], label='odomAV.y')
	Utils.FormatAxe(ax1, "X Error", "t(s)", "mm")
	Utils.FormatAxe(ax2, "Y Error", "t(s)", "mm")

	matplotlib.pyplot.figure()
	#matplotlib.pyplot.plot(t, Utils.Mod2Pi(real.theta),    label='real')
	matplotlib.pyplot.plot(t, Utils.Mod2Pi(theta-real.theta),         label='yaw')
	matplotlib.pyplot.plot(t, Utils.Mod2Pi(thetao-real.theta),        label='odomAR')
	"""
	matplotlib.pyplot.plot(t, Utils.Mod2Pi(thetam-real.theta), '*-',  label='m')
	matplotlib.pyplot.plot(t, Utils.Mod2Pi(thetam2-real.theta),'+-',  label='m2')
	matplotlib.pyplot.plot(t, Utils.Mod2Pi(thetam_-real.theta), '*-',  label='m_')
	matplotlib.pyplot.plot(t, Utils.Mod2Pi(thetam2_-real.theta),'+-',  label='m2_')
	"""
	#matplotlib.pyplot.plot(t[0:-1], Utils.Mod2Pi(thetao2-real.theta), label='odomAV')
	"""--- repere agv """
	dxAgv = []
	dyAgv = []
	r = []
	d = []
	di = 0
	for i in range(0,len(t)):
		dx = real.x[i]-x[i]
		dy = real.y[i]-y[i]
		di = di + sqrt( deltaNP.dx[i]*deltaNP.dx[i] + deltaNP.dy[i]*deltaNP.dy[i])
		thetai = real.theta[i]
		d.append(di)
		dxAgv.append( dx*cos(thetai)+dy*sin(thetai))
		dyAgv.append( -dx*sin(thetai)+dy*cos(thetai))
		r.append(sqrt(dx*dx+dy*dy))

	matplotlib.pyplot.figure()
	matplotlib.pyplot.grid(True)
	matplotlib.pyplot.legend()
	ax1 = matplotlib.pyplot.subplot(1,1,1)
	ax1.plot(d, dxAgv, label='dxAgv')
	ax1.plot(d, dyAgv, label='dyAgv')
	ax1.plot(d, r, label='r')
	Utils.FormatAxe(ax1, "Error/R AGV", "d(mm)", "mm")

	matplotlib.pyplot.figure()
	matplotlib.pyplot.grid(True)
	matplotlib.pyplot.legend()
	ax1 = matplotlib.pyplot.subplot(1,1,1)
	ax1.plot(t, dxAgv, label='dxAgv')
	ax1.plot(t, dyAgv, label='dyAgv')
	ax1.plot(t, r, label='r')
	Utils.FormatAxe(ax1, "Error/R AGV", "t(s)", "mm")


def RotationMatrix2D(theta):
	c = cos(theta)
	s = sin(theta)
	return numpy.array([ [ c, -s], [s, c] ])

def EulerRotationMatrix(yaw,roll,pitch):
	# yaw,roll pith is phi,theta,psi
	cphi = cos(yaw)
	sphi = sin(yaw)
	ctheta = cos(roll)
	stheta = sin(roll)
	cpsi = cos(pitch)
	spsi = sin(pitch)

	m = pylab.array( 
           [ [ cphi*ctheta, cphi*stheta*spsi-sphi*cpsi, cphi*stheta*cpsi+sphi*spsi ],
           [ sphi*ctheta, sphi*stheta*spsi+cphi*cpsi, sphi*stheta*cpsi-cphi*spsi],
           [ -stheta, ctheta*spsi, ctheta*cpsi ] ] )
	return m

def CalculateDrift(n1, n2):
	e = [ continuousIntegratedYaw[i]-continuousRealYaw[i] for i in range(n1, n2) ]
	a,b = numpy.polyfit( t[n1:n2], e, 1)
	b = b + a*t1
	return a, b
	
def DriftYaw():
	drift = Drift()
	res = []
	debut = True
	prevT= t[0]
	s = 0
	for ti,yaw,drifti in zip(t,integratedYaw,drift):
		#drifti = numpy.deg2rad(20.0/3600)
		dt = ti - prevT
		s = s + drifti*dt
		#s = drifti*(ti-t[0])
		yaw2 = yaw - s
		res.append(yaw2)
		prevT = ti
	return res
	
def PlotYaw():
	matplotlib.pyplot.figure()
	ax1 = matplotlib.pyplot.subplot(2,1,1)
	ax1.plot(t,         numpy.rad2deg(Utils.ContinuousAngle(realYaw)),       '-+', label='real yaw')
	ax1.plot(t,         numpy.rad2deg(Utils.ContinuousAngle(xsensYaw)),      '-+', label='xsens yaw')
	ax1.plot(t,         numpy.rad2deg(Utils.ContinuousAngle(odomYaw)),       '-+', label='odom yaw')
	ax1.plot(t[0:-1],   numpy.rad2deg(Utils.ContinuousAngle(driftYaw)),      '-+', label='yaw drift')
	ax1.plot(t,         numpy.rad2deg(Utils.ContinuousAngle(integratedYaw)), '-+', label='integrated Yaw')
	
	if real.dtype.fields.has_key("psitheta"):
		ax1.plot(real.timestamp, numpy.rad2deg(Utils.ContinuousAngle(real.psitheta)), '-o', label='psi')

	ax1.plot([t1, t2], [0,0], 					'*' , label='drift ref')
	#ax1.plot(t,         numpy.rad2deg(Utils.Mod2Pi(deltaNP.theta)),            label='deltaNp')
	Utils.FormatAxe(ax1, "Yaw", "t(s)", "deg")


	ax2 = matplotlib.pyplot.subplot(2,1,2, sharex=ax1)
	ax2.plot(t,         numpy.rad2deg(Utils.Mod2Pi(integratedYaw-realYaw)),'-',      label='integrated yaw')
	ax2.plot(t,         numpy.rad2deg(Utils.Mod2Pi(xsensYaw-realYaw)),               label='xsens yaw')
	ax2.plot(t,         numpy.rad2deg(Utils.Mod2Pi(odomYaw-realYaw)),                label='odom yaw')
	#ax2.plot(t[0:-1],   numpy.rad2deg(Utils.Mod2Pi(driftYaw-realYaw[0:-1])), '-+',   label='yaw drift')
	ax2.plot([t1, t2], [0,0], '*',                                      label='drift ref')
	Utils.FormatAxe(ax2, "Yaw Error", "t(s)", "deg")

def Drift():
	drift = [ w[i,2]- Utils.Mod2Pi(realYaw[1+i]-realYaw[i])/(t[1+i]-t[i]) for i in range(0,len(t)-1)]

	fe = 1/0.03
	fc = 1/100.0
	a = 1 / ( 1 + fe/fc)
	b = 1 / ( 1 + fc/fe)

	drift2 = []
	d2 = 0

	# une seconde d'immobilite est necessaire
	nb = int(1.0/0.03)
	k = 0

	for i in range(0,len(drift)):
		d=drift[i]

		# estimation du biais seulement si vtheta < 1 deg/s
		if fabs(w[i,2]) < numpy.deg2rad(2.0):
			k = k + 1
		else:
			k = 0

		if k > nb : 
			d2 = a*d + b*d2
		else:
			d2 = d2
		drift2.append(d2)
	return drift2

def PlotDrift():
	driftI = [ w[i,2]- Utils.Mod2Pi(realYaw[1+i]-realYaw[i])/(t[1+i]-t[i]) for i in range(0,len(t)-1)]
	driftE = Drift()

	matplotlib.pyplot.figure()
	ax1 = matplotlib.pyplot.subplot(1,1,1)
	#ax1.plot(t[0:-1], numpy.multiply(numpy.rad2deg(Utils.Utils.low_pass_filter(driftI,1/0.03,1/200.0)),3600), '-', label='dritfI')
	ax1.plot(t[0:-1], numpy.multiply(numpy.rad2deg(driftE),3600), '-', label='dritfE')
	Utils.FormatAxe(ax1, 'drift', "t(s)", "deg/h")

def PlotMag():
	ax1 = matplotlib.pyplot.subplot(1,1,1)
	ax1.plot(t, mag[:,0], label='magX')
	ax1.plot(t, mag[:,1], label='magY')
	ax1.plot(t, mag[:,2], label='magZ')
	Utils.FormatAxe(ax1, "magnetic field", "t(s)", "magnetic field unit(?)")

def PlotAcc():
	# ------------------ X
	matplotlib.pyplot.figure()
	ax1 = matplotlib.pyplot.subplot(2,1,1)
	ax1.plot(t, ac2[:,0], '-', label="Acc2X-Xsens")
	ax1.plot(t[0:-1], accNPgyro[:,0], '-o', label="accNP gyro x")
	Utils.FormatAxe(ax1, "Gyro - Accelerations", "t(s)", "m/s^2")

	ax2 = matplotlib.pyplot.subplot(2,1,2, sharex=ax1)

	ax2.plot(t[0:-1], accNPodom[:,0], '-x', label="accNP odom x")
	Utils.FormatAxe(ax2, "Odom Accelerations", "t(s)", "m/s")


	# ------------------ Y
	matplotlib.pyplot.figure()
	ax1 = matplotlib.pyplot.subplot(2,1,1)
	ax1.plot(t, ac2[:,1], '-', label="Acc2Y-Xsens")
	ax1.plot(t[0:-1], accNPgyro[:,1], '-o', label="accNP gyro y")
	Utils.FormatAxe(ax1, "Gyro - Accelerations", "t(s)", "m/s^2")

	ax2 = matplotlib.pyplot.subplot(2,1,2, sharex=ax1)
	#ax2.plot(t[0:-1], accNPodom[:,0], '-x', label="accNP odom x")
	ax2.plot(t[0:-1], accNPodom[:,1], '-x', label="accNP odom y")
	Utils.FormatAxe(ax2, "Odom Accelerations", "t(s)", "m/s")

	# ------------------ Z

	matplotlib.pyplot.figure()
	ax1 = matplotlib.pyplot.subplot(1,1,1)

	ax1.plot(t, acc[:,2], '-', label="AccZ-Xsens")
	ax1.plot(t, ac2[:,2], '-', label="Acc2Z-Xsens")
	Utils.FormatAxe(ax1, "Accelerations Z", "t(s)", "m/s")

	# ============================

	matplotlib.pyplot.figure()
	ax1 = matplotlib.pyplot.subplot(2,1,1)

	ax1.plot(t[0:-1], numpy.multiply(accNPgyro[:,0],1000), '.', label="accNP gyro x")
	ax1.plot(t[0:-1], accNPodom[:,0], '-', label="accNP odom x")
	ax1.plot(t[0:-2], Utils.low_pass_filter(reperageAcc[:,0]), '-', label="accNP reperage x")
	ax1.plot(t[0:-1], Utils.low_pass_filter(numpy.multiply(accNPgyro[:,0],1000)), '-x', label="F accNP gyro x")
	ax1.plot(t[0:-1], Utils.low_pass_filter(accNPodom[:,0]), '-x', label="F accNP odom x")	
	Utils.FormatAxe(ax1, "Gyro - Odom Acc  X", "t(s)", "m/s^2")

	ax2 = matplotlib.pyplot.subplot(2,1,2, sharex=ax1)
	ax2.plot(t[0:-1], numpy.multiply(accNPgyro[:,1],1000), '.', label="accNP gyro y")
	ax2.plot(t[0:-1], accNPodom[:,1], '-', label="accNP odom y")
	ax2.plot(t[0:-2], Utils.low_pass_filter(reperageAcc[:,1]), '-', label="accNP reperage y")
	ax2.plot(t[0:-1], Utils.low_pass_filter(numpy.multiply(accNPgyro[:,1],1000)), '-x', label="F accNP gyro y")
	ax2.plot(t[0:-1], Utils.low_pass_filter(accNPodom[:,1]), '-x', label="F accNP odom y")
	Utils.FormatAxe(ax2, "Gyro - Odom Acc  Y", "t(s)", "m/s^2")

	# ============================
	matplotlib.pyplot.figure()
	ax1 = matplotlib.pyplot.subplot(1,1,1)
	ax1.plot(t[0:-1], Utils.low_pass_filter(numpy.multiply(accNPgyro[:,0],1000)-accNPodom[:,0]), '-x', label="F diff acc x")
	ax1.plot(t[0:-1], Utils.low_pass_filter(numpy.multiply(accNPgyro[:,1],1000)-accNPodom[:,1]), '-x', label="F diff acc y")
	Utils.FormatAxe(ax1, "Gyro - Diff Acc  F", "t(s)", "m/s^2")

def ConvertToAbs():
	resAcc = []
	resW = []
	n = len(t)
	for i in range(0,n):
		m = EulerRotationMatrix(0,angle[i,1],angle[i,2])
		acc2 = pylab.dot(m,acc[i,:])
		resAcc = Utils.AddArrayLine(resAcc, acc2)

		w2 = pylab.dot(m,w[i,:])
		resW = Utils.AddArrayLine(resW, w2)
	return resAcc,resW

''' compute NP acceleration from motion control data & odom. The derivation of w is noisy, result to be filtered !
@return accGyro acceleration of the NP calculated  with motion control
@return accOdom acceleration of the NP calculateur with dead reckoning
'''
def ComputeAccNP():
	'''wz = w[:,2] '''
	ab = numpy.array([1.040,-0.560,0.750])
	'''xa =  1.040
	ya = -0.560'''

	#debug components
	#c1 = []
	#c2 = []

	accGyro = []
	for i in range(0,len(dt)):
		'''ancienne formule 2D
		omega = wz[i]
		omega_prime = ( wz[i+1] - wz[i] ) / dt[i]
		a = ac2[i,:] + [ xa*omega*omega + ya*omega_prime , ya*omega*omega - xa*omega_prime, 0 ]
		avec 	wz = w[:,2]  
		'''
		omega = w[i]
		omega_prime = ( w[i+1] - w[i] ) / dt[i]
		a = ac2[i,:] - numpy.cross(omega_prime,ab) - numpy.cross(omega, numpy.cross(omega,ab))
		accGyro.append(a)

	accOdom = []
	for i in range(0,len(dt)):
		vtheta = odomYawVelocity[i]
		vx = odomSpeed[i,0]
		vy = odomSpeed[i,1]
		a0 = (odomSpeed[i+1,:]-odomSpeed[i,:])/dt[i]
		a = a0 + numpy.transpose([ 0, vtheta*vx ])
		accOdom.append(a)

	return numpy.array(accGyro), numpy.array(accOdom) #, numpy.array(c1), numpy.array(c2) 

def IntegratedSpeed():
	speed = pylab.array([0.0,0.0,0.0])
	res = []
	for i in range(0, pylab.shape(ac2)[0]-1):
		speed = speed + ac2[i,:]*dt[i]
		res = Utils.AddArrayLine(res, speed)
	return res


def ReperageSpeed():
	vx = (real.x[1:]-real.x[0:-1])/dt
	vy = (real.y[1:]-real.y[0:-1])/dt
	res = []
	for i in range(0,len(dt)):
		v = numpy.array( [vx[i], vy[i] ] )
		m = RotationMatrix2D( -real.theta[i] )
		res.append(numpy.dot(m,v))
	return numpy.array(res)

def ReperageAcc():
	ax = (reperageSpeed[1:,0]-reperageSpeed[0:-1,0])/dt[0:-1]
	ay = (reperageSpeed[1:,1]-reperageSpeed[0:-1,1])/dt[0:-1]
	return pylab.transpose(pylab.array([ax,ay]))

def OdomSpeed():
	res = []
	for i in range(0,len(t)):
		vx = deltaNP.dx[i] / tcycle
		vy = deltaNP.dy[i] / tcycle
		res = Utils.AddArrayLine(res, numpy.array([vx,vy]))
	return res

def PlotQ():
	# ------------------ X

	matplotlib.pyplot.figure()
	ax1 = matplotlib.pyplot.subplot(2,1,1)
	ax1.plot(t, q[:,0], '-', label="q0")
	ax1.plot(t, q[:,1], '-', label="q1")
	ax1.plot(t, q[:,2], '-', label="q2")
	ax1.plot(t, q[:,3], '-', label="q3")

	ax2 = matplotlib.pyplot.subplot(2,1,2, sharex=ax1)
	ax2.plot(t[0:-1], q[1:,0]-q[:-1,0], '-', label="dq0")
	ax2.plot(t[0:-1], q[1:,1]-q[:-1,1], '-', label="dq1")
	ax2.plot(t[0:-1], q[1:,2]-q[:-1,2], '-', label="dq2")
	ax2.plot(t[0:-1], q[1:,3]-q[:-1,3], '-', label="dq3")

def PlotSpeed():
	matplotlib.pyplot.figure()
	ax1 = matplotlib.pyplot.subplot(1,1,1)
	ax1.plot(t, odomSpeed[:,0], '-', label='odomX')
	ax1.plot(t, odomSpeed[:,1], '-', label='odomY')
	ax1.plot(t[0:-1], deltaNP.dx[0:-1]/dt, '-', label='dnpx')
	ax1.plot(t[0:-1], deltaNP.dy[0:-1]/dt, '-', label='dnpy')
	ax1.plot(t[0:-1], numpy.multiply(integratedSpeed[:,0],1000), '-', label='intx')
	ax1.plot(t[0:-1], numpy.multiply(integratedSpeed[:,0],1000), '-', label='inty')
	Utils.FormatAxe(ax1, "speeds", "t(s)", "mm/s")


#quaternions

def conjugate(q):
	return Quaternion.quaternion((q.q[0],-q.q[1],-q.q[2],-q.q[3]))

def computeQ():
	qlist=[]
	for qi in q:
	        if  numpy.max(qi) == 0.0:
			qi = numpy.array([ 1.,  0.,  0.,  0.])
		quat = Quaternion.quaternion(qi)
        	qlist.append(quat.unit())
	dq=[]
	for i in range(0,len(q)-1):
		dq.append((qlist[i+1]-qlist[i])/dt[i])

	w=[]
	for i in range(0,len(q)-1):
		w.append( 2.0*dq[i]*qlist[i].inv() )

	return qlist,w

matplotlib.pyplot.ion()

print "Xsens Log Analyzer"
#matplotlib.pyplot.close("all")


print("import datas ....")
try:
	print("len(datas)=",len(datas),"(already loaded)")
except NameError:
	try:
		datas=Import("CentraleInertielleXSens.txt")
	except IOError:
		datas=Import("CentraleInertielle.txt")
	print("len(datas)=",len(datas),"loaded")

	print "Rescale logs..."
	[datas, real, deltaNP] = \
		Utils.TimeRescale([datas, LogReperage.datas, LogDeltaNP.datas] )
	t = datas.timestamp


	if real.dtype.fields.has_key("psitheta"):
		realYaw=real.psitheta
	else:
		realYaw=real.theta

	dt = t[1:]-t[0:-1]
	t1=t[0]+20
	t2=t[0]+60


	print '[t1, t2]=', t1, ' , ', t2, ']'
	cycle = numpy.average(dt)
	print "cycle=", cycle
	n1 = int((t1-t[0])/cycle)
	n2 = int((t2-t[0])/cycle)
	t1=t[n1]
	t2=t[n2]
	print '[t1, t2]=', t1, ' , ', t2, ']'

	print "Ectract fields..."
	angle, acc, w, mag, q = Extract()

	print "Odometry integration..."
	odomYawVelocity = OdomYawVelocity()
	odomYaw  = OdomYaw()
	print 'odomYaw=', odomYaw
	continuousRealYaw = Utils.ContinuousAngle(realYaw)
	integratedYaw=IntegratedYaw()
	continuousIntegratedYaw = Utils.ContinuousAngle(integratedYaw)
	print "...xsens"
	xsensYaw=XsensYaw()

	#print "Calculate Drift ..."
	drift_a, drift_b = CalculateDrift(n1, n2)
	print "disable drift"
	drift_a=0

	dritf=Drift()

	driftYaw=DriftYaw()
	print "Calculate acc&w/R0..."
	ac2, w2 =ConvertToAbs()

	print "Calculate Reperage datas"
	reperageSpeed=ReperageSpeed()
	reperageAcc=ReperageAcc()

	print "OdomSpeed"
	odomSpeed = OdomSpeed()

	print "Integrate speed"
	integratedSpeed = IntegratedSpeed()

	print "Calculate acc NP..."
	#accNPgyro, accNPodom, c1, c2 =ComputeAccNP()
	accNPgyro, accNPodom =ComputeAccNP()

	print "calculate pos..."
	print "yaw..."
	x,y,theta=ComputePositionYaw( t[0]+60 )
	print "odom..."
	xo,yo,thetao=ComputePositionOdom( t[0]+60 )

	print "Final offset:"
	print "odom"
	dx=xo[-1]-real.x[-1]
	dy=yo[-1]-real.y[-1]
	print "dx=",dx," dy=",dy, "d=", sqrt(dx*dx+dy*dy)
	print "yaw"
	dx= x[-1]-real.x[-1]
	dy= y[-1]-real.y[-1]
	print "dx=",dx," dy=",dy, "d=", sqrt(dx*dx+dy*dy)


def DriftInterpolate(ti):
	return Utils.InterpolateValue(t, drift, ti)

