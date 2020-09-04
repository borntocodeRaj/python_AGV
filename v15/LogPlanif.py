#!/usr/bin/python
import matplotlib.pyplot as plt
import matplotlib.mlab
from math import *
import numpy
#from scipy import interpolate

datas=[]
datasRalenti=[]
datasTranspondeurs=[]

def Import():
	datasDeb=matplotlib.mlab.csv2rec('SegmAgvLimitDeb.csv',delimiter='\t')
	datasFin=matplotlib.mlab.csv2rec('SegmAgvLimitFin.csv',delimiter='\t')
	datasPrep=matplotlib.mlab.csv2rec('SegmAgvPrepVitesse.csv',delimiter='\t')
	return datasDeb, datasFin, datasPrep

##Plot a single sequence
def PlotSeq(noSeq):
	res = False

	## Check whether the sequence exists
	for i in range(1, len(datasPrep)):
		if datasPrep[i].sequ == noSeq:
			res = True
			i = len(datasPrep)
 	
	if res == False:
		print 'The sequence does not exist or is an action. Check with PlotT'
		return;

	plt.figure()
	ax1 = plt.subplot(1,1,1)

	s = [ data.s for data in datasPrep if data.sequ == noSeq ]
	vDeb = [ data.v for data in datasDeb if data.sequ == noSeq ]		
	vFin = [ data.v for data in datasFin if data.sequ == noSeq ]		
	vPrep = [ data.v for data in datasPrep if data.sequ == noSeq ]
	reperes = []
	reperev = []

	x = [s[0]]
	for i in range(1, len(s)):
		if s[i]-s[i-1]>0:
			x2 = x[-1] + s[i]-s[i-1]
		else:
			x2 = x[-1] 
			reperes.append(x2)
			reperev.append(vPrep[i])
		x.append(x2)
		
	plt.plot(x, vPrep, '--', label ='dataPrep (step 1)')
	plt.plot(x, vFin, '-.', label ='dataDec (step 2)')
	plt.plot(x, vDeb, label ='dataAcc (step 3)')

	plt.plot(reperes, reperev, '*', label ='*')
		
	ax1.legend()
	ax1.grid(True)

##Plot the whole scenario
def PlotT():

	plt.figure()
	ax1 = plt.subplot(2,1,1)

	s = [ data.s for data in datasPrep ]		
	vPrep = [ data.v for data in datasPrep ]
	reperes = []
	reperev = []

	x = [s[0]]
	for i in range(1, len(s)):
		if s[i]-s[i-1]>0:
			x2 = x[-1] + s[i]-s[i-1]
		else:
			x2 = x[-1] 
			reperes.append(x2)
			reperev.append(vPrep[i])
			if datasPrep[i].sequ != datasPrep[i-1].sequ:
				ax1.text( x2, -20, 's', fontsize=12, horizontalalignment='left')
				ax1.text( x2+3, -20, datasPrep[i].sequ, fontsize=12, horizontalalignment='left')
		x.append(x2)
	
	ax1.plot(x, vPrep, '--', label ='dataPrep (step 1)')

	ax1.plot(reperes, reperev, '*', label ='*')
		
	ax1.legend()
	ax1.grid(True)

	ax2 = plt.subplot(2,1,2, sharex=ax1)

	s2 = [ data.s for data in datasFin ]
	vDeb = [ data.v for data in datasDeb ]
	vFin = [ data.v for data in datasFin ]
	reperes = []
	reperev = []

	x = [s2[0]]
	for i in range(1, len(s2)):
		if s2[i]-s2[i-1]>0:
			x2 = x[-1] + s2[i]-s2[i-1]
		else:
			x2 = x[-1] 
			reperes.append(x2)
			reperev.append(vFin[i])
		x.append(x2)
	
	ax2.plot(x, vFin, '--', label ='dataDec (step 2)')
	ax2.plot(x, vDeb, label ='dataAcc (step 3)')

	ax2.plot(reperes, reperev, '*', label ='*')
		
	ax2.legend()
	ax2.grid(True)


plt.ion()
try:
	datasDeb, datasFin, datasPrep = Import()
	#datasPrep = Import()
	print 'LogPlanification:import datas OK'
except:
	print 'LogPlanification:Could not import datas'


