#!/usr/bin/python
import matplotlib.pyplot as plt
import matplotlib.mlab
from math import *
import numpy
from bzrlib import timestamp
#PANDA
from pandas import DataFrame, read_csv
import pandas as pd #this is how I usually import pandas
from matplotlib.pyplot import savefig
from cmath import pi
#CSV
import csv
from mpmath import linspace
from mercurial.hgweb.webcommands import graph

#config
isFigureSaved=True

navigation=[]
rep_psinav=[]
rep_ekf=[]
ekf=[]
ekf_rec=[]
unified_data=[]
ekf_recalage_df=pd.DataFrame()

def stats(data, isStatPrinted=False, isStatSaved=True):
	elCpt = len(data.x_rep_ekf)
	
	tabErrLon= (data.x_rep_ekf-data.x_rep_psinav) * [cos(theta) for theta in data.theta_rep_psinav]+ (data.y_rep_ekf-data.y_rep_psinav) * [sin(theta) for theta in data.theta_rep_psinav]
	tabErrLat= (data.x_rep_ekf-data.x_rep_psinav) * [sin(theta) for theta in data.theta_rep_psinav]+ (data.y_rep_ekf-data.y_rep_psinav) * [cos(theta) for theta in data.theta_rep_psinav]
	tabErrCap=[delinearize(dtheta) for dtheta in unified_data.theta_rep_ekf - unified_data.theta_rep_psinav]
	#Somme des erreurs
	errLatTotale = numpy.sum(tabErrLat)
	errLonTotale = numpy.sum(tabErrLon)
	errCapTotale = numpy.sum(tabErrCap)
	
	if isStatPrinted:
		print("### Stats ###")
		print("Stats sur {0} elements".format(elCpt))
		print("-- Extremums --")
		print("Err_lat_max= {0}\nErr_lat_min= {1}".format(numpy.amax(tabErrLat),numpy.amin(tabErrLat)))
		print("\nErr_lon_max= {0}\nErr_long_min= {1}".format(numpy.amax(tabErrLon),numpy.min(tabErrLon)))
		print("\nErr_cap_max= {0}\nErr_cap_min= {1}\n".format(numpy.amax(tabErrCap),numpy.amin(tabErrCap)))
		
		print("-- Moyennes --")
	moyErrLat = numpy.abs(errLatTotale)/elCpt
	moyErrLon = numpy.abs(errLonTotale)/elCpt
	moyErrCap = numpy.abs(errCapTotale)/elCpt
	if isStatPrinted:
		print("V.abs Err lat Moy= {0}\nV.abs Err long Moy= {1}\nV.abs Err cap Moy= {2}".format(moyErrLat,moyErrLon,moyErrCap))
	
	ecart_type_x  = numpy.std(data.x_rep_psinav - data.x_rep_ekf)
	ecart_type_y  = numpy.std(data.y_rep_psinav - data.y_rep_ekf)
	ecart_type_theta  = numpy.std((data.theta_rep_psinav - data.theta_rep_ekf)%pi)
	
	if isStatPrinted:
		print("-- Ecarts types --")
		print("Ecart-type_x = {0}\nEcart-type_y= {1}\nEcart-type_theta= {2}".format(ecart_type_x,ecart_type_y,ecart_type_theta))
	
		print("### Fin des Stats ###")
	
	if isStatSaved:
		statFilename = 'stats.csv'
		with open(statFilename, 'wb') as csvfile:
			writer = csv.writer(csvfile, delimiter='\t',quotechar='|', quoting=csv.QUOTE_MINIMAL)
			writer.writerow(["Err_max_lat",numpy.amax(tabErrLat)])
			writer.writerow(["Err_mix_lat",numpy.amin(tabErrLat)])
			writer.writerow(["Err_max_lon",numpy.amax(tabErrLon)])
			writer.writerow(["Err_mix_lon",numpy.amin(tabErrLon)])
			writer.writerow(["Err_max_cap",numpy.amax(tabErrCap)])
			writer.writerow(["Err_mix_cap",numpy.amin(tabErrCap)])
			
			writer.writerow(["Err_moyenne_abs_lat",moyErrLat])
			writer.writerow(["Err_moyenne_abs_lon",moyErrLon])
			writer.writerow(["Err_moyenne_abs_cap",moyErrCap])
			
			writer.writerow(["Ecart_type_lat",ecart_type_x])
			writer.writerow(["Ecart_type_lon",ecart_type_y])
			writer.writerow(["Ecart_type_cap",ecart_type_theta])
		print("saved at {0}".format(statFilename))
	return

