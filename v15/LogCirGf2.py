#!/usr/bin/python
import matplotlib.pyplot  as plt
import matplotlib.mlab
import collections
import numpy as np



def Import(filename):
    datas=[]
    try:
	datas=matplotlib.mlab.csv2rec(filename,delimiter='\t')
	print "LogCirgf2:", filename, "OK n=", len(datas)
    except:
	print filename, "empty file ?"
	datas=None
    return datas


#CIR (coordonnee du centre instantanne de rotation selon l'axe des roues AR : indique le rayon du virage)
#on n'a pas gere ici les divisions par 0 : python met qqs messages en consequence, mais rien de grave : c'est normal que le CIR parte a l'inifni quand on roule droit
#on limite par defaut l'affichage selon l'axe Y pour y voir quelque chose, mais c'est tout
def PlotCIR():
    p = 1800 #empattement
    dAR = 1345  # voie arriere
    dAV = 908  #voie avant


    used_size = min(len(tractionArD),len(tractionArG))



    CIR_from_VAr_consignes = dAR / 2.0 * (tractionArD.consignevitesse[0:used_size] + tractionArG.consignevitesse[0:used_size])/(tractionArD.consignevitesse[0:used_size] - tractionArG.consignevitesse[0:used_size])

    CIR_from_VAr_appliquee = dAR / 2.0 * (tractionArD.vitesseappliquee[0:used_size] + tractionArG.vitesseappliquee[0:used_size])/(tractionArD.vitesseappliquee[0:used_size] - tractionArG.vitesseappliquee[0:used_size])
    
    CIR_from_VAr_measures = dAR / 2.0 * (tractionArD.vitesseactuelle[0:used_size] + tractionArG.vitesseactuelle[0:used_size]) / (tractionArD.vitesseactuelle[0:used_size] - tractionArG.vitesseactuelle[0:used_size])

    plt.figure()
    ax1 = plt.subplot(2,1,1)
    ax1.plot(tractionArD.timestamp[0:used_size], CIR_from_VAr_consignes , '-+',label="CIR from VarD and VarG consigne")
    ax1.plot(tractionArD.timestamp[0:used_size], CIR_from_VAr_appliquee , '-+',label="CIR from VarD and VarG appliquee")
    ax1.plot(tractionArD.timestamp[0:used_size], CIR_from_VAr_measures , '-+',label="CIR from VarD and VarG measure")
    ax1.legend()
    ax1.grid(True)
    ax1.set_title('ccord (mm) du CIR avec les tractions')
    axes = plt.gca()
    axes.set_ylim(-6000,6000)

    CIR_from_PhiAvCons = p*np.cos(directionAv.consigneposition) / np.sin(directionAv.consigneposition)
    CIR_from_PhiAvDCons = p * np.cos(directionAvD.consigneposition) / np.sin(directionAvD.consigneposition) - dAV/2;
    CIR_from_PhiAvGCons = p* np.cos(directionAvG.consigneposition) / np.sin(directionAvG.consigneposition) + dAV/2;

    CIR_from_PhiAvMeas = p*np.cos(directionAv.positionactuelle) / np.sin(directionAv.positionactuelle)
    CIR_from_PhiAvDMeas = p * np.cos(directionAvD.positionactuelle) / np.sin(directionAvD.positionactuelle) - dAV/2;
    CIR_from_PhiAvGMeas = p* np.cos(directionAvG.positionactuelle) / np.sin(directionAvG.positionactuelle) + dAV/2;
    
    ax2 = plt.subplot(2,1,2, sharex = ax1)

#    ax2.plot(directionAv.timestamp, CIR_from_PhiAvCons, '-+',label="CIR from PhiAv consigne")
    ax2.plot(directionAvD.timestamp, CIR_from_PhiAvDCons, '-+',label="CIR from PhiAvD consigne")
    ax2.plot(directionAvG.timestamp, CIR_from_PhiAvGCons, '-+',label="CIR from PhiAvG consigne")

#    ax2.plot(directionAv.timestamp, CIR_from_PhiAvMeas, '-+',label="CIR from PhiAv mesure")
    ax2.plot(directionAvD.timestamp, CIR_from_PhiAvDMeas, '-+',label="CIR from PhiAvD mesure")
    ax2.plot(directionAvG.timestamp, CIR_from_PhiAvGMeas, '-+',label="CIR from PhiAvG mesure")

    ax2.legend()
    ax2.grid(True)
    ax2.set_title('coord (mm) du CIR avec les directions')
    axes = plt.gca()
    axes.set_ylim(-6000,6000)
    
    plt.show()

plt.ion()

try:
    directionAv=Import("DirectionAv.txt")
    print "DirectionAv OK"
    tractionAv=Import("TractionAv.txt")
    print "TractionAv OK"


    tractionArD=Import("TractionArDroite.txt")
    print "tractionArD OK"
    tractionArG=Import("TractionArGauche.txt")
    print "tractionArG OK"
    directionAvD=Import("DirectionAvDroite.txt")
    print "directionAvD OK"
    directionAvG=Import("DirectionAvGauche.txt")
    print "directionAvG OK"

except:
    print 'EndCinematiqueVoiture'


print "Import Done"

