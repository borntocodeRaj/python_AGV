#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
from  matplotlib.widgets import Slider
import matplotlib.pyplot as plt

from Tkinter import Tk
from tkFileDialog import askopenfilename

import LaserScanReader
import numpy
from math import *

class PlotLaserScans(object):
	def __init__(self, filename):
		self.laserScanRecord = LaserScanReader.openFile(filename)
		self.l = len(self.laserScanRecord.scanDatas)
		self.fig = plt.figure(filename)
		self.fig.clear()
		self.ax = plt.subplot(1,1,1)
		self.sliderax = self.fig.add_axes([0.2, 0.02, 0.6, 0.03], axisbg='yellow')
		self.slider = DiscreteSlider(self.sliderax, 'Cluster', 0, self.l-1, increment=1, valinit=0)
		self.slider.on_changed(self.update)
		self.line = None

		x = [ 1500, 1500, -1500, -1500, 1500 ]
		y = [ 0, 3000, 3000, 0, 0]
		self.ax.plot(x,y, color='black')
		self.ax.grid(True)

		self.gotoScan(0)
		self.ax.axis('equal')
		plt.legend()
		plt.grid(True)


	def animate(self):
		for i in range(0,1000):
			self.gotoScan(i)
			self.fig.canvas.draw()

	def gotoScan(self, scanIndex):
		# clear texts
		#for line in self.lines:
		#	line.remove()
		#self.lines = []
		x = []
		y = []
		r = []
		scanData = self.laserScanRecord.scanDatas[scanIndex]

		thetaMin = self.laserScanRecord.sensorHeader['thetaMin']
		thetaMax = self.laserScanRecord.sensorHeader['thetaMax']
		nbPoints = self.laserScanRecord.sensorHeader['nbPoints']
		angles = numpy.linspace(thetaMin, thetaMax, nbPoints)

		for angle, dist, reflectivity in zip(angles, scanData.distance, scanData.reflectivity): #scanData.distance
			x.append(dist*cos(angle))
			y.append(dist*sin(angle))
			r.append(reflectivity)
		#self.ax.clear()
		if self.line != None:
			self.line.remove()
			'''
			for i in self.line:
				i.remove()
			'''
		self.line = None
		self.line = self.ax.scatter(x,y, c=r)

		plt.title('Scan %03d' % scanIndex)
		plt.legend()

	def update(self, val):
		scanIndex = int(val)
		self.gotoScan(scanIndex)

	def show(self):
		plt.show()

class DiscreteSlider(Slider):
	"""A matplotlib slider widget with discrete steps."""
	def __init__(self, *args, **kwargs):
		"""
		Identical to Slider.__init__, except for the new keyword 'allowed_vals'.
		This keyword specifies the allowed positions of the slider
		"""
		self.inc = kwargs.pop('increment', 1)
		Slider.__init__(self, *args, **kwargs)

	def set_val(self, val):
		discrete_val = int(val / self.inc) * self.inc
		xy = self.poly.xy
		xy[2] = discrete_val, 1
		xy[3] = discrete_val, 0
		self.poly.xy = xy
		self.valtext.set_text(self.valfmt % discrete_val)
		if self.drawon:
			self.ax.figure.canvas.draw()
		self.val = val
		if not self.eventson:
			return
		for cid, func in self.observers.iteritems():
			func(discrete_val)

plt.ion()

Tk().withdraw()
filename = askopenfilename()
p = PlotLaserScans(filename)
p.show()

