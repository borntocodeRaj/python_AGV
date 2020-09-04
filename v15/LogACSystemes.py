#!/usr/bin/python
import matplotlib.pyplot as plt
import matplotlib.mlab
from math import *
import numpy

datas=[]
datasTranspondeurs=[]


def Import(filename):
	datas=matplotlib.mlab.csv2rec(filename,delimiter='\t')
	return datas

		
def PlotT():
	plt.figure()
	ax1 = plt.subplot(4,1,1)
	ax1.plot(datas.timestamp, datas.consphiavreel, label="consPhiAvReel")
	ax1.plot(datas.timestamp, datas.consphiavtheo,     label="consPhiAvTheo")
	ax1.plot(datas.timestamp, datas.phiavreel, label="phiAvReel")
	ax1.plot(datas.timestamp, datas.vcuconspvgdirav,     label="VcuConsPvgDirAv")

	ax1.legend()
	ax1.grid(True)
	
	ax2 = plt.subplot(4,1,2, sharex=ax1)
	ax2.plot(datas.timestamp, datas.consphiarreel, label="consPhiArReel")
	ax2.plot(datas.timestamp, datas.consphiartheo,     label="consPhiArTheo")
	ax2.plot(datas.timestamp, datas.phiarreel, label="phiArReel")
	ax2.plot(datas.timestamp, datas.vcuconspvgdirar,     label="VcuConsPvgDirAr")

	ax2.legend()
	ax2.grid(True)


	ax3 = plt.subplot(4,1,3, sharex=ax1)
	ax3.plot(datas.timestamp, datas.vitavreel, label="vitAvReel")
	ax3.plot(datas.timestamp, datas.vitarreel,     label="vitArReel")
	ax3.plot(datas.timestamp, datas.batravg, label="baTrAvG")
	ax3.plot(datas.timestamp, datas.batravd,     label="baTrAvD")
	ax3.plot(datas.timestamp, datas.batrarg,     label="baTrArG")
	ax3.plot(datas.timestamp, datas.batrard,     label="baTrArD")
	ax3.plot(datas.timestamp, 100*datas.vcuconsctraction,     label="VcuConsCTraction*100")

	ax3.legend()
	ax3.grid(True)

	ax4 = plt.subplot(4,1,4, sharex=ax1)
	ax4.plot(datas.timestamp, datas.consphiavtheo, label="consPhiAvTheo")
	ax4.plot(datas.timestamp, datas.consphiavreel,     label="consPhiAvReel")
	ax4.plot(datas.timestamp, datas.consphiartheo, label="consPhiArTheo")
	ax4.plot(datas.timestamp, datas.consphiarreel,     label="consPhiArReel")
	ax4.plot(datas.timestamp, datas.consphiartheo, label="consPhiArTheo")
	
	ax4.legend()
	ax4.grid(True)

plt.ion()
try:
	datas=Import("NavigationACSystemes.txt")
	print 'LogACSystemes:import datas OK'
except:
	print 'LogACSystemes:Could not import datas'


