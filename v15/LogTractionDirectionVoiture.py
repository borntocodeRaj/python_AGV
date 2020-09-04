#!/usr/bin/python
import matplotlib.pyplot  as plt
import matplotlib.mlab
import collections
import numpy as np



def Import(filename):
    datas=[]
    try:
	datas=matplotlib.mlab.csv2rec(filename,delimiter='\t')
	print "LogTractionDirectionVoiture:", filename, "OK n=", len(datas)
    except:
	print filename, "empty file ?"
	datas=None
    return datas


#replace infinity datas with nan
#def infinityisNan(data, infinity):
#    if infinity: 
#        return numpy.nan
#    else:
#        return data
    

#directions avant
def PlotCohDirections():

    plt.figure()
	
    ax1 = matplotlib.pyplot.subplot(2,1,1)
    try :
        ax1.plot(codeurAbsoluVirtuel.timestamp, np.rad2deg(codeurAbsoluVirtuel.phiav), marker='+', label = "phiAv (deg)")
        ax1.plot(codeurAbsoluVirtuel.timestamp, np.rad2deg(codeurAbsoluVirtuel.phiavd), marker='+', label="phi AvD")
        ax1.plot(codeurAbsoluVirtuel.timestamp, np.rad2deg(codeurAbsoluVirtuel.phiavg), marker='+', label="phi AvG")
        ax1.plot(codeurAbsoluVirtuel.timestamp, codeurAbsoluVirtuel.coherentcir, marker='+', label="coherence CIR")
    except :
        print "End Codeur Absolu virtuel"
    ax1.legend()
    ax1.grid(True)
    ax1.set_title('angles (deg)')  
        
    ax2 = matplotlib.pyplot.subplot(2,1,2, sharex = ax1)
    try :
        ax2.plot(codeurAbsoluVirtuel.timestamp, np.rad2deg(codeurAbsoluVirtuel.phiavd),'-+',label="phiavd")
        ax2.plot(codeurAbsoluVirtuel.timestamp, np.rad2deg(codeurAbsoluVirtuel.phiavdth),'-+',label="phiavDTh calcule d apres phiAvG")
        ax2.plot(codeurAbsoluVirtuel.timestamp, np.rad2deg(codeurAbsoluVirtuel.phiavd - codeurAbsoluVirtuel.phiavdth),'-+',label="phiavD - phiavDTh en degres")
    except :
        print "END phiTH"
    ax2.legend()
    ax2.grid(True)
    ax2.set_title('Coherence des angles mesures')

    plt.show()


#tractions 
def PlotCohTractions():
    plt.figure()

    ax1 = plt.subplot(211)
    ax2 = plt.subplot(212, sharex = ax1)
    try :
        ax1.plot(deltanp.timestamp, np.rad2deg(deltanp.phiav), '-+',label='phiAv (deg)')
        ax1.plot(deltanp.timestamp, deltanp.deltasdroite, '-+',label='deltaSARDroite')
        ax1.plot(deltanp.timestamp, deltanp.deltasgauche, '-+',label='deltaSARGauche')
        ax1.plot(deltanp.timestamp, deltanp.coherentv, '-+',label='vitesses coherentes')

        ax1.plot(deltanp.timestamp, deltanp.deltasavdroite, '-+',label='deltaSAVDroite')
        ax1.plot(deltanp.timestamp, deltanp.deltasavgauche, '-+',label='deltaSAVGauche')
        
        ax2.plot(deltanp.timestamp, deltanp.deltasdroite, '-+',label='deltaSDroite')
        ax2.plot(deltanp.timestamp, deltanp.deltasdroiteth, '-+',label='deltaSDroiteTheorique')
        ax2.plot(deltanp.timestamp, deltanp.deltasdroite-deltanp.deltasdroiteth, '-+',label='deltaSdroite - deltaSDroiteTheorique')

    except :
        print "END coherence Traction"

    ax1.legend()
    ax1.grid(True)
    ax1.set_title('') 

    ax2.legend()
    ax2.grid(True)
    ax2.set_title('Coherence des vitesses mesurees') 

    plt.show()


def movingaverage(interval, window_size):
    window= np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')

