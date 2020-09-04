#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ctypes
import os
import sys

import matplotlib.mlab
import matplotlib.pyplot as plt
from PyQt4 import QtGui
from PyQt4.QtCore import *
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar

# Utilisation de la lib C ctypes pour creer une structure Union
c_uint8 = ctypes.c_uint8
c_uint16 = ctypes.c_uint16


# Definition de la structure du registre de statut, en commencencant par le bit de poids faible
class Status_bits(ctypes.LittleEndianStructure):
    _fields_ = [
        ("readytoswitchon", c_uint8, 1),
        ("switchedon", c_uint8, 1),
        ("operationenabled", c_uint8, 1),
        ("fault", c_uint8, 1),
        ("voltageenabled", c_uint8, 1),
        ("quickstop", c_uint8, 1),
        ("switchondisabled", c_uint8, 1),
        ("warning", c_uint8, 1),
        ("manufacturerspecific1", c_uint8, 1),
        ("remote", c_uint8, 1),
        ("targetreached", c_uint8, 1),
        ("internallimitactive", c_uint8, 1),
        ("operationmodespecific", c_uint8, 2),
        ("manufacturerspecific2", c_uint8, 2),
    ]

# Definition de la structure en Union pour le registre de Statut
class Status(ctypes.Union):
    _fields_ = [
        ("b", Status_bits),
        ("asbits", c_uint16)
    ]
    _anonymous_ = ("b")


def filterOperationMode(value, validdata):
    """
    fonction de filtrage du reperage, si validata est faux, on retourne NAN
    :param value:
    :param validdata:
    :return:
    """
    if validdata:
        return value
    else:
        return 0


def filterdataswhenProfilePositionMode(datas, operationMode):
    """
    Fonction appliquant un filtre sur la valeur distancereperageodom d'un reperage
    :param reperage:
    :param datasEasyTrackstarted:
    :return:
    """
    datas.operationmodespec = map(filterOperationMode, datas.operationmodespec, operationMode)
    return datas


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
                datas = matplotlib.mlab.csv2rec("tracer/"+filename, delimiter='\t')
                if self.filter:
                    pass
                self.emit(SIGNAL("loaded"), filename, len(datas), datas)
            except:
                self.emit(SIGNAL("fail"))


