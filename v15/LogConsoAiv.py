#!/usr/bin/python
import matplotlib.pyplot as plt
import matplotlib.mlab
from math import *
import numpy
#from scipy import interpolate

dataTraction=[]
dataTrMeanOnSeq=[]
dataPowerpack=[]
dataPowerpackOnSeq=[]


def Import(filename):
	data=matplotlib.mlab.csv2rec(filename,delimiter='\t')
	return data

def MeanCompute(listData):
	meanTrace = list(listData)
	somme =0;
	for i in range(0, len(meanTrace)-1):
		somme += listData[i]
		meanTrace[i] = somme /(i+1)
	return meanTrace

def MeanCompute2s(listData):
	meanTrace = list(listData)
	mean2s=[0] * 1000
	for i in range(1, len(meanTrace)-1):
		j=i%1000;
		mean2s[i%1000]=listData[i]
		meanTrace[i] = sum(mean2s)/1000
	return meanTrace

def ClearPBUINT(listData):
	#for i in range(0, len(listData)-1):
	#	if listData[i] < -10000:
	#		listData[i] = listData[i] + 65536
	return listData

def CleanTraceSeq(listData):
	listDataClear = list(listData)
	for i in range(1, len(listDataClear)):
		if listDataClear[-i] ==0 or listDataClear[-i] ==1 :
			listDataClear[-i]= listDataClear[-(i-1)]
	for i in range(1, len(listDataClear)):
		if listDataClear[i] ==0 or listDataClear[i] ==1 :
			listDataClear[i]= listDataClear[(i-1)]
	return listDataClear

def ComputeTempsVitesse(listData):
	T00 = 0
	T01 = 0
	T12 = 0
	T23 = 0
	T34 = 0
	T45 = 0
	T56 = 0
	for i in range(0, len(listData)-1):
		if abs(listData[i]) >= 5000 :
			T56 = T56+1
		elif abs(listData[i]) >= 4000 :
			T45 = T45+1
		elif abs(listData[i]) >= 3000 :
			T34 = T34+1
		elif abs(listData[i]) >= 2000 :
			T23 = T23+1
		elif abs(listData[i]) >= 1000 :
			T12 = T12+1
		elif abs(listData[i]) >= 200 :
			T01 = T01+1
		else :
			T00 = T00+1
	print "0-0.2m/s =",100*T00/len(listData)," %"
	print "0.2-1m/s =",100*T01/len(listData)," %"
	print "1-2m/s =",100*T12/len(listData)," %"
	print "2-3m/s =",100*T23/len(listData)," %"
	print "3-4m/s =",100*T34/len(listData)," %"
	print "4-5m/s =",100*T45/len(listData)," %"
	print "5-6m/s =",100*T56/len(listData)," %"
	
##Plot the whole scenario
def PlotT():

	ComputeTempsVitesse(dataTraction.vtraction)
	plt.figure()

## etat batterie powerpack
	ax1 = plt.subplot(4,1,1)

	ax1.plot(dataPowerpack.timestamp, dataPowerpack.txchargeinit, label="InitTxCharge")
	ax1.plot(dataPowerpack.timestamp, dataPowerpack.txcharge, label="RemainingTxCharge")
	miseAechelleDechargeSeq=dataPowerpack.dechargeseq*100
	ax1.plot(dataPowerpack.timestamp, miseAechelleDechargeSeq, label="DechargeSurSeq")

	ax1.legend()
	ax1.grid(True)

## consommation
	ax2 = plt.subplot(4,1,2, sharex=ax1)
	##conversion en W
 	powerconsinstW=dataPowerpack.powerconsinst*10
	powerconsonseqW=dataPowerpack.powerconsonseq*10
	ax2.plot(dataPowerpack.timestamp, powerconsinstW, label="InstPwConsumption (W)")
	ax2.plot(dataPowerpack.timestamp, powerconsonseqW, label="MeanPwConsumptionSeq (W)")
	ax2.plot(dataPowerpack.timestamp, MeanCompute(powerconsinstW), label="MeanPwConsumptionTrace (W)")
	ax2.plot(dataPowerpack.timestamp, MeanCompute(powerconsonseqW), label="MeanPwConsumptionTraceMean (W)")
	ax2.plot(dataPowerpack.timestamp, MeanCompute2s(powerconsinstW), label="MeanPwConsumption2s (W)")
	ax2.legend()
	ax2.grid(True)

