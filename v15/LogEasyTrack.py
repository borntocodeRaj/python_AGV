#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import numpy
import Utils
import ctypes

from PyQt4 import QtGui
from PyQt4.QtCore import *
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import matplotlib.mlab
import os

#--- Utilisation de la lib C ctypes pour creer une structure Union
c_uint8 = ctypes.c_uint8
c_uint16 = ctypes.c_uint16

#Definition de la structure du registre de statut, en commencencant par le bit de poids faible
class Status_bits(ctypes.LittleEndianStructure):
    _fields_ = [
        ("err", c_uint8, 1),
        ("np", c_uint8, 1),
        ("wrn", c_uint8, 1),
        ("cc1", c_uint8, 1),
        ("reserved2", c_uint8, 1),
        ("rl", c_uint8, 1),
        ("ll", c_uint8, 1),
        ("nl", c_uint8, 1),
        ("rp", c_uint8, 1),
        ("lc0", c_uint8, 1),
        ("lc1", c_uint8, 1),
        ("tag", c_uint8, 1),
        ("reserved", c_uint8, 4),
    ]

#Definition de la structure en Union pour le registre de Statut
class Status(ctypes.Union):
    _fields_ = [
        ("b", Status_bits),
        ("asbits", c_uint16)
    ]
    _anonymous_ = ("b")

def check_status(log):
    """
    Fonction realisant des controles de coherence sur les donnees brutes issues du PGV
    :param log: ligne en provenance du tracer PGVCan
    :return: Rien si pas de soucis, une chaine sinon
    """
    status = Status()
    status.asbits = log.status

    if not (status.ll and status.rl):
        return "Erreur de configuration de la selection de ligne"

    if not status.lc0 and status.lc1:
        return "2 lignes detectees en Y=%d" % log.axis_y

    if status.lc0 and status.lc1:
        return "2 lignes ou plus detectees en Y=%d" % log.axis_y

    if status.wrn:
        return "Alerte %d detectee en Y=%d"% log.warning

    if status.err:
        return "Erreur %d detectee en Y=%d"% log.axis_x, log.axis_y

    if status.rp:
        return "Ligne reparee detectee en Y=%d"% log.axis_y

    return None



def anglepgvtosigneddegres(angle):
    """
    Retourne la valeur d'un angle entre 0 et 360 sur une echelle de -179 à +180 degres
    :param angle: angle en degres entre 0 et 360
    :return: angle en degres entre -179 et +180
    """
    if 180 < angle <= 360:
        return angle - 360
    else:
        return angle


def filterreperage(value, validdata):
    """
    fonction de filtrage du reperage, si validata est faux, on retourne NAN
    :param value:
    :param validdata:
    :return:
    """
    if validdata:
        return value
    else:
        return numpy.nan

def filterdatasXYTwhenreperageisok(reperage, datasEasyTrackok):
    """
    Fonction appliquant un filtre sur les valeurs X Y et Theta d'un reperage
    :param reperage:
    :param datasEasyTrackok:
    :return:
    """
    reperage.x = map(filterreperage, reperage.x, datasEasyTrackok)
    reperage.y = map(filterreperage, reperage.y, datasEasyTrackok)
    reperage.theta = map(filterreperage, reperage.theta, datasEasyTrackok)
   
    return reperage


def filterdataswhenreperageisok(reperage, datasEasyTrackok):
    """
    Fonction appliquant un filtre sur les valeurs retournee par le reperageEasyTrack
    :param reperage:
    :param datasEasyTrackok:
    :return:
    """
    reperage = filterdatasXYTwhenreperageisok (reperage, datasEasyTrackok)
    reperage.dypgv = map(filterreperage, reperage.dypgv, datasEasyTrackok)
    reperage.xpgvodo = map(filterreperage, reperage.xpgvodo, datasEasyTrackok)
    reperage.ypgvodo = map(filterreperage, reperage.ypgvodo, datasEasyTrackok)
    reperage.thetapgvodo = map(filterreperage, reperage.thetapgvodo, datasEasyTrackok)
    reperage.xpgv = map(filterreperage, reperage.xpgv, datasEasyTrackok)
    reperage.ypgv = map(filterreperage, reperage.ypgv, datasEasyTrackok)

    return reperage

def filterdataswhenreperageisstarted(reperage, datasEasyTrackstarted):
    """
    Fonction appliquant un filtre sur la valeur distancereperageodom d'un reperage
    :param reperage:
    :param datasEasyTrackstarted:
    :return:
    """
    reperage.distancereperageodom = map(filterreperage, reperage.distancereperageodom, datasEasyTrackstarted)
    return reperage

def moduloCentre(angle, centre):
    if angle > centre + numpy.pi :
        return (angle - 2.0*numpy.pi)
    elif angle <= centre -numpy.pi :
        return (angle + 2.0*numpy.pi)
    else :
            return (angle)


