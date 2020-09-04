#!/usr/bin/python
import matplotlib.pyplot as plt
import matplotlib.mlab
from math import *
import numpy
#PANDA
from pandas import DataFrame, read_csv
import pandas as pd #this is how I usually import pandas

navigation=[]
rep_transpondeur=[]
rep_effibox=[]
effibox_localization=[]
unified_data=[]

def reduceHeadingErr(heading):
	while heading > pi/2.0:
                heading -= pi
        while heading < -pi/2.0:
                heading += pi
        return heading

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
	plt.plot(unified_data.x_rep_transpondeur, unified_data.y_rep_transpondeur, marker='.', label='rep_transpondeur', color='green')
	plt.plot(unified_data.x_rep_effibox   , unified_data.y_rep_effibox   , marker='.', label='rep_effibox'   , color='red'  )

	plt.grid(True)

	plt.axis('equal')
	plt.legend()
	plt.grid(True)

def PlotT(plotDerive=False):
	plt.figure()

	ax1 = plt.subplot(6,1,1)
	dlong = (unified_data.x_rep_transpondeur - unified_data.x_rep_effibox) * [cos(v) for v in unified_data.theta_rep_transpondeur] - (unified_data.y_rep_transpondeur - unified_data.y_rep_effibox) * [sin(v) for v in unified_data.theta_rep_transpondeur]
	sigma_long = unified_data.sigmax_effibox_localization * [abs(cos(v)) for v in unified_data.theta_rep_transpondeur] + unified_data.sigmay_effibox_localization * [abs(sin(v)) for v in unified_data.theta_rep_transpondeur]
	ax1.plot(unified_data.timestamp_rep_transpondeur, dlong,     label="long-err (mm)"    , marker='+')
	ax1.plot(unified_data.timestamp_rep_transpondeur, 3 * sigma_long,     label="+ 3.stddev(long)"    , marker='+')
	ax1.plot(unified_data.timestamp_rep_transpondeur, -3 * sigma_long,     label="- 3.stddev(long)"    , marker='+')
	ax1.legend()
	ax1.grid(True)
	
	ax2 = plt.subplot(6,1,2, sharex=ax1)
	dlat = (unified_data.x_rep_transpondeur - unified_data.x_rep_effibox) * [sin(v) for v in unified_data.theta_rep_transpondeur] + (unified_data.y_rep_transpondeur - unified_data.y_rep_effibox) * [cos(v) for v in unified_data.theta_rep_transpondeur]
	sigma_lat = unified_data.sigmax_effibox_localization * [abs(sin(v)) for v in unified_data.theta_rep_transpondeur] + unified_data.sigmay_effibox_localization * [abs(cos(v)) for v in unified_data.theta_rep_transpondeur]
	ax2.plot(unified_data.timestamp_rep_transpondeur, dlat,     label="lat-err (mm)"    , marker='+')
	ax2.plot(unified_data.timestamp_rep_transpondeur, 3 * unified_data.sigmay_effibox_localization,     label="+ 3.stddev(lat)"    , marker='+')
	ax2.plot(unified_data.timestamp_rep_transpondeur, -3 * unified_data.sigmay_effibox_localization,     label="- 3.stddev(lat)"    , marker='+')
	ax2.legend()
	ax2.grid(True)

	ax3 = plt.subplot(6,1,3, sharex=ax1)
	ax3.plot(unified_data.timestamp_rep_transpondeur, [reduceHeadingErr(err) * 180.0 / pi for err in unified_data.theta_rep_transpondeur - unified_data.theta_rep_effibox], label="heading-err (deg)", marker='+')
	ax3.plot(unified_data.timestamp_rep_transpondeur, 0.003 * unified_data.sigmaheading_effibox_localization,     label="+ 3.stddev(heading)"    , marker='+')
	ax3.plot(unified_data.timestamp_rep_transpondeur, -0.003 * unified_data.sigmaheading_effibox_localization,     label="- 3.stddev(heading)"    , marker='+')
	ax3.legend()
	ax3.grid(True)

	ax4 = plt.subplot(6,1,4, sharex=ax1)
	ax4.plot(unified_data.timestamp_rep_transpondeur, unified_data.vav_navigation, label="speed (mm/s)", marker='+')
	ax4.legend()
	ax4.grid(True)

	ax5 = plt.subplot(6,1,5, sharex=ax1)
	ax5.plot(unified_data.timestamp_rep_transpondeur, unified_data.x_rep_transpondeur - unified_data.x_rep_effibox,     label="x-err (mm)"    , marker='+')
	ax5.plot(unified_data.timestamp_rep_transpondeur, 3 * unified_data.sigmax_effibox_localization,     label="+ 3.stddev(x)"    , marker='+')
	ax5.plot(unified_data.timestamp_rep_transpondeur, -3 * unified_data.sigmax_effibox_localization,     label="- 3.stddev(x)"    , marker='+')
	ax5.legend()
	ax5.grid(True)
	
	ax6 = plt.subplot(6,1,6, sharex=ax1)
	ax6.plot(unified_data.timestamp_rep_transpondeur, unified_data.y_rep_transpondeur - unified_data.y_rep_effibox,     label="y-err (mm)"    , marker='+')
	ax6.plot(unified_data.timestamp_rep_transpondeur, 3 * unified_data.sigmay_effibox_localization,     label="+ 3.stddev(y)"    , marker='+')
	ax6.plot(unified_data.timestamp_rep_transpondeur, -3 * unified_data.sigmay_effibox_localization,     label="- 3.stddev(y)"    , marker='+')
	ax6.legend()
	ax6.grid(True)

