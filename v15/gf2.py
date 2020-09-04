import Utils
import Track
import LogReperage
import LogEncoder
import matplotlib.pyplot as plt
import numpy

from math import *

def f_phiAvD(t):
    return Utils.InterpolateValue( LogEncoder.codeurDirectionAvD.timestamp,
                                   LogEncoder.codeurDirectionAvD.position, t)

def f_phiAvG(t):
    return Utils.InterpolateValue( LogEncoder.codeurDirectionAvG.timestamp,
                                   LogEncoder.codeurDirectionAvG.position, t)

def f_phiAv(t):
    return Utils.InterpolateValue( LogEncoder.codeurDirectionAv.timestamp,
                                   LogEncoder.codeurDirectionAv.position, t)

def f_x(t):
    return Utils.InterpolateValue( LogReperage.datas.timestamp,
                                   LogReperage.datas.x, t)
def f_y(t):
    return Utils.InterpolateValue( LogReperage.datas.timestamp,
                                   LogReperage.datas.y, t)
def f_theta(t):
    return Utils.InterpolateValue( LogReperage.datas.timestamp,
                                   LogReperage.datas.theta, t)


E = Track.dataAgv.xTourelleAv
VoieAr = Track.dataAgv.voie
VoieAv = 908


def PlotRouesAv():
    x = LogReperage.datas.x
    y = LogReperage.datas.y
    theta = LogReperage.datas.theta
    xD = x + numpy.multiply( VoieAv/2.0, numpy.sin(theta)) + numpy.multiply(E, numpy.cos(theta))
    yD = y - numpy.multiply( VoieAv/2.0, numpy.cos(theta)) + numpy.multiply(E, numpy.sin(theta))
    xG = x - numpy.multiply( VoieAv/2.0, numpy.sin(theta)) + numpy.multiply(E, numpy.cos(theta))
    yG = y + numpy.multiply( VoieAv/2.0, numpy.cos(theta)) + numpy.multiply(E, numpy.sin(theta))
    plt.plot(xD, yD, color='darkred')
    plt.plot(xG, yG, color='darkblue')


def PlotCircles(t):
    phiAv = f_phiAv(t)
    phiAvD = f_phiAvD(t)
    phiAvG = f_phiAvG(t)
    x = f_x(t)
    y = f_y(t)
    theta = f_theta(t)

    print phiAvD
    print phiAvG

    M=numpy.array([ [0,-VoieAr/2],[0,VoieAr/2],
                    [0,0],[E,0],
                    [-100,-VoieAr/2],[100,-VoieAr/2],
                    [-100, VoieAr/2],[100, VoieAr/2],
                    [E,-VoieAv/2],[E,VoieAv/2],
                    [E-100*cos(phiAvD),-VoieAv/2-100*sin(phiAvD)], [E+100*cos(phiAvD),-VoieAv/2+100*sin(phiAvD)],
                    [E-100*cos(phiAvG), VoieAv/2-100*sin(phiAvG)], [E+100*cos(phiAvG), VoieAv/2+100*sin(phiAvG)]
                  ] )

    rot = numpy.array([[cos(theta),-sin(theta)],[sin(theta),cos(theta)]])    
    
    Rar = E / tan(phiAv)
    xCIR = x - Rar * sin(theta)
    yCIR = y + Rar * cos(theta)
    
    plt.figure('XY')
    plt.axis('equal')
    LogReperage.PlotXY()
    LogReperage.PlotWheelTraj(Track.dataAgv)
    ax = plt.gca()
    circle1 = plt.Circle((xCIR, yCIR), Rar, color='blue', fill=False, linestyle='dashed')
    ax.add_artist(circle1)
    
    RarD = Rar - VoieAr/2.0
    RarG = Rar + VoieAr/2.0
    circle2 = plt.Circle((xCIR, yCIR), RarD, color='red', fill=False, linestyle='dashed')
    circle3 = plt.Circle((xCIR, yCIR), RarG, color='green', fill=False, linestyle='dashed')
    ax.add_artist(circle2)
    ax.add_artist(circle3)

    M2 = numpy.dot(rot, M.T).T
    for i in range(0,7):
        x1 = x+M2[2*i,0]
        y1 = y+M2[2*i,1]
        x2 = x+M2[2*i+1,0]
        y2 = y+M2[2*i+1,1]
        plt.plot([x1,x2],[y1,y2], color='black', linewidth=4)    
    
    RavD = sqrt( E**2 + (Rar+VoieAv/2)**2)
    RavG = sqrt( E**2 + (Rar-VoieAv/2)**2)
    print "RavD", RavD
    print "RarD", RarD
    circle4 = plt.Circle((xCIR, yCIR), RavD, color='darkred', fill=False, linestyle='dashed')
    circle5 = plt.Circle((xCIR, yCIR), RavG, color='darkblue', fill=False, linestyle='dashed')
    ax.add_artist(circle4)
    ax.add_artist(circle5)










