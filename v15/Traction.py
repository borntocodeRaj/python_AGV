import matplotlib.pyplot
import matplotlib.mlab
from math import *
import numpy

import LogMouvement
import Utils

datas=[]

# plot a mouvement
def AddMvt(ax, datas, name):
	ax.plot(datas.timestamp, datas.consignevitesse,  '-',  label=name+".consigne",         linewidth=1)
	ax.plot(datas.timestamp, datas.vitesseappliquee, '-',  label=name+".vitesseAppliquee", linewidth=1)
	ax.plot(datas.timestamp, datas.vitesseactuelle,  '-',  label=name+".vitesseActuelle",  linewidth=1)
	
# plot y=f(t) and y=-f(t) with **one** line
def SymetricPlot(ax, t, y, name):
	t2 = numpy.append(t , t[::-1])
	y2 = numpy.append(y, -y[::-1])	
	ax.plot(t2, y2,  '-',  label=name, linewidth=2)

def PlotT():
	matplotlib.pyplot.figure()
	ax1 = matplotlib.pyplot.subplot(1,1,1)

	if len(tractionAv)!=0:
	    AddMvt(ax1, tractionAv, "TractionAv")
	if len(tractionAr)!=0:
		AddMvt(ax1, tractionAr, "TractionAr")

	SymetricPlot(ax1, datas.timestamp, datas.conscourante, 'ConsCourante')
	SymetricPlot(ax1, datas.timestamp, datas.conscontrainte, 'LimitConsContrainte')
	SymetricPlot(ax1, datas.timestamp, datas.vaatteindre, 'LimitVaAtteindre')
	ax1.plot(datas.timestamp, datas.arretagvretenu, label='arretagvretenu')

	prevData=datas[0]
	x=[]
	y=[]
	i = 1
	for data in datas[1:]:
		t=data.timestamp
		if data.raisonlimitation != prevData.raisonlimitation:
			t = data.timestamp
			v = data.conscontrainte
			if isnan(v):
				v = 0
			name = data.raisonlimitation
			ax1.text( t, v, name, fontsize=12, horizontalalignment='left')
			prevData = data
			x.append(t)
			y.append(v)
			i = i+1

	ax1.plot(x, y, '*', label='*')
	Utils.FormatAxe(ax1, "speeds", "t(s)", "mm/s")


datas=matplotlib.mlab.csv2rec("LimitationVitesseMngCalcul.txt", delimiter='\t')
print "datas ok"


tractionAv = LogMouvement.tractionAv
tractionAr = LogMouvement.tractionAr

"""
if len(tractionAr)==0:
	(datas, tractionAv) = Utils.TimeRescale((datas,tractionAv))
else:
	(datas, tractionAv, tractionAr) = Utils.TimeRescale((datas,tractionAv, tractionAr))

"""




