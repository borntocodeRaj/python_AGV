#!/usr/bin/python
import matplotlib.pyplot as plt
import matplotlib.mlab
from math import *
import numpy

datas=[]
datasTranspondeurs=[]
datasSansInfra=[]


def Import(filename):
	datas=matplotlib.mlab.csv2rec(filename,delimiter='\t')
	return datas

#param traceReperageTranspondeur : True pour tracer la sortie du logTranspondeur
#param traceReperageSansInfra : True pour tracer la sortie du logSansInfra
def PlotXY(traceReperageTranspondeur=False, traceReperageSansInfra=False):
	plt.figure('XY')
	#adds 20 time markers
	for i in range(0,20):
		j=i*(len(datas.x)/20)
		plt.annotate("t="+str(datas.timestamp[j]),[datas.x[j],datas.y[j]], color='blue')

	x=[]
	y=[]
	for data in datas:
		theta=(data.theta-data.dtheta)*pi/180.0
		x.append(data.x+data.dy*sin(theta))
		y.append(data.y-data.dy*cos(theta))

	plt.plot(x, y, label='traj', color='red')

	plt.plot(datas.x, datas.y, marker='.', label='Nav', color='blue')

	if traceReperageTranspondeur and len(datasTranspondeurs)!=0:
		plt.plot(datasTranspondeurs.x, datasTranspondeurs.y, marker='+', label='reperageTranspondeurs', color='red')
	if traceReperageSansInfra and len(datasSansInfra)!=0:
		plt.plot(datasSansInfra.x, datasSansInfra.y, marker='+', label='reperageSansInfra', color='grey')

	plt.grid(True)

	plt.axis('equal')
	plt.legend()
	plt.grid(True)


def PlotAgv(dataAgv, data, color='black'):
    x = data.x
    y = data.y
    theta = numpy.deg2rad(data.theta)
    l = [ [ dataAgv.xAvGabaritAgv,  dataAgv.yGaucheGabaritAgv ] ,
          [ dataAgv.xAvGabaritAgv,  dataAgv.yDroiteGabaritAgv ] ,
          [ dataAgv.xArGabaritAgv,  dataAgv.yDroiteGabaritAgv ] ,
          [ dataAgv.xArGabaritAgv,  dataAgv.yGaucheGabaritAgv ] , 
          [ dataAgv.xAvGabaritAgv,  dataAgv.yGaucheGabaritAgv ] ] 

    lx = []
    ly = []
    for [ x2, y2 ] in l:
        lx.append( x + x2*cos(theta) - y2*sin(theta) )
        ly.append( y + x2*sin(theta) + y2*cos(theta) )
	plt.figure('XY')
    plt.plot(lx, ly, color=color)


def PlotWheelTraj(dataAgv):
	xRoueAv = dataAgv.xTourelleAv
	yRoueAv = dataAgv.yTourelleAv

	xRoueAr = dataAgv.xTourelleAr
	yRoueAr = dataAgv.yTourelleAr

	# NP
	xAv=[]
	yAv=[]
	xAr=[]
	yAr=[]

	# Traj
	xAvTraj=[]
	yAvTraj=[]
	xArTraj=[]
	yArTraj=[]

	plt.figure('XY')

	for data in datas:
		theta=(data.theta-data.dtheta)*pi/180.0
		x=data.x
		y=data.y
		xAv.append(x+xRoueAv*cos(theta)-yRoueAv*sin(theta))
		yAv.append(y+xRoueAv*sin(theta)+yRoueAv*cos(theta))
		xAr.append(x+xRoueAr*cos(theta)-yRoueAr*sin(theta))
		yAr.append(y+xRoueAr*sin(theta)+yRoueAr*cos(theta))

		x=data.x+data.dy*sin(theta)
		y=data.y-data.dy*cos(theta)
		xAvTraj.append(x+xRoueAv*cos(theta)-yRoueAv*sin(theta))
		yAvTraj.append(y+xRoueAv*sin(theta)+yRoueAv*cos(theta))
		xArTraj.append(x+xRoueAr*cos(theta)-yRoueAr*sin(theta))
		yArTraj.append(y+xRoueAr*sin(theta)+yRoueAr*cos(theta))

	plt.plot(xAv, yAv, '-', label='av')
	plt.plot(xAvTraj, yAvTraj, '-', label='avTraj')


	if dataAgv.nbTourelles == 2:
		plt.plot(xAr, yAr, '-', label='ar')
		plt.plot(xArTraj, yArTraj, '-', label='arTraj')
	plt.legend()
		
def PlotT(plotDerive=False):
	plt.figure()
	ax1 = plt.subplot(3,1,1)
	ax1.plot(datas.timestamp, datas.phiavcons, label="PhiAvCons")
	ax1.plot(datas.timestamp, datas.phiav,     label="PhiAv")
	ax1.plot(datas.timestamp, datas.phiarcons, label="PhiArCons")
	ax1.plot(datas.timestamp, datas.phiar,     label="PhiAr")
	ax1.plot(datas.timestamp, datas.theta,     label="Theta")
	
	if plotDerive==True:
		dt=datas.timestamp[1]-datas.timestamp[0]
		dphiAvdt=numpy.multiply(datas.phiav[1:-1]-datas.phiav[0:-2],1.0/dt)
		dphiArdt=numpy.multiply(datas.phiar[1:-1]-datas.phiar[0:-2],1.0/dt)
		ax1.plot(datas.timestamp[0:-2], dphiAvdt, label="dPhiAv/dt")
		ax1.plot(datas.timestamp[0:-2], dphiArdt, label="dPhiAr/dt")

	ax1.legend()
	ax1.grid(True)
	
	ax2 = plt.subplot(3,1,2, sharex=ax1)

	if len(datasTranspondeurs)!=0:
		ax2.plot(datasTranspondeurs.timestamp, datasTranspondeurs.dodom, label="dodomTranspondeurs")
	if len(datasSansInfra)!=0:
		ax2.plot(datasSansInfra.timestamp, datasSansInfra.dodom, label="dodomReperageSansInfra")
	ax2.plot(datas.timestamp, datas.s,       label="s",       linewidth=2)
	ax2.plot(datas.timestamp, datas.d_1,     label="d-",      linewidth=3)
	ax2.plot(datas.timestamp, datas.vavcons, label="VavCons", linewidth=2)
	ax2.plot(datas.timestamp, datas.vav,     label="Vav",     linewidth=3)
	ax2.plot(datas.timestamp, datas.varcons, label="VarCons", linewidth=2)
	ax2.plot(datas.timestamp, datas['var'],  label="Var",     linewidth=3)

	ax2.legend()
	ax2.grid(True)

	ax3 = plt.subplot(3,1,3, sharex=ax1)
	ax3.plot(datas.timestamp, datas.dy, '-+', label="dy")
	ax3.plot(datas.timestamp, [ 100.0*data.dtheta for data in datas], '-+', label="dtheta*100")
	ax3.plot(datas.timestamp, datas.dyav, '-+', label="dyav")

	ax3.legend()
	ax3.grid(True)

plt.ion()
try:
	datas=Import("NavigationLaser.txt")
	print 'LogNavigation:import datas OK'
except:
	print 'LogNavigation:Could not import datas'

try:
	datasTranspondeurs=Import("Transpondeur.txt")
	print 'LogNavigation:import transpondeurs OK'
except:
	print 'LogNavigation:Could not import transpondeurs'

try:
	datasSansInfra=Import("ReperageSansInfra.txt")
	print 'LogNavigation:import reperage sans infra OK'
except:
	print 'LogNavigation:Could not import reperage sans infra'



