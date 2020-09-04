#!/usr/bin/python
import matplotlib.pyplot as plt
import matplotlib.mlab
from math import *

datas=[]
datasRalenti=[]

def Import(filename):
    datas=matplotlib.mlab.csv2rec(filename,delimiter='\t')
    return datas

def Plot():
    plt.figure()
    ax1 = plt.subplot(3,1,1)
    ax1.plot(datas.timestamp, datas.xa0, '-*', label="XA0")
    ax1.plot(datas.timestamp, datas.ya0, '-*', label="YA0")
    ax1.plot(datas.timestamp, datas.xai, '-*', label="XAi")
    ax1.plot(datas.timestamp, datas.yai, '-*', label="YAI")
    ax1.legend()
    ax1.grid(True)

    ax2 = plt.subplot(3,1,2, sharex=ax1)
    ax2.plot(datas.timestamp, datas.xr0, '-*', label="XR0")
    ax2.plot(datas.timestamp, datas.yr0, '-*', label="YR0")
    ax2.plot(datas.timestamp, datas.xri, '-*', label="XRi")
    ax2.plot(datas.timestamp, datas.yri, '-*', label="YRi")
    ax2.legend()
    ax2.grid(True)

    ax3 = plt.subplot(3,1,3, sharex=ax1)
    ax3.plot(datas.timestamp, datas.thetaa, '-*', label="ThetaA")
    ax3.plot(datas.timestamp, datas.thetar, '-*', label="ThetaR")
    ax3.plot(datas.timestamp, datas.thetanp, '-*', label="ThetaNP")
    ax3.legend()
    ax3.grid(True)

def PlotT2():
    plt.figure()
    ax1 = plt.subplot(2,1,1)
    ax1.plot(datas.timestamp, datas.dtheta, '-*', label="dtheta")
    ax1.legend()
    ax1.grid(True)

    ax2 = plt.subplot(2,1,2, sharex=ax1)
    ax2.plot(datas.timestamp, datas.dx, '-*', label="dx")
    ax2.plot(datas.timestamp, datas.dy, '-*', label="dy")
    ax2.plot(datas.timestamp, datas.dylateral, '-*', label="dyLateral")
    ax2.legend()
    ax2.grid(True)

def PlotXY2(scale = 1.0):
	plt.figure('XY')
	plt.quiver(datas.xreel,datas.yreel, datas.dx, datas.dy, width=0.0025, angles='xy', scale_units='xy', scale=scale,label="Recalage")
	plt.plot(datas.xmesure,datas.ymesure, '-x' ,label="mesure")


def PlotXY():
    plt.figure('XY')
    plt.plot(datas.xa0, datas.ya0, '*', label='Abs0')
    plt.plot(datas.xai, datas.yai, '*', label='AbsI')
    
    x0=[]
    y0=[]
    for data in datas:
        x0.append(data.xnp+data.xr0*cos(data.thetanp)-data.yr0*sin(data.thetanp))
        y0.append(data.ynp+data.xr0*sin(data.thetanp)+data.yr0*cos(data.thetanp))
    plt.plot(x0,y0, '*', label='RelAv')

    xi=[]
    yi=[]
    for data in datas:
        xi.append(data.xnp+data.xri*cos(data.thetanp)-data.yri*sin(data.thetanp))
        yi.append(data.ynp+data.xri*sin(data.thetanp)+data.yri*cos(data.thetanp))
    plt.plot(xi,yi, '*', label='RelAr')

    for i in range(0,len(datas)):
        data=datas[i]
        plt.plot([data.xa0, data.xai],[data.ya0, data.yai], color='blue')
        plt.plot([x0[i],xi[i]],[y0[i],yi[i]], color='pink')

    plt.legend()
    

plt.ion()
try:
    datas=Import("DeuxAntennesTranspondeur.txt")
    print 'LogDeuxAntennesTranspondeur:import datas OK'
except IOError:
    print 'LogDeuxAntennesTranspondeur:Could not import datas'
