#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from __future__ import print_function

import os
import sys
import argparse
import math
import csv
import matplotlib.mlab

import matplotlib.pyplot as plt
import numpy as np

dir_ = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(dir_, ".."))
sys.path.insert(0, os.path.join(dir_, "..", "py_baTools"))

def readline(s):
    if sys.version_info < (3, 0):
        return raw_input(s)
    else:
        return input(s)

def ImportFromCvs(filename):
    datas = matplotlib.mlab.csv2rec(filename, delimiter='\t')
    return datas


def checkDir(path):
    res = os.path.isdir(path)
    if not res:       
        print("The path \"%s\" is not a directory" % path)
    return res

def checkFile(path):
    res = os.path.isfile(path)
    if not res:       
        print("The path \"%s\" is not a file" % path)
    return res

class VectPlan:
    def __init__(self, x=0, y=0, theta=0, date=0):
        self.x = x
        self.y = y
        self.theta = theta
        self.date = date
    
class SlamMergeInfo:
    def __init__(self,
                 outNp,
                 deltaSlam,
                 deltaOdoNp,
                 res_np,
                 newSlamNpValid,
                 reperageOk,
                 odometryWeight,
                 slamWeight):
        self.outNp = outNp
        self.deltaSlam = deltaSlam
        self.deltaOdoNp = deltaOdoNp
        self.res_np = res_np
        self.newSlamNpValid = newSlamNpValid
        self.reperageOk = reperageOk
        self.odometryWeight = odometryWeight
        self.slamWeight = slamWeight
        
class SlamLogInfo:
    def __init__(self,
                 npPosition,
                 npSpeed,
                 npCorrection,
                 outNp,
                 newSlamNpValid,
                 outNpQuality,
                 outSlamState,
                 npSlamOnlyDate):
        self.npPosition = npPosition
        self.npSpeed = npSpeed
        self.npCorrection = npCorrection
        self.outNp = outNp
        
        self.newSlamNpValid = newSlamNpValid
        self.outNpQuality = outNpQuality
        self.outSlamState = outSlamState
        self.npSlamOnlyDate = npSlamOnlyDate
      
        
        
def String2VectPlan(x="0", y="0", theta="0", date="0"):
    return VectPlan(float(x), float(y), float(theta), int(date))


def ImportSlamMerge(filePath):
    return ImportFromCvs(filePath)

def ImportSlamLog(filePath):
    return ImportFromCvs(filePath)

def getResultMerge(slamMergeResultDico):
    cyclesList = slamMergeResultDico.keys()
    cyclesList.sort()
    outNpxList = []
    outNpyList = []
    outNpthetaList = []
    res_npxList = []
    res_npyList = []
    res_npthetaList = []
    
    for c in cyclesList:
        outNpxList.append(slamMergeResultDico[c].outNp.x)
        outNpyList.append(slamMergeResultDico[c].outNp.y)
        outNpthetaList.append(slamMergeResultDico[c].outNp.theta)
        res_npxList.append(slamMergeResultDico[c].res_np.x)
        res_npyList.append(slamMergeResultDico[c].res_np.y)
        res_npthetaList.append(slamMergeResultDico[c].res_np.theta)
    
    return [cyclesList,
            outNpxList,
            outNpyList,
            outNpthetaList,
            res_npxList,
            res_npyList,
            res_npthetaList]

def plotSlamMergeResult(slamMergeResult):
    plt.ion()
   
    plt.figure('slamMergeResultX')
    plt.plot(slamMergeResult.timestamp, slamMergeResult.npx, label="slamNp:x")
    plt.plot(slamMergeResult.timestamp, slamMergeResult.rnpx, label="MergeNp:x")
    plt.legend()
    plt.grid(True)
    
    plt.figure('slamMergeResultY')
    plt.plot(slamMergeResult.timestamp, slamMergeResult.npy, label="slamNp:y")
    plt.plot(slamMergeResult.timestamp, slamMergeResult.rnpy, label="MergeNp:y")
    plt.legend()
    plt.grid(True)
    
    plt.figure('slamMergeResultTheta')
    plt.plot(slamMergeResult.timestamp, slamMergeResult.nptheta, label="slamNp:theta")
    plt.plot(slamMergeResult.timestamp, slamMergeResult.rnptheta, label="MergeNp:theta")
    plt.legend()
    plt.grid(True)
    
    
