#!/usr/bin/env python

import matplotlib.pyplot as plt
import matplotlib.mlab as ml
import numpy
from  matplotlib.widgets import Slider
from tqdm import *
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection
from math import *

import glob
import os

import ConfigAgv

scrutatorNames = [ "front_LMS",  "front_TIM", "back_LMS", "back_TIM", "right_LMS", "left_LMS" ]
thetaScrutateurs = [ -pi/2, -pi/2, pi/2, pi/2, 0, 0 ]

class plotSodebo(object):
	def __init__(self, clusters, l):
		self.l = l
		self.clusters = clusters
		self.scans = []
	
		self.fig = plt.figure('Navette')
		self.fig.clear()
		self.ax = plt.subplot(1,1,1)
		self.sliderax = self.fig.add_axes([0.2, 0.02, 0.6, 0.03], axisbg='yellow')
		self.slider = DiscreteSlider(self.sliderax, 'Cluster', 0, self.l, increment=1, valinit=0)
		self.slider.on_changed(self.update)
		self.collection1 = None
		self.collection2 = None
		self.collection3 = None
		self.texts = []

		self.posScrutators = []

		# recuperation de la position des scrutateurs dans le fichier de config
		for i in range(0,6):
			fullName = 'Enviroscan.' + scrutatorNames[i] + '.dataConfig'
			x =  ConfigAgv.configAgv['Parameters'][fullName]['X']
			y = ConfigAgv.configAgv['Parameters'][fullName]['Y']
			z = ConfigAgv.configAgv['Parameters'][fullName]['Z']
			self.posScrutators.append([x,y,z])

		# la navette
		x0 = 8708/2.0
		y0 = 2904/2.0
		self.ax.add_patch( mpatches.Rectangle( (-x0, -y0), 2*x0, 2*y0, fill = False, linewidth=3 ))

		# les legendes
		for i in range(0,6):
			x, y = self. convertLocalToAbs(0.0 , 0.0, i )
			label = scrutatorNames[i]
			self.ax.text(x, y, label , color = 'black', bbox=dict(facecolor='white'))
			self.ax.plot(x,y, '*', label='scrutateurs')

		self.gotoScan(0)

		self.ax.axis('equal')
		plt.legend()
		plt.grid(True)

	def animate(self):
		for i in range(0,1000):
			self.gotoScan(i)
			self.fig.canvas.draw()

	def gotoScan(self, scanIndex):
		# clear scans
		if self.collection1 != None:
			self.collection1.remove()
			self.collection1 = None
		if self.collection2 != None:
			self.collection2.remove()
			self.collection2 = None
		if self.collection3 != None:
			self.collection3.remove()
			self.collection3 = None
		# clear texts
		for text in self.texts:
			text.remove()
		self.texts = []

		if len(rectangles[scanIndex])>100 or len(sectors[scanIndex])>100:
			print "cowardly returns"
			return

		# les rectangles de recherche

		patches = []
		for rectangle in rectangles[scanIndex]:
			x1, y1 = self.convertLocalToAbs( rectangle.x1, rectangle.y1, rectangle.index )
			x2, y2 = self.convertLocalToAbs( rectangle.x2, rectangle.y2, rectangle.index )
			m=mpatches.Rectangle( 
				xy = (x1, y1), 
				width=x2-x1, 
				height=y2-y1,
				ec="none", fill=False)
			patches.append(m)
			self.texts.append( self.ax.text( (x1+x2)/2.0, (y1+y2)/2.0, rectangle.name, fontsize=12, color='blue'))

		#collection = PatchCollection(patches, facecolors = ("gray",), edgecolors=("blue",) )
		#collection = PatchCollection(patches, edgecolors=("blue",) )
		collection = PatchCollection(patches, cmap=plt.cm.Greys, alpha=0.3)

		colors = numpy.linspace(0, 1, len(patches))
		collection.set_array(numpy.array(colors))
		
		self.collection2 = self.ax.add_collection(collection)


		# les secteurs
		patches = []
		for sector in sectors[scanIndex]:
			index = sector.index
			x0 = self.posScrutators[index][0]
			y0 = self.posScrutators[index][1]
			'''
			theta0 = -pi/2
			if index==2:
				theta0 = pi/2
			'''
			theta0 = thetaScrutateurs[index]
			x1 = x0 + sector.rmin * cos(sector.thetamin+theta0) 
			y1 = y0 + sector.rmin * sin(sector.thetamin+theta0) 
			x2 = x0 + sector.rmax * cos(sector.thetamin+theta0) 
			y2 = y0 + sector.rmax * sin(sector.thetamin+theta0) 
			x3 = x0 + sector.rmax * cos(sector.thetamax+theta0) 
			y3 = y0 + sector.rmax * sin(sector.thetamax+theta0)
			x4 = x0 + sector.rmin * cos(sector.thetamax+theta0) 
			y4 = y0 + sector.rmin * sin(sector.thetamax+theta0)
			x, y = self.convertLocalToAbs( numpy.array([x1, x2, x3, x4, x1]) , numpy.array([y1, y2, y3, y4, y1]) , sector.index )
			m=mpatches.Polygon( numpy.transpose(numpy.array([x,y])), animated = True)
			patches.append(m)
			self.texts.append( self.ax.text( x[0], y[0], sector.name, fontsize=12, color='blue'))

		#colors = numpy.linspace(0, 1, len(patches))
		#collection = PatchCollection(patches, cmap=plt.cm.cool, alpha=0.3)
		collection = PatchCollection(patches, cmap=plt.cm.Greys, alpha=0.3)
		#colors = numpy.linspace(0, 1, len(patches))
		#collection.set_array(numpy.array(colors))

		self.collection3 = self.ax.add_collection(collection)

		# les scans
		patches = []
		for i in range(0,6):
			# ATTENTION SCAN A L'ENVERS !!!!!!!!!!!!!!      ======> 
			x, y = self.singleScanPlot(clusters[scanIndex][i].x, -clusters[scanIndex][i].y, i )
			m=mpatches.Polygon( numpy.transpose(numpy.array([x,y])), animated = True)
			patches.append(m)

		collection = PatchCollection(patches, cmap=plt.cm.hsv, alpha=0.3)
		colors = numpy.linspace(0, 1, len(patches))
		collection.set_array(numpy.array(colors))
		self.collection1 = self.ax.add_collection(collection)

		plt.title('Scan %03d' % scanIndex)

	def update(self, val):
		scanIndex = int(val)
		self.gotoScan(scanIndex)

	def show(self):
		plt.show()
	
	def singleScanPlot(self, x, y, i):
		if i<4:
			x0 = self.posScrutators[i][0]
			y0 = self.posScrutators[i][1]
		else:
			x0 = 0.0
			y0 = 0.0

		x = numpy.insert( numpy.insert( x, 0, x0), -1, x0)
		y = numpy.insert( numpy.insert( y, 0, y0), -1, y0)
		x2, y2 = self.convertLocalToAbs(x, y, i)
		return x2, y2

	def convertLocalToAbs(self, x, y, i):
		x2 = numpy.array(x)
		y2 = numpy.array(y)
		if i == 4:
			y2 = numpy.add(-y, -4200.0)
		if i == 5:
			y2 = numpy.add(y, 4200.0)
		return x2, y2

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

#p = plotEnviroscan('distParcours_0.txt', 'distParcours_0_ROI.txt')
#p.show()

clusters = []
rectangles = []
sectors = []

fileList = glob.glob("*.txt")

for i in tqdm(range(0,1000)):
	# clusters
	item = []
	for noScrutateur in range(0,6):
		filename = 	'cluster_' + str(i).zfill(3) + "_Scrutateur" + str(noScrutateur) + ".txt"
		if not filename in fileList:
			break
		item.append(ml.csv2rec(filename, delimiter='\t'))
		clusters.append(item)

	#rectangles
	filename = 	'rectangles_' + str(i).zfill(3) + ".txt"
	if not filename in fileList:
		break
	rectangle = ml.csv2rec(filename, delimiter='\t')
	rectangles.append(ml.csv2rec(filename, delimiter='\t'))
	#sectors
	filename = 	'sectors_' + str(i).zfill(3) + ".txt"
	if not filename in fileList:
		break
	sector = ml.csv2rec(filename, delimiter='\t')
	sectors.append(sector)

	l=i

print "l=", l
plt.ion()
p = plotSodebo(clusters, l)
p.show();



