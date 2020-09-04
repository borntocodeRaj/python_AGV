#!/usr/bin/python
import matplotlib.pyplot as plt
import matplotlib.mlab
import numpy
import math
import Utils
import ConfigAgv

dictDatas = dict()   #contient les donnes sous forme de tuple (sinon, les donnees ne sont pas iterables)
tractionAv=[]

def Import(filename):
    datas=matplotlib.mlab.csv2rec(filename,delimiter='\t')
    datas.flags.writeable = False    #de toutes facons on ne modifie pas les donnees d'entree
    tDatas = tuple(datas.flat)
    dictDatas[tDatas] = filename
    print "LogMouvement:", filename, "OK n=", len(datas)
    return datas


def PlotPosition():
    """
    trace les positions consigne et actuelle de chaque fourche
    """
    plt.figure()

    ax1 = matplotlib.pyplot.subplot(4,1,1)
    for field in ["consigneposition", "positionactuelle" ]:
        ax1.plot(fourcheDroiteExt.timestamp,fourcheDroiteExt[field], '-+', label=field)
        ax1.legend()
        ax1.grid(True)
        ax1.set_title('fourche Droite Ext')

    ax2 = matplotlib.pyplot.subplot(4,1,2, sharex=ax1) 
    for field in ["consigneposition", "positionactuelle" ]:
        ax2.plot(fourcheGaucheExt.timestamp,fourcheGaucheExt[field], '-+', label=field)
        ax2.legend()
        ax2.grid(True)
        ax2.set_title('fourche Gauche Ext')
    
    ax3 = matplotlib.pyplot.subplot(4,1,3, sharex=ax1)
    for field in ["consigneposition", "positionactuelle" ]:
        ax3.plot(fourcheDroiteInt.timestamp,fourcheDroiteInt[field], '-+', label=field)
        ax3.legend()
        ax3.grid(True)
        ax3.set_title('fourche Droite Int')
    
    ax4 = matplotlib.pyplot.subplot(4,1,4, sharex=ax1)
    for field in ["consigneposition", "positionactuelle" ]:
        ax4.plot(fourcheGaucheInt.timestamp,fourcheGaucheInt[field], '-+', label=field)
        ax4.legend()
        ax4.grid(True)
        ax4.set_title('fourche Gauche Int')

    plt.show()


def PlotParametres():
    """
    trace le mode de consigne du positionneur, et les valeurs de e1 et e2
    """
    plt.figure();


    ax = plt.subplot(4,1,1)
    try:
        ax.plot(positFourches.timestamp, positFourches.position, '-+', label='mode : 0 : SINGLE, 1 : DUAL, 2 : INCOHERENT')
        ax.plot(positFourches.timestamp, positFourches.consigne, '-+', label='consigne positionneur de fourches')
        ax.legend()
        ax.grid(True)
    except :
        print "No forksPositioner"

    ax1 = plt.subplot(4,1,2,sharex = ax)
    try:
        ax1.plot(positFourches.timestamp, positFourches.enposition, '-+', label='en position')
        ax1.plot(positFourches.timestamp, positFourches.ensecurite, '-+', label='en securite')
        ax1.legend()
        ax1.grid(True)
    except :
        print "No forksPositioner"
                                
    ax2 = plt.subplot(4,1,3,sharex = ax)
    try:
        ax2.plot(positFourches.timestamp, positFourches.e1, '-+', label='parametre e1 (mm)')
        ax2.plot(positFourches.timestamp, positFourches.ce1, '-+', label='consigne e1 (mm)')
        ax2.plot(positFourches.timestamp, positFourches.e1min, label ='e1min')
        ax2.plot(positFourches.timestamp, positFourches.e1max, label ='e1max')
        ax2.legend()
        ax2.grid(True)
    except :
        print "No forksPositioner"

    ax3 = plt.subplot(4,1,4,sharex = ax)
    try:
        ax3.plot(positFourches.timestamp, positFourches.e2, '-+', label='parametre e2 (mm)')
        ax3.plot(positFourches.timestamp, positFourches.ce2, '-+', label='consigne e2 (mm)')
        ax3.plot(positFourches.timestamp, positFourches.e2min, label = 'e2min')
        ax3.plot(positFourches.timestamp, positFourches.e2max, label = 'e2max')
        ax3.legend()
        ax3.grid(True)
    except :
        print "No forksPositioner"

    plt.show()
    