class Loader(QThread):
    """
    This class read tracer files send them to local variables
    """
    def __init__(self, files, filter=None, parent=None):
        QThread.__init__(self, parent)
        self.files = files
        self.filter = filter

    def __del__(self):
        self.wait()

    def read(self):
        self.start()

    def run(self):
        for filename in self.files:
            self.emit(SIGNAL("start"), filename)
            try:
                datas = matplotlib.mlab.csv2rec(filename, delimiter='\t')
                if self.filter:
                    pass
                self.emit(SIGNAL("loaded"), filename, len(datas), datas)
            except:
                self.emit(SIGNAL("fail"))


class Window(QtGui.QDialog):
    """
    This class initialize a QT Window and make computation on tracers
    """

    pgvCan = None
    datas = []
    dataTypes = {}
    datasEasyTrack = []
    datasPsinav = []
    datasEasyTrackerreur = []
    datasNav = []
    #modifier en fonction de l'angle du segment observe pour que l'affichage des angles theta se passe bien
    angleCentre = numpy.pi

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.loader = Loader(["PGVCAN.txt", "MultiReperage.txt", "ReperageEasyTrack.txt", "ReperagePsiNav.txt", "NavigationLaser.txt","ReperageEasyTrackRepMeasure.txt"])

        # a figure instance to plot on
        self.figure1 = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure1)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.button = QtGui.QPushButton('PGV x y angle')
        self.button.clicked.connect(self.plotxyangle)

        self.button1 = QtGui.QPushButton('X Y Reperages')
        self.button1.clicked.connect(self.plotxy)

        self.button2 = QtGui.QPushButton('Recalages EasyTrack')
        self.button2.clicked.connect(self.plotRecalages)

        self.button5 = QtGui.QPushButton('X Y Theta Reperages')
        self.button5.clicked.connect(self.plotxyt)

        self.button6 = QtGui.QPushButton('EasyTrackDistanceOdo')
        self.button6.clicked.connect(self.plotEasyTrackDistanceOdo)

        self.button7 = QtGui.QPushButton('dYPgv')
        self.button7.clicked.connect(self.plotEasyTrackdYPgv)

        self.button8 = QtGui.QPushButton('NPXYT')
        self.button8.clicked.connect(self.plotEasyTrackNPXYT)

        self.button9 = QtGui.QPushButton('PgvXY')
        self.button9.clicked.connect(self.plotEasyTrackPgvXYT)

        self.button10 = QtGui.QPushButton('EasyTrackErreur')
        self.button10.clicked.connect(self.plotEasyTrackErreurMeasure)

        self.button11 = QtGui.QPushButton('NavPlotT')
        self.button11.clicked.connect(self.NavPlotT)

        self.button12 = QtGui.QPushButton('Load Data')
        self.button12.clicked.connect(self.loadData)
        self.button12.setEnabled(True)

        self.button13 = QtGui.QPushButton('DeltaNP')
        self.button13.clicked.connect(self.plotDeltaNP)
        self.button13.setEnabled(True)
        
        self.button14 = QtGui.QPushButton('Flags')
        self.button14.clicked.connect(self.plotFlags)
        self.button14.setEnabled(True)
       

        self.buttonPGVSetEnabled(False)
        self.buttonReperageSetEnabled(False)
        self.buttonReperageErrorSetEnabled(False)
        self.buttonNavigationSetEnabled(False)

        self.connect(self.loader, SIGNAL("loaded"), self.signalloaded)
        self.connect(self.loader, SIGNAL("start"), self.signalstart)
        self.connect(self.loader, SIGNAL("fail"), self.signalfail)

        # set the layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addWidget(self.button)
        buttonLayout.addWidget(self.button1)
        buttonLayout.addWidget(self.button2)
        buttonLayout.addWidget(self.button5)
        buttonLayout.addWidget(self.button6)
        buttonLayout.addWidget(self.button7)
        buttonLayout.addWidget(self.button8)
        buttonLayout.addWidget(self.button9)
        buttonLayout.addWidget(self.button10)
        buttonLayout.addWidget(self.button11)
        buttonLayout.addWidget(self.button12)
        buttonLayout.addWidget(self.button13)
        buttonLayout.addWidget(self.button14)
        layout.addLayout(buttonLayout)
        self.textedit = QtGui.QTextEdit()
        self.textedit.setFixedHeight(150)
        layout.addWidget(self.textedit)
        self.setLayout(layout)

        #optimisation de l'utilisation de la place dans la fenetre pour avoir des courbes les plus grandes possibles
        plt.subplots_adjust(left=0.05, bottom=0.04, right=0.96, top=0.95,  wspace=0.20, hspace=0.22)

        #afficher le nom du repertoire dans le titre de la fenetre
        currentPath = os.getcwd()
        self.setWindowTitle(currentPath)

        #lancer directement le chargement des fichiers
        self.loadData()



    def loadData(self):
        self.loader.read()

    def signalstart(self, filename):
        self.textedit.append("Loading file " + filename)

    def signalloaded(self,filename, nbelement, values):
        self.textedit.append("Loading done for " + filename + "," + str(nbelement) + " elements")

        if filename ==  "PGVCAN.txt" :
            self.pgvCan=values
            if self.pgvCan is not None:
                for elt in self.pgvCan:
                    msg = check_status(elt)
                    if  msg is not None:
                        # save
                        fw = self.textedit.fontWeight()
                        tc = self.textedit.textColor()
                        # append
                        self.textedit.setFontWeight(QtGui.QFont.DemiBold)
                        self.textedit.setTextColor(QtGui.QColor("red"))
                        self.textedit.append(msg)
                        # restore
                        self.textedit.setFontWeight(fw)
                        self.textedit.setTextColor(tc)
                self.buttonPGVSetEnabled(True)
            else:
                self.textedit.append('No PGV CAN datas')

        if filename == "MultiReperage.txt":
            self.datas = values
            
            #modulo centre pour gerer le cas où angle est de +-180deg
            self.datas.theta = [moduloCentre(angle, self.angleCentre) for angle in self.datas.theta ];

        if filename == "ReperageEasyTrack.txt":
            self.datasEasyTrack = values
            if self.datasEasyTrack is not None:
                # on met a nan les donnees ou le reperage n est pas OK
                self.dataTypes["easytrack"] = filterdataswhenreperageisok(self.datasEasyTrack, self.datasEasyTrack.ok)
                self.dataTypes["easytrack"] = filterdataswhenreperageisstarted(self.datasEasyTrack, self.datasEasyTrack.reperagedemarre)

                #modulo centre pour gerer le cas où angle est de +-180deg
                self.dataTypes["easytrack"].theta = [moduloCentre(angle, self.angleCentre) for angle in self.dataTypes["easytrack"].theta];
                self.dataTypes["easytrack"].thetaodo = [moduloCentre(angle, self.angleCentre) for angle in self.dataTypes["easytrack"].thetaodo ];
                self.dataTypes["easytrack"].thetapgvodo = [moduloCentre(angle, self.angleCentre) for angle in self.dataTypes["easytrack"].thetapgvodo ];
            else:
                self.textedit.append('No PGV Datas')

        if filename == "ReperagePsiNav.txt":
            self.datasPsinav = values
            if self.datasPsinav is not None:
                
                #modulo centre pour gerer le cas ou angle est de +-180deg
                self.datasPsinav.theta = [moduloCentre(angle, self.angleCentre) for angle in self.datasPsinav.theta ];
                self.dataTypes["psinav"] = self.datasPsinav               
                
            else:
                self.textedit.append('No PsiNav Datas')

        self.buttonReperageSetEnabled(True)
        
        if filename == "ReperageEasyTrackRepMeasure.txt":
            self.datasEasyTrackerreur = values
            
            if self.datasEasyTrackerreur is not None:
                
                # modulo centre pour gerer le cas où angle est de +-180 degres                    
                self.datasEasyTrackerreur.theta = [moduloCentre(angle, self.angleCentre) for angle in self.datasEasyTrackerreur.theta ];
                self.datasEasyTrackerreur.thetapsinav = [moduloCentre(angle, self.angleCentre) for angle in self.datasEasyTrackerreur.thetapsinav]
                self.datasEasyTrackerreur.pgvtheta = [moduloCentre(angle, self.angleCentre) for angle in self.datasEasyTrackerreur.pgvtheta]
                
                if self.datasEasyTrackerreur.dtype.fields.has_key("ok"):  
                    # on met a nan les donnees ou le reperage n est pas OK
                    self.dataTypes["EasyTrackerreur"]= filterdatasXYTwhenreperageisok(self.datasEasyTrackerreur, self.datasEasyTrackerreur.ok)        

                else :
                    self.dataTypes["EasyTrackerreur"] = self.datasEasyTrackerreur                       
                
            else:
                self.textedit.append('No ReperageEasyTrackRepMeasure Datas')
    
            self.buttonReperageErrorSetEnabled(True)

        
        if filename == "NavigationLaser.txt":
            self.dataNav = values            
            if self.dataNav is not None:
                self.dataTypes["Nav"] = values    
                self.buttonNavigationSetEnabled(True)       

            else:
                self.textedit.append('No NavigationLaser Datas')

        self.buttonLoadSetEnabled(False)    


    def signalfail(self):
        self.textedit.append("Echec du chargement du fichier ")

    def buttonPGVSetEnabled(self, enabled):
        self.button.setEnabled(enabled)

    def buttonReperageErrorSetEnabled(self, enabled):
        self.button10.setEnabled(enabled)
    
    def buttonReperageSetEnabled(self, enabled):
        self.button1.setEnabled(enabled)
        self.button2.setEnabled(enabled)
        self.button5.setEnabled(enabled)
        self.button6.setEnabled(enabled)
        self.button7.setEnabled(enabled)
        self.button8.setEnabled(enabled)
        self.button9.setEnabled(enabled)
        self.button13.setEnabled(enabled)
        self.button14.setEnabled(enabled)

    def buttonNavigationSetEnabled(self, enabled):
        self.button11.setEnabled(enabled)

    def buttonLoadSetEnabled(self, enabled):
        self.button12.setEnabled(enabled)

    def plotDeltaNP(self):
        """
        Plot deltaNP   
        :return:
        """

        #Clear display
        self.figure1.clf()

        ax1 = plt.subplot(311)
        ax2 = plt.subplot(312, sharex=ax1)
        ax3 = plt.subplot(313, sharex=ax1)

        if self.dataTypes.has_key("easytrack"):
            datasEasyTrack = self.dataTypes["easytrack"]
            if self.datasEasyTrack.dtype.fields.has_key("dx"):
            	ax1.plot(datasEasyTrack.timestamp, datasEasyTrack.dx, marker='+', label='deltaNP x')
            	ax2.plot(datasEasyTrack.timestamp, datasEasyTrack.dy, marker='+', label='deltaNP y')
           	ax3.plot(datasEasyTrack.timestamp, datasEasyTrack.dth, marker='+', label='deltaNP theta')
	        ax1.legend()
	        ax1.grid(True)
	        ax2.legend()
	        ax2.grid(True)
	        ax3.legend()
	        ax3.grid(True)
    
    
        # refresh canvas
        self.canvas.draw()
    
    
    def plotFlags(self):
        """
        Plot flags   
        :return:
        """

        #Clear display
        self.figure1.clf()

        ax1 = plt.subplot(511)
        ax2 = plt.subplot(512, sharex=ax1)
        ax3 = plt.subplot(513, sharex=ax1)
        ax4 = plt.subplot(514, sharex=ax1)
        ax5 = plt.subplot(515, sharex=ax1)

        if self.dataTypes.has_key("easytrack"):
            datasEasyTrack = self.dataTypes["easytrack"]
            if self.datasEasyTrack.dtype.fields.has_key("segmd"):
                ax1.plot(datasEasyTrack.timestamp, datasEasyTrack.segmd, marker='+', label='segment droit')
	        ax1.legend()
		ax1.grid(True)
        
	    if self.datasEasyTrack.dtype.fields.has_key("inter"):
                ax1.plot(datasEasyTrack.timestamp, datasEasyTrack.inter,  label='intersection')
                ax1.legend()
		ax1.grid(True)    
        
	    if self.datasEasyTrack.dtype.fields.has_key("detectok"):
                ax2.plot(datasEasyTrack.timestamp, datasEasyTrack.detectok, marker='+', label='PGV OK')
	        ax2.legend()
	        ax2.grid(True)
        
            if self.datasEasyTrack.dtype.fields.has_key("ok"):
                ax3.plot(datasEasyTrack.timestamp, datasEasyTrack.ok, marker='+', label='EasyTrack OK')
	        ax3.legend()
		ax3.grid(True)
        
            if self.datasEasyTrack.dtype.fields.has_key("reperagedemarre"):
                ax4.plot(datasEasyTrack.timestamp, datasEasyTrack.reperagedemarre, marker='+', label='demarre')
    		ax4.grid(True)
		ax4.legend()
        
	    if self.datasEasyTrack.dtype.fields.has_key("pgvparalleley"):
                ax5.plot(datasEasyTrack.timestamp, datasEasyTrack.pgvparalleley, marker='+', label='PGV parallele axe Y')
                ax5.grid(True)
                ax5.legend()
	
	    if self.datasEasyTrack.dtype.fields.has_key("segmentparalleley"):
                ax5.plot(datasEasyTrack.timestamp, datasEasyTrack.segmentparalleley, marker='+', label='segment parallele axe Y')
                ax5.grid(True)
                ax5.legend()

               
        # refresh canvas
        self.canvas.draw()
                
    def plotxyangle(self):
        """
        Plot X Y and Theta from PGVCAN
        :return:
        """
        # Clear Display
        self.figure1.clf()

        # create an axis
        ax = self.figure1.add_subplot(311)
        ax2 = self.figure1.add_subplot(312, sharex=ax)
        ax3 = self.figure1.add_subplot(313, sharex=ax)

        # plot data Number of Lanes
        ax.set_xlabel('TimeStamp')
        ax.plot(self.pgvCan.timestamp, self.pgvCan.numberoflane, '-+', label='NumberOfLane')
        ax.legend()
        ax.set_ylim([0, 3])
        ax.grid(True)

        # plot data X, Y theta from PGV
        ax2.set_xlabel('TimeStamp')
        ax2.plot(self.pgvCan.timestamp, self.pgvCan.axis_y, '-+b', label='Axis_Y')
        ax2.plot(self.pgvCan.timestamp, self.pgvCan.axis_x, '-+r', label='Axis_X')
        # ab.axhspan(-75, -45, facecolor='r', alpha=0.1, label='Filtre')
        # ab.axhspan(45, 75, facecolor='r', alpha=0.1)
        ax2.legend()
        ax2.set_ylim([-75, 75])
        ax2.grid(True)

        ax3.set_xlabel('TimeStamp')
        ax3.plot(self.pgvCan.timestamp, map(anglepgvtosigneddegres, self.pgvCan.angledegrees), '-+g', label='Angle (degres)')
        ax3.legend()
        ax3.grid(True)

        # refresh canvas
        self.canvas.draw()



    def plotxy(self):
        """
        Plot X and Y from ReperagePGV and ReperagePsiNav
        :return:
        """
        #Clear display
        self.figure1.clf()
        ax = self.figure1.add_subplot(111)
        # adds 160 time markers
        N = 160
        for i in range(0, N):
            j = i * (len(self.datas.x) / N)
            x = self.datas.x[j]
            y = self.datas.y[j]
            ax.annotate("t=" + str(self.datas.timestamp[j]), [x, y], color='blue')
            '''
            if j+1 < len(datas.x):
                dx=datas.x[j+1]-datas.x[j]
                dy=datas.y[j+1]-datas.y[j]
                ax.quiver(x,y, dx, dy, width=0.01, angles='xy', scale_units='xy', scale= 1000, color='blue')
                print j
            '''
        ax.plot(self.datas.x, self.datas.y, marker='+', label='Multi reperage')

        if self.dataTypes.has_key("easytrack"):
            datasEasyTrack = self.dataTypes["easytrack"]
            ax.plot(datasEasyTrack.x, datasEasyTrack.y, marker='+', label='Reperage EasyTrack')

        if self.dataTypes.has_key("psinav"):
            datasPsinav = self.dataTypes["psinav"]
            ax.plot(datasPsinav.x, datasPsinav.y, marker='+', label='Reperage Psinav')

        ax.legend()
        ax.grid(True)
        # refresh canvas
        self.canvas.draw()

    
    
    def plotRecalages(self):
        """
        Plot recalage informations from reperage EasyTrack
        :return:
        """
        #Clear display
        self.figure1.clf()

        #plt.figure()
        ax1 = self.figure1.add_subplot(311)
        ax2 = plt.subplot(312, sharex=ax1)
        ax3 = plt.subplot(313, sharex=ax1)

        ax1.plot(self.datas.timestamp, numpy.rad2deg(self.datas.theta), marker ='+', label='Multi reperage')
        
        if self.dataTypes.has_key("psinav"):
            self.datasPsinav = self.dataTypes["psinav"]
            ax1.plot(self.datasPsinav.timestamp, numpy.rad2deg(self.datasPsinav.theta), marker ='+', label='Reperage Psinav')
            ax2.plot(self.datasPsinav.timestamp, self.datasPsinav.ok, '+-', label='Reperage Psinav OK')

        if self.dataTypes.has_key("easytrack"):
            self.datasEasyTrack = self.dataTypes["easytrack"]
            ax1.plot(self.datasEasyTrack.timestamp, numpy.rad2deg(self.datasEasyTrack.theta), marker='+', label='Reperage Pgv')


            ax2.plot(self.datasEasyTrack.timestamp, self.datasEasyTrack.ok, marker='+', label='Reperage EasyTrack OK')
            if self.datasEasyTrack.dtype.fields.has_key("reperagedemarre"):  
                ax2.plot(self.datasEasyTrack.timestamp, self.datasEasyTrack.reperagedemarre, marker='+', label='EasyTrack demarre')
            if self.datasEasyTrack.dtype.fields.has_key("thetaestimeok"):  
                ax2.plot(self.datasEasyTrack.timestamp, self.datasEasyTrack.thetaestimeok, marker='+', label='thetaestimeok')
            
            if self.datasEasyTrack.dtype.fields.has_key("dypgv"): 
                ax3.plot(self.datasEasyTrack.timestamp, self.datasEasyTrack.dypgv, marker='+', label='dypgv centre (mm)')
            if self.datasEasyTrack.dtype.fields.has_key("dyrecal"):
                ax3.plot(self.datasEasyTrack.timestamp, self.datasEasyTrack.dyrecal, marker='+', label='recalage y (mm)')
            if self.datasEasyTrack.dtype.fields.has_key("dthetarecal"):
                ax3.plot(self.datasEasyTrack.timestamp, 10*numpy.rad2deg(self.datasEasyTrack.dthetarecal), marker='+', label='10* recalage theta (deg)')


        Utils.FormatAxe(ax1, "theta", "t(s)", "deg")
        ax1.legend()
        ax1.grid(True)

        ax2.legend()
        ax2.grid(True)

        ax3.legend()
        ax3.grid(True)

        # refresh canvas
        self.canvas.draw()

       
    def plotxyt(self):
        """
        Plot X, Y Theta values from Multireperage, EasyTrack and PsiNAv
        :return:
        """
        #Clear display
        self.figure1.clf()

        ax1 = plt.subplot(311)
        ax2 = plt.subplot(312, sharex=ax1)
        ax3 = plt.subplot(313, sharex=ax1)

        ax1.plot(self.datas.timestamp, self.datas.x, label='Multi reperage')
        if self.dataTypes.has_key("easytrack"):
            datasEasyTrack = self.dataTypes["easytrack"]
            ax1.plot(datasEasyTrack.timestamp, datasEasyTrack.x, marker='+', label='Reperage EasyTrack')

        if self.dataTypes.has_key("psinav"):
            datasPsinav = self.dataTypes["psinav"]
            ax1.plot(datasPsinav.timestamp, datasPsinav.x, '--', label='Reperage Psinav')

        ax2.plot(self.datas.timestamp, self.datas.y, label='Multi reperage')
        if self.dataTypes.has_key("easytrack"):
            datasEasyTrack = self.dataTypes["easytrack"]
            ax2.plot(datasEasyTrack.timestamp, datasEasyTrack.y, marker='+', label='Reperage EasyTrack')

        if self.dataTypes.has_key("psinav"):
            datasPsinav = self.dataTypes["psinav"]
            ax2.plot(datasPsinav.timestamp, datasPsinav.y, '--', label='Reperage Psinav')


        ax3.plot(self.datas.timestamp, numpy.rad2deg(self.datas.theta), label='Multi reperage')
        if self.dataTypes.has_key("easytrack"):
            datasEasyTrack = self.dataTypes["easytrack"]
            ax3.plot(datasEasyTrack.timestamp, numpy.rad2deg(datasEasyTrack.theta), marker='+', label='Reperage EasyTrack')

        if self.dataTypes.has_key("psinav"):
            datasPsinav = self.dataTypes["psinav"]
            ax3.plot(datasPsinav.timestamp, numpy.rad2deg(datasPsinav.theta), '--', label='Reperage Psinav')


        Utils.FormatAxe(ax1, "X", "t(s)", "mm")
        Utils.FormatAxe(ax2, "Y", "t(s)", "mm")
        Utils.FormatAxe(ax3, "Theta", "t(s)", "deg")
        ax1.legend()
        ax1.grid(True)
        ax2.legend()
        ax2.grid(True)
        ax3.legend()
        ax3.grid(True)
        # refresh canvas
        self.canvas.draw()

    
    
    def plotEasyTrackDistanceOdo(self):
        """
        Plot Distance Parcourue en odometrie par le reperage EasyTrack, and OK, demarre, dY 
        :return:
        """
        # Clear display
        self.figure1.clf()
        

        ax1 = plt.subplot(3, 1, 1)
        ax2 = plt.subplot(3, 1, 2, sharex=ax1)
        ax3 = plt.subplot(3, 1, 3, sharex=ax1)

        datasEasyTrack = self.dataTypes["easytrack"]
        ax1.plot(datasEasyTrack.timestamp, datasEasyTrack.distancereperageodom, marker='+', label='Reperage EasyTrack distancereperageodom')
        ax2.plot(datasEasyTrack.timestamp, datasEasyTrack.ok, marker='+', label='Reperage EasyTrack OK')
        ax2.plot(datasEasyTrack.timestamp, datasEasyTrack.reperagedemarre, marker='+', label='Reperage EasyTrack demarre')
        ax3.plot(datasEasyTrack.timestamp, datasEasyTrack.dypgv, marker='+', label='Reperage EasyTrack dypgv centre')

        if self.dataTypes.has_key("psinav"):
            datasPsinav = self.dataTypes["psinav"]
            ax2.plot(datasPsinav.timestamp, datasPsinav.ok, '--', label='Reperage Psinav OK')

        Utils.FormatAxe(ax1, "distancereperageodom", "t(s)", "mm")
        Utils.FormatAxe(ax2, "OK", "t(s)", "bool")
        Utils.FormatAxe(ax3, "dypgv", "t(s)", "mm")

        ax1.legend()
        ax1.grid(True)
        ax2.legend()
        ax2.grid(True)
        ax3.legend()
        ax3.grid(True)
        # refresh canvas
        self.canvas.draw()

    
    
    def plotEasyTrackNPXYT(self):
        """
        Plot X, Y, Theta of Navigation Point frame, computed by Easytrack reperage  
        :return:
        """
        self.figure1.clf()
        ax1 = plt.subplot(3, 1, 1)
        ax2 = plt.subplot(3, 1, 2, sharex=ax1)
        ax3 = plt.subplot(3, 1, 3, sharex=ax1)

        datasEasyTrack = self.dataTypes["easytrack"]
        ax1.plot(datasEasyTrack.timestamp, datasEasyTrack.x, '-+', label='X NP final')
        ax1.plot(datasEasyTrack.timestamp, datasEasyTrack.xodo, '--', label='x NP odo')

        ax2.plot(datasEasyTrack.timestamp, datasEasyTrack.y, '-+', label='Y NP final')
        ax2.plot(datasEasyTrack.timestamp, datasEasyTrack.yodo, '--', label='Y NP odo')

        ax3.plot(datasEasyTrack.timestamp, numpy.rad2deg(datasEasyTrack.theta), '-+', label='Theta NP final')
        ax3.plot(datasEasyTrack.timestamp, numpy.rad2deg(datasEasyTrack.thetaodo), '--', label='Theta NP odo')

        Utils.FormatAxe(ax1, "X", "t(s)", "mm")
        Utils.FormatAxe(ax2, "Y", "t(s)", "mm")
        Utils.FormatAxe(ax3, "Theta", "t(s)", "deg")
        ax1.legend()
        ax1.grid(True)
        ax2.legend()
        ax2.grid(True)
        ax3.legend()
        ax3.grid(True)
        # refresh canvas
        self.canvas.draw()

    
    
    def plotEasyTrackPgvXYT(self):
        """
        Plot X, Y, Theta of PGV frame, computed by Easytrack reperage  
        :return:
        """
        self.figure1.clf()
        ax1 = plt.subplot(2, 1, 1)
        ax2 = plt.subplot(2, 1, 2, sharex=ax1)

        datasEasyTrack = self.dataTypes["easytrack"]
        ax1.plot(datasEasyTrack.timestamp, datasEasyTrack.xpgv, '+-', label='X Pgv final')
        ax1.plot(datasEasyTrack.timestamp, datasEasyTrack.xpgvodo, '--', label='x Pgv odo')

        ax2.plot(datasEasyTrack.timestamp, datasEasyTrack.ypgv, '-+', label='Y Pgv final')
        ax2.plot(datasEasyTrack.timestamp, datasEasyTrack.ypgvodo, '--', label='Y Pgv odo')


        Utils.FormatAxe(ax1, "X", "t(s)", "mm")
        Utils.FormatAxe(ax2, "Y", "t(s)", "mm")
        
        ax1.legend()
        ax1.grid(True)
        ax2.legend()
        ax2.grid(True)
        # refresh canvas
        self.canvas.draw()



    def plotEasyTrackdYPgv(self):
        """
        Plot dYcentre (=dYpgv-Yoffset (calibration) 
        :return:
        """
        self.figure1.clf()
        ax1 = plt.subplot(2, 1, 1)
        ax2 = plt.subplot(2, 1, 2, sharex=ax1)

        datasEasyTrack = self.dataTypes["easytrack"]
        ax1.plot(datasEasyTrack.timestamp, datasEasyTrack.dypgv, marker='+', label='Reperage EasyTrack dypgv centre')


        ax2.plot(datasEasyTrack.timestamp, datasEasyTrack.ok, marker='+', label='Reperage EasyTrack OK')
        ax2.plot(datasEasyTrack.timestamp, datasEasyTrack.reperagedemarre, marker='+', label='Reperage EasyTrack demarre')
        if self.dataTypes.has_key("psinav"):
            datasPsinav = self.dataTypes["psinav"]
            ax2.plot(datasPsinav.timestamp, datasPsinav.ok, '--', label='Reperage Psinav OK')


        Utils.FormatAxe(ax1, "dYPGVcentre", "t(s)", "mm")
        Utils.FormatAxe(ax2, "OK", "t(s)", "")
        ax1.legend()
        ax1.grid(True)
        ax2.legend()
        ax2.grid(True)
        # refresh canvas
        self.canvas.draw()



    def plotEasyTrackErreurMeasure(self):
        """
        Plot X, Y, Theta errors : psiNav - EasyTrack 
        :return:
        """
        if self.dataTypes.has_key("EasyTrackerreur"):
            datasEasyTrackrepMeasure =  self.dataTypes["EasyTrackerreur"]

            datasEasyTrackrepMeasure.datasEasyTrackrepMeasureerreurX =  datasEasyTrackrepMeasure.xpsinav- datasEasyTrackrepMeasure.x
            datasEasyTrackrepMeasure.datasEasyTrackrepMeasureerreurY =  datasEasyTrackrepMeasure.ypsinav- datasEasyTrackrepMeasure.y
            datasEasyTrackrepMeasure.datasEasyTrackrepMeasureerreurTheta = numpy.rad2deg(datasEasyTrackrepMeasure.thetapsinav- datasEasyTrackrepMeasure.theta)
            
            self.figure1.clf()
            ax1 = plt.subplot(3,1,1)
            ax2 = plt.subplot(3,1,2, sharex=ax1)
            ax3 = plt.subplot(3,1,3, sharex=ax1)
            
    
            ax1.plot(datasEasyTrackrepMeasure.timestamp,  datasEasyTrackrepMeasure.datasEasyTrackrepMeasureerreurX, marker='+', label='erreur Psinav - easyTrack')
            ax2.plot(datasEasyTrackrepMeasure.timestamp,  datasEasyTrackrepMeasure.datasEasyTrackrepMeasureerreurY, marker='+', label='erreur Psinav - easyTrack')
            ax3.plot(datasEasyTrackrepMeasure.timestamp,  datasEasyTrackrepMeasure.datasEasyTrackrepMeasureerreurTheta, marker='+', label='erreur Psinav - easyTrack')
             
            datasEasyTrack = self.dataTypes["easytrack"]
            ax3.plot(datasEasyTrack.timestamp, datasEasyTrack.ok, marker='+', label='Reperage EasyTrack OK')
            ax3.plot(datasEasyTrack.timestamp, datasEasyTrack.reperagedemarre, marker='+', label='Reperage EasyTrack demarre')
            
            if self.dataTypes.has_key("psinav"):
                datasPsinav = self.dataTypes["psinav"]
                ax3.plot(datasPsinav.timestamp, datasPsinav.ok, '--', label='Reperage Psinav OK')
    
      
            Utils.FormatAxe(ax1, "erreur X", "t(s)", "mm")
            Utils.FormatAxe(ax2, "erreur Y", "t(s)", "mm")
            Utils.FormatAxe(ax3, "erreur theta", "t(s)", "deg")
            
            self.canvas.draw()
        else:
            print("no EasyTrackerreur data available")



    def NavPlotT(self):
        """
        Plot copy from PlotNavigation 
        :return:
        """
