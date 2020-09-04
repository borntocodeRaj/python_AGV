#!/usr/bin/python
import matplotlib.pyplot as plt
import matplotlib.mlab
from math import *
import LogReperage

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

	xok = []
	yok = []
	xnotok = []
	ynotok = []
	for data in av:
		if data.transponderpresent == 1:
			t = data.timestamp
			x = LogReperage.fx(t)
			y = LogReperage.fy(t)
			if data.codereadtranspondervalid == 1:
				xok.append(x)
				yok.append(y)
			else:
				xnotok.append(x)
				ynotok.append(y)
	plt.plot(xok, yok, '-x', label='av.ok', color='green')
	plt.plot(xnotok, ynotok, '-x', label='av.notok', color='red')

plt.ion()
try:
	av=Import("AntenneTranspondeur.Av-msg.txt")
	print 'LogAntennesTranspondeur:import av OK'
	ar=Import("AntenneTranspondeur.Ar-msg.txt")
	print 'LogAntennesTranspondeur:import ar OK'
except IOError:
	print 'LogDeuxAntennesTranspondeur:Could not import datas'
