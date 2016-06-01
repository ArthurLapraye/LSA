#!/usr/bin/python
#-*- encoding: utf-8 -*-

import openpyxl as opx
import gensim
import sys
import os

from PyQt4 import *
from PyQt4 import QtCore, QtGui, QtWebKit
from PyQt4.QtGui import *
from PyQt4.QtCore import *

_fromUtf8 = QtCore.QString.fromUtf8

class frame(QtGui.QTableWidget):
	def __init__(self):
		pass

class Main(QtGui.QMainWindow):
	
	def __init__(self):
		super(Main, self).__init__()
		
		self.initUI()
	
	
	def changeTitle(self,row,col):
		self.setWindowTitle(self.table.tr("row:%s,col:%s"%(row,col)))
	
		
	def initUI(self):               
		
		exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Quitter', self)        
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip("Quitte l'application")
		exitAction.triggered.connect(QtGui.qApp.quit)
		
		loadAction = QtGui.QAction(QtGui.QIcon('open.png'),'&Ouvrir',self)
		loadAction.setShortcut("Ctrl+O")
		loadAction.setStatusTip("Ouvre un fichier .xlsx")
		loadAction.triggered.connect(lambda : self.openfile(self.getfilename() ) )
		
		self.textbar = QLineEdit()
		
		self.statusBar()
		menubar = self.menuBar()
		fileMenu = menubar.addMenu('&Fichier')
		fileMenu.addAction(loadAction)
		fileMenu.addAction(exitAction)
		self.tabs	= QtGui.QTabWidget()
		
		self.setCentralWidget(self.tabs)
		
		self.tabtable = dict()
		
		
		bardoutil= QToolBar()
		bardoutil.addWidget(self.textbar)
		self.addToolBar(Qt.TopToolBarArea, bardoutil)
		
		
		self.setGeometry(100,100,800,600)
		self.show()
	
	def getfilename(self):
		files_types = "XLSX (*.xlsx);;XLS (*.xls);;CSV (*.csv);;txt (*.txt);; Tous les fichiers (*)"
		filename = QFileDialog.getOpenFileName(None,
						caption=QtCore.QString("Ouvrir"),
						directory=QtCore.QString('./'),
						filter=files_types,
						selectedFilter=QtCore.QString('*.xlsx'))
		
		return unicode(filename)
		
	def openfile(self, filename):
			if filename.endswith(".xlsx"):
				
				wb = opx.load_workbook(filename, guess_types=True)
		
				for sheet in wb:
					
					row_count = sheet.max_row - 1
					column_count = sheet.max_column + 1
					
					
					self.tabtable[sheet.title] = QtGui.QTableWidget(row_count, column_count)
					self.tabs.addTab(self.tabtable[sheet.title],sheet.title)
					
					self.show()
									
					r,x=0,0
					for row in sheet:
						x=0
						for fn in row:
							if fn.value:
								newitem=QtGui.QTableWidgetItem( unicode(fn.value))
							else:
								newitem=QtGui.QTableWidgetItem("")
							#newitem.setText("toto")
							self.tabtable[sheet.title].setItem(r,x,newitem)
							x += 1
						
						r += 1
					
					#self.table.setRowCount(r)
					#self.table.setColumnCount(x)
					
					self.tabtable[sheet.title].show()
					
					#self.setCentralWidget(self.table)
					#self.setGeometry(300, 300, 300, 200)
				self.setWindowTitle(os.path.basename(filename) )
			
			else:
				QMessageBox.about(self, "Erreur","Format de fichier non pris en charge.")


				
if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	ex = Main()
	sys.exit(app.exec_())
