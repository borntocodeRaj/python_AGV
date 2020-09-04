#!/usr/bin/python
import matplotlib
import matplotlib.pyplot
import matplotlib.mlab
import numpy
import math
import Utils
import ConfigAgv

tractionAv=[]
dictDatas=dict();

def Import(filename):
    try:
        datas=matplotlib.mlab.csv2rec(filename,delimiter='\t')
        print "LogMouvement:", filename, "OK n=", len(datas)
        dictDatas[filename[0:-4]]=datas
    except Exception as e: 
        print filename, " : ", e
        datas = list()
    return datas

def Import2(names):
	datas=[]
	for name in names:
		datas = Import(name)
		if len(datas) != 0 :
			return datas
	return None


def getDataName(datas):
    res = '?'
    for name,d in zip(dictDatas.keys(), dictDatas.values()):
        if d is datas:
            res = name[0:-4]
            break
    return res            
        

def PlotPosition(datas, newFig = True):
    """
        Draws a beautifull diagram for a "Position Mouvement".
 
        :param datas: The data to be drawn
        :param newFin: True for a new figure 
        :type a: recarray
        :type b: bool
 
        :Example:
 
        >>> LogMouvement.plotPosition(LogMouvement.directionAv, True)
    """
    name = getDataName(datas)

    if newFig:
        matplotlib.pyplot.figure("LogMouvement - Position" + name)
    else:
        matplotlib.pyplot.figure("LogMouvement - Position")

    ax1 = matplotlib.pyplot.subplot(4,1,1)
    for field in ["consigneposition", "positionactuelle" ]: 
        ax1.plot(datas.timestamp,datas[field], '-+', label=name+'.'+field)
        ax1.legend()
        ax1.grid(True)

    ax2 = matplotlib.pyplot.subplot(4,1,2, sharex=ax1)
    ax2.plot(datas.timestamp,datas.erreur, '-+', label=name+'.'+'erreur')
    ax2.plot(datas.timestamp,datas.consigneposition-datas.positionactuelle, '-+', label=name+'.'+'diff')
    ax2.legend()
    ax2.grid(True)

    ax3 = matplotlib.pyplot.subplot(4,1,3, sharex=ax1)
    for field in ["vitesseappliquee", "vitesseactuelle" ]: 
        ax3.plot(datas.timestamp,datas[field], '-+', label=name+'.'+field)
        ax3.legend()
        ax3.grid(True)

    ax4 = matplotlib.pyplot.subplot(4,1,4, sharex=ax1)
    ax4.set_title('Courant')
    for field in ["courant" ]: 
        ax4.plot(datas.timestamp,datas[field], '-+', label=name+'.'+field)
        ax4.legend()
        ax4.grid(True)


def PlotVitesse(datas, newFig = True):
    """
        Draws a beautifull diagram for a "Vitesse Mouvement".
 
        :param datas: The data to be drawn
        :param newFin: True for a new figure 
        :type a: recarray
        :type b: bool
 
        :Example:
 
        >>> LogMouvement.plotVitesse(LogMouvement.tractionAv, True)
    """
    name = getDataName(datas)
    if newFig:
        matplotlib.pyplot.figure("LogMouvement - vitesse"+name)
    else:
        matplotlib.pyplot.figure("LogMouvement - vitesse")

    ax1 = matplotlib.pyplot.subplot(3,1,1)
    ax1.plot(datas.timestamp, datas.consignevitesse, label="consigne")
    ax1.plot(datas.timestamp, datas.vitesseappliquee, label="vitesseAppliquee")
    ax1.plot(datas.timestamp, datas.vitesseactuelle, label="vitesseActuelle")
    ax1.legend()
    ax1.grid(True)

    ax2 = matplotlib.pyplot.subplot(3,1,2, sharex=ax1)
    for field in ["cdevitesse", "cdeposition", "mvtmarche" ]: 
        ax2.plot(datas.timestamp,datas[field], '-+', label=name+'.'+field)
        ax2.legend()
        ax2.grid(True)

    ax3 = matplotlib.pyplot.subplot(3,1,3, sharex=ax1)
    for field in ["courant" ]: 
        ax3.plot(datas.timestamp,datas[field], '-+', label=name+'.'+field)
        ax3.legend()
        ax3.grid(True)

