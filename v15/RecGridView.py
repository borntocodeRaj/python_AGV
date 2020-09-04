from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import matplotlib.mlab
import PyQt4.QtCore as QtCore
from PyQt4 import QtCore, QtGui 

class RecTable(QtGui.QTableView):
	def __init__(self, datas):
		QTableWidget.__init__(self)
		self.tm=TableModel(self)
		self.tm.setDatas(datas)
		self.setModel(self.tm)
		self.resizeColumnsToContents()
		self.resizeRowsToContents()
		self.setSortingEnabled(True)

class TableModel(QtCore.QAbstractTableModel): 
	def __init__(self, parent=None, *args): 
		super(TableModel, self).__init__()
		self.datas = []
		self.names = []

	def setDatas(self, datas):
		self.datas = datas
		self.names = self.datas.dtype.names

	def update(self, dataIn):
		print 'Updating Model ???'
		print dataIn
		#print 'Datatable : {0}'.format(self.datatable)

	def headerData(self, section, orientation, role=Qt.DisplayRole):
		if role == Qt.DisplayRole and orientation == Qt.Horizontal:
			return self.names[section]
		return QAbstractTableModel.headerData(self, section, orientation, role)

	def sort(self, Ncol, order):
		if self.datas != None:
			"""Sort table by given column number.
			"""
			self.emit(SIGNAL("layoutAboutToBeChanged()"))
			self.datas.sort( order=self.datas.dtype.names[Ncol] )
			if order == Qt.DescendingOrder:
				self.datas = self.datas[::-1]
			self.emit(SIGNAL("layoutChanged()"))

	def rowCount(self, parent=QtCore.QModelIndex()):
		if self.datas != None:
			return len(self.datas) 
		return 0

	def columnCount(self, parent=QtCore.QModelIndex()):
		if self.datas != None:
			return len(self.datas.dtype) 
		return 0

	def data(self, index, role=QtCore.Qt.DisplayRole):
		if self.datas != None and role == QtCore.Qt.DisplayRole:
			i = index.row()
			j = index.column()
			#return '{0}'.format(self.datatable.iget_value(i, j))
			return str(self.datas[i][j])
		else:
			return QtCore.QVariant()

	def flags(self, index):
		return QtCore.Qt.ItemIsEnabled

""" display a data in a QT Grid
@param datas rec.array """
def display(datas):
	app = QApplication(sys.argv)
	table = RecTable(datas)
	table.show()
	app.exec_()

