#!/usr/bin/python
import matplotlib.pyplot as plt
import matplotlib.mlab
import matplotlib
from math import *
import numpy as np
#PANDA
from pandas import DataFrame, read_csv
import pandas as pd #this is how I usually import pandas
from matplotlib.pyplot import savefig
from cmath import pi
from sympy.physics.units import length
from scipy.spatial.distance import mahalanobis
from numpy import rad2deg, NAN
# import string


rep_psinav=[]
rep_ekf=[]
ekf_data=[]
unified_data=[]
nav_laser=[]
ekf_variances=[]
latLonVariances=[]
latLonRVariances=[]
mahaPosture=[]
ekf_recal=[]
errLatLonTh_thetaPsinav=[]
errLatLonTh_thetaEkf=[]
allMaha=[]

def pow2(number):
	return np.power(number,2)
def pow2OnAll(array):
	arrayout = [ pow2(el) for el in array] 
	return arrayout

def sqrtOnAll(array):
	arrayOut = [np.sqrt(el) for el in array]
	return arrayOut

#WARNING fonction R en dur ici
def convertRVariances2LatLon():
	problemSize = len(unified_data.timestamp_rep_psinav)
	latLonRVariancesOut = np.zeros((problemSize,3),np.double)
	R=np.matrix([[23.5,0,0],
				[0,23.5,0],
				[0,0,np.deg2rad(0.128)]])
	for i in range(0,problemSize) :
		R0m=getR0m(unified_data.theta_rep_psinav[i])
		latLonRVariancesMat=R0m.transpose().dot(R).dot(R0m)
		latLonRVariancesOut[i]=[latLonRVariancesMat.item(0,0),latLonRVariancesMat.item(1,1),latLonRVariancesMat.item(2,2)]
	return latLonRVariancesOut

def convertVariances2LatLon():
	problemSize = len(unified_data.timestamp_rep_psinav)
	latlonVariancesOut = np.zeros((problemSize,3),np.double)
	for i in range(0,problemSize) :
		R0m=getR0m(unified_data.theta_rep_psinav[i])		
		variances=np.array([[unified_data.p11_variances[i],unified_data.p12_variances[i],unified_data.p13_variances[i]],
							[unified_data.p21_variances[i],unified_data.p22_variances[i],unified_data.p23_variances[i]],
							[unified_data.p31_variances[i],unified_data.p32_variances[i],unified_data.p33_variances[i]]])
		latlonVariances=R0m.transpose().dot(variances).dot(R0m)
		latlonVariancesOut[i]=[latlonVariances.item(0,0),latlonVariances.item(1,1),latlonVariances.item(2,2)]
	return latlonVariancesOut

def computeMahaPosture():
	global mahaPosture
	problemSize = len(unified_data.timestamp_rep_psinav)
	mahaPosture = np.zeros((problemSize,3),np.double)
	problemSize = len(unified_data.timestamp_rep_psinav)
	np.zeros((problemSize,3),np.double)
	
	for i in range(0,problemSize):
		mahaLong = np.sqrt(pow2(errLatLonTh_thetaPsinav[i,0])/(pow2(latLonVariances[i,0])+pow2(latLonRVariances[i,0])))
		mahaLat = np.sqrt(pow2(errLatLonTh_thetaPsinav[i,1])/(pow2(latLonVariances[i,1])+pow2(latLonRVariances[i,1])))
		mahaTheta = np.sqrt(pow2(errLatLonTh_thetaPsinav[i,2])/(pow2(latLonVariances[i,2])+pow2(latLonRVariances[i,2])))
		mahaPosture[i]=[mahaLong,mahaLat,mahaTheta]

def getR0m(theta):
	return np.matrix([[np.cos(theta),-np.sin(theta),0.],[np.sin(theta),np.cos(theta),0.0],[0.,0.,1.]])

