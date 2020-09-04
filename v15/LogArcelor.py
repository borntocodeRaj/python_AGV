#!/usr/bin/python
import matplotlib.pyplot
import matplotlib.mlab
import collections

def Import(filename):
	datas=matplotlib.mlab.csv2rec(filename,delimiter='\t')
	print "LogCan20:", filename, "OK n=", len(datas)
	return datas


def PlotT(datas	):
	matplotlib.pyplot.figure()
	ax1 = matplotlib.pyplot.subplot(1,1,1)

	ignore_fields=set(['date_hour', 'timestamp', 'cycle', 'unuseddata', 'unuseddata_1', 'unuseddata_2', 'unuseddata_3', 'unuseddata_4', 'unuseddata_5', 'unuseddata_6'])

	for field in datas.dtype.names:
		if field not in ignore_fields:
			ax1.plot(datas.timestamp,datas[field], label=field)
	ax1.legend()
	ax1.grid(True)

matplotlib.pyplot.ion()

try:
	infosVCU=Import("AgentCanArcelorInfoFromVcu.txt")
	inputVCU=Import("AgentCanArcelorInputFromVcu.txt")
	outputVCU=Import("AgentCanArcelorOutputToVcu.txt")

	print 'OK'
except IOError:
	print 'End.'

	