def errLatLon(x,y,theta):
	longitudinal = x*cos(theta) + y*sin(theta)
	lateral = x*sin(theta - y*cos(theta))
	return [longitudinal,lateral]

def ecartAngulaire(angle1,angle2):
	delta_theta = angle1 - angle2
	while delta_theta > pi/2.0:
		delta_theta -= pi
	while delta_theta < -pi/2.0:
		delta_theta += pi
	return delta_theta

def ecartAngulaireOnALL(angleArray1,angleArray2):
	ecartTab=[]
	for angleIndex, angle1 in enumerate(angleArray1):
		print angleIndex
		ecartTab.append(ecartAngulaire(angle1, angleArray2[angleIndex]))
	return ecartTab

def Import(filename):
	datas=matplotlib.mlab.csv2rec(filename,delimiter='\t')
	return datas

#param traceReperageTranspondeur : True pour tracer la sortie du logTranspondeur
#param traceReperageSansInfra : True pour tracer la sortie du logSansInfra
def PlotXY(traceReperageTranspondeur=False, traceReperageSansInfra=False):
	plt.figure('XY')
	#adds 20 time markers
	for i in range(0,20):
		j=i*(len(unified_data.x_navigation)/20)
		plt.annotate("t=" + str(unified_data.timestamp_navigation[j]), [unified_data.x_navigation[j], unified_data.y_navigation[j]], color='blue')

	plt.plot(unified_data.x_navigation, unified_data.y_navigation, marker='.', label='navigation', color='blue' )
	plt.plot(unified_data.x_rep_psinav, unified_data.y_rep_psinav, marker='.', label='rep_psinav', color='green')
	plt.plot(unified_data.x_rep_ekf   , unified_data.y_rep_ekf   , marker='.', label='rep_ekf'   , color='red'  )
	plt.plot(unified_data.xpre_ekf    , unified_data.ypre_ekf    , marker='.', label='ekf'       , color='black')

	plt.axis('equal')
	plt.legend()
	plt.grid(True)
	
def PlotXYKalman():
	plt.figure('XY')
	
	plt.plot(ekf.xpre, ekf.ypre, label="EKF predit", marker=".")
	plt.plot(rep_psinav.x, rep_psinav.y, label="psiNav", marker=".")
	plt.plot(ekf_rec.x, ekf_rec.y, label="EKF recal", marker="+")
	
	plt.grid(True)
	plt.axis('equal')
	plt.legend()	
	

