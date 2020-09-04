#!/usr/bin/python
import csv
import collections
import matplotlib.pyplot as plt
import matplotlib.mlab
#import numpy as np

Recalage = collections.namedtuple("Recalage",
	"timeStamp id name xe ye thetae DNPx DNPy DNPtheta mdxT mdyT mdthetaT xme yme xr yr ok noDetection")
				
def printStatus(file, res):
	print "FileName=", file.name, " records=", len(res)
				
def ImportMagnet():
	res = [] 
	file = open("Magnet.txt", "rb")
	reader = csv.DictReader(file, delimiter='\t')
	for row in reader:
		recalage = Recalage(
			timeStamp = float(row["TimeStamp"]),
			id = int(row["id"]),
			name = row["name"],
			xe = float(row["xe"]),
			ye = float(row["ye"]),
			thetae = float(row["thetae"]),
			DNPx = float(row["DNPx"]),
			DNPy = float(row["DNPy"]),
			DNPtheta = float(row["DNPtheta"]),
			mdxT =	float(row["mdxT"]),
			mdyT =	float(row["mdyT"]),
			mdthetaT = float(row["mdthetaT"]),
			xme = float(row["xme"]),
			yme = float(row["yme"]),
			xr = float(row["xr"]),
			yr = float(row["yr"]),
			ok = bool(row["ok"]),
			noDetection = int(row["n"])			
		)
		res.append(recalage)
	printStatus(file,res)
	return res

# Affichage des recalages
# position du magnet estime et fleche de recalage
# une ligne pour lier les positions estimee
def PlotRecalage():
	x=[]
	y=[]
	rx=[]
	ry=[]
	xme=[]
	yme=[]
	for recalage in recalages:
		x.append(recalage.xe-recalage.mdxT)
		y.append(recalage.ye-recalage.mdyT)
		rx.append(recalage.mdxT)
		ry.append(recalage.mdyT)
		xme.append(recalage.xme)
		yme.append(recalage.yme)
	plt.figure('XY')
	plt.quiver(x,y, rx, ry, width=0.0025, angles='xy', scale_units='xy', scale= 1,label="Recalage")
	plt.plot(xme,yme, 'ro', label="MagnetEstime")
	
	#
	x=[]
	y=[]
	x0=recalages[0].xe+5000
	y0=recalages[0].ye+5000
	DNPx=0
	marcheAv=True
	for recalage in recalages:
		xe=recalage.xe
		ye=recalage.ye
		if abs(xe-x0) > 3000 or abs(ye-y0) > 3000 or recalage==recalages[-1] or DNPx*recalage.DNPx <=0:
			if len(x)!=0:
				if marcheAv:
					plt.plot(x,y, 'g-')
				else:
					plt.plot(x,y, 'r-')
				x=[]
				y=[]
		x.append(xe)
		y.append(ye)
		x0=xe
		y0=ye
		DNPx=recalage.DNPx
		marcheAv=(DNPx>0)

# Nouveau format d'importation
class Detection:
	def __init__(self):
		self.timeStamp = 0
		self.noDetection = 0
		self.t = []
		self.y = []
	def __repr__(self):
		return "Detection()"
	def __str__(self):
		return "Detection(timeStamp="+str(self.timeStamp)+",noDetection="+str(self.noDetection)+",t="+str(self.t)+",y="+str(self.y)+")"

def ImportDetect():
	file = open("Detect.txt", "rb")
	reader = csv.reader(file, delimiter='\t')
	# attention en fonction des versions soft, c'est 1 ou 2
	indiceDebut = 1	

	state=0
	res = []
	for row in reader:
		if state==0:
			state=1
			continue
		if state==1:
			noDetection=int(row[indiceDebut])
			l1=row[(indiceDebut+1):]
			state=2;
			continue;
		if state==2:
			if int(row[indiceDebut]) == noDetection:
				l2=row[(indiceDebut+1):]
				d = Detection()
				d.timeStamp = float(row[0])
				for i in range(0, min(len(l1),len(l2))):
					a=l1[i]
					b=l2[i]
					if len(a)>0 and len(b)>=3:
						d.t.append(float(l1[i]))
						d.y.append(float(l2[i]))
				d.noDetection = noDetection
				state=1
				res.append(d)
			else:
				# en fait, on vient de lire un t, et non un y
				# on ignore la ligne suivante
				state=0
				print noDetection,"/",int(row[1])
	printStatus(file,res)
	return res
		
DetectResult = collections.namedtuple("DetectResult", "timeStamp res y t a b c noDetection nx ny ntheta")

