#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from __future__ import print_function
import re
from collections import namedtuple
import struct
import numpy
from math import *


STX=chr(0x02)

#usefull types

''' type for LaserScan : 
 - fileHeader : dict
 - sensorHeader : dict
 - scanDatas : ScanData list  '''
LaserScanRecord = namedtuple('LaserScanRecord', ['fileHeader', 'sensorHeader', 'scanDatas'])

''' type for Velocity :
 - linear : numpay array 3 [vx,vy,vz]
 - angular : numpay array 3 [wx,wy,wz] '''
Velocity = namedtuple('Velocity', ['linear', 'angular'])

''' type for Pose 
  - position : numpay array 3 [x,y,z]
  - orientation : numpy array 3x3, orientation matrix '''
Pose = namedtuple('Pose', ['position', 'orientation'])

'''type for LeadarHeader'''
LidarHeader = namedtuple('LidarHeader', ['timestamp', 'lidarPose', 'robotPose', 'robotVelocity'])

'''type for ScanData'''
ScanData = namedtuple('ScanData', ['lidarHeader', 'distance', 'reflectivity'])

def createPose(posx, posy, posz, m11, m12, m13, m21, m22, m23, m31, m32, m33):
	position = numpy.array([posx, posy, posz])
	orientation = numpy.array( [[m11,m12,m13],[m21,m22,m23],[m31,m32,m33]] )
	return Pose(position, orientation)

def createVelocity( vx, vy, vz, wx, wy, wz ):
	linear = numpy.array([vx, vy, vz])
	angular = numpy.array([wx, wy, wz])
	return Velocity(linear, angular)

#usefull helpers

''' readline and remove cr
@param f file
@return line read '''
def readline_without_cr(f):
	res = f.readline()
	if len(res)>0 and res[-1]=='\n':
		res = res[0:-1]
	return res

''' converts a string to the most appropriate numerical format :
first tries int then float and finally string
@param val string
@return numercial value if possible, val otherwise'''
def tryConvertNum(val):
	try:
		res = int(val)
	except ValueError:
		try:
			res = float(val)
		except ValueError:
			res = val
	return res	

''' @return fileHeader, sensorHeader, scanDatas'''
def openFile(filename):
	# header
	fileHeader = dict()
	sensorHeader = dict()
	# datas
	scanDatas = []
	infos = []

	# opening file
	lineNumber = 0
	f=open(filename)
	truncatedFile =	False

	#read file header
	line = readline_without_cr(f)
	if line != 'BEGIN_FILE_HEADER':
		raise KeyError('BEGIN_FILE_HEADER exptected')
	line = readline_without_cr(f)
	while line != 'END_FILE_HEADER':
		s = re.split(' : ', line)
		key = s[0]
		value = s[1]
		fileHeader[key]=tryConvertNum(value)
		line = readline_without_cr(f)

	#read sensor header
	line = readline_without_cr(f)
	if line != 'BEGIN_SENSOR_HEADER':
		raise KeyError('BEGIN_SENSOR_HEADER exptected')
	line = readline_without_cr(f)
	while line != 'END_SENSOR_HEADER':
		s = re.split(' : ', line)
		key = s[0]
		value = s[1]
		sensorHeader[key]=tryConvertNum(value)
		line = readline_without_cr(f)

	nbPoints = sensorHeader['nbPoints']
	scanDataSize = fileHeader['scan_data_size']

	line = readline_without_cr(f)
	if line != 'BEGIN_SCANS_DATA':
		raise KeyError('SCANS_DATA exptected')

	print("=== Headers OK ===")
	print("fileHeader=", fileHeader)
	print("sensorHeader=", sensorHeader)

	# switch to binary
	buff = f.read()

	if buff[-15:] != 'END_SCANS_DATA\n':
		print("Warning: truncated file")
		truncatedFile = True
	else:
		# remove useless end
		buff = buff[0:-16]
	
	if len(buff) %  scanDataSize != 0:
		if truncatedFile:
			print("Warning : size not correct")
		else:
			print("ERROR : size not correct, still trying to read that...")

	nbScans = len(buff) / scanDataSize
	print("going to read:", nbScans, "scans...", " scanDataSize=", scanDataSize)

	for i in range(0, nbScans):
		lidarHeaderFormat = '<d12f12f6fh'
		lidarHeaderSize = struct.calcsize(lidarHeaderFormat) 

		buff2=buff[scanDataSize*i:scanDataSize*(i+1)]
		h = struct.unpack(lidarHeaderFormat, buff2[0:lidarHeaderSize])
		timestamp = h[0]
		lidarPose = createPose( *h[1:13] )
		robotPose = createPose( *h[13:25] )
		robotVelocity = createVelocity( *h[25:31] )
		lidarHeader = LidarHeader(timestamp, lidarPose, robotPose, robotVelocity)
		nbPoints = h[31]
		if sensorHeader['nbPoints'] != nbPoints:
			print("Warning, nbPoints sensorHeader", sensorHeader['nbPoints'], "!= sensorData", h[31])
			nbPoints =sensorHeader['nbPoints']

		datasFormat = '>' + 'I'*nbPoints + 'H'*nbPoints # 2 unsigned per point
		datasSize = struct.calcsize(datasFormat) 
		h = struct.unpack( datasFormat, buff2[lidarHeaderSize:lidarHeaderSize+datasSize])
		distance = h[0:nbPoints]
		reflectivity = h[nbPoints:2*nbPoints]
		scanData = ScanData(lidarHeader, distance, reflectivity)
		scanDatas.append(scanData)

		if lidarHeaderSize+datasSize != scanDataSize:
			raise BufferError('Extra bytes not expected')
	return LaserScanRecord(fileHeader, sensorHeader, scanDatas)