def convertErr2LatLon():
	global errLatLonTh_thetaPsinav, errLatLonTh_thetaEkf
	problemSize = len(unified_data.timestamp_rep_psinav)
	errX = unified_data.x_rep_psinav - unified_data.x_rep_ekf
	errY = unified_data.y_rep_psinav - unified_data.y_rep_ekf
	errTh = [ delinearize(theta) for theta in unified_data.theta_rep_psinav - unified_data.theta_rep_ekf]
	errLatLonTh_thetaPsinav=np.zeros((problemSize,3),np.double)
	errLatLonTh_thetaEkf=np.zeros((problemSize,3),np.double)
	for i in range(0,problemSize):
		#avec THETA psinav
		R0m=getR0m(unified_data.theta_rep_psinav[i])
		errPosture = np.array([[errX[i]],[errY[i]],[errTh[i]]])
		latLonErr=R0m.dot(errPosture)
		errLatLonTh_thetaPsinav[i]=[latLonErr.item(0),latLonErr.item(1),latLonErr.item(2)]
		
		#avec THETA ekf
		R0m=getR0m(unified_data.theta_rep_ekf[i])
		latLonErr=R0m.dot(errPosture)
		errLatLonTh_thetaEkf[i]=[latLonErr.item(0),latLonErr.item(1),latLonErr.item(2)]

def plotErrLatLon():
	convertErr2LatLon()
	
	plt.figure("Err lat/lon",figsize=(13.0,10.0))
	plotNb = 3
	subplots=[]
	
	axErrLat = plt.subplot(plotNb,1,1)
	axErrLat.plot(unified_data.timestamp_rep_psinav,errLatLonTh_thetaEkf[:,0],'r.',label="Err longi EKF")
	axErrLat.plot(unified_data.timestamp_rep_psinav,errLatLonTh_thetaPsinav[:,0],'b.',label="Err longi $\Psi$")
	subplots.append(axErrLat)
	
	axErrLon = plt.subplot(plotNb,1,2,sharex=axErrLat)
	axErrLon.plot(unified_data.timestamp_rep_psinav,errLatLonTh_thetaEkf[:,1],'r.',label="Err lat EKF")
	axErrLon.plot(unified_data.timestamp_rep_psinav,errLatLonTh_thetaPsinav[:,1],'b.',label="Err lat $\Psi$")
	subplots.append(axErrLon)
# 	
	axErrTheta = plt.subplot(plotNb,1,3,sharex=axErrLat)
	normalizedTheta = [rad2deg(delinearize(th)) for th in unified_data.theta_rep_ekf - unified_data.theta_rep_psinav]
	axErrTheta.plot(unified_data.timestamp_rep_psinav,normalizedTheta,'g.',label="Err $\\theta$")
	subplots.append(axErrTheta)
	
	for subplot in subplots:
		subplot.legend()
		subplot.grid(True)
	plt.show()
	
	fig_path = "plotErrDection.png"
	savefig(fig_path)
	print("Saved at {0}".format(fig_path))
	
def plotMahas():
	isInternalMahaPlotted = True
	isErrorBasedMahaPlotted = False
	global latLonRVariances, latLonVariances
	mahaThreshold = 2.7055
	convertErr2LatLon()
	latLonVariances = convertVariances2LatLon()
	latLonRVariances = convertRVariances2LatLon()
	computeMahaPosture()
	
	plt.figure("Mahalanobis distances long/lat/heading",figsize=(13.0,10.0))
	plotNb = 3
	subplots=[]
	
	axMahaLong = plt.subplot(plotNb,1,1)
	if isErrorBasedMahaPlotted:
		axMahaLong.plot(unified_data.timestamp_rep_psinav,mahaPosture[:,0],'.',label="$mh_{long}$")
	if isInternalMahaPlotted:
		axMahaLong.plot(unified_data.timestamp_rep_psinav,unified_data.mahalongi_mahas,'r.',label="$mhCpp_{long}$")
	axMahaLong.plot(unified_data.timestamp_rep_psinav,len(unified_data.timestamp_rep_psinav)*[mahaThreshold],'--',label="$mh_{threshold}$")
	subplots.append(axMahaLong)
	
	axMahaLat = plt.subplot(plotNb,1,2,sharex=axMahaLong)
	if isErrorBasedMahaPlotted:
		axMahaLat.plot(unified_data.timestamp_rep_psinav,mahaPosture[:,1],'.',label="$mh_{lat}$")
	if isInternalMahaPlotted:
		axMahaLat.plot(unified_data.timestamp_rep_psinav,unified_data.mahalat_mahas,'r.',label="$mhCpp_{lat}$")
	axMahaLat.plot(unified_data.timestamp_rep_psinav,len(unified_data.timestamp_rep_psinav)*[mahaThreshold],'--')
	subplots.append(axMahaLat)
	
	axMahaHeading = plt.subplot(plotNb,1,3,sharex=axMahaLong)
	if isErrorBasedMahaPlotted:
		axMahaHeading.plot(unified_data.timestamp_rep_psinav,mahaPosture[:,2],'.',label="$mh_{\\theta}$")
	if isInternalMahaPlotted:
		axMahaHeading.plot(unified_data.timestamp_rep_psinav,unified_data.mahatheta_mahas,'r.',label="$mhCpp_{\\theta}$")
	axMahaHeading.plot(unified_data.timestamp_rep_psinav,len(unified_data.timestamp_rep_psinav)*[mahaThreshold],'--')
	subplots.append(axMahaHeading)
	
	for subplot in subplots:
		subplot.legend()
		subplot.grid(True)
	plt.show()
	
	fig_path = "plotErrDection_mahas.png"
	savefig(fig_path)
	print("Saved at {0}".format(fig_path))
	