class Window(QtGui.QDialog):
    """
    This class initialize a QT Window and make computation on tracers
    """

    mvtTim = None
    dunkerTim = []

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.loader = Loader(["MvtMotoTimOutil.txt", "DunkerBG45CI_TimOutil.txt"])

        # a figure instance to plot on
        self.figure1 = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure1)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.button = QtGui.QPushButton('Dunker Tim')
        self.button.clicked.connect(self.plotDunker)

        self.button1 = QtGui.QPushButton('Mvt Tim')
        self.button1.clicked.connect(self.plotmvttim)

        self.button12 = QtGui.QPushButton('Load Data')
        self.button12.clicked.connect(self.loadData)
        self.button12.setEnabled(True)

        self.buttonDunkertimSetEnabled(False)
        self.buttonMvtTimSetEnabled(False)

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
        buttonLayout.addWidget(self.button12)
        layout.addLayout(buttonLayout)
        self.textedit = QtGui.QTextEdit()
        self.textedit.setFixedHeight(150)
        layout.addWidget(self.textedit)
        self.setLayout(layout)

        # optimisation de l'utilisation de la place dans la fenetre pour avoir des courbes les plus grandes possibles
        plt.subplots_adjust(left=0.05, bottom=0.04, right=0.96, top=0.95,  wspace=0.20, hspace=0.22)

        # afficher le nom du repertoire dans le titre de la fenetre
        currentPath = os.getcwd()
        self.setWindowTitle(currentPath)

        # lancer directement le chargement des fichiers
        self.loadData()

    def loadData(self):
        self.loader.read()

    def signalstart(self, filename):
        self.textedit.append("Loading file " + filename)

    def signalloaded(self,filename, nbelement, values):
        self.textedit.append("Loading done for " + filename + "," + str(nbelement) + " elements")

        if filename ==  "MvtMotoTimOutil.txt" :
            self.mvtTim = values
            if self.mvtTim is not None:
                self.buttonMvtTimSetEnabled(True)
            else:
                self.textedit.append('No Movement datas')

        if filename == "DunkerBG45CI_TimOutil.txt":
            self.dunkerTim = values
            if self.dunkerTim is not None:
                self.buttonDunkertimSetEnabled(True)
            else:
                self.textedit.append('No Dunker Datas')

    def signalfail(self):
        self.textedit.append("Echec du chargement du fichier ")

    def buttonDunkertimSetEnabled(self, enabled):
        self.button.setEnabled(enabled)

    def buttonMvtTimSetEnabled(self, enabled):
        self.button1.setEnabled(enabled)

    def buttonLoadSetEnabled(self, enabled):
        self.button12.setEnabled(enabled)
                
    def plotmvttim(self):
        """
        Plot X Y and Theta from MvtTim
        :return:
        """
        # Clear Display
        self.figure1.clf()

        names = list(self.mvtTim.dtype.names)
        print names
        print type(self.mvtTim)

        # create an axis
        ax = self.figure1.add_subplot(411)
        ax1 = self.figure1.add_subplot(412, sharex=ax)
        ax2 = self.figure1.add_subplot(413, sharex=ax)
        ax3 = self.figure1.add_subplot(414, sharex=ax)

        # plot data Number of Lanes
        ax.set_xlabel('Velocity')
        ax.plot(self.mvtTim.timestamp, self.mvtTim.mvtactualposition, color='blue', linestyle='-', label='Mvt Position')
        ax.plot(self.mvtTim.timestamp, self.mvtTim.consposition, color='orange', linestyle='-', label='Cons Position')
        ax.set_ylim([-(self.mvtTim.consposition.min() + 50), self.mvtTim.consposition.max() + 50])
        ax.legend()
        ax.grid(True)

        # plot Init
        ax1.set_xlabel('Initialization')
        ax1.plot(self.mvtTim.timestamp, self.mvtTim.mvtisinit, color='blue', linestyle='-', label='Mvt IsInit')
        ax1.plot(self.mvtTim.timestamp, self.mvtTim.cdesethome, color='orange', linestyle='-', label='Set Home')
        ax1.legend()
        ax1.grid(True)

        ax2.set_xlabel('TimeStamp')
        ax2.plot(self.mvtTim.timestamp, self.mvtTim.motoractualposition, color="blue", linewidth=2.5, linestyle="-", label='Motor Pos')
        ax2.plot(self.mvtTim.timestamp, self.mvtTim.mvtconsposition, color="red", linewidth=2.5, linestyle="-", label='Mvt Cons Pos')
        ax2.plot(self.mvtTim.timestamp, self.mvtTim.mvtactualposition, color="green", linewidth=2.5, linestyle="-", label='Mvt Pos')
        # Affichage d'une limite horizontale
        # ax2.axhspan(-75, -45, facecolor='r', alpha=0.1, label='Filtre')
        # ax2.axhspan(45, 75, facecolor='r', alpha=0.1)
        ax2.legend()
        ax2.set_ylim([-(self.mvtTim.mvtconsposition.min()+50), self.mvtTim.mvtconsposition.max()+50])
        ax2.grid(True)

        ax3.set_xlabel('TimeStamp')
        ax3.plot(self.mvtTim.timestamp, self.mvtTim.cdehalt, color="black", linewidth=2.5, linestyle="-", label='Cde Halt')
        ax3.plot(self.mvtTim.timestamp, self.mvtTim.cdenewpoint, color="green", linewidth=2.5, linestyle="-", label='New Point')
        ax3.plot(self.mvtTim.timestamp, self.mvtTim.targetreached, color="red", linewidth=2.5, linestyle="-", label='targetreached')
        ax3.legend()
        ax3.set_ylim(-2,2)
        ax3.grid(True)

        # refresh canvas
        self.canvas.draw()

    def plotDunker(self):
        """
        Plot Speed, Position and Flags from Dunker
        :return:
        """

        names = list(self.dunkerTim.dtype.names)
        print names

        # Clear display
        self.figure1.clf()
        ax = self.figure1.add_subplot(311)
        ax2 = self.figure1.add_subplot(312, sharex=ax)
        ax3 = self.figure1.add_subplot(313, sharex=ax)
        # ax4 = self.figure1.add_subplot(414, sharex=ax)

        ax.set_xlabel('Velocity')
        # ax.plot(self.dunkerTim.timestamp, self.dunkerTim.consvel, color='blue', linestyle='-', label='ConsVelocity')
        ax.plot(self.dunkerTim.timestamp, self.dunkerTim.actualvel, color='orange', linestyle='-', label='Velocity')
        ax.plot(self.dunkerTim.timestamp, self.dunkerTim.conspos, color='red', linestyle='-', label='ConsPosition')
        ax.plot(self.dunkerTim.timestamp, self.dunkerTim.actualpos, color='green', linestyle='-', label='Position')

        ax2.set_xlabel('Current')
        ax2.plot(self.dunkerTim.timestamp, self.dunkerTim.actualcurrent, color='black', linestyle='-', label='Current')
        # Affichage d'une limite horizontale
        ax2.axhspan(self.dunkerTim.currentlim[0], 15000, facecolor='red', alpha=0.1, label='MaxPosCurrent')
        ax2.axhspan(-self.dunkerTim.currentlim[0], -15000, facecolor='red', alpha=0.1, label='MinPosCurrent')
        ax2.set_ylim([-self.dunkerTim.currentlim[0]-1000, self.dunkerTim.currentlim[0]+1000])

        ax3.set_xlabel('Status')
        ax3.plot(self.dunkerTim.timestamp, self.dunkerTim.readytomove, color='black', linestyle='-',linewidth=2, label='DS402Ready')
        ax3.plot(self.dunkerTim.timestamp, self.dunkerTim.targetreached, color='red', linestyle='-', label='TargetReached')
        # ax3.plot(self.dunkerTim.timestamp, self.dunkerTim.halt, color='green', linestyle='-', label='Halt')
        # self.dunkerTim = filterdataswhenProfilePositionMode(self.dunkerTim, self.dunkerTim.operationmodespec)
        # ax3.plot(self.dunkerTim.timestamp, self.dunkerTim.operationmodespec, color='blue', linestyle='-', label='OperationModeSpec')

        ax.legend()
        ax.grid(True)
        ax2.legend()
        ax2.grid(True)
        ax3.legend()
        ax3.grid(True)

        # refresh canvas
        self.canvas.draw()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main = Window()
    main.show()
    sys.exit(app.exec_())
