#!/usr/bin/python

from __future__ import unicode_literals
import sys
import os
from time import sleep
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import lidar_ctr

#from py_baTools.baQtTools import PlayThread

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

from lidar_ui import Ui_MainWindow

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar

import time


class LidarCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        self.axes1 = fig.add_subplot(111)
        self.axes1.grid(True)
        self.axes1.hold(True)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


class Editor(QMainWindow):

    def __init__(self):
        super(Editor, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.__lidarCanvas = LidarCanvas(
            self.ui.centralwidget, width=5, height=4, dpi=100)
        self.ui.gridLayout_Lidar.addWidget(self.__lidarCanvas)
        mpl_toolbar1 = NavigationToolbar(
            self.__lidarCanvas, self.ui.centralwidget)

        self.ui.gridLayout_Lidar.addWidget(mpl_toolbar1)

        self.initConnect()

        self.__displayManager = lidar_ctr.displayManager()

        self.__displayManager.setGraphAxes(self.__lidarCanvas.axes1)

        self.__workingFile = None
        self.__forceStopPlay = False

        #self.__playThread = PlayThread()
        #self.__playThread.doWork = self.OnStepUpChange

        self.show()

    def initConnect(self):
        self.ui.pushButton_openDir.clicked.connect(self.openWorkingFile)
        self.ui.timeSlider.sliderReleased.connect(self.OnTimeSliderChange)
        self.ui.StepDownButton.clicked.connect(self.OnStepDownChange)
        self.ui.StepUpButton.clicked.connect(self.OnStepUpChange)
        self.ui.StepStopButton.clicked.connect(self.OnStepStopChange)
        self.ui.StepPlayButton.clicked.connect(self.OnStepPlayChange)

    def OnStepDownChange(self):
        c = self.__displayManager.getCurentFrame() - 1
        if c >= 0:
            self.ui.timeSlider.setValue(c)
            self.__displayManager.drawGraph(c)
            self.__lidarCanvas.draw()
            return not self.__forceStopPlay
        else:
            return False

    def OnStepUpChange(self):
        c = self.__displayManager.getCurentFrame() + 1
        if c < self.__displayManager.getNbFrame():
            self.ui.timeSlider.setValue(c)
            self.__displayManager.drawGraph(c)
            self.__lidarCanvas.draw()
            return not self.__forceStopPlay
        else:
            return False

    def OnStepStopChange(self):
        self.__forceStopPlay = True
        self.__playThread.setForceStop()

    def OnStepPlayChange(self):
        self.__forceStopPlay = False
        self.__playThread.resetForceStop()
        self.__playThread.start()

    def OnTimeSliderChange(self):
        if self.__displayManager.isReady():
            value = self.ui.timeSlider.value()
            self.__displayManager.drawGraph(value)
            self.__lidarCanvas.draw()

    def openWorkingFile(self):
        self.__workingFile = str(
            QFileDialog.getOpenFileName(self, caption="Select file"))
        self.__displayManager.setworkingFile(self.__workingFile)
        if self.__workingFile != "":
            self.ui.label_workingDir.setText(
                "workingDir:" + self.__workingFile)
            self.__drawInitPlot()

    def __drawInitPlot(self):
        self.__displayManager.loadFiles()
        self.__setSlider()
        self.__displayManager.drawGraph()

    def __setSlider(self):
        self.ui.timeSlider.setRange(0, self.__displayManager.getNbFrame() - 1)


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Lidar")
    app.setOrganizationName("basystemes")
    app.setOrganizationDomain("basystemes.com")
    ex = Editor()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
