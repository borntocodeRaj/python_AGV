#!/usr/bin/python
import matplotlib.pyplot as plt
import matplotlib.mlab
from math import *

av=[]
ar=[]


def Import(filename):
	datas=matplotlib.mlab.csv2rec(filename,delimiter='\t')
	return datas

def PlotT():
	plt.figure()
	ax1 = plt.subplot(2,1,1)
	ax2 = plt.subplot(2,1,2, sharex=ax1)

	if len(av) != 0 :
		ax1.plot(av.timestamp, av.relativex, '-*', label="x-av")
		ax2.plot(av.timestamp, av.relativey, '-*', label="y-av")

	if len(ar) != 0 :
		ax1.plot(ar.timestamp, ar.relativex, '-*', label="x-ar")
		ax2.plot(ar.timestamp, ar.relativey, '-*', label="y-ar")

	ax1.legend()
	ax1.grid(True)
	ax2.legend()
	ax2.grid(True)


def PlotXY():
	plt.figure('XY')
	try:
		plt.plot(av.absolutex, av.absolutey, '-x', label='av.absolute')
		plt.plot(ar.absolutex, ar.absolutey, '-x', label='ar.absolute')
	except:
		print " "		

plt.ion()
try:
	av=Import("AntenneTranspondeur.Av.txt")
	print 'LogAntennesTranspondeur:import av OK'
	ar=Import("AntenneTranspondeur.Ar.txt")
	print 'LogAntennesTranspondeur:import ar OK'
except IOError:
	print 'LogDeuxAntennesTranspondeur:Could not import datas'