def cleanTheta(datas):
    res = []
    for data in datas:
        tetha = data * 180. / math.pi
        if tetha > 300.:
            res.append(tetha - 360.)
        elif tetha < -300.:
            res.append(tetha + 360.)
        else:
            res.append(tetha)
    return res
    
def plotSlamLogResult(slamLogResult):
    plt.ion()
   
    
    plt.figure('slamLogResultX')
    ax1 = plt.subplot(3, 1, 1)
    ax1.plot(slamLogResult.timestamp, slamLogResult.nppx, label="slamInputNp:x")
    ax1.plot(slamLogResult.timestamp, slamLogResult.outnpx, label="slamOutputNp:x")
    plt.legend()
    ax1.grid(True)
    ax2 = plt.subplot(3, 1, 2, sharex=ax1)
    ax2.plot(slamLogResult.timestamp, slamLogResult.npcx, label="slamCorectionNp:x")
    datas = (slamLogResult.outnpx - slamLogResult.nppx)
    ax2.plot(slamLogResult.timestamp, datas, label="slamDiffInOut:x")
    plt.legend()
    ax2.grid(True)
    ax3 = plt.subplot(3, 1, 3, sharex=ax1)
    ax3.plot(slamLogResult.timestamp, slamLogResult.npsx, label="slamSpeedNp:x")
    plt.legend()
    ax3.grid(True)
    
    
    plt.figure('slamLogResultY')
    ax1 = plt.subplot(3, 1, 1)
    ax1.plot(slamLogResult.timestamp, slamLogResult.nppy, label="slamInputNp:y")
    ax1.plot(slamLogResult.timestamp, slamLogResult.outnpy, label="slamOutputNp:y")
    plt.legend()
    ax1.grid(True)
    ax2 = plt.subplot(3, 1, 2, sharex=ax1)
    ax2.plot(slamLogResult.timestamp, slamLogResult.npcy, label="slamCorectionNp:y")
    datas = (slamLogResult.outnpy - slamLogResult.nppy)
    ax2.plot(slamLogResult.timestamp, datas, label="slamDiffInOut:y")
    plt.legend()
    ax2.grid(True)
    ax3 = plt.subplot(3, 1, 3, sharex=ax1)
    ax3.plot(slamLogResult.timestamp, slamLogResult.npsy, label="slamSpeedNp:y")
    plt.legend()
    ax3.grid(True)
    
    plt.figure('slamLogResultTheta')
    ax1 = plt.subplot(3, 1, 1)
    ax1.plot(slamLogResult.timestamp, slamLogResult.npptheta * 180. / math.pi, label="slamInputNp:theta")
    ax1.plot(slamLogResult.timestamp, slamLogResult.outnptheta * 180. / math.pi, label="slamOutputNp:theta")
    plt.legend()
    ax1.grid(True)
    ax2 = plt.subplot(3, 1, 2, sharex=ax1)
    ax2.plot(slamLogResult.timestamp, slamLogResult.npctheta * 180. / math.pi, label="slamCorectionNp:theta")
    datas = (slamLogResult.outnptheta - slamLogResult.npptheta)
    ax2.plot(slamLogResult.timestamp, cleanTheta(datas), label="slamDiffInOut:theta")
    plt.legend()
    ax2.grid(True)
    ax3 = plt.subplot(3, 1, 3, sharex=ax1)
    ax3.plot(slamLogResult.timestamp, slamLogResult.npstheta, label="slamSpeedNp:theta")
    plt.legend()
    ax3.grid(True)
    

    PlotXY(slamLogResult)


#[PORTUAIRE]Optimisation du theta pour le MULTIREPERAGE et le SLAM
# all positives and in degree
def optimisationtheta(slamMergeResult):
	for data in slamMergeResult:
		if (data.mnptheta > 0 and data.nptheta < 0):
			data.nptheta = -data.nptheta

		if data.mnptheta < 0:
			if data.nptheta < 0:
				data.nptheta = -data.nptheta
			data.mnptheta = -data.mnptheta				

		if data.mnptheta < 2*math.pi and data.mnptheta < 2*math.pi:
			data.mnptheta = data.mnptheta*180/math.pi
			data.nptheta = data.nptheta*180/math.pi

