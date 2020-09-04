#!/usr/bin/python

from __future__ import unicode_literals
import sys
import os
import getopt
from time import sleep
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import reflector_ctrl

from baQtTools import PlayThread

import random
import operator

from matplotlib.backends import qt4_compat
from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtGui import QSizePolicy, QMainWindow, QApplication, QFont, QFileDialog, QMessageBox, QDialog
from PyQt4.QtCore import QAbstractTableModel, Qt, QVariant, SIGNAL, QThread


from numpy import arange, sin, pi
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from numpy import arange, sin, pi

from reflector_ihm_ui import Ui_MainWindow

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar

import time

###################################################################################################
class ScanCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        self.axes1 = fig.add_subplot(111, xlim=[-100, 2000], ylim=[-250, 250])
        self.axes1.grid(True)
        self.axes1.hold(True)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

###################################################################################################
class Editor(QMainWindow):

###################################################################################################
    def __init__(self, inputFile):
        super(Editor, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.__scanCanvas = ScanCanvas(self.ui.centralwidget, width=5, height=4, dpi=100)
        self.ui.gridLayout_Graph.addWidget(self.__scanCanvas)
        
        mpl_toolbar1 = NavigationToolbar(self.__scanCanvas, self.ui.centralwidget)
        self.ui.gridLayout_Graph.addWidget(mpl_toolbar1)

        self.initConnect()
        self.__seuil = 0
        self.__coeffFilter = 0
        self.__dynamicBinarize = 0

        self.__displayManager = reflector_ctrl.displayManager()

        self.__displayManager.setGraphAxes(self.__scanCanvas.axes1)

        self.__file = inputFile
        self.__forceStopPlay = False

        self.__playThread = PlayThread()
        self.__playThread.doWork = self.OnStepUpChange

        self.show()
        if self.__file != "":
            self.__loadFile()
            self.__draw()
            self.__updateStatusBar("Fichier : " + self.__file)

###################################################################################################
    def __loadFile(self):
        self.__displayManager.loadFile(self.__file)
        nbScanReaded = self.__displayManager.getNbScan()
        currentScan  = self.__displayManager.getCurrentScanIndex()
        self.__setScanSliderRange(0, nbScanReaded-1)
        self.__updateScanSlider(currentScan)
        self.__setScanLabel(currentScan, nbScanReaded-1)
        self.__seuil = 0
        self.__coeffFilter = 0
        self.__dynamicBinarize = 0
        self.__updateSeuilSpinBox(self.__seuil)
        self.__updateStatusBar("Fichier : " + self.__file)
        self.__updateBinarSlider(self.__dynamicBinarize)

###################################################################################################
    def initConnect(self):
        self.ui.OpenFileButton.clicked.connect(self.OpenFile)
        self.ui.ScanSlider.valueChanged.connect(self.OnScanSliderChange)
        self.ui.TypeBinarSlider.valueChanged.connect(self.OnTypeBinarSliderChange)
        self.ui.SeuilSpinBox.valueChanged.connect(self.OnSeuilSpinBoxChange)
        self.ui.FilterSpinBox.valueChanged.connect(self.OnFilterSpinBoxChange)
        self.ui.StepUpButton.clicked.connect(self.OnStepUpChange)
        self.ui.StepDownButton.clicked.connect(self.OnStepDownChange)
        
###################################################################################################
    def OpenFile(self):
        self.__file = str( QFileDialog.getOpenFileName(self, caption="Select file"))
        self.__loadFile()
        self.__draw()

###################################################################################################
    def OnScanSliderChange(self):
        if self.__displayManager.isReady():
            nbScanReaded = self.__displayManager.getNbScan()
            currentScanIndex = self.ui.ScanSlider.value()
            self.__setScanLabel(currentScanIndex, nbScanReaded-1)
            self.__displayManager.updateCurrentScanIndex(currentScanIndex)
            self.__draw()
            
###################################################################################################
    def OnTypeBinarSliderChange(self):
        if self.__displayManager.isReady():
            self.__dynamicBinarize = self.ui.TypeBinarSlider.value()
            self.__draw()

###################################################################################################
    def OnSeuilSpinBoxChange(self):   
        if self.__displayManager.isReady():
            self.__seuil = self.ui.SeuilSpinBox.value()
            self.__draw()
            
###################################################################################################
    def OnFilterSpinBoxChange(self):   
        if self.__displayManager.isReady():
            value = self.ui.FilterSpinBox.value()
            self.__coeffFilter = value
            self.__draw()

###################################################################################################
    def OnStepUpChange(self):    
        nextScanIndex = self.__displayManager.getCurrentScanIndex() + 1
        if nextScanIndex > self.__displayManager.getNbScan() - 1:
            nextScanIndex = 0
        self.__updateScanSlider(nextScanIndex)
        self.__displayManager.updateCurrentScanIndex(nextScanIndex)
        self.__draw()

###################################################################################################
    def OnStepDownChange(self):   
        nextScanIndex = self.__displayManager.getCurrentScanIndex() - 1
        if nextScanIndex < 0:
            nextScanIndex = self.__displayManager.getNbScan() - 1
        self.__updateScanSlider(nextScanIndex)
        self.__displayManager.updateCurrentScanIndex(nextScanIndex)
        self.__draw()

###################################################################################################
    def __draw(self):
        nbPoints, time, date, reflectorLen, reflectorMid = self.__displayManager.draw(self.__seuil, self.__dynamicBinarize, self.__coeffFilter)
        self.__scanCanvas.draw()
        self.__setNbPointsLabel(nbPoints)
        self.__setTimeLabel(time, date)
        self.__updateReflectorLenLCD(reflectorLen)
        self.__updateReflectorMidLCD(reflectorMid)

###################################################################################################
    def __setScanSliderRange(self, start, end):
        self.ui.ScanSlider.setRange(start, end)

###################################################################################################
    def __updateScanSlider(self, index):
        nbScanReaded = self.__displayManager.getNbScan()
        self.__setScanLabel(index, nbScanReaded-1)
        self.ui.ScanSlider.setValue(index)
        
###################################################################################################
    def __updateBinarSlider(self, index):
        self.ui.TypeBinarSlider.setValue(index)
        
###################################################################################################
    def __updateSeuilSpinBox(self, index):
        self.ui.SeuilSpinBox.setValue(index)
        
###################################################################################################
    def __setScanLabel(self, start, end):
        self.ui.ScanLabel.setText("Scan " + str(start) + "/" + str(end))
        
###################################################################################################
    def __setNbPointsLabel(self, value):
        self.ui.NbPointsLabel.setText("Nombre de points = " + str(value))
        
###################################################################################################
    def __setTimeLabel(self, numCycle, date):
        self.ui.TimeLabel.setText("Num Cycle = " + numCycle + " // Date = " + date)
        
###################################################################################################
    def __updateStatusBar(self, message):
        self.ui.statusbar.showMessage(message)
        
###################################################################################################
    def __updateReflectorLenLCD(self, reflectorLen):
        self.ui.ReflectorLenLCD.display(reflectorLen)
        
###################################################################################################
    def __updateReflectorMidLCD(self, reflectorMid):
        self.ui.ReflectorMidLCD.display(reflectorMid)

###################################################################################################
def main(argv):
    inputFile = ""
    try:
        opts, args = getopt.getopt(argv,"i:",["input="])
    except getopt.GetoptError:
        print 'reflectorAnalyzer.py [-i <scanfile>]'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-i", "--input"):
            inputFile = arg

    app = QApplication(sys.argv)
    app.setApplicationName("Reflector Analyzer")
    app.setOrganizationName("basystemes")
    app.setOrganizationDomain("basystemes.com")
    ex = Editor(inputFile)
    sys.exit(app.exec_())

###################################################################################################
if __name__ == '__main__':
    main(sys.argv[1:])