## traction
	ax3 = plt.subplot(4,1,3, sharex=ax1)

	ax3.plot(dataTraction.timestamp, dataTraction.vconstraction, label="ConsigneVitesse")
	ax3.plot(dataTraction.timestamp, dataTraction.vtraction, label="InstVitesse")
	ax3.plot(dataTraction.timestamp, dataTraction.acceleration, label="InstAcceleration")
	miseAechelleRegenerationState=dataTraction.regeneration*2000
	ax3.plot(dataTraction.timestamp, miseAechelleRegenerationState, label="RegenerationState")
	ax3.plot(dataTraction.timestamp, MeanCompute(abs(dataTraction.vtraction)), label="Vitesse Moyenne (abs)")

	ax3.legend()
	ax3.grid(True)

## over a sequence
	ax4 = plt.subplot(4,1,4)
	numseqClear = CleanTraceSeq(dataPowerpackOnSeq.numseq)
	dataTrMeanOnSeqClear = CleanTraceSeq(dataTrMeanOnSeq.idseq)

	ax4.plot(dataTrMeanOnSeqClear, dataTrMeanOnSeq.vtractiononseq, label="MeanSpeed")
	powerseqW=dataPowerpackOnSeq.powerconsonseq*10
	ax4.plot(numseqClear, powerseqW, label="MeanPowerCons")
	miseAechelleDuration=dataPowerpackOnSeq.seqduration*00
	ax4.plot(numseqClear, miseAechelleDuration, label="SequenceDuration x100")

	ax4.legend()
	ax4.grid(True)
	plt.show()

	plt.figure()

## consommation
	ax21 = plt.subplot(4,1,1)
	ax21.plot(dataPowerpack.timestamp, powerconsinstW, label="InstPwConsumption (W)")
	ax21.plot(dataPowerpack.timestamp, powerconsonseqW, label="MeanPwConsumptionSeq (W)")
	ax21.plot(dataPowerpack.timestamp, MeanCompute(powerconsinstW), label="MeanPwConsumptionTrace (W)")
	ax21.legend()
	ax21.grid(True)

## consommation Hydraulique
	ax22 = plt.subplot(4,1,2, sharex=ax21)
	##conversion en W
 	powerVarPompeW=ClearPBUINT(dataInvertorInterControlCanDataInDebug.rx3*10)
	powerVarConvW=dataInvertorInterControlCanDataInDebug.rx4
	ax22.plot(dataInvertorInterControlCanDataInDebug.timestamp, powerVarPompeW, label="InstPw Pompe (W)")
	ax22.plot(dataInvertorInterControlCanDataInDebug.timestamp, powerVarConvW, label="InstPw Convertisseur (W)")
	ax22.plot(dataInvertorInterControlCanDataInDebug.timestamp, MeanCompute(powerVarPompeW), label="Mean Pw Pompe (W)")
	ax22.plot(dataInvertorInterControlCanDataInDebug.timestamp, MeanCompute(powerVarConvW), label="Mean Pw Convertisseur (W)")
	ax22.legend()
	ax22.grid(True)