#[PORTUAIRE]All plots
def plotSlamPortuaire(slamLogResult, slamMergeResult):
    #plotErrorSlamOdo(slamLogResult, slamMergeResult) #To improve the results
    plotErrorSlamOdoC3(slamLogResult, slamMergeResult)


#[PORTUAIRE]Error Slam/Odo : variation de la position du systeme SLAM par rapport a la progression odometrique
#Etude sur l'ensemble de la plage de donnees
def plotErrorSlamOdo(slamLogResult, slamMergeResult):
    plt.ion()

    # Declaration des donnees
    errorsox = []
    errorsoy = []
    errorsotheta = []
    abserrorsox = []
    abserrorsoy = []
    abserrorsotheta = []
    critere1 = []
    critere2 = []
    critere3 = []
    mnpx = []
    npptv = []
    npi = []
    yav = []
    yar = []
    dstationx = []
    dstationy = []

    # Initialisation des donnees
    nbElementC1 = 0
    i=0
    for data in slamLogResult:
	if i != 0:
	    	if data.npq != 0 and data.npptv >= 50 and slamMergeResult.npx[i] > 159000 and abs(slamMergeResult.npx[i-1] + slamMergeResult.dodonpx[i] - slamMergeResult.npx[i]) > 0.05 and abs(slamMergeResult.npy[i-1] + slamMergeResult.dodonpy[i] - slamMergeResult.npy[i]) > 0.01 and abs(slamMergeResult.nptheta[i-1] + slamMergeResult.dodonptheta[i] - slamMergeResult.nptheta[i]) > 0.001:
	    		errorsox.append(slamMergeResult.npx[i-1] + slamMergeResult.dodonpx[i] - slamMergeResult.npx[i])
			errorsoy.append(slamMergeResult.npy[i-1] + slamMergeResult.dodonpy[i] - slamMergeResult.npy[i])
			errorsotheta.append(slamMergeResult.nptheta[i-1] + slamMergeResult.dodonptheta[i] - slamMergeResult.nptheta[i])

			abserrorsox.append(abs(slamMergeResult.npx[i-1] + slamMergeResult.dodonpx[i] - slamMergeResult.npx[i]))
			abserrorsoy.append(abs(slamMergeResult.npy[i-1] + slamMergeResult.dodonpy[i] - slamMergeResult.npy[i]))
			abserrorsotheta.append(abs(slamMergeResult.nptheta[i-1] + slamMergeResult.dodonptheta[i] - slamMergeResult.nptheta[i]))
			
			npptv.append(data.npptv)
		
			yav.append(slamMergeResult.npy[i] + 7112 * math.sin(slamMergeResult.nptheta[i] * math.pi / 180))
			yar.append(slamMergeResult.npy[i] - 7112 * math.sin(slamMergeResult.nptheta[i] * math.pi / 180))
	
			critere1.append(data.npq)
			critere2.append(data.npq*data.npptv/1141)
			mnpx.append(slamMergeResult.mnpx[i])
			npi.append(data.npi)
			nbElementC1 += 1
	i+=1

    # Construction du nouveau critere 3 : MIX du c1 et c2
    nbElementC3 = 0
    j = 0
    while j < nbElementC1:
	if critere1[j] < 0.7:
		critere3.append(0)
	else:
		critere3.append(critere2[j])
		nbElementC3 += 1
	j+=1

    # Visualisation d'une docking station
    fp = open("/home/localuser/workspace/agv/target/AIV/map_real_hericourt.map", 'r')
    if fp != True:
	for line in fp:
		dstationx.append(int(line.split()[0]) + 7135)
		dstationy.append(line.split()[1])
    else:
	print ("Map not open")

    # Critere de comparaison 2 : Ratio/Possible
    plt.figure('ErrorSlamOdo = fct(Critere 2)')
    ax1 = plt.subplot(3,2,1)
    ax1.plot(critere2, errorsox, '*', label="ErrorSlamOdoX")
    ax1.axhline(np.mean(errorsox), label = "MoyenneESOX", color = 'r')
    ax1.axhline(np.median(errorsox), label = "MedianESOX", color = 'g')
    ax1.axhline(np.std(errorsox), label = "Ecart-TypeESOX", color = "black")
    ax1.axhline(np.max(errorsox), label = "MaxESOX", color = 'grey')
    ax1.axhline(np.min(errorsox), label = "MinESOX", color = 'yellow')
    plt.legend()
    ax1.grid(True)
    ax2 = plt.subplot(3,2,3, sharex = ax1)
    ax2.plot(critere2, errorsoy, '*', label="ErrorSlamOdoY")
    ax2.axhline(np.mean(errorsoy), label = "MoyenneESOY", color = 'r')
    ax2.axhline(np.median(errorsoy), label = "MedianESOY", color = 'g')
    ax2.axhline(np.std(errorsoy), label = "Ecart-TypeESOY", color = "black")
    ax2.axhline(np.max(errorsox), label = "MaxESOY", color = 'grey')
    ax2.axhline(np.min(errorsox), label = "MinESOY", color = 'yellow')
    plt.legend()
    ax2.grid(True)
    ax3 = plt.subplot(3,2,5, sharex = ax1)
    ax3.plot(critere2, errorsotheta, '*', label="ErrorSlamOdoTheta")
    ax3.axhline(np.mean(errorsotheta), label = "MoyenneESOTheta", color = 'r')
    ax3.axhline(np.median(errorsotheta), label = "MedianESOTheta", color = 'g')
    ax3.axhline(np.std(errorsotheta), label = "Ecart-TypeESOTheta", color = "black")
    ax3.axhline(np.max(errorsotheta), label = "MaxESOTheta", color = 'grey')
    ax3.axhline(np.min(errorsotheta), label = "MinESOTheta", color = 'yellow')
    plt.legend()
    ax3.grid(True)
    ax4 = plt.subplot(3,2,2, sharex = ax1)
    ax4.plot(critere2, abserrorsox, '*', label="AbsErrorSlamOdoX")
    plt.legend()
    ax4.grid(True)
    ax5 = plt.subplot(3,2,4, sharex = ax1)
    ax5.plot(critere2, abserrorsoy, '*', label="AbsErrorSlamOdoY")
    plt.legend()
    ax5.grid(True)
    ax6 = plt.subplot(3,2,6, sharex = ax1)
    ax6.plot(critere2, abserrorsotheta, '*', label="AbsErrorSlamOdoTheta")
    plt.legend()
    ax6.grid(True)

    # Critere de comparaison 3 : MIX C1/C2
    plt.figure('ErrorSlamOdo = fct(Critere 3)')
    ax1 = plt.subplot(3,2,1)
    ax1.plot(critere3, errorsox, '*', label="ErrorSlamOdoX")
    ax1.axhline(np.mean(errorsox), label = "MoyenneESOX", color = 'r')
    ax1.axhline(np.median(errorsox), label = "MedianESOX", color = 'g')
    ax1.axhline(np.std(errorsox), label = "Ecart-TypeESOX", color = "black")
    ax1.axhline(np.max(errorsox), label = "MaxESOX", color = 'grey')
    ax1.axhline(np.min(errorsox), label = "MinESOX", color = 'yellow')
    plt.legend()
    ax1.grid(True)
    ax2 = plt.subplot(3,2,3, sharex = ax1)
    ax2.plot(critere3, errorsoy, '*', label="ErrorSlamOdoY")
    ax2.axhline(np.mean(errorsoy), label = "MoyenneESOY", color = 'r')
    ax2.axhline(np.median(errorsoy), label = "MedianESOY", color = 'g')
    ax2.axhline(np.std(errorsoy), label = "Ecart-TypeESOY", color = "black")
    ax2.axhline(np.max(errorsox), label = "MaxESOY", color = 'grey')
    ax2.axhline(np.min(errorsox), label = "MinESOY", color = 'yellow')
    plt.legend()
    ax2.grid(True)
    ax3 = plt.subplot(3,2,5, sharex = ax1)
    ax3.plot(critere3, errorsotheta, '*', label="ErrorSlamOdoTheta")
    ax3.axhline(np.mean(errorsotheta), label = "MoyenneESOTheta", color = 'r')
    ax3.axhline(np.median(errorsotheta), label = "MedianESOTheta", color = 'g')
    ax3.axhline(np.std(errorsotheta), label = "Ecart-TypeESOTheta", color = "black")
    ax3.axhline(np.max(errorsotheta), label = "MaxESOTheta", color = 'grey')
    ax3.axhline(np.min(errorsotheta), label = "MinESOTheta", color = 'yellow')
    plt.legend()
    ax3.grid(True)
    ax4 = plt.subplot(3,2,2, sharex = ax1)
    ax4.plot(critere3, abserrorsox, '*', label="AbsErrorSlamOdoX")
    plt.legend()
    ax4.grid(True)
    ax5 = plt.subplot(3,2,4, sharex = ax1)
    ax5.plot(critere3, abserrorsoy, '*', label="AbsErrorSlamOdoY")
    plt.legend()
    ax5.grid(True)
    ax6 = plt.subplot(3,2,6, sharex = ax1)
    ax6.plot(critere3, abserrorsotheta, '*', label="AbsErrorSlamOdoTheta")
    plt.legend()
    ax6.grid(True)

    # Distance parcourue
    plt.figure('ErrorSlamOdo = fct(X)')
    ax1 = plt.subplot(5,1,1)
    ax1.plot(mnpx, abserrorsox, '*', label="AbsErrorSlamOdoX")
    plt.legend()
    ax1.grid(True)
    ax2 = plt.subplot(5,1,2, sharex = ax1)
    ax2.plot(mnpx, abserrorsoy, '*', label="AbsErrorSlamOdoY")
    plt.legend()
    ax2.grid(True)
    ax3 = plt.subplot(5,1,3, sharex = ax1)
    ax3.plot(mnpx, abserrorsotheta, '*', label="AbsErrorSlamOdoTheta")
    plt.legend()
    ax3.grid(True)
    ax4 = plt.subplot(5,1,4, sharex = ax1)
    ax4.plot(mnpx, critere1, '*', label="Critere1")
    ax4.plot(mnpx, critere2, '+', label="Critere2")
    ax4.plot(mnpx, critere3, '*', label="Critere3")
    plt.legend()
    ax4.grid(True)
    ax5 = plt.subplot(5,1,5, sharex = ax1)
    ax5.plot(mnpx, npptv, label = "NbPtV")
    ax5.plot(mnpx, npi, label = "I")
    plt.legend()
    ax5.grid(True)

    # Position AV/AR AIV
    plt.figure('Yav & Yar = fct(X)')
    ax1 = plt.subplot(1,1,1)
    ax1.plot(mnpx, yav, '*', label = "Yav", color = 'red')
    ax1.plot(mnpx, yar, '+', label = "Yar", color = 'blue')
    ax1.plot(dstationx, dstationy, '.', label = "Real Docking Station", color = 'green')
    plt.legend()
    ax1.grid(True)

