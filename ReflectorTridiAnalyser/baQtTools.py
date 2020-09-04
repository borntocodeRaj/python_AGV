#!/usr/bin/python

from PyQt4.QtCore import QThread, pyqtSignal, pyqtSlot
import time


class PlayThread(QThread):

    workingTrigger = pyqtSignal()

    def __init__(self):
        QThread.__init__(self)
        self.__sleepTime = 0.1
        self.__controlRun = 0

        self.__forceStop = False
        self.__isRunning = False

    def setStepTime(self, stepTime):
        self.__sleepTime = stepTime

    def setForceStop(self):
        self.__forceStop = True

    def resetForceStop(self):
        self.__forceStop = False

    def __del__(self):
        self.wait()

    def stop(self):
        return self.__forceStop

    def doWork(self):
        self.workingTrigger.emit()

    def isRunning(self):
        return self.__isRunning

    def run(self):
        self.__isRunning = True
        while(not self.stop()):
            self.doWork()
            time.sleep(self.__sleepTime)

        self.__isRunning = False