def PlotAuto():
    """
    trace les etats de l'automate du positionneur et certains flags
    """
    plt.figure();

    ax = plt.subplot(3,1,1)
    try:
        ax.plot(autoPositFourches.timestamp, autoPositFourches.state, '-+',label='courant')
        ax.plot(autoPositFourches.timestamp, autoPositFourches.demandestate, '-+', label = 'demande')
        ax.plot(positFourches.timestamp, positFourches.marche, '-+', label = 'marche')
        ax.set_title("0:Init, 1:Single, 2:Dual, 3:MvtVersIntermediaire, 4:MvtExt, 5:MvtSynch, 6:Incoherent, 7: Mode Commande en vitesse")
        ax.legend()
        ax.grid(True)
    except:
        print "no Positioner automate"


    ax1 = plt.subplot(3,1,2, sharex = ax)
    try:
        ax1.plot(autoPositFourches.timestamp, autoPositFourches.notincharge, '-+', label = 'pas en charge')
        ax1.plot(autoPositFourches.timestamp, autoPositFourches.notsingle, '-+', label = 'pas en single')
        ax1.legend()
        ax1.grid(True)
    except:
        print "no Positioner automate"


    ax2 = plt.subplot(3,1,3, sharex = ax)
    try:
        ax2.plot(autoPositFourches.timestamp, autoPositFourches.extauthorized, '-+', label = 'exterieur autorise')
        ax2.plot(autoPositFourches.timestamp, autoPositFourches.synchroauthorized, '-+', label = 'synchro autorisee')
        ax2.legend()
        ax2.grid(True)
    except:
        print "no Positioner automate"


    plt.show()



def PlotPositionneur():
    """
    trace les positions des 4 fourches et le mode du positionneur
    """
    plt.figure();
    ax = plt.subplot(3,1,1)

    try:
        ax.plot(coteFourchesGauche.timestamp, coteFourchesGauche.positionint, '+-', label ='Gauche actuelle int')
        ax.plot(coteFourchesGauche.timestamp, coteFourchesGauche.positionext, '+-', label ='ext')
        ax.plot(coteFourchesDroite.timestamp, -coteFourchesDroite.positionint, '+-', label ='Droite int')
        ax.plot(coteFourchesDroite.timestamp, -coteFourchesDroite.positionext, '+-', label ='ext')
        ax.set_title("Position des fourches")
        ax.legend()
        ax.grid(True)
    except:
        print "no coteFourchesGauche.consint, coteFourchesGauche.consext, coteFourchesDroite.consint, coteFourchesDroite.consext,"
        
    ax1 = plt.subplot(3,1,2,sharex=ax)
    try :
        ax1.plot(coteFourchesGauche.timestamp, coteFourchesGauche.consint, '+-', label='Gauche consigne int')
        ax1.plot(coteFourchesGauche.timestamp, coteFourchesGauche.consext, '+-', label='consigne ext')
        ax1.plot(coteFourchesDroite.timestamp, -coteFourchesDroite.consint, '+-', label='Droite consigne int')
        ax1.plot(coteFourchesDroite.timestamp, -coteFourchesDroite.consext, '+-', label='consigne ext')
        ax1.legend()
        ax1.grid(True)
    except:
        print "no coteFourchesGauche.consint, coteFourchesGauche.consext, coteFourchesDroite.consint, coteFourchesDroite.consext,"

    ax2 = plt.subplot(3,1,3,sharex=ax)
    try:
        ax2.plot(positFourches.timestamp, positFourches.position, '-+', label='mode courant')
        ax2.plot(positFourches.timestamp, positFourches.consigne, '-+', label='mode consigne')
        ax2.set_title("0 : SINGLE, 1 : DUAL, 2 : INCOHERENT")
        ax2.grid(True)
        ax2.legend()
    except:
        print "no positFourches"

    plt.show()


def PlotFourches(coteFourches):
    """
    trace les positions des fourches du cote passe en parametre : positions de chacune des 2 fourches, et parametres e1, e2
    """
    plt.figure();

    ax = plt.subplot(6,1,1)
    try:
        ax.plot(coteFourches.timestamp, coteFourches.positionext, '-+', label = "position fourche exterieure")
        ax.plot(coteFourches.timestamp, coteFourches.consext, '-+')
#        ax.set_title('position fourche Int')
        ax.legend()
        ax.grid(True)
    except:
        print "no field coteFourches.positionint"

    ax1 = plt.subplot(6,1,2,sharex = ax)
    try:
        ax1.plot(coteFourches.timestamp, coteFourches.positionint, '-+', label = "position fourche interieure")
        ax1.plot(coteFourches.timestamp, coteFourches.consint, '-+')