#[PORTUAIRE]Error Slam/Odo : variation de la position du systeme SLAM par rapport a la progression odometrique
#Etude du critere 3 : MIX C1 et C2 (condition sur C1 : 120 pts, 0.7%(C1) et 162500, valeur = C2)
def plotErrorSlamOdoC3(slamLogResult, slamMergeResult):
    plt.ion()

    # Declaration des donnees
    errorsox = []
    errorsoy = []
    errorsotheta = []
    abserrorsox = []
    abserrorsoy = []
    abserrorsotheta = []
    critere3 = []
    timestamp = []
    mnpx = []
    npptv = []
    npi = []

    # Initialisation des donnees
    nbElementC3 = 0
    i=0
    for data in slamLogResult:
	if i != 0:
	    	if data.npq != 0 and data.npptv >= 120 and slamMergeResult.npx[i] > 163000 and abs(slamMergeResult.npx[i-1] + slamMergeResult.dodonpx[i] - slamMergeResult.npx[i]) > 0.05 and abs(slamMergeResult.npy[i-1] + slamMergeResult.dodonpy[i] - slamMergeResult.npy[i]) > 0.01 and abs(slamMergeResult.nptheta[i-1] + slamMergeResult.dodonptheta[i] - slamMergeResult.nptheta[i]) > 0.001 and data.npq > 0.7:
	    		errorsox.append(slamMergeResult.npx[i-1] + slamMergeResult.dodonpx[i] - slamMergeResult.npx[i])
			errorsoy.append(slamMergeResult.npy[i-1] + slamMergeResult.dodonpy[i] - slamMergeResult.npy[i])
			errorsotheta.append(slamMergeResult.nptheta[i-1] + slamMergeResult.dodonptheta[i] - slamMergeResult.nptheta[i])

			abserrorsox.append(abs(slamMergeResult.npx[i-1] + slamMergeResult.dodonpx[i] - slamMergeResult.npx[i]))
			abserrorsoy.append(abs(slamMergeResult.npy[i-1] + slamMergeResult.dodonpy[i] - slamMergeResult.npy[i]))
			abserrorsotheta.append(abs(slamMergeResult.nptheta[i-1] + slamMergeResult.dodonptheta[i] - slamMergeResult.nptheta[i]))
			
			npptv.append(data.npptv)
			timestamp.append(slamMergeResult.timestamp[i])
			mnpx.append(slamMergeResult.mnpx[i])
			npi.append(data.npi)

			critere3.append(data.npq*data.npptv/1141)

			nbElementC3 += 1

	i+=1

    # Critere de comparaison 3 : MIX C1/C2
    plt.figure('ErrorSlamOdoC3 = fct(Critere 3)')
    ax1 = plt.subplot(3,2,1)
    ax1.plot(critere3, errorsox, '*', label="ErrorSlamOdoX")
    ax1.axhline(np.mean(errorsox), label = "MoyenneESOX", color = 'r')
    ax1.axhline(np.median(errorsox), label = "MedianESOX", color = 'g')
    ax1.axhline(np.std(errorsox), label = "Ecart-TypeESOX", color = "black")
    ax1.axhline(np.max(errorsox), label = "MaxESOX", color = 'grey')
    ax1.axhline(np.min(errorsox), label = "MinESOX", color = 'yellow')
    plt.legend()
    ax1.grid(True)
    ax2 = plt.subplot(3,2,3, sharex = ax1)
    ax2.plot(critere3, errorsoy, '*', label="ErrorSlamOdoY")
    ax2.axhline(np.mean(errorsoy), label = "MoyenneESOY", color = 'r')
    ax2.axhline(np.median(errorsoy), label = "MedianESOY", color = 'g')
    ax2.axhline(np.std(errorsoy), label = "Ecart-TypeESOY", color = "black")
    ax2.axhline(np.max(errorsox), label = "MaxESOY", color = 'grey')
    ax2.axhline(np.min(errorsox), label = "MinESOY", color = 'yellow')
    plt.legend()
    ax2.grid(True)
    ax3 = plt.subplot(3,2,5, sharex = ax1)
    ax3.plot(critere3, errorsotheta, '*', label="ErrorSlamOdoTheta")
    ax3.axhline(np.mean(errorsotheta), label = "MoyenneESOTheta", color = 'r')
    ax3.axhline(np.median(errorsotheta), label = "MedianESOTheta", color = 'g')
    ax3.axhline(np.std(errorsotheta), label = "Ecart-TypeESOTheta", color = "black")
    ax3.axhline(np.max(errorsotheta), label = "MaxESOTheta", color = 'grey')
    ax3.axhline(np.min(errorsotheta), label = "MinESOTheta", color = 'yellow')
    plt.legend()
    ax3.grid(True)
    ax4 = plt.subplot(3,2,2, sharex = ax1)
    ax4.plot(critere3, abserrorsox, '*', label="AbsErrorSlamOdoX")
    plt.legend()
    ax4.grid(True)
    ax5 = plt.subplot(3,2,4, sharex = ax1)
    ax5.plot(critere3, abserrorsoy, '*', label="AbsErrorSlamOdoY")
    plt.legend()
    ax5.grid(True)
    ax6 = plt.subplot(3,2,6, sharex = ax1)
    ax6.plot(critere3, abserrorsotheta, '*', label="AbsErrorSlamOdoTheta")
    plt.legend()
    ax6.grid(True)

    # Distance parcourue
    plt.figure('ErrorSlamOdoC3 = fct(X)')
    ax1 = plt.subplot(5,1,1)
    ax1.plot(mnpx, abserrorsox, '*', label="AbsErrorSlamOdoX")
    plt.legend()
    ax1.grid(True)
    ax2 = plt.subplot(5,1,2, sharex = ax1)
    ax2.plot(mnpx, abserrorsoy, '*', label="AbsErrorSlamOdoY")
    plt.legend()
    ax2.grid(True)
    ax3 = plt.subplot(5,1,3, sharex = ax1)
    ax3.plot(mnpx, abserrorsotheta, '*', label="AbsErrorSlamOdoTheta")
    plt.legend()
    ax3.grid(True)
    ax4 = plt.subplot(5,1,4, sharex = ax1)
    ax4.plot(mnpx, critere3, '*', label="Critere3")
    plt.legend()
    ax4.grid(True)
    ax5 = plt.subplot(5,1,5, sharex = ax1)
    ax5.plot(mnpx, npptv, '*', label = "NbPtV")
    ax5.plot(mnpx, npi, '*', label = "I")
    plt.legend()
    ax5.grid(True)

    # Time
    plt.figure('ErrorSlamOdoC3 = fct(T)')
    ax1 = plt.subplot(5,1,1)
    ax1.plot(timestamp, errorsox, '*', label="ErrorSlamOdoX")
    plt.legend()
    ax1.grid(True)
    ax2 = plt.subplot(5,1,2, sharex = ax1)
    ax2.plot(timestamp, errorsoy, '*', label="ErrorSlamOdoY")
    plt.legend()
    ax2.grid(True)
    ax3 = plt.subplot(5,1,3, sharex = ax1)
    ax3.plot(timestamp, errorsotheta, '*', label="ErrorSlamOdoTheta")
    plt.legend()
    ax3.grid(True)
    ax4 = plt.subplot(5,1,4, sharex = ax1)
    ax4.plot(timestamp, critere3, '*', label="Critere3")
    plt.legend()
    ax4.grid(True)
    ax5 = plt.subplot(5,1,5, sharex = ax1)
    ax5.plot(timestamp, npptv, '*', label = "NbPtV")
    ax5.plot(timestamp, npi, '*', label = "I")
    plt.legend()
    ax5.grid(True)