#,  plotDerive= False):
        self.figure1.clf()
        #plt.figure()
        ax1 = plt.subplot(3,1,1)

        datasNav = self.dataTypes["Nav"]

        ax1.plot(datasNav.timestamp, datasNav.phiavcons, label="PhiAvCons")
        ax1.plot(datasNav.timestamp, datasNav.phiav,     label="PhiAv")
        ax1.plot(datasNav.timestamp, datasNav.phiarcons, label="PhiArCons")
        ax1.plot(datasNav.timestamp, datasNav.phiar,     label="PhiAr")
        ax1.plot(datasNav.timestamp, datasNav.theta,     label="Theta")
        
#        if plotDerive==True:
#            dt=datasNav.timestamp[1]-datasNav.timestamp[0]
#            dphiAvdt=numpy.multiply(datasNav.phiav[1:-1]-datasNav.phiav[0:-2],1.0/dt)
#            dphiArdt=numpy.multiply(datasNav.phiar[1:-1]-datasNav.phiar[0:-2],1.0/dt)
#            ax1.plot(datasNav.timestamp[0:-2], dphiAvdt, label="dPhiAv/dt")
#            ax1.plot(datasNav.timestamp[0:-2], dphiArdt, label="dPhiAr/dt")
#    
        ax1.legend()
        ax1.grid(True)
        
        ax2 = plt.subplot(3,1,2, sharex=ax1)
    
        
        ax2.plot(datasNav.timestamp, datasNav.s,       label="s",       linewidth=2)
        ax2.plot(datasNav.timestamp, datasNav.d_1,     label="d-",      linewidth=3)
        ax2.plot(datasNav.timestamp, datasNav.vavcons, label="VavCons", linewidth=2)
        ax2.plot(datasNav.timestamp, datasNav.vav,     label="Vav",     linewidth=3)
        ax2.plot(datasNav.timestamp, datasNav.varcons, label="VarCons", linewidth=2)
        ax2.plot(datasNav.timestamp, datasNav['var'],  label="Var",     linewidth=3)
    
        ax2.legend()
        ax2.grid(True)
    
               
        ax3 = plt.subplot(3,1,3, sharex=ax1)
        ax3.plot(datasNav.timestamp, datasNav.dy, '-+', label="dy")
        ax3.plot(datasNav.timestamp,  [ 100.0*data.dtheta for data in datasNav], '-+', label="dtheta*100")
        ax3.plot(datasNav.timestamp, datasNav.dyav, '-+', label="dyav")
    
        ax3.legend()
        ax3.grid(True)  


        self.canvas.draw()


