#!/usr/bin/python
#-*- encoding: utf-8 -*-

import openpyxl as opx
import gensim
import sys
import os
import csv

from PyQt4 import *
from PyQt4 import QtCore, QtGui, QtWebKit
from PyQt4.QtGui import *
from PyQt4.QtCore import *

_fromUtf8 = QtCore.QString.fromUtf8


class Table(QtGui.QTableWidget):
	def __init__(self,sheet=None):
		
		if sheet:
			self.sheet=sheet
				
			row_count = sheet.max_row + 1
			column_count = sheet.max_column + 1
			super(Table,self).__init__(row_count,column_count)
			
			
			r,y=0,0
			for row in sheet:
				y=0
				for fn in row:
					if fn.value:
						newitem=QtGui.QTableWidgetItem( unicode(fn.value))
					else:
						newitem=QtGui.QTableWidgetItem("")
					
					self.setItem(r,y,newitem)
					
					y += 1
					
				r += 1
		else:
			super(Table,self).__init__(500,500)
		
	def __getitem__(self,pair):
		x,y=pair
		return self.itemAt(x, y).text
	
	def __setitem__(self,pair,value):
		x,y=pair
		x+=1
		y+=1
		item=self.itemAt(x, y)
		
		if not item:
			if value:
				item=QtGui.QTableWidgetItem(value)
			else:
				item=QtGui.QTableWidgetItem("")
			self.setItem(x,y, item)
		else:
			item.setText(value)
		
		#QMessageBox.about(self, "Info",value)
		
class Main(QtGui.QMainWindow):
	
	def __init__(self):
		super(Main, self).__init__()
		
		
		exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Quitter', self)        
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip("Quitte l'application")
		exitAction.triggered.connect(QtGui.qApp.quit)
		
		loadAction = QtGui.QAction(QtGui.QIcon('open.png'),'&Ouvrir',self)
		loadAction.setShortcut("Ctrl+O")
		loadAction.setStatusTip("Ouvre un fichier .xlsx ou .csv")
		loadAction.triggered.connect(lambda : self.openfile(self.getfilename(flag=1) ) )
		
		
		saveAction = QtGui.QAction(QtGui.QIcon('save.png'),'&Sauvegarder',self)
		saveAction.setShortcut('Ctrl+S')
		saveAction.setStatusTip("Sauvegarde le fichier courant")
		saveAction.triggered.connect(lambda : self.savefile(self.getfilename(flag=2) ) )
		
		self.textbar = QLineEdit()
		
		self.statusBar()
		menubar = self.menuBar()
		fileMenu = menubar.addMenu('&Fichier')
		fileMenu.addAction(loadAction)
		fileMenu.addAction(saveAction)
		fileMenu.addAction(exitAction)
		
		self.tabindex=0
		self.tabs	= QtGui.QTabWidget()
		self.setCentralWidget(self.tabs)
		self.tabtable = dict()
		
		
		bardoutil= QToolBar()
		bardoutil.addWidget(self.textbar)
		self.addToolBar(Qt.TopToolBarArea, bardoutil)
		
		
		self.setGeometry(100,100,1280,1024)
		self.show()
	
	def getfilename(self,flag=None):
		files_types = "XLSX (*.xlsx);;XLS (*.xls);;CSV (*.csv);;txt (*.txt);; Tous les fichiers (*)"
		filename=""
		if flag == 1:
			filename = QFileDialog.getOpenFileName(None,
							caption=QtCore.QString("Ouvrir"),
							directory=QtCore.QString('./'),
							filter=files_types,
							selectedFilter=QtCore.QString('*.xlsx'))
		elif flag == 2:
			filename = QFileDialog.getSaveFileName(None,
							caption=QtCore.QString("Sauvegarder"),
							directory=QtCore.QString('./'),
							filter=files_types,
							selectedFilter=QtCore.QString('*.xlsx'))
		else:
			QMessageBox.critical(self,"Erreur","Le drapeau :",flag," ne correspond à aucune action.")
		return unicode(filename)

	def savefile(self,filename):
		QMessageBox.critical(self, "Erreur","Non implémenté !")
		
	
	def openfile(self, filename):
			if filename:
				if filename.endswith(".xlsx"):
					subtab= QtGui.QTabWidget()
					wb = opx.load_workbook(filename, guess_types=False)
			
					for sheet in wb:
						
						self.tabtable[sheet.title] = Table(sheet)
						subtab.addTab(self.tabtable[sheet.title],sheet.title)
										
					self.tabs.addTab(subtab,os.path.basename(filename))
					self.tabs.setTabToolTip (self.tabindex, QString(filename))
					self.tabindex += 1
					# self.show()
				
				elif filename.endswith(".csv"):
					with open(filename) as openfile:
						z=csv.reader(openfile,delimiter="\t")
						self.tabtable[filename]=Table()
						for i,x in enumerate(z):
							print i,x
							for j,y in enumerate(x):
								print j,y
								self.tabtable[filename][i,j]=y
					
					#subtab.addTab(self.tabtable[filename],os.path.basename(filename))
					self.tabs.addTab(self.tabtable[filename],os.path.basename(filename))
					self.tabs.setTabToolTip (self.tabindex, QString(filename))
					self.tabindex += 1
					self.show()
						
				
				else:
					QMessageBox.about(self, "Erreur","Format de fichier non pris en charge.")
					

				
if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	ex = Main()
	sys.exit(app.exec_())
