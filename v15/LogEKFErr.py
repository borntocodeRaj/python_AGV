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
from numpy import rad2deg
# import string

isVarianceIncluded=True
isPlotCoupled=True

rep_psinav=[]
rep_ekf=[]
ekf_data=[]
unified_data=[]
nav_laser=[]
ekf_variances=[]
latLonVariances=[]
mahalanobisTab=[]
ekf_recal=[]

def computeMahalanobis():
	mahalanobisTabOut= np.zeros(len(unified_data.timestamp_rep_psinav))
	for i in range(0,len(unified_data.timestamp_rep_psinav)):
		predicted=np.array([[unified_data.x_rep_ekf[i]],[unified_data.y_rep_ekf[i]],[unified_data.theta_rep_ekf[i]]])
		psi=np.array([[unified_data.x_rep_psinav[i]],[unified_data.y_rep_psinav[i]],[unified_data.theta_rep_psinav[i]]])
		covarMatrix = np.diagflat([unified_data.p11_variances[i],unified_data.p22_variances[i],unified_data.p33_variances[i]])
		Qgamma=np.diagflat([25*25,25*25,1*np.pi/180.0])
		maha = np.sqrt((psi-predicted).transpose().dot(covarMatrix+Qgamma).dot(psi-predicted))
		mahalanobisTabOut[i]=maha
	print mahalanobisTabOut
	return mahalanobisTabOut
	
def convertVariances2LatLon():
	problemSize = len(unified_data.timestamp_rep_psinav)
	latlonVariancesOut = np.zeros((problemSize,3),np.double)
	for i in range(0,problemSize) :
		theta = unified_data.theta_rep_psinav[i]
		R0m=np.matrix([[np.cos(theta),-np.sin(theta),0.],[np.sin(theta),np.cos(theta),0.0],[0.,0.,1.]])
		#variances=np.matrix([[unified_data.p11_variances[i],0,0],[0,unified_data.p22_variances[i],0],[0,0,unified_data.p33_variances[i]]])		
		variances=np.array([[unified_data.p11_variances[i],unified_data.p12_variances[i],unified_data.p13_variances[i]],
							[unified_data.p21_variances[i],unified_data.p22_variances[i],unified_data.p23_variances[i]],
							[unified_data.p31_variances[i],unified_data.p32_variances[i],unified_data.p33_variances[i]]])
		latlonVariances=R0m.transpose().dot(variances).dot(R0m)
		latlonVariancesOut[i]=[latlonVariances.item(0,0),latlonVariances.item(1,1),latlonVariances.item(2,2)]
	return latlonVariancesOut

def delinearize(theta):
	while theta > pi:
		theta -= 2.0 * pi
	while theta < -pi:
		theta += 2.0 * pi
	return theta

def Import(filename):
	try:
		var=matplotlib.mlab.csv2rec(filename,delimiter='\t')
		print 'Import {0} OK, {1} values'.format(filename,len(var))
		return var
	except:
		print 'WARNING: Could not import {0}'.format(filename)
		return []
	
def PlotMaha():
	plt.figure("Mahalanobis distance",figsize=(13.0,10.0))
	plt.suptitle("Mahalanobis distance for robot posture")
	plt.plot(unified_data.timestamp_rep_psinav,mahalanobisTab, "ro", label="Maha. dist.")
	plt.ylabel("mahaDist")
	plt.legend()
	plt.grid(True)
	
def PlotXY():
	if isPlotCoupled:
		plt.figure("xy position psi",figsize=(13.0,10.0))
		plt.suptitle("Trajectoires Psinav et EKF")
		plt.plot(unified_data.x_rep_psinav,unified_data.y_rep_psinav, label="Psinav", color="red", linestyle="None", marker=".")	
		plt.plot(unified_data.x_rep_ekf,unified_data.y_rep_ekf, label="EKF", color="blue", linestyle="None", marker=".")
		plt.axis('equal')
		plt.xlabel("x (mm)")
		plt.ylabel("y (mm)")
		plt.legend()
		plt.grid(True)
	else:
		plt.figure("xy position psi",figsize=(13.0,10.0))
		plt.suptitle("Trajectoires Psinav et EKF")
		plt.plot(unified_data.x_rep_psinav,unified_data.y_rep_psinav, label="Psinav", color="red", linestyle="None", marker=".")
		plt.axis('equal')
		plt.xlabel("x (mm)")
		plt.ylabel("y (mm)")
		plt.legend()
		plt.grid(True)
		plt.figure("xy EKF",figsize=(13.0,10.0))
		plt.plot(unified_data.x_rep_ekf,unified_data.y_rep_ekf, label="EKF", color="blue", linestyle="None", marker=".")
		plt.axis('equal')
		plt.xlabel("x (mm)")
		plt.ylabel("y (mm)")
		plt.legend()
		plt.grid(True)