def PlotT():
	plt.figure(figsize=(13.0,10.0))
	
	#empeche les affichages exp
	ax = plt.gca()
	ax.get_xaxis().get_major_formatter().set_useOffset(False)
	ax.get_xaxis().get_major_formatter().set_scientific(False)

	ax1 = plt.subplot(4,1,1)
	ax1.plot(unified_data.timestamp_rep_psinav, unified_data.x_rep_psinav, marker='.', label="x-rep-psinav", color='green')
	ax1.plot(unified_data.timestamp_rep_ekf   , unified_data.x_rep_ekf   , marker='.', label="x-rep-ekf"   , color='red'  )
	ax1.plot(updated_data.timestamp_ekf_recalage, updated_data.x_ekf_recalage, marker='.', label="x-ekf_rec", color='yellow')
	ax1.legend()
	ax1.get_xaxis().get_major_formatter().set_useOffset(False)
	ax1.grid(True)
	
	ax2 = plt.subplot(4,1,2, sharex=ax1)
	ax2.plot(unified_data.timestamp_rep_psinav, unified_data.y_rep_psinav, marker='.', label="y-rep-psinav", color='green')
	ax2.plot(unified_data.timestamp_rep_ekf   , unified_data.y_rep_ekf   , marker='.', label="y-rep-ekf"   , color='red'  )
	ax2.plot(updated_data.timestamp_ekf_recalage, updated_data.y_ekf_recalage, marker='.', label="y-ekf_rec"       , color='yellow')
	ax2.legend()
	ax2.get_xaxis().get_major_formatter().set_useOffset(False)
	ax2.grid(True)

	ax3 = plt.subplot(4,1,3, sharex=ax1)
	ax3.plot(unified_data.timestamp_rep_psinav, unified_data.theta_rep_psinav, marker='.', label="theta-rep-psinav", color='green')
	ax3.plot(unified_data.timestamp_rep_ekf   , unified_data.theta_rep_ekf   , marker='.', label="theta-rep-ekf"   , color='red'  )
	ax3.plot(updated_data.timestamp_ekf_recalage       , updated_data.th_ekf_recalage, marker='.', label="theta-ekf_rec", color='yellow')
	ax3.legend()
	ax3.grid(True)
	
	ax4 = plt.subplot(4,1,4, sharex=ax1)
	ax4.plot(unified_data.timestamp_rep_psinav, unified_data.x_rep_psinav     - unified_data.x_rep_ekf,     label="x-err"    , marker='+')
	ax4.plot(unified_data.timestamp_rep_psinav, unified_data.y_rep_psinav     - unified_data.y_rep_ekf,     label="y-err"    , marker='+')
	
	#normalisation des ecarts angulaires sur [-pi/2,pi/2]
	ecart = [ecartAngulaire(val, unified_data.theta_rep_ekf[index]) for index,val in enumerate(unified_data.theta_rep_psinav)]	
		
	ax4.plot(unified_data.timestamp_rep_psinav,	ecart, label="theta-err", marker='+')	
	ax4.legend()
	ax4.grid(True)
	
	
	
	#rend des statistiques sur les erreurs rendues
	stats(unified_data)
	
	if isFigureSaved:
		fig_path = "../plot.png" 
		savefig(fig_path)
		print("Saved at {0}".format(fig_path))
		
	
def PlotErr():
	plt.figure(figsize=(13.0,10.0))
	plt.suptitle("Erreurs entre les reperes EKF et Psinav")

	ax1 = plt.subplot(3,1,1)
	dx = (unified_data.x_rep_ekf - unified_data.x_rep_psinav) * [cos(v) for v in unified_data.theta_rep_psinav] - (unified_data.y_rep_ekf - unified_data.y_rep_psinav) * [sin(v) for v in unified_data.theta_rep_psinav]
	ax1.plot(unified_data.timestamp_rep_psinav, dx,     label="long-err"    , marker='+')
	ax1.legend()
	ax1.grid(True)
	
	ax2 = plt.subplot(3,1,2, sharex=ax1)
	dy = (unified_data.x_rep_ekf - unified_data.x_rep_psinav) * [sin(v) for v in unified_data.theta_rep_psinav] + (unified_data.y_rep_ekf - unified_data.y_rep_psinav) * [cos(v) for v in unified_data.theta_rep_psinav]
	ax2.plot(unified_data.timestamp_rep_psinav, dy,     label="lat-err"    , marker='+')
	ax2.legend()
	ax2.grid(True)

	ax3 = plt.subplot(3,1,3, sharex=ax1)
	ax3.plot(unified_data.timestamp_rep_psinav, [delinearize(dtheta) for dtheta in unified_data.theta_rep_ekf - unified_data.theta_rep_psinav], label="head-err", marker='+')
	ax3.legend()
	ax3.grid(True)
	
	plt.show()
	
	fig_path = "../plotErr.png" 
	savefig(fig_path)
	print("Saved at {0}".format(fig_path))

def PlotWheels():
	plt.figure(figsize=(13.0,10.0))
	plt.suptitle("Rayons de roues estimes")
	
	rightWheelPlot = plt.subplot(2,1,1)
	rightWheelPlot.plot(ekf.timestamp,ekf.gd)
	
	leftWheelPlot = plt.subplot(2,1,2)
	leftWheelPlot.plot(ekf.timestamp,ekf.gg)