def ImportDetectRes():
	res = [] 
	file = open("DetectRes.txt", "rb")
	reader = csv.DictReader(file, delimiter='\t')
	for row in reader:
		detectResult = DetectResult(
			timeStamp = float(row["TimeStamp"]),
			res = int(row["res"]),
			y = float(row["y"]),
			t = float(row["t"]),
			a = float(row["a"]),
			b = float(row["b"]),
			c = float(row["c"]),
			noDetection = int(row["noDetection"]),
			nx = float(row["now.x"]),
			ny = float(row["now.y"]),
			ntheta = float(row["now.theta"])
			)
		res.append(detectResult)
	printStatus(file,res)
	return res
				
def PlotDetection(detection):
	plt.figure('Detection')
	plt.plot(detection.t, detection.y, label="m:"+str(detection.noDetection))
	l2 = [ rd for rd in detectionResults if rd.noDetection == detection.noDetection ]
	if len(l2)==1 and len(detection.t)>2:
		detectionResult = l2[0]
		plt.plot(detectionResult.t, detectionResult.y, label="PointRetenu", marker="x")
		a = detectionResult.a
		b = detectionResult.b
		c = detectionResult.c
		yr = [ a*t*t+b*t+c for t in detection.t ]
		plt.plot(detection.t, yr, label="regression")
	plt.grid(True)
	plt.legend()

class BalluffData:
	def __init__(self):
		self.timeStamp = 0
		self.cycle = 0
		self.state = 0
		self.group = 0
		self.age = 0
		self.mesures = []
	def __repr__(self):
		return "BalluffData()"
	def __str__(self):
		return "BalluffData(timeStamp="+str(self.timeStamp)+",cycle="+str(self.cycle)+",state="+str(self.state)+",group="+str(self.group)+",age"+str(self.age)+",mesures="+str(self.mesures)+")"

		
def ImportBalluff():
	res=[]
	file = open("Balluff.txt", "rb")
	reader = csv.reader(file, delimiter='\t')
	rows=[row for row in reader]
	for row in rows[1:]:
		balluffData = BalluffData()
		balluffData.timeStamp=float(row[0])
		balluffData.cycle=int(row[1])
		balluffData.state=int(row[2])
		balluffData.group=int(row[3])
		balluffData.age=int(row[4])
		for i in range(0,15):
			balluffData.mesures.append(float(row[5+i]))
		res.append(balluffData)
	printStatus(file,res)
	return res
	
	
def PlotBalluffDatas(cycle):
	cycles = [balluffData.cycle for balluffData in balluffDatas]
	i=cycles.index(cycle)
	print "i=",i
	i0=i
	i1=i
	while i0 > 0 and balluffDatas[i0-1].cycle == balluffDatas[i0].cycle-1:
		i0=i0-1
	while (i1+1) < len(balluffDatas) and balluffDatas[i1+1].cycle == balluffDatas[i1].cycle+1:
		i1=i1+1
	print "i0=",i0,",i1=",i1
	datas=[]
	for mesures in [ balluffData.mesures for balluffData in balluffDatas[i0:i1+1] ]:
		datas.extend([x for x in mesures if x!= 0])
	print(datas)
	plt.figure()
	plt.plot( [2*i for i in range(0,len(datas))], datas, label="Balluff", marker='x' )


Magnet = collections.namedtuple("Magnet","id name x y enabled")

def ImportMagnetTrack():
	file = open("../etc/circuit.trk", "rb")
	reader = csv.reader(file, delimiter='\t')
	state=0
	res=[]
	for row in reader:
		if len(row)==0:
			continue
		if state==0:
			if row[0]=="[MAGNET]":
				state=1
				continue
		if state==1:
			state=2
			continue
		if state==2:
			if len(row)==1:
				break
			magnet = Magnet(
				id=int(row[1]),
				name=row[0],
				x=float(row[2]),
				y=float(row[3]),
				enabled=bool(row[4]))
			res.append(magnet)
	printStatus(file,res)
	return res

def PlotMagnet(plotLabels=True):
	if plotLabels:
		for magnet in magnets:
			plt.annotate(magnet.name,[magnet.x,magnet.y])
	plt.figure("XY")
	plt.plot([magnet.x for magnet in magnets], [magnet.y for magnet in magnets], 'o', label='Magnet')
	
plt.ion()

try:
	recalages=ImportMagnet()
	print "recalages OK:", len(recalages)
	detections = ImportDetect()
	print "detections OK:", len(detections)
	detectionResults = ImportDetectRes()
	print "detectionResults OK:", len(detectionResults)
	balluffDatas=ImportBalluff()
	print "balluffDatas OK:", len(balluffDatas)
	magnets=ImportMagnetTrack()
	print "magnets OK:", len(magnets)
	print 'LogMagnet:import OK'
	useMagnet=True
except IOError:
	print 'LogMagnet:Could not import all datas'
	useMagnet=False