def PlotErr():
	convertVariances2LatLon()
	#parametrage
	plotNb=6
	isErrMaxPlotted=True
	plt.figure("Errors",figsize=(13.0,10.0))
	plt.suptitle("Erreurs entre les reperes EKF et Psinav")

	axPosErr = plt.subplot(plotNb,1,1)
	#errors max/min
	if isErrMaxPlotted:
		errMax=[20]*len(unified_data.timestamp_rep_psinav)
		errMin=[-1*el for el in errMax]
	#erreur longitudinale	
	dx = (unified_data.x_rep_ekf - unified_data.x_rep_psinav) * [cos(v) for v in unified_data.theta_rep_psinav] - (unified_data.y_rep_ekf - unified_data.y_rep_psinav) * [sin(v) for v in unified_data.theta_rep_psinav]
	axPosErr.plot(unified_data.timestamp_rep_psinav, dx,     label="$err_{long}$", color="blue", linestyle='None', marker='.')
	#variances erreur longi
	axPosErr.plot(unified_data.timestamp_rep_psinav,3*np.sqrt(latLonVariances[:,0]),label="$3\sigma_{long}$", color="orange", linestyle='None', marker='.')
	axPosErr.plot(unified_data.timestamp_rep_psinav,-3*np.sqrt(latLonVariances[:,0]),color="orange", linestyle='None', marker='.')
	if isErrMaxPlotted:
		axPosErr.plot(unified_data.timestamp_rep_psinav,errMax, label="$+20mm$", color="red", linestyle='--')
		axPosErr.plot(unified_data.timestamp_rep_psinav,errMin, label="$-20mm$", color="red", linestyle='--')
	axPosErr.set_ylabel("$long_{err} (mm)$")
	axPosErr.legend()
	axPosErr.grid(True)
	#erreur laterale
	ayPosErr = plt.subplot(plotNb,1,2,sharex=axPosErr)
	dy = (unified_data.x_rep_ekf - unified_data.x_rep_psinav) * [sin(v) for v in unified_data.theta_rep_psinav] + (unified_data.y_rep_ekf - unified_data.y_rep_psinav) * [cos(v) for v in unified_data.theta_rep_psinav]
	ayPosErr.plot(unified_data.timestamp_rep_psinav, dy,     label="$err_{lat}$", color="blue", linestyle='None', marker='.')
	#variance erreur lat
	ayPosErr.plot(unified_data.timestamp_rep_psinav,3*np.sqrt(latLonVariances[:,1]),label="$3\sigma_{lat}$", color="orange", linestyle='None', marker='.')
	ayPosErr.plot(unified_data.timestamp_rep_psinav,-3*np.sqrt(latLonVariances[:,1]),color="orange", linestyle='None', marker='.')
	#erreurs max
	if isErrMaxPlotted:
		ayPosErr.plot(unified_data.timestamp_rep_psinav,errMax, label="$+20mm$", color="red", linestyle='--')
		ayPosErr.plot(unified_data.timestamp_rep_psinav,errMin, label="$-20mm$", color="red", linestyle='--')
	ayPosErr.set_ylabel("$lat_{err} (mm)$")
	ayPosErr.legend()
	ayPosErr.grid(True)
	#erreur orientation
	axHeadingErr = plt.subplot(plotNb,1,3, sharex=axPosErr)
	axHeadingErr.plot(unified_data.timestamp_rep_psinav, [ rad2deg(delinearize(dtheta)) for dtheta in unified_data.theta_rep_ekf - unified_data.theta_rep_psinav], label="$err_{heading} (\degree)$", linestyle='None', marker='.')
	#variances
	axHeadingErr.plot(unified_data.timestamp_rep_psinav, rad2deg(3*np.sqrt(unified_data.p33_variances)), label="$3\sigma_{\\theta} (\degree)$", color="purple", linestyle='None', marker='.')
	axHeadingErr.plot(unified_data.timestamp_rep_psinav, rad2deg(-3*np.sqrt(unified_data.p33_variances)), color="purple", linestyle='None', marker='.')
	axHeadingErr.set_ylabel("$\\theta_{err} (\degree)$")
	axHeadingErr.legend()
	axHeadingErr.grid(True)
	#Biais rayons de roue applique
	errD=0.0
	errG=0.0
	print("Note: Error set on wheels: rightWh=",errD,"% leftWh=",errG,"%")
	rayonReeld=1.0/(1.0+errD/100.0)
	rayonReelg=1.0/(1.0+errG/100.0)
	rayonReeld=1.022047
	rayonReelg=1.025460
	axWheel = plt.subplot(plotNb,1,4,sharex=axPosErr)
	#rayons de roue
	axWheel.plot(ekf_data.timestamp,(rayonReeld-ekf_data.gd)*100,label="$wheel_r$", linestyle='None', marker='.')
	axWheel.plot(ekf_data.timestamp,(rayonReelg-ekf_data.gg)*100,label="$wheel_l$", linestyle='None', marker='.')
	#variances	
	axWheel.plot(unified_data.timestamp_rep_psinav,3*np.sqrt(unified_data.p44_variances),label="$3\sigma_r$",color="purple", linestyle='None', marker='.')
	axWheel.plot(unified_data.timestamp_rep_psinav,-3*np.sqrt(unified_data.p44_variances),color="purple", linestyle='None', marker='.')
	axWheel.plot(unified_data.timestamp_rep_psinav,3*np.sqrt(unified_data.p55_variances),label="$3\sigma_l$",color="orange", linestyle='None', marker='.')
	axWheel.plot(unified_data.timestamp_rep_psinav,-3*np.sqrt(unified_data.p55_variances),color="orange", linestyle='None', marker='.')
	axWheel.set_ylabel("$rad_{err}(\%)$")
	axWheel.legend()
	axWheel.grid(True)
	#MAHA
