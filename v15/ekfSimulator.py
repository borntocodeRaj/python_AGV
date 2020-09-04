#!/usr/bin/python
import numpy as np
from numpy import matrix, deg2rad
from numpy import sin
from numpy import cos
from numpy.linalg import inv
from sys import exit

import matplotlib

import csv
#from sympy.physics.units import current

class Posture:
    def __init__(self,x,y,theta):
        self.x=x
        self.y=y
        self.theta=theta
class State:
    def __init__(self):
        self.x=1.0
        self.y=1.0
        self.theta=0.
        self.rGain=1.0
        self.lGain=1.0
    def initFromPosture(self,x,y,th):
        self.x=x
        self.y=y
        self.theta=th
        self.rGain=1.0
        self.lGain=1.0
        return self
    def initFromAll(self,x,y,th,gg,gd):
        self.x=x
        self.y=y
        self.theta=th
        self.rGain=gd
        self.lGain=gg
        return self
    def predict(self,deltaD,deltaTheta):
        self.x=self.x+cos(self.theta)*deltaD
        self.y=self.y+sin(self.theta)*deltaD
        self.theta=self.theta+deltaTheta
    def toVector(self):
        return np.array([[self.x], [self.y], [self.theta], [self.rGain], [self.lGain]])
    def fromVector(self, v):
        self.x = v.item((0, 0))
        self.y = v.item((1, 0))
        self.theta = v.item((2, 0))
        self.rGain = v.item((3, 0))
        self.lGain = v.item((4, 0))
class Input:
    def __init__(self):
        self.lCodeur=0.0
        self.rCodeur=0.0
    def initFromValues(self,rCodeur,lCodeur):
        self.lCodeur=lCodeur
        self.rCodeur=rCodeur
class Logger:
    def __init__(self,filename):
        self.filename=filename
        csv.register_dialect('baDial', delimiter='\t', quoting=csv.QUOTE_NONE)
    def setHeaders(self,headers):
        with open(self.filename,'wb') as loggerFile:
            writer=csv.writer(loggerFile,"baDial")
            writer.writerow(headers)
    def addRow(self,row):
        with open(self.filename,'a') as loggerFile:
            writer=csv.writer(loggerFile,"baDial")
            writer.writerow(row)
    def close(self):
        self.file.close()

def pow2(number):
    return np.power(number,2)

voieEnDur=1048
#variables filtre
stateSize=5#taille de l etat
X=State()#etat
P=np.eye(stateSize)#matrice de prediction

#bruit de process
qxy=25
qth=np.deg2rad(1)
qRoue=1e-5
#Matrice de covariance des bruits de process
Q=np.diagflat([qxy,qxy,qth,qRoue,qRoue])
#bruit de mesure
R=np.array([[pow2(qxy),0,0],
            [0,pow2(qxy),0],
            [0,0,pow2(qth)]])
H=np.array([[1,0,0,0,0],
          [0,1,0,0,0],
          [0,0,1,0,0]])
#simulator parameter
currentCycle=0.
currentTimestamp=0.

def replayOdo(codeurArd,codeurArg,voie,cycle,timestamp):
    global currentCycle, currentTimestamp
    currentCycle=cycle
    currentTimestamp=timestamp
    predict(codeurArd, codeurArg,voie,cycle,timestamp)
    return [X.x,X.y,X.theta]

def replayInit(x,y,theta,cycle, timestamp):
    global currentCycle, currentTimestamp
    initialState(x, y, theta)
    currentCycle=cycle
    currentTimestamp=timestamp

def replayUpdate(x,y,theta,cycle,timestamp):
    global currentCycle, currentTimestamp
    currentCycle=cycle
    update(x, y, theta, cycle, timestamp)

