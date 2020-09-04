#!/usr/bin/python

import csv
import collections
import matplotlib.pyplot as plt
import matplotlib.mlab

datas=[]
def Import(filename):
	datas=matplotlib.mlab.csv2rec(filename,delimiter='\t')
	return datas

def PlotDetection(datas):
	plt.figure('XY')
	ymin, ymax = plt.gca().get_ylim()
	ecart = (ymax - ymin)/5
	for data in datas:
		try:
			if(data.instop==1):
				plt.annotate(str(int(data.vitessemesuree))+' mm/s', xy=(data.x,data.y), xytext=(data.x,data.y+ecart), arrowprops=dict(facecolor='red', shrink=0.02))
			if(data.inslowdown==1):
				plt.annotate(str(int(data.vitessemesuree))+' mm/s', xy=(data.x,data.y), xytext=(data.x,data.y+ecart), arrowprops=dict(facecolor='yellow', shrink=0.02))
			if(data.InSpecial==1):
				plt.annotate(str(int(data.vitessemesuree))+' mm/s', xy=(data.x,data.y), xytext=(data.x,data.y+ecart), arrowprops=dict(facecolor='bleu', shrink=0.02))
			if(data.InEdge==1):
				plt.annotate(str(int(data.vitessemesuree))+' mm/s', xy=(data.x,data.y), xytext=(data.x,data.y+ecart), arrowprops=dict(facecolor='green', shrink=0.02))
		except :
			if(data.detectionsecurite==1):
				plt.annotate(str(int(data.vitessemesuree))+' mm/s', xy=(data.x,data.y), xytext=(data.x,data.y+ecart), arrowprops=dict(facecolor='red', shrink=0.02))
			if(data.detectionalarme==1):
				plt.annotate(str(int(data.vitessemesuree))+' mm/s', xy=(data.x,data.y), xytext=(data.x,data.y+ecart), arrowprops=dict(facecolor='yellow', shrink=0.02))


plt.ion()
importOk=False
try :
	datas=Import("DetectionSecu.txt")
	PlotDetection(datas)
	importOk=True
except:
	print 'Erreur import "DetectionSecu.txt'

try :
	datas=Import("DetectionSecu.Avant.txt")
	PlotDetection(datas)
	datas=Import("DetectionSecu.Arriere.txt")
	PlotDetection(datas)
	importOk=True
except:
	print 'Erreur import "DetectionSecu.Avant.txt ou DetectionSecu.Arriere.txt'

if(importOk==False):
	print 'DetectionSecu:Could not import datas'