def PlotT(datas, newFig = True):
    """
        Draws a beautifull diagram for a "Vitesse Mouvement".
        It will automatically choose between "Position/VItesse" display. 

        :param datas: The data to be drawn
        :param newFin: True for a new figure 
        :type a: recarray
        :type b: bool
 
        :Example:
 
        >>> LogMouvement.plotVitesse(LogMouvement.tractionAv, True)
    """
    if len(datas)>0 and datas[0].cdeposition==1:
        PlotPosition(datas, newFig)
    else:
        PlotVitesse(datas, newFig)

def PlotCourant():
    matplotlib.pyplot.figure()
    # premier axe : position des codeurs de direction
    ax1 = matplotlib.pyplot.subplot(3,1,1)
    ax1.set_title('Codeurs Direction')
    #deuxieme axe : vitesses
    ax2 = matplotlib.pyplot.subplot(3,1,2, sharex=ax1)
    ax2.set_title('VItesses')
    # troisieme axe : courants
    ax3 = matplotlib.pyplot.subplot(3,1,3, sharex=ax1)
    ax3.set_title('Courants')

    for name in dictDatas:
        print "Coing to plot:", name
        datas = dictDatas[name]
        if numpy.max(datas.courant) != 0.0:
            #name = dictDatas[datas]

            if datas[0].cdeposition==1:
                for field in ["consigneposition", "positionactuelle" ]: 
                    ax1.plot(datas.timestamp,datas[field], '-', label=name+'.'+field)

            if datas[0].cdevitesse==1:
                for field in ["vitesseappliquee", "vitesseactuelle" ]: 
                    ax2.plot(datas.timestamp,datas[field], '-', label=name+'.'+field)

            if datas[0].cdevitesse==1:
                mark = '-o'
            else:
                mark = '-x'
            ax3.plot(datas.timestamp,datas.courant, mark, label=name)
    ax1.legend()
    ax1.grid(True)            
    ax2.legend()
    ax2.grid(True)
    ax3.legend()
    ax3.grid(True)

def PlotAll(newFig = False):
    for key in dictDatas.keys():
        datas = dictDatas[key]
        PlotT(datas, newFig)

matplotlib.pyplot.ion()

print("Importation...")
# - directions -
directionAv=Import("DirectionAv.txt")
directionAr=Import("DirectionAr.txt")
directionAvD=Import2(["DirectionAvDroite.txt", "DirectionAvantDroite.txt"])
directionAvG=Import2(["DirectionAvGauche.txt", "DirectionAvantDroite.txt"])
directionArD=Import2(["DirectionArDroite.txt", "DirectionArriereDroite.txt"])
directionArG=Import2(["DirectionArGauche.txt", "DirectionArriereGauche.txt"])

# - tractions -
tractionAv=Import("TractionAv.txt")
tractionAr=Import("TractionAr.txt")
tractionAvD=Import2(["TractionAvDroite.txt", "TractionAvantDroite.txt"])
tractionAvG=Import2(["TractionAvGauche.txt", "TractionAvantGauche.txt"])
tractionArD=Import2(["TractionArDroite.txt", "TractionArriereDroite.txt"])
tractionArG=Import2(["TractionArGauche.txt", "TractionArriereGauche.txt"])

# - Outil -
levage=Import("MvtLevage.txt")
rectract=Import("MvtRetract.txt")
fourcheDroiteExt = Import ("MvtFourcheDroiteExterieur.txt")
fourcheDroiteInt = Import ("MvtFourcheDroiteInterieur.txt")
fourcheGaucheExt = Import ("MvtFourcheGaucheExterieur.txt")
fourcheGaucheInt = Import ("MvtFourcheGaucheInterieur.txt")

tilt = Import("MvtTilt.txt")
TDL = Import ("MvtTDL.txt") 

print("Ready to go...")