def computeJacobian(X,U,deltaD,deltaTheta,voie):
    A_out=matrix([[1,    0,  -sin(X.theta)*deltaD,    cos(X.theta)*U.rCodeur/2.0,   cos(X.theta)*U.lCodeur/2.0],
                 [0,    1,  cos(X.theta)*deltaD,     sin(X.theta)*U.rCodeur/2.0,   cos(X.theta)*U.lCodeur/2.0],
                 [0,    1,  1,                       U.rCodeur/voie,               -U.lCodeur/voie],
                 [0,    0,  0,                          1,                                  0],
                 [0,    0,  0,                          0,                                  1]])
    B_out=matrix([[X.rGain*cos(X.theta)/2.0,          X.lGain*cos(X.theta)/2.0],
                 [X.rGain*sin(X.theta)/2.0,          X.lGain*sin(X.theta)/2.0],
                 [X.rGain/voie,                      -X.lGain/voie],
                 [0,                                    0],
                 [0,                                    0]])
    return [A_out,B_out]

def initialState(x,y,theta):
    global X, P, ekfLogger,varianceLogger,recalageLogger
    X.initFromPosture(x,y,theta)
    P=np.eye(stateSize)
    print "EKF Filter @AJE start"
    ekfLogger=Logger("ekf.txt")
    ekfLogger.setHeaders(["Date Hour","Timestamp","Cycle","xPre","yPre","thPre","deltaD","deltaTh","gd","gg"])
    varianceLogger=Logger("ekfVariances.txt")
    varianceLogger.setHeaders(["Date Hour","TimeStamp","Cycle","p11","p22","p33","p44","p55"])
    recalageLogger=Logger("ekfRecalage.txt")
    recalageLogger.setHeaders(["Date Hour","TimeStamp","Cycle","x","y","th","errMesureX","errMesureY","errMesureTh","gd","gg"])

def predict(codeurD,codeurG,voie,cycle=currentCycle,timestamp=currentTimestamp):
    global X, P, ekfLogger,varianceLogger,recalageLogger
#     print "cD=",codeurD," codeurG=",codeurG
    U=Input()
    U.initFromValues(codeurD,codeurG)
    deltaD=(X.rGain*U.rCodeur+X.lGain*U.lCodeur)/2.0
    deltaTheta=(X.rGain*U.rCodeur-X.lGain*U.lCodeur)/voie
    print "deltaD=",deltaD," deltaTh=",deltaTheta
    #predictionModel
    X.predict(deltaD, deltaTheta)
    [A,B]=computeJacobian(X,U,deltaD,deltaTheta,voie)
    #P = A.dot(P).dot(A.transpose())+B.dot(Q).dot(B.transpose())
    P = A.dot(P).dot(A.transpose())
    ekfLoggerData=["2017-1-1:0,0,0",timestamp,cycle,X.x,X.y,X.theta,deltaD,deltaTheta,X.rGain,X.lGain]
    ekfLogger.addRow(ekfLoggerData)
    varianceLoggerData=["2017-1-1:0,0,0",timestamp,cycle, P.item((0,0)),P.item((1,1)),P.item((2,2)),P.item((3,3)),P.item((4,4))]
    varianceLogger.addRow(varianceLoggerData)
#     print "P=",P
#     print "A=",A

def update(xPsi,yPsi,thetaPsi,cycle=currentCycle,timestamp=currentTimestamp):
    global X, P, ekfLogger,varianceLogger,recalageLogger
    S=H.dot(P).dot(H.transpose())+R
    print "S=", S
    invS=inv(S)
    K=P.dot(H.transpose()).dot(invS)
    psiPosture=[[xPsi], [yPsi], [thetaPsi]]
    errMesure=psiPosture-H.dot(X.toVector())
    X.fromVector(X.toVector()+K.dot(errMesure))
    P = (np.identity(5)-K.dot(H)).dot(P)
    print "P=",P
    recalageLoggerData=["2017-1-1:0,0,0",timestamp,cycle,X.x,X.y,X.theta,errMesure[0],errMesure[1],errMesure[2],X.lGain,X.rGain]
    recalageLogger.addRow(recalageLoggerData)
    varianceLoggerData=["2017-1-1:0,0,0",timestamp,cycle,P.item((0,0)),P.item((1,1)),P.item((2,2)),P.item((3,3)),P.item((4,4))]
    varianceLogger.addRow(varianceLoggerData)

def Import(filename):
    try:
        var=matplotlib.mlab.csv2rec(filename,delimiter='\t')
        print 'Import {0} OK'.format(filename)
        return var
    except:
        print 'WARNING: Could not import {0}'.format(filename)
        return []