def PlotVariance():
	plt.figure(figsize=(13.0,10.0))
	plt.suptitle("Variances d'erreur sur le filtre")
	
	t=linspace(0,1,ekf_variances.length())
	graph_x = plt.subplot(3,1,1)
	sigmaX = ekf_variances.p11
	troisSigma = 3*sigmaX;
	graph_x.plot(t,sigmaX)
	graph_x.plot(t,troisSigma,'g')
	graph_x.plot(t,-troisSigma,'g')
	
	graph_y = plt.subplot(3,2,1)
	sigmaY = ekf_variances.p22
	troisSigma = 3*sigmaY
	graph_y.plot(t,sigmaY)
	graph_y.plot(t,troisSigma,'g')
	graph_y.plot(t,-troisSigma,'g')

	graph_theta = plt.subplot(3,3,1)
	sigmaTh = ekf_variances.p33
	troisSigma = 3*sigmaTh
	graph_theta.plot(t,sigmaTh)
	graph_theta.plot(t,troisSigma,'g')
	graph_theta.plot(t,-troisSigma,'g')

def delinearize(theta):
	while theta > pi:
		theta -= 2.0 * pi
	while theta < -pi:
		theta += 2.0 * pi
	return theta

def mergeAll():
	navigation_df = pd.DataFrame.from_records(navigation)
	navigation_df.theta = navigation_df.theta * pi / 180.0
	navigation_df.columns = navigation_df.columns + "_navigation"
	
	rep_psinav_df = pd.DataFrame.from_records(rep_psinav)
	rep_psinav_df.columns = rep_psinav_df.columns + "_rep_psinav"
	
	rep_ekf_df = pd.DataFrame.from_records(rep_ekf)
	rep_ekf_df.columns = rep_ekf_df.columns + "_rep_ekf"
	
	ekf_df = pd.DataFrame.from_records(ekf)
	ekf_df.columns = ekf_df.columns + "_ekf"
	
	ekf_recalage_df = pd.DataFrame.from_records(ekf_rec_temp)
	ekf_recalage_df.columns = ekf_recalage_df.columns + "_ekf_recalage"
	
	unified_data_df = pd.merge(navigation_df, rep_psinav_df, how='inner', left_on='cycle_navigation', right_on='cycle_rep_psinav')
	unified_data_df = unified_data_df.merge(rep_ekf_df     , how='inner', left_on='cycle_navigation', right_on='cycle_rep_ekf'   )
	unified_data_df = unified_data_df.merge(ekf_df         , how='inner', left_on='cycle_navigation', right_on='cycle_ekf'       )
	
	#merge sur recalage	 == filtrage data hors fenetre	
	temp_initial = unified_data_df.timestamp_navigation[0]
	
	temp = ekf_recalage_df.loc[ekf_recalage_df['timestamp_ekf_recalage']>=temp_initial]
	ekf_recalage_df = temp

	#reconversion		
	fuzed_data = unified_data_df.to_records()
	updated_data = ekf_recalage_df.to_records()	
	
	return [fuzed_data,updated_data]
	
##### MAIN CODE EXECUTION #####
isNavigationFailed=False
plt.ion()
try:
	navigation=Import("NavigationLaser.txt")
	print 'Import NavigationLaser.txt\t\tOK'
	isNavigationFailed=False
except:
	print 'Could not import NavigationLaser.txt'
	isNavigationFailed=True

try:
	rep_psinav=Import("ReperagePsiNav.txt")
	print 'Import ReperagePsiNav.txt\t\tOK'
except:
	print 'Could not import ReperagePsiNav.txt'

try:
	rep_ekf=Import("ReperageEKF.txt")
	print 'Import ReperageEKF.txt\t\t\tOK'
except:
	print 'Could not import ReperageEKF.txt'

try:
	ekf=Import("ekf.txt")
	print 'Import ekf.txt\t\t\t\tOK'
except:
	print 'Could not import ekf.txt'
	
try:
	ekf_rec_temp = Import("ekfRecalage.txt")
	print "Import ekfRecalage.txt\t\t\tOk"
except:
	print 'Could not import ekfRecalage.txt'
try:
	ekf_variances = Import("ekfVariances.txt")
	print "Import ekfVariances.txt\t\t\tOk"
except:
	print 'Could not import ekfVariances.txt'

#Merging
if not isNavigationFailed:
	[unified_data, updated_data ] = mergeAll()
	print "Merging done"

