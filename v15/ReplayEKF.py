#!/usr/bin/python
import matplotlib.pyplot as plt
import matplotlib.mlab
from math import *
import numpy
#PANDA
from pandas import DataFrame, read_csv
import pandas as pd #this is how I usually import pandas
#local files
import ekfSimulator
import warnings
#warnings.filterwarnings("ignore", category=numpy.VisibleDeprecationWarning)

def Import(filename):
	datas=matplotlib.mlab.csv2rec(filename,delimiter='\t')
	return datas

#start is the cycle to start with
def Replay(start):
	file = open("ReperageEKF.txt","w") 
 
	file.write("timestamp\tcycle\tx\ty\ttheta\n") 
 
	iPsy = rep_psinav['cycle'] == start
	ekfSimulator.replayInit(rep_psinav.x[iPsy][0], rep_psinav.y[iPsy][0], rep_psinav.theta[iPsy][0], rep_psinav.cycle[iPsy][0], rep_psinav.timestamp[iPsy][0])
	for line in rep_psinav:
		if line.cycle > start:
			iCard = codeurArD['cycle'] == line.cycle
			iCarg = codeurArG['cycle'] == line.cycle
			ok = True
			try:
				ArD = codeurArD.deltacodeurinc[iCard][0] * 0.0279951 * 1.0
				ArG = codeurArG.deltacodeurinc[iCarg][0] * 0.0279951 * 1.0
			except:
				ok = False
			if ok:
				print "ekfSimulator.replayOdo({}, {}, {}, {}, {})".format(ArD, ArG, 1048, line.cycle, line.timestamp)
				[x,y,theta]=ekfSimulator.replayOdo(ArD, ArG, 1048, line.cycle, line.timestamp)
				print "{}, {}, {}".format(x, y, theta)
				if line.cycle % 50 == 0:
					print "ekfSimulator.replayUpdate({}, {}, {}, {}, {})".format(line.x, line.y, line.theta, line.cycle, line.timestamp)
					ekfSimulator.replayUpdate(line.x, line.y, line.theta, line.cycle, line.timestamp)
				file.write("{}\t{}\t{}\t{}\t{}\n".format(line.timestamp, line.cycle, x, y, theta))
	file.close() 

try:
	rep_psinav=Import("ReperagePsiNav.txt")
	print 'Import ReperagePsiNav.txt OK'
except:
	print 'Could not import ReperagePsiNav.txt'

try:
	codeurArD=Import("codeurCodeurArDroite.txt")
	print "CodeurArDroite OK"
except:
	print 'Could not import codeurCodeurArDroite.txt'

try:
	codeurArG=Import("codeurCodeurArGauche.txt")
	print "CodeurArGauche OK"
except:
	print 'Could not import codeurCodeurArGauche.txt'