## consommation Variateur Traction
	ax23 = plt.subplot(3,1,3, sharex=ax21)
	##conversion en W
	powerVarAvGW=dataInvertorInterControlCanDataInDebug.rx5*10
	powerVarAvDW=dataInvertorInterControlCanDataInDebug.rx6*10
	powerVarArGW=dataInvertorInterControlCanDataInDebug.rx7*10
	powerVarArDW=dataInvertorInterControlCanDataInDebug.rx8*10


	ax23.plot(dataInvertorInterControlCanDataInDebug.timestamp, powerVarAvGW, label="InstPw VAR Av Gauche (W)")
	ax23.plot(dataInvertorInterControlCanDataInDebug.timestamp, powerVarAvDW, label="InstPw VAR Av Droite (W)")
	ax23.plot(dataInvertorInterControlCanDataInDebug.timestamp, powerVarArGW, label="InstPw VAR Ar Gauche (W)")
	ax23.plot(dataInvertorInterControlCanDataInDebug.timestamp, powerVarArDW, label="InstPw VAR Ar Droite (W)")

	ax23.plot(dataInvertorInterControlCanDataInDebug.timestamp, MeanCompute(powerVarAvGW), label="MeanPw VAR Av Gauche (W)")
	ax23.plot(dataInvertorInterControlCanDataInDebug.timestamp, MeanCompute(powerVarAvDW), label="MeanPw VAR Av Droite (W)")
	ax23.plot(dataInvertorInterControlCanDataInDebug.timestamp, MeanCompute(powerVarArGW), label="MeanPw VAR Ar Gauche (W)")
	ax23.plot(dataInvertorInterControlCanDataInDebug.timestamp, MeanCompute(powerVarArDW), label="MeanPw VAR Ar Droite (W)")
	ax23.legend()
	ax23.grid(True)

## de nouveau le graphe le plus interessant

	plt.figure()

## consommation
	ax31 = plt.subplot(2,1,1)

	ax31.plot(dataTraction.timestamp, dataTraction.vconstraction, label="ConsigneVitesse")
	ax31.plot(dataTraction.timestamp, dataTraction.vtraction, label="InstVitesse")
	ax31.plot(dataTraction.timestamp, dataTraction.acceleration, label="InstAcceleration")
	ax31.legend()
	ax31.grid(True)
## consommation Variateur Traction
	ax32 = plt.subplot(2,1,2, sharex=ax31)
	##conversion en W
	ax32.plot(dataInvertorInterControlCanDataInDebug.timestamp, powerVarAvGW, label="InstPw VAR Av Gauche (W)")
	ax32.plot(dataInvertorInterControlCanDataInDebug.timestamp, powerVarAvDW, label="InstPw VAR Av Droite (W)")
	ax32.plot(dataInvertorInterControlCanDataInDebug.timestamp, powerVarArGW, label="InstPw VAR Ar Gauche (W)")
	ax32.plot(dataInvertorInterControlCanDataInDebug.timestamp, powerVarArDW, label="InstPw VAR Ar Droite (W)")

	ax32.plot(dataInvertorInterControlCanDataInDebug.timestamp, MeanCompute(powerVarAvGW), label="MeanPw VAR Av Gauche (W)")
	ax32.plot(dataInvertorInterControlCanDataInDebug.timestamp, MeanCompute(powerVarAvDW), label="MeanPw VAR Av Droite (W)")
	ax32.plot(dataInvertorInterControlCanDataInDebug.timestamp, MeanCompute(powerVarArGW), label="MeanPw VAR Ar Gauche (W)")
	ax32.plot(dataInvertorInterControlCanDataInDebug.timestamp, MeanCompute(powerVarArDW), label="MeanPw VAR Ar Droite (W)")
	ax32.legend()
	ax32.grid(True)
	plt.show()




plt.ion()
try:
	print 'LogConsoAiv:import data Traction...'
	dataTraction = Import('Traction.txt') 
	print 'LogConsoAiv::import data TractionMeanOnSeq...'
	dataTrMeanOnSeq = Import('TractionMeanOnSeq.txt')
	print 'LogConsoAiv::import data BatteriePowerpack...'
	dataPowerpack = Import('BatteriePowerpack.txt')
	print 'LogConsoAiv::import data BatteriePowerpackOnSeq...'
	dataPowerpackOnSeq = Import('BatteriePowerpackOnSeq.txt')
	print 'LogConsoAiv::import data InterControlCanDataInDebug.txt...' 
	dataInvertorInterControlCanDataInDebug = Import('InterControlCanDataInDebug.txt')
	print 'LogConsoAiv:import datas OK'
except:
	print 'LogConsoAiv:Could not import datas'

PlotT()