def PlotErr():
	plt.figure()
	
	unified_data = mergeAll()
	plt.plot(unified_data.timestamp_rep_transpondeur, unified_data.x_rep_transpondeur     - unified_data.x_rep_effibox,     label="x-err"    , marker='.')
	plt.plot(unified_data.timestamp_rep_transpondeur, unified_data.y_rep_transpondeur     - unified_data.y_rep_effibox,     label="y-err"    , marker='.')
	plt.plot(unified_data.timestamp_rep_transpondeur, [reduceHeadingErr(err) * 180.0 / pi for err in unified_data.theta_rep_transpondeur - unified_data.theta_rep_effibox], label="theta-err", marker='.')
	plt.legend()
	plt.grid(True)
	
	xErrTable = unified_data.x_rep_transpondeur     - unified_data.x_rep_effibox
	yErrTable =   unified_data.y_rep_transpondeur     - unified_data.y_rep_effibox
	thetaErrTable = unified_data.theta_rep_transpondeur - unified_data.theta_rep_effibox
	
	print "Somme des erreurs en x = {0} en y={1} en theta={2}".format(sum(xErrTable),sum(yErrTable),sum(thetaErrTable))

plt.ion()

def mergeAll():
	navigation_df = pd.DataFrame.from_records(navigation)
	navigation_df.theta = navigation_df.theta * pi / 180.0
	navigation_df.columns = navigation_df.columns + "_navigation"
	
	rep_transpondeur_df = pd.DataFrame.from_records(rep_transpondeur)
	rep_transpondeur_df.columns = rep_transpondeur_df.columns + "_rep_transpondeur"
	
	rep_effibox_df = pd.DataFrame.from_records(rep_effibox)
	rep_effibox_df.columns = rep_effibox_df.columns + "_rep_effibox"
	
	effibox_localization_df = pd.DataFrame.from_records(effibox_localization)
	effibox_localization_df.columns = effibox_localization_df.columns + "_effibox_localization"
	
	unified_data_df = pd.merge(navigation_df, rep_transpondeur_df    , how='inner', left_on='cycle_navigation', right_on='cycle_rep_transpondeur')
	unified_data_df = unified_data_df.merge(rep_effibox_df           , how='inner', left_on='cycle_navigation', right_on='cycle_rep_effibox'   )
	unified_data_df = unified_data_df.merge(effibox_localization_df  , how='inner', left_on='cycle_navigation', right_on='cycle_effibox_localization'   )
	
	return unified_data_df.to_records()
	
	
try:
	navigation=Import("NavigationLaser.txt")
	print 'Import NavigationLaser.txt OK'
except:
	print 'Could not import NavigationLaser.txt'

try:
	rep_transpondeur=Import("ReperageTranspondeur.txt")
	print 'Import ReperageTranspondeur.txt OK'
except:
	print 'Could not import ReperageTranspondeur.txt'

try:
	rep_effibox=Import("ReperageSansInfra.txt")
	print 'Import ReperageSansInfra.txt OK'
except:
	print 'Could not import ReperageSansInfra.txt'

try:
	effibox_localization=Import("ReperageSansInfraLocalization.DataIn.txt")
	print 'Import ReperageSansInfraLocalization.DataIn.txt OK'
except:
	print 'Could not import ReperageSansInfraLocalization.DataIn.txt'

unified_data = mergeAll()