def getSlamLogResult(dirPath="."):
    slamLogPath = os.path.join(dirPath, "SlamReperage.txt")
    resLog = checkFile(slamLogPath)
    if not resLog:
        sys.exit(1)
    
    return ImportSlamLog(slamLogPath)
    
def PlotXY(slamLogResult=None):
    if (slamLogResult is None):
        plt.ion()
        slamLogResult = getSlamLogResult()
        
    plt.figure('XY')
    plt.plot(slamLogResult.nppx, slamLogResult.nppy, marker='+', label='slamInputNp', color='blue')
    plt.plot(slamLogResult.outnpx, slamLogResult.outnpy, '-*', label='slamOutputNp', color='green')
    plt.axis('equal')
    plt.legend()
    plt.grid(True)
    
def PlotSlam(dirPath="."):
    slamMergeLogPath = os.path.join(dirPath, "SlamReperageMerge.txt")
    resMerge = checkFile(slamMergeLogPath)
    
    if not resMerge:
        sys.exit(1)
    
    slamLogResult = getSlamLogResult(dirPath)
    slamMergeResult = ImportSlamMerge(slamMergeLogPath)
    
    #plotSlamMergeResult(slamMergeResult)
    #plotSlamLogResult(slamLogResult) do not commit
    
    optimisationtheta(slamMergeResult)
    plotSlamPortuaire(slamLogResult, slamMergeResult)


def cmdPlotSlam(dirPath="."):
    PlotSlam(dirPath=dirPath)
    readline("... Enter ...\n")



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument(
        "--debug", help="output debug info", action="store_true")
    parser.add_argument(
        "--dirPath", "-d", help="path to the Slam log dir", default=".")
    args = parser.parse_args()
    if args.verbose:
        VERBOSE = True
        print("verbosity turned on")
    else:
        pass
    
    if not checkDir(args.dirPath):
        sys.exit(1)
        
    cmdPlotSlam(dirPath=args.dirPath)


if __name__ == '__main__':
    main()
