# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lidar.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(658, 594)
        self.centralwidget = QtGui.QWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMaximumSize(QtCore.QSize(10000, 10000))
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.gridLayout_6 = QtGui.QGridLayout()
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.gridLayout_8 = QtGui.QGridLayout()
        self.gridLayout_8.setContentsMargins(50, 0, -1, -1)
        self.gridLayout_8.setObjectName(_fromUtf8("gridLayout_8"))
        self.gridLayout_5 = QtGui.QGridLayout()
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.StepDownButton = QtGui.QPushButton(self.centralwidget)
        self.StepDownButton.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/image/image/ba_rewind.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.StepDownButton.setIcon(icon)
        self.StepDownButton.setObjectName(_fromUtf8("StepDownButton"))
        self.gridLayout_5.addWidget(self.StepDownButton, 0, 1, 1, 1)
        self.pushButton_openDir = QtGui.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setKerning(True)
        self.pushButton_openDir.setFont(font)
        self.pushButton_openDir.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/image/image/ba_eject.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_openDir.setIcon(icon1)
        self.pushButton_openDir.setObjectName(_fromUtf8("pushButton_openDir"))
        self.gridLayout_5.addWidget(self.pushButton_openDir, 0, 0, 1, 1)
        self.StepUpButton = QtGui.QPushButton(self.centralwidget)
        self.StepUpButton.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/image/image/ba_forward.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.StepUpButton.setIcon(icon2)
        self.StepUpButton.setObjectName(_fromUtf8("StepUpButton"))
        self.gridLayout_5.addWidget(self.StepUpButton, 0, 3, 1, 1)
        self.label_workingDir = QtGui.QLabel(self.centralwidget)
        self.label_workingDir.setObjectName(_fromUtf8("label_workingDir"))
        self.gridLayout_5.addWidget(self.label_workingDir, 0, 5, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem, 0, 6, 1, 1)
        self.StepPlayButton = QtGui.QPushButton(self.centralwidget)
        self.StepPlayButton.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/image/image/ba_play.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.StepPlayButton.setIcon(icon3)
        self.StepPlayButton.setObjectName(_fromUtf8("StepPlayButton"))
        self.gridLayout_5.addWidget(self.StepPlayButton, 0, 2, 1, 1)
        self.StepStopButton = QtGui.QPushButton(self.centralwidget)
        self.StepStopButton.setEnabled(True)
        self.StepStopButton.setToolTip(_fromUtf8(""))
        self.StepStopButton.setStatusTip(_fromUtf8(""))
        self.StepStopButton.setWhatsThis(_fromUtf8(""))
        self.StepStopButton.setAccessibleName(_fromUtf8(""))
        self.StepStopButton.setAccessibleDescription(_fromUtf8(""))
        self.StepStopButton.setText(_fromUtf8(""))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/image/image/ba_pause.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.StepStopButton.setIcon(icon4)
        self.StepStopButton.setObjectName(_fromUtf8("StepStopButton"))
        self.gridLayout_5.addWidget(self.StepStopButton, 0, 4, 1, 1)
        self.gridLayout_8.addLayout(self.gridLayout_5, 2, 2, 1, 1)
        self.timeSlider = QtGui.QSlider(self.centralwidget)
        self.timeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.timeSlider.setObjectName(_fromUtf8("timeSlider"))
        self.gridLayout_8.addWidget(self.timeSlider, 0, 2, 1, 1)
        self.gridLayout_6.addLayout(self.gridLayout_8, 4, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_6, 1, 0, 1, 1)
        self.gridLayout_Lidar = QtGui.QGridLayout()
        self.gridLayout_Lidar.setObjectName(_fromUtf8("gridLayout_Lidar"))
        self.gridLayout.addLayout(self.gridLayout_Lidar, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 658, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Lidar", None))
        self.label_workingDir.setText(_translate("MainWindow", "workingDir:None", None))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar", None))

import lsi_ui_rc