# 	mahaThreshold=[6.2514]*len(ekf_recal.timestamp)
# 	axMaha = plt.subplot(plotNb,1,5,sharex=axPosErr)
# 	mahalanobisTabOk=mahalanobisTab.copy()
# 	mahalanobisTabNotOk=mahalanobisTab.copy()
# 	mahalanobisTabOk[mahalanobisTabOk>mahaThreshold]=np.nan
# 	mahalanobisTabNotOk[mahalanobisTabNotOk<=mahaThreshold]=np.nan
# 	axMaha.plot(ekf_recal.timestamp,mahalanobisTabNotOk, "ro")
# 	axMaha.plot(ekf_recal.timestamp,mahalanobisTabOk, "go")
# 	axMaha.plot(ekf_recal.timestamp,mahaThreshold, label="Threshold")
# 	axMaha.legend()
# 	axMaha.grid(True)

	axMaha = plt.subplot(plotNb,1,5,sharex=axPosErr)
	mahaThreshold=[6.2514]*len(unified_data.timestamp_rep_psinav)
	axMaha.plot(unified_data.timestamp_rep_psinav, unified_data.maha_ekf_recal,label="$maha_{distance}$", linestyle='None', marker='.')
	axMaha.plot(unified_data.timestamp_rep_psinav, mahaThreshold,label="$maha_{threshold}$")
	axMaha.set_ylabel("$Maha_{posture}$")
	axMaha.legend()
	axMaha.grid(True)

	#vitesse
	axSpeed = plt.subplot(plotNb,1,6,sharex=axPosErr)
	axSpeed.plot(unified_data.timestamp_rep_psinav,unified_data.vav_nav_laser,label="$speed (mm/s)$", linestyle='None', marker='.')
	axSpeed.set_xlabel("time (s)")
	axSpeed.set_ylabel("$speed (mm.s^{-1})$")
	axSpeed.legend()
	axSpeed.grid(True)	
	plt.show()
	
	fig_path = "plotErr.png"
	savefig(fig_path)
	print("Saved at {0}".format(fig_path))

plt.ion()


def mergeAll(start_date_hour="none"):
	rep_psinav_df = pd.DataFrame.from_records(rep_psinav)
	if(start_date_hour!="none"):
		rep_psinav_df_filtered = rep_psinav_df[rep_psinav_df["date_hour"]>start_date_hour]
		rep_psinav_df = rep_psinav_df_filtered
		print "filtered before {0}".format(start_date_hour)
	
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
	
	return unified_data_df.to_records()
	
	
rep_psinav=Import("ReperagePsiNav.txt")
rep_ekf=Import("ReperageEKF.txt")
nav_laser=Import("NavigationLaser.txt")
ekf_data=Import("ekf.txt")
ekf_variances=Import("ekfVariances.txt")
ekf_recal=Import("ekfRecalage.txt")

unified_data = mergeAll()
latLonVariances=convertVariances2LatLon()
mahalanobisTab=ekf_recal.maha