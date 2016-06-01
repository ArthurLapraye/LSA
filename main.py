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


class frame(QtGui.QTableWidget):
	def __init__(self):
		pass

class Example(QtGui.QMainWindow):
	
	def __init__(self):
		super(Example, self).__init__()
		
		self.initUI()
	
	
	def changeTitle(self,row,col):
		self.setWindowTitle(self.table.tr("row:%s,col:%s"%(row,col)))
	
		
	def initUI(self):               
		
		exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Quitter', self)        
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip('Exit application')
		exitAction.triggered.connect(QtGui.qApp.quit)
		
		loadAction = QtGui.QAction(QtGui.QIcon('open.png'),'&Ouvrir',self)
		loadAction.setShortcut("Ctrl+O")
		loadAction.setStatusTip("Ouvre un fichier .xlsx")
		loadAction.triggered.connect(self.openfile)
		
		
		self.statusBar()
		menubar = self.menuBar()
		fileMenu = menubar.addMenu('&File')
		fileMenu.addAction(loadAction)
		fileMenu.addAction(exitAction)
		self.tabs	= QtGui.QTabWidget()
		
		self.tabtable = dict()
		
		self.show()
	
	def openfile(self):
		files_types = "XLSX (*.xlsx *.xls);;CSV (*.csv);;txt (*.txt);; Tous les fichiers (*)"
		filename = QFileDialog.getOpenFileName(None,
						caption=QtCore.QString("Ouvrir"),
						directory=QtCore.QString('./'),
						filter=files_types,
						selectedFilter=QtCore.QString('*.xlsx'))
	
		wb = opx.load_workbook(filename, guess_types=True)
		
		
		if filename.endswith(".xlsx") or filename.endswith("xls"):
			for sheet in wb:
				self.tabtable[sheet.title] = QtGui.QTableWidget(row_count, column_count)
				self.tabs.addTab(self.tabtable[sheet.title],sheet.title)
				row_count = sheet.max_row - 1
				column_count = sheet.max_column + 1
				self.tabs.show()
								
				r,x=0,0
				for row in sheet:
					x=0
					for fn in row:
						#print fn.value
						newitem=QtGui.QTableWidgetItem( unicode(fn.value))
						#newitem.setText("toto")
						self.tabtable[sheet.title].setItem(r,x,newitem)
						x += 1
					
					r += 1
				
				#self.table.setRowCount(r)
				#self.table.setColumnCount(x)
				
				self.tabtable[sheet.title].show()
				
				#self.setCentralWidget(self.table)
				self.setGeometry(300, 300, 300, 200)
				#self.setWindowTitle('Menubar')    
				
				
				
		
		self.show()
		
		
def main():
	
	app = QtGui.QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()    