#    def NavPlotT(plotDerive=False):
#        self.figure1.clf()
#        #plt.figure()
#        ax1 = plt.subplot(3,1,1)
#
#        datasNav = self.dataTypes["Navplot"]
#
#        ax1.plot(datasNav.timestamp, datasNav.phiavcons, label="PhiAvCons")
#        ax1.plot(datasNav.timestamp, datasNav.phiav,     label="PhiAv")
#        ax1.plot(datasNav.timestamp, datasNav.phiarcons, label="PhiArCons")
#        ax1.plot(datasNav.timestamp, datasNav.phiar,     label="PhiAr")
#        ax1.plot(datasNav.timestamp, datasNav.theta,     label="Theta")
#        
#        if plotDerive==True:
#            dt=datasNav.timestamp[1]-datasNav.timestamp[0]
#            dphiAvdt=numpy.multiply(datasNav.phiav[1:-1]-datasNav.phiav[0:-2],1.0/dt)
#            dphiArdt=numpy.multiply(datasNav.phiar[1:-1]-datasNav.phiar[0:-2],1.0/dt)
#            ax1.plot(datasNav.timestamp[0:-2], dphiAvdt, label="dPhiAv/dt")
#            ax1.plot(datasNav.timestamp[0:-2], dphiArdt, label="dPhiAr/dt")
#    
#        ax1.legend()
#        ax1.grid(True)
#        
#        ax2 = plt.subplot(3,1,2, sharex=ax1)
#    
#        
#        ax2.plot(datasNav.timestamp, datasNav.s,       label="s",       linewidth=2)
#        ax2.plot(datasNav.timestamp, datasNav.d_1,     label="d-",      linewidth=3)
#        ax2.plot(datasNav.timestamp, datasNav.vavcons, label="VavCons", linewidth=2)
#        ax2.plot(datasNav.timestamp, datasNav.vav,     label="Vav",     linewidth=3)
#        ax2.plot(datasNav.timestamp, datasNav.varcons, label="VarCons", linewidth=2)
#        ax2.plot(datasNav.timestamp, self.datasNav['var'],  label="Var",     linewidth=3)
#    
#        ax2.legend()
#        ax2.grid(True)
#    
#               
#        ax3 = plt.subplot(3,1,3, sharex=ax1)
#        ax3.plot(datasNav.timestamp, datasNav.dy, '-+', label="dy")
#        ax3.plot(datasNav.timestamp, [ 100.0*self.data.dtheta for data in self.datas], '-+', label="dtheta*100")
#        ax3.plot(datasNav.timestamp, datasNav.dyav, '-+', label="dyav")
#    
#        ax3.legend()
#        ax3.grid(True)    

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())
