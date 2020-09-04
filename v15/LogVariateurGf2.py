#!/usr/bin/python
import matplotlib.pyplot  as plt
import matplotlib.mlab
import collections
import numpy as np


#config du moteur de traction
config_Vm2 = 3779 #tr/min
config_V1 = 2  #m/s

coef_RPM_V = 1000.0*2.0/3779.0;   #passage des RPM aux mm/s


def Import(filename):
    datas=[]
    try:
	datas=matplotlib.mlab.csv2rec(filename,delimiter='\t')
	print "VariateurCanTractionGF2Read:", filename, "OK n=", len(datas)
    except:
	print filename, "empty file ?"
	datas=None
    return datas


#Donnee du variateur
def PlotVariateur():
    plt.figure()
    ax1 = plt.subplot(2,1,1)
    ax1.plot(VariateurCanTractionGF2Read.timestamp, VariateurCanTractionGF2Read.current_slave/10 , '-+',label="ecartCourant")
    ax1.plot(VariateurCanTractionGF2Read.timestamp, VariateurCanTractionGF2Read.current_rms/10 , '-+',label="CourantMaster")
    ax1.legend()
    ax1.grid(True)
    ax1.set_title('Courants')
    axes = plt.gca()
    axes.set_ylim(-300,300)
    
    ax2 = plt.subplot(2,1,2, sharex = ax1)

    ax2.plot(VariateurCanTractionGF2Read.timestamp, VariateurCanTractionGF2Read.run, '-+',label="run")
    ax2.legend()
    ax2.grid(True)
    ax2.set_title('RUN')
    axes = plt.gca()
    axes.set_ylim(-0.5,1.5)
    
    plt.show()

#Donnee du variateur
def PlotMasterSpeeds():

    plt.figure()
    ax1 = plt.subplot(1,1,1)
    ax1.plot(VariateurCanTractionGF2Read.timestamp, coef_RPM_V * VariateurCanTractionGF2Read.motor_rpm , '-+',label="Motor RPM (en mm/s)")
    ax1.plot(tractionArD.timestamp, tractionArD.vitesseappliquee, label="Vitesse appliquee (mm/s)")
    ax1.plot(tractionArD.timestamp, tractionArD.vitesseactuelle , '-+',label="Vitesse mesuree par le codeur (en mm/s)")

    ax1.legend()
    ax1.grid(True)
    ax1.set_title('Vitesses du moteur de traction master (ArD)')
    axes = plt.gca() 
    plt.show()

def PlotBits():

    plt.figure()
    ax1 = plt.subplot(3,1,1)
    ax1.plot(VariateurCanTractionGF2Read.timestamp,  VariateurCanTractionGF2Read.si_spd , '-+',label="SI_spd (0 : en couple, 1 : en vitesse)")

    ax1.legend()
    ax1.grid(True)
    ax1.set_title('SI_spd : Asservissement du variateur esclave')


    ax2 = plt.subplot(3,1,2)
    ax2.plot(VariateurCanTractionGF2Read.timestamp,  VariateurCanTractionGF2Read.los , '-+',label="LOS (0 : no warning, 1 : Limited Operating Strategy)")

    ax2.legend()
    ax2.grid(True)
    ax2.set_title('LOS')


    ax3 = plt.subplot(3,1,3)
    ax3.plot(VariateurCanTractionGF2Read.timestamp,  VariateurCanTractionGF2Read.warn , '-+',label="WARN (0 : no warning, 1 : Reduced Torque")

    ax3.legend()
    ax3.grid(True)
    ax3.set_title('WARN')

    axes = plt.gca() 
    plt.show()

plt.ion()

try:
    VariateurCanTractionGF2Read=Import("VariateurCanTractionGF2Read.txt")
    print "VariateurCanTractionGF2Read OK"
except:
    print 'EndVariateur'

try:
    tractionArD=Import("TractionArDroite.txt")
    print "tractionArD OK"
except:
    print "End Traction ArD"








print "Import Done"

