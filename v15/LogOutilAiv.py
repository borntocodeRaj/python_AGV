#!/usr/bin/python
import matplotlib.pyplot as plt
import matplotlib.mlab
from math import *
import numpy
#from scipy import interpolate

dataTractionAv=[]
dataTractionArr=[]
dataOutil=[]
dataCodeur=[]
dataNav=[]
dataFreins=[]

def Import():
	dataTractionAv=matplotlib.mlab.csv2rec('TractionAv.txt',delimiter='\t')
	#dataTractionArr=matplotlib.mlab.csv2rec('TractionArr.txt',delimiter='\t')
	dataOutil=matplotlib.mlab.csv2rec('MvtAivLift.txt',delimiter='\t')
	dataCodeur=matplotlib.mlab.csv2rec('codeurCodeurMvtAivLift.txt',delimiter='\t')
	dataNav=matplotlib.mlab.csv2rec('NavigationLaser.txt',delimiter='\t')
	dataFreins=matplotlib.mlab.csv2rec('FreinageAivCalcul.txt',delimiter='\t')

	return dataTractionAv, dataOutil, dataCodeur, dataNav, dataFreins

##Plot the whole scenario
def PlotT():

	plt.figure()
	ax1 = plt.subplot(3,1,1)

#	ax1.plot(dataOutil.timestamp, dataOutil.cdevitesse, label="Outilcdevitesse")
#	ax1.plot(dataOutil.timestamp, dataOutil.cdeposition,     label="Outilcdeposition")
#	ax1.plot(dataOutil.timestamp, dataOutil.consignevitesse, label="Outilconsignevitesse")
	ax1.plot(dataOutil.timestamp, dataOutil.consigneposition,     label="Outil_ConsignePosition")
	consigne=dataOutil.consigneposition*dataOutil.mvtmarche
	ax1.plot(dataOutil.timestamp, consigne,     label="Outil_MvtMarche")
#	ax1.plot(dataOutil.timestamp, dataOutil.isenposition,     label="Outilisenposition")	
#	ax1.plot(dataOutil.timestamp, dataOutil.marcheactive,     label="Outilmarcheactive")
	ax1.plot(dataCodeur.timestamp, dataCodeur.position,     label="Codeur_position")
	ax1.plot(dataOutil.timestamp, dataOutil.frontliftpos,     label="Outil_FrontLiftPos")
	ax1.plot(dataOutil.timestamp, dataOutil.rearliftpos,     label="Outil_rearLiftPos")

	ax1.legend()
	ax1.grid(True)

	ax2 = plt.subplot(3,1,2, sharex=ax1)

	ax2.plot(dataTractionAv.timestamp, dataTractionAv.vitesseappliquee,     label="TractionAv_VitAppliquee")
	ax2.plot(dataTractionAv.timestamp, dataTractionAv.vitesseactuelle,     label="TractionAv_VitActuelle")	
	ax2.plot(dataFreins.timestamp, dataFreins.consdynav*10,     label="Frein_Dyn_AV")
	ax2.plot(dataFreins.timestamp, dataFreins.consdynarr*10,     label="Frein_Dyn_AR")

	ax2.legend()
	ax2.grid(True)

	ax3 = plt.subplot(3,1,3, sharex=ax1)

	ax3.plot(dataNav.timestamp, dataNav.d,     label="Nav_DistFromLastSeq")	
	ax3.plot(dataNav.timestamp, dataNav.d_1,     label="Nav_DistToNextSeq")

	ax3.legend()
	ax3.grid(True)

plt.ion()
try:
	dataTractionAv, dataOutil, dataCodeur, dataNav, dataFreins = Import()
	print 'LogOutilAiv:import datas OK'
except:
	print 'LogOutilAiv:Could not import datas'


