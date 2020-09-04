#!/usr/bin/python
import sys
import matplotlib.pyplot as plt

plt.ion()
try:

	print('Plot Navigation')
	import LogNavigation
	LogNavigation.PlotT()
	plt.draw()
	LogNavigation.PlotXY()
	plt.draw()
except :
	print('Erreur import LogNavigation', sys.exc_info())
	
try:
	print('Plot Transpondeur')
	import LogTransponder
	LogTransponder.PlotAdjust()
	plt.draw()
except:
	print('Erreur import LogTransponder', sys.exc_info())

print('\n Afficher les arrets scrutateur ? (y/n) [n] :')
if (raw_input() == 'y') :
	try:
		print('Plot Scrutateur')
		import LogScrutateur
		plt.draw()
	except:
		print('Erreur import Scrutateur', sys.exc_info())


try:
	print('Plot Track')
	import Track
	Track.PlotBase()
	plt.draw()
except:
	print('Erreur import Track', sys.exc_info())

print('\n Afficher trajet odometrie pur ?(y/n) [n] :')
if (raw_input() == 'y') :
	a = raw_input("Timestamp de depart (ms) [0] :")
	
	if (a=='') :
	   a = '0'
	b = raw_input("Timestamp de fin (ms) [3000] :")
	if (b==''):
	   b='3000'
	tmDebut = int(a)
	tmFin = int(b)
	try:
		print('Plot Modele Odometrique')
		import OdomModel
		OdomModel.PlotSimulOdom(tmDebut,tmFin)
		plt.legend()
		plt.draw()
	except:
		print('Erreur Plot Odom', sys.exc_info())



print('\n Outil ? (y/n) [n] :')
if (raw_input() == 'y') :
	try:
		print('Plot Outil')
		import LogOutilAiv
		LogOutilAiv.PlotT()
		plt.draw()
	except:
		print('Erreur import outilAiv', sys.exc_info()[0])


print('\n Traction ? (y/n) [n] :')
if (raw_input() == 'y') :
	try:
		print('Plot Traction')
		import Traction
		Traction.PlotT()
		plt.draw()
	except:
		print('Erreur import traction', sys.exc_info())


print('\n Planif ? (y/n) [n] :')
if (raw_input() == 'y') :
	try:
		print('Plot Planif')
		import LogPlanif
		LogPlanif.PlotT()
		plt.draw()
	except:
		print('Erreur import planif', sys.exc_info())


print('\n Consommation ? (y/n) [n] :')
if (raw_input() == 'y') :
	try:
		print('Plot Consommation')
		import LogConsoAiv
		LogConsoAiv.PlotT()
		plt.draw()
	except:
		print('Erreur import consommation', sys.exc_info())

print('\n Centrale Inertielle ? (y/n) [n] :')
if (raw_input() == 'y') :
	try:
		print('Plot Xsens')
		import LogXsens
		LogXsens.PlotT()
		plt.draw()
	except:
		print('Erreur import xsens', sys.exc_info())

print('\n Log Asservissement ? (y/n) [n] :')
if (raw_input() == 'y') :
	try:
		print('Plot Asservissement')
		import LogACSystemes
		LogACSystemes.PlotT()
		plt.draw()
	except:
		print('Erreur import Asservissement', sys.exc_info())

print('\n Log SLAM ? (y/n) [n] :')
if (raw_input() == 'y') :
	try:
		print('Plot SLAM')
		import LogSlam
		LogSlam.PlotSlam()
		plt.draw()
	except:
		print('Erreur import SLAM', sys.exc_info())


print('\n Appuyer sur Entree pour quitter')
raw_input()