#        ax1.set_title('position fourche Ext')
        ax1.legend()
        ax1.grid(True)
    except:
        print "no field coteFourches.positionext"

    ax2 = plt.subplot(6,1,3,sharex = ax)
    try:
        ax2.plot(coteFourches.timestamp, coteFourches.e1, '-+', label='e1 mesure')
        ax2.plot(coteFourches.timestamp, coteFourches.conse1, '-+', label='e1 consigne')
        ax2.plot(coteFourches.timestamp, coteFourches.e1min,label="e1min")
        ax2.plot(coteFourches.timestamp, coteFourches.e1max, label="e1max")
#        ax2.plot(coteFourches.timestamp, coteFourches.positionext-coteFourches.positionint, '-+', label='diff ext-int+80')
#        ax2.set_title('e1')
        ax2.legend()
        ax2.grid(True)
    except:
        print "no field coteFourches.e1"

    ax3 = plt.subplot(6,1,4, sharex = ax)
    try:
        ax3.plot(coteFourches.timestamp, coteFourches.e2, '-+', label = 'e2 mesure')
        ax3.plot(coteFourches.timestamp, coteFourches.conse2, '-+', label = 'e2 consigne')
        ax3.plot(coteFourches.timestamp, coteFourches.e2min,label="e2min")
        ax3.plot(coteFourches.timestamp, coteFourches.e2max,label ="e2max")
 #       ax3.set_title('e2')
        ax3.legend()
        ax3.grid(True)
    except:
        print "no field coteFourches.e2"

    ax4 = plt.subplot(6,1,5,sharex = ax)
    try:
        ax4.plot(coteFourches.timestamp, coteFourches.mvtext, '+-', label = "exterieur")
        ax4.plot(coteFourches.timestamp, coteFourches.mvtsynchro, '-+', label = "synchro")
        ax4.legend()
 #       ax4.set_title('type de mouvement en cours')
        ax4.grid(True)
    except:
        print "no field mvtExt mvtSynchro"


    ax5 = plt.subplot(6,1,6,sharex = ax)
    try:
        ax5.plot(coteFourches.timestamp, coteFourches.enposition, '+-', label = "en Position")
        ax5.plot(coteFourches.timestamp, coteFourches.ensecurite, '-+', label = "en Securite")
        ax5.legend()
 #       ax4.set_title('type de mouvement en cours')
        ax5.grid(True)
    except:
        print "no field en position en securite"


    plt.show()



matplotlib.pyplot.ion()

try :
    fourcheDroiteExt = Import ("MvtFourcheDroiteExterieur.txt")
    print "fourcheDroiteExt OK"
    fourcheDroiteInt = Import ("MvtFourcheDroiteInterieur.txt")
    print "fourcheDroiteInt OK"
    fourcheGaucheExt = Import ("MvtFourcheGaucheExterieur.txt")
    print "fourcheGaucheExt OK"
    fourcheGaucheInt = Import ("MvtFourcheGaucheInterieur.txt")
    print "fourcheGaucheInt OK"
except :
    print "Pas de mouvements fourches"


try:
    positFourches = Import ("Positionneur.txt")
    print "positionneur OK"
except:
    print "Pas de positionneur"

try:
    coteFourchesDroite = Import("FourchesPositionneurDroite.txt")
    coteFourchesGauche = Import("FourchesPositionneurGauche.txt")
    print "FourchesPositionneur.txt OK"
except:
    print "fichier FourchesPositionneur.txt"



try:
    autoPositFourches = Import("AutoPositionneur.txt")
    print "automate du positionneur OK"
except:
    print "pas de donnees automate du positionneur"


print 'Use PlotAuto pour tracer les etats de l''automate du positionneur et les mouvements interdits'
print 'Use PlotParametres pour tracer les positions mesurees et consigne du positionneur (mode et parametres e1, e2)'
print 'Use PlotPosition pour tracer la position et la consigne laterale de chacune des 4 fourches'
print 'Use PlotPositionneur pour tracer la position du positionneur (4 fourches cotes a cotes), et le mode'
print 'Use PlotFourches(LogPositionneur.coteFourchesDroite) ou PlotFourches(LogPositionneur.coteFourchesGauche) pour tracer la position des fourches et les parametres e1,e2 du cote passe en parametre'