def delinearize(theta):
	while theta > pi:
		theta -= 2.0 * pi
	while theta < -pi:
		theta += 2.0 * pi
	return theta

def Import(filename):
	try:
		var=matplotlib.mlab.csv2rec(filename,delimiter='\t')
		print 'Import {0} OK'.format(filename)
		return var
	except:
		print 'WARNING: Could not import {0}'.format(filename)
		return []

def mergeAll(start_date_hour="none",startCycle=NAN):
	rep_psinav_df = pd.DataFrame.from_records(rep_psinav)
	if(start_date_hour!="none"):
		rep_psinav_df_filtered = rep_psinav_df[rep_psinav_df["date_hour"]>start_date_hour]
		rep_psinav_df = rep_psinav_df_filtered
		print "filtered before {0}".format(start_date_hour)
	
	if(isnan(startCycle)==False):
		rep_psinav_df_filtered = rep_psinav_df[rep_psinav_df["cycle"]>startCycle]
		rep_psinav_df = rep_psinav_df_filtered
		print "filtered before cycle {0}".format(startCycle)
	
	rep_psinav_df.columns = rep_psinav_df.columns + "_rep_psinav"
	
	rep_ekf_df = pd.DataFrame.from_records(rep_ekf)
	rep_ekf_df.columns = rep_ekf_df.columns + "_rep_ekf"
	
	unified_data_df = pd.merge(rep_psinav_df, rep_ekf_df, how='inner', left_on='cycle_rep_psinav', right_on='cycle_rep_ekf')
	
	#fusing nav laser
	nav_laser_df = pd.DataFrame.from_records(nav_laser)
	nav_laser_df.columns += "_nav_laser"	
	
	unified_data_df = pd.merge(unified_data_df, nav_laser_df, how="left", left_on="cycle_rep_psinav", right_on="cycle_nav_laser")
	
	ekf_recal_df = pd.DataFrame.from_records(ekf_recal)
	ekf_recal_df.columns += "_ekf_recal"	
	unified_data_df = pd.merge(unified_data_df, ekf_recal_df, how="left", left_on="cycle_rep_psinav", right_on="cycle_ekf_recal")
	
	variances_df = pd.DataFrame.from_records(ekf_variances)
	variances_df.columns+="_variances"
	unified_data_df = pd.merge(unified_data_df,variances_df, how="inner", left_on="cycle_rep_psinav", right_on="cycle_variances")
	
	maha_df = pd.DataFrame.from_records(allMaha)
	maha_df.columns+="_mahas"
	unified_data_df = pd.merge(unified_data_df,maha_df, how="left", left_on="cycle_rep_psinav",right_on="cycle_mahas")
	
	return unified_data_df.to_records()


rep_psinav=Import("ReperagePsiNav.txt")
rep_ekf=Import("ReperageEKF.txt")
nav_laser=Import("NavigationLaser.txt")
ekf_data=Import("ekf.txt")
ekf_variances=Import("ekfVariances.txt")
ekf_recal=Import("ekfRecalage.txt")
allMaha=Import("mahalanobisTrace.txt")

unified_data = mergeAll()

plt.ion()