#tractions 
def PlotCohTractionsDirections():
    plt.figure()

    ax1 = plt.subplot(311)
    ax2 = plt.subplot(312, sharex = ax1)
    ax3 = plt.subplot(313, sharex = ax1)
    try :
        ax1.plot(deltanp.timestamp, np.rad2deg(deltanp.phiav), '-+',label='phiAv (deg)')
        ax1.plot(deltanp.timestamp, np.rad2deg(deltanp.phicalc), '-+',label='phiAv from VAR')

        ax2.plot(deltanp.timestamp, np.rad2deg(deltanp.phiav)-np.rad2deg(deltanp.phicalc) , '-+',label='erreur phiAv from VAR (deg)')

        err = deltanp.phiav - deltanp.phicalc;
        err_mean = movingaverage(err,200);

        ax2.plot(deltanp.timestamp, np.rad2deg(deltanp.erreurcohtracdir), '-+',label='erreur phiAv lissee from C (deg)')
        
        ax3.plot(deltanp.timestamp, np.rad2deg(deltanp.erreurcohtracdir), '-+',label='erreur phiAv lissee from C (deg)')
        ax3.plot(deltanp.timestamp, np.rad2deg(err_mean), '-+',label='erreur phiAv lissee (deg)')

    except :
        print "END coherence Traction Direction"


    ax1.legend()
    ax1.grid(True)
    ax1.set_title('') 

    ax2.legend()
    ax2.grid(True)
    ax2.set_title('Coherence des vitesses mesurees a l''arriere avec l''angle de direction') 

    ax3.legend()
    ax3.grid(True)
    ax3.set_title('Erreur Lissee : coherence des vitesses mesurees a l''arriere avec l''angle de direction') 

#Vitesses selon l'axe Y du chariot, en projettant les deplacements des roues avant, avec leur angle
def PlotVitessesYAvant():
    plt.figure()

    ax1 = plt.subplot(211)
    ax2 = plt.subplot(212, sharex = ax1)
    try :
#        ax1.plot(deltanp.timestamp, np.rad2deg(deltanp.phiav), label='phiAv (deg)')
        ax1.plot(deltanp.timestamp, deltanp.vcy, '-+',label='deplacement centre Y')
        ax1.plot(deltanp.timestamp, deltanp.vdy, '-+',label='deplacement droit Y')
        ax1.plot(deltanp.timestamp, deltanp.vgy, '-+',label='deplacement gauche Y')


        ax2.plot(deltanp.timestamp, deltanp.vcy-deltanp.vdy, '-+',label='erreur v centre Y - v droit Y')
        ax2.plot(deltanp.timestamp, deltanp.vcy-deltanp.vgy, '-+',label='erreur v centre Y - v gauche Y')

        ax2.plot(deltanp.timestamp, deltanp.vdy-deltanp.vgy, '-+',label='erreur v droit Y - v gauche Y')

    except :
        print "END PlotVitessesYAvant"

    ax1.legend()
    ax1.grid(True)
    ax1.set_title('') 

    ax2.legend()
    ax2.grid(True)
    ax2.set_title('') 

    plt.show()


#deplacement du NP : selon X et theta (nul selon Y dans le cas du monotourelle)
def PlotDeltaNP():
    plt.figure()

    ax1 = plt.subplot(211)

    ax2 = plt.subplot(212, sharex = ax1)
    try :
#        ax1.plot(deltanp.timestamp, np.rad2deg(deltanp.phiav), label='phiAv (deg)')
        ax1.plot(deltanp.timestamp, deltanp.deltax, '-+', label='deltaX codeurs Ar')
        ax1.plot(deltanp.timestamp, deltanp.delta2x, '-+',label='deltaX moyenne 4 codeurs')
        ax1.plot(deltanp.timestamp, deltanp.deltax - deltanp.delta2x, '-+',label ='erreur')

        ax2.plot(deltanp.timestamp, deltanp.deltatheta,'-+', label='deltaTheta codeursAr')
        ax2.plot(deltanp.timestamp, deltanp.delta2theta,'-+', label='deltaTheta moyenne 4 codeurs')
        ax2.plot(deltanp.timestamp, deltanp.deltatheta - deltanp.delta2theta,'-+', label = 'erreur')

    except :
        print "END PlotDeltaNP"

    ax1.legend()
    ax1.grid(True)
    ax1.set_title('') 

    ax2.legend()
    ax2.grid(True)
    ax2.set_title('') 
    
    plt.show()


#deplacement du NP obtenu a partir des differents codeurs
def PlotDeltaNPAll():
    plt.figure()

    ax1 = plt.subplot(211)
    ax2 = plt.subplot(212, sharex = ax1)
    try :
#        ax1.plot(deltanp.timestamp, np.rad2deg(deltanp.phiav), label='phiAv (deg)')
        ax1.plot(deltanp2.timestamp, deltanp2.deltaarx, '-+',label='deltaX codeurs Ar')
        ax1.plot(deltanp2.timestamp, deltanp2.deltaavdx, '-+',label='deltaX codeur AV Droite')
        ax1.plot(deltanp2.timestamp, deltanp2.deltaavgx, '-+',label ='deltaX codeur AV Gauche')

        ax2.plot(deltanp2.timestamp, deltanp2.deltaartheta, '-+',label='deltaTheta codeurs Ar')
        ax2.plot(deltanp2.timestamp, deltanp2.deltaavdtheta, '-+',label='deltaTheta codeur AV Droite')
        ax2.plot(deltanp2.timestamp, deltanp2.deltaavgtheta, '-+',label = 'deltaTheta codeur AV Gauche')

    except :
        print "END PlotDeltaNP"

    ax1.legend()
    ax1.grid(True)
    ax1.set_title('Deplacement du NP : deltaX, deltaTheta') 

    ax2.legend()
    ax2.grid(True)
    ax2.set_title('') 

    plt.show()


#deplacement des roues ARRIERE : mesure, et comparaison avec le calcul du deplacement a partir du delatNP
def PlotDeltaSAr():
    plt.figure()

    ax1 = plt.subplot(211)
    ax2 = plt.subplot(212,sharex = ax1)
 
    try :
        ax1.plot(deltanp3.timestamp, deltanp3.deltasdroite, '-+',label = 'deltaSDroite')
        ax1.plot(deltanp3.timestamp, deltanp3.deltasdc, '-+',label ='deltaSDroite calculee avec le deltaNP')
        ax1.plot(deltanp3.timestamp, deltanp3.deltasdroite - deltanp3.deltasdc, '-+',label ='diff')

        ax2.plot(deltanp3.timestamp, deltanp3.deltasgauche, '-+',label = 'deltaSGauche')
        ax2.plot(deltanp3.timestamp, deltanp3.deltasgc, '-+',label = 'deltaSGauche calculee avec le deltaNP')
        ax2.plot(deltanp3.timestamp, deltanp3.deltasgauche - deltanp3.deltasgc, '-+',label = 'diff')

    except :
        print "END PlotDeltaSAr"

    ax1.legend()
    ax1.grid(True)
    ax1.set_title('')

    ax2.legend()
    ax2.grid(True)
    ax2.set_title('')
    
    plt.show()



#deplacement des roues AVANT : mesure, et comparasion avec le calcul du deplacement a partir du delatNP
def PlotDeltaSAv():
    plt.figure()

    ax1 = plt.subplot(211)
    ax2 = plt.subplot(212,sharex = ax1)
 
    try :
        ax1.plot(deltanp3.timestamp, deltanp3.deltasavdroite, '-+',label = 'deltaSDroite AVANT')
        ax1.plot(deltanp3.timestamp, deltanp3.deltasavdc, '-+',label ='deltaSDroite AVANT calculee avec le deltaNP')
        ax1.plot(deltanp3.timestamp, deltanp3.deltasavdroite - deltanp3.deltasavdc, '-+',label ='diff')

        ax2.plot(deltanp3.timestamp, deltanp3.deltasavgauche, '-+',label = 'deltaSGauche AVANT')
        ax2.plot(deltanp3.timestamp, deltanp3.deltasavgc, '-+',label = 'deltaSGauche AVANT calculee avec le deltaNP')
        ax2.plot(deltanp3.timestamp, deltanp3.deltasavgauche - deltanp3.deltasavgc, '-+',label = 'diff')

    except :
        print "END PlotDeltaSAv"

    ax1.legend()
    ax1.grid(True)
    ax1.set_title('')

    ax2.legend()
    ax2.grid(True)
    ax2.set_title('')
    
    plt.show()


#vitesses et angles
def PlotAll():
    plt.figure()
    ax1 = plt.subplot(2,1,1)

    try:
        ax1.plot(tractionDirectionVoiture.timestamp, tractionDirectionVoiture.vav , '-+',label="vAv consigne")
        ax1.plot(tractionDirectionVoiture.timestamp, tractionDirectionVoiture.vard, '-+',label="vArD consigne")
        ax1.plot(tractionDirectionVoiture.timestamp, tractionDirectionVoiture.varg, '-+',label="vArG consigne")
    except:
        print "End Driving"

    ax1.legend()
    ax1.grid(True)
    ax1.set_title('vitesses tractions (mm/s)')

    ax2 = plt.subplot(2,1,2, sharex = ax1)
    try :
        ax2.plot(tractionDirectionVoiture.timestamp, np.rad2deg(tractionDirectionVoiture.phiav), '-+',label="phi Av consigne")
        ax2.plot(tractionDirectionVoiture.timestamp, np.rad2deg(tractionDirectionVoiture.phiavd), '-+',label="phi AvD consigne")
        ax2.plot(tractionDirectionVoiture.timestamp, np.rad2deg(tractionDirectionVoiture.phiavg), '-+',label="phi AvG consigne")
#                ax2.plot(tractionDirectionVoiture.timestamp, numpy.rad2deg(tractionDirectionVoiture.phiav), label="phi Av")
#                ax2.plot(tractionDirectionVoiture.timestamp, numpy.rad2deg(tractionDirectionVoiture.phiavd), label="phi AvD")
#                ax2.plot(tractionDirectionVoiture.timestamp, numpy.rad2deg(tractionDirectionVoiture.phiavg), label="phi AvG")
    except:
	print "End Steering"
        
    ax2.legend()
    ax2.grid(True)
    ax2.set_title('angles directions (deg)')
    plt.show()



#CIR
def PlotCIR():
    p = 1800 #empattement
    dAR = 1345  # voie arriere
    dAV = 908  #voie avant

    CIR_from_VAr_consignes = dAR / 2.0 * (tractionDirectionVoiture.vard + tractionDirectionVoiture.varg)/(tractionDirectionVoiture.vard - tractionDirectionVoiture.varg)

    CIR_from_VAr_measures = dAR / 2.0 * ( deltanp.deltasdroite + deltanp.deltasgauche) / ( deltanp.deltasdroite - deltanp.deltasgauche)

    plt.figure()
    ax1 = plt.subplot(2,1,1)
    ax1.plot(tractionDirectionVoiture.timestamp, CIR_from_VAr_consignes , '-+',label="CIR from VarD and VarG consigne")
    ax1.plot(deltanp.timestamp, CIR_from_VAr_measures, '-+',label="CIR from VarD and VarG measures")
    ax1.legend()
    ax1.grid(True)
    ax1.set_title('')
    

    CIR_from_PhiAvCons = p*np.cos(tractionDirectionVoiture.phiav) / np.sin(tractionDirectionVoiture.phiav)
    CIR_from_PhiAvDCons = p * np.cos(tractionDirectionVoiture.phiavd) / np.sin(tractionDirectionVoiture.phiavd) - dAV/2;  
    CIR_from_PhiAvGCons = p* np.cos(tractionDirectionVoiture.phiavg) / np.sin(tractionDirectionVoiture.phiavg) + dAV/2;

    ax2 = plt.subplot(2,1,2, sharex = ax1)

    ax2.plot(tractionDirectionVoiture.timestamp, CIR_from_PhiAvCons, '-+',label="CIR from PhiAv consigne")
    ax2.plot(tractionDirectionVoiture.timestamp, CIR_from_PhiAvDCons, '-+',label="CIR from PhiAvD consigne")
    ax2.plot(tractionDirectionVoiture.timestamp, CIR_from_PhiAvGCons, '-+',label="CIR from PhiavG consigne")

    ax2.legend()
    ax2.grid(True)
    ax2.set_title('')
    plt.show()


plt.ion()

tractionDirectionVoiture = Import("TractionDirectionVoiture.txt")
print "tractionDirectionVoiture OK"
codeurAbsoluVirtuel = Import("CodeurAbsoluVirtuelDirectionGF2.txt")
print "codeurAbsoluVirtuel OK"
deltanp = Import("DeltaNPGF2.txt")
print "deltaNP OK"

deltanp2 = Import("DeltaNPGF22.txt")
print "deltaNP2 OK"

deltanp3 = Import("DeltaNPGF23.txt")
print "deltaNP3 OK"

print "Import Done"
print "Use PlotAll() to see speeds of driving  and position of steering"
print "Use PlotCohDirections() to see posistion of front steering, and if they are coherent"
print "Use PlotCohTractions()() to see speeds of rear driving, and if they are coherent"
print "Use PlotVitessesYAvant() to see lateral speeds estimated with front encoder"
print "USe PlotDeltaNP() to see Navigation Point deltaX and deltaTheta"
print "Use PlotDeltaNPAll() to see Navigation Point deltaX and deltaTheta, estimated with front and rear encoders"
print "USe PlotDeltaSAr() to see rear speed, estimated using deltaNP, and compare it with rear encoder data"
print "USe PlotDeltaSAv() to see front speed, estimated using deltaNP, and compare it with front encoder data"

