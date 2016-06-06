#!/usr/bin/python
#-*- encoding: utf-8 -*-

import openpyxl as opx
import gensim
import sys
import os
import csv
import logging
import re

from collections import defaultdict
from gensim import corpora, models, similarities,matutils #Licence LGPL (check version)


from PyQt4 import *
from PyQt4 import QtCore, QtGui, QtWebKit
from PyQt4.QtGui import *
from PyQt4.QtCore import *

_fromUtf8 = QtCore.QString.fromUtf8

from lda import Lemmtok

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
						newitem=QtGui.QTableWidgetItem( _fromUtf8(unicode(fn.value)))
					else:
						newitem=QtGui.QTableWidgetItem("")
					
					self.setItem(r,y,newitem)
					
					y += 1
					
				r += 1
		else:
			super(Table,self).__init__(500,100)
		
	def __getitem__(self,pair):
		x,y=pair
		item=self.item(x, y)
		#print item
		z = unicode(item.text()) if item else ""
		
		return z
	
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
		
		self.setGeometry(100,100,800,600)
		self.show()
		
		#Actions du menu fichier
		
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
		
		#Actions du menu recherche
		
		lemmaSearch = QtGui.QAction(QtGui.QIcon('searchMenu.png'),'&Recherche par lemmes',self)
		lemmaSearch.setShortcut('Ctrl+Maj+L')
		lemmaSearch.setStatusTip("Rechercher les différentes formes d'un mot dans le corpus")
		lemmaSearch.triggered.connect(self.lemmasearch)
		
		#Actions du menu classifier
		classAction = QtGui.QAction(QtGui.QIcon('searchMenu.png'),'&Classification LDA',self)
		classAction.setShortcut('Ctrl+Maj+T')
		classAction.setStatusTip("Classifier automatiquement les éléments du corpus.")
		classAction.triggered.connect(self.classify)
		
		#Mise en place de la barre d'outil et de la barre d'état.
		self.textbar = QLineEdit()
		self.statusBar()
		
		#Barre d'outil
		menubar = self.menuBar()
		
		#Menu fichier
		fileMenu = menubar.addMenu('&Fichier')
		fileMenu.addAction(loadAction)
		fileMenu.addAction(saveAction)
		fileMenu.addAction(exitAction)
		
		#Menu recherche
		searchMenu = menubar.addMenu('&Recherche')
		searchMenu.addAction(lemmaSearch)
		
		#Menu classifier
		classMenu = menubar.addMenu("Classifier")
		classMenu.addAction(classAction)
		
		self.tabindex=0
		self.nameindex=dict()
		self.tabs	= QtGui.QTabWidget()
		self.setCentralWidget(self.tabs)
		self.tabtable = defaultdict(dict)
		
		
		bardoutil= QToolBar()
		bardoutil.addWidget(self.textbar)
		self.addToolBar(Qt.TopToolBarArea, bardoutil)
		
		self.ltok=None
		
		# self.show()
	
	def getfilename(self,flag=None):
		files_types = "XLSX (*.xlsx);;CSV (*.csv);;txt (*.txt);; Tous les fichiers (*)"
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
		if filename:
			if filename.endswith(".xlsx"):
				name=self.nameindex[self.tabs.currentIndex()]
				
				fichier=opx.Workbook(write_only=True,guess_types=True)
				
				for elem in self.tabtable[name]:
					sheet=fichier.create_sheet()
					print elem
					sheet.title = elem
					table = self.tabtable[name][elem]
					print name,elem
					for row in xrange(1,table.rowCount()):
						sheet.append([ table[row,col] for col in xrange(1,table.columnCount()) ])
						#for col in table.columnCount():
				
				
				fichier.save(filename)
				
				# 
				# for index in xrange(0,currwidg.count()):
					# z=currwidg.widget(index)
					# name=currwidg.tabtext()
			if filename.endswith(".csv"):
				currtable=self.tabs.currentWidget().currentWidget()
				with open(filename,"w") as sortie:
					delimiter,quotechar=self.csvaskbox()
					for row in xrange(0,currtable.rowCount()):
						for col in xrange(0,currtable.columnCount()):
							rangee=""
							element= currtable[row,col]
							
							if col > 1:
									rangee += delimiter
							if len(quotechar) == 1:
								rangee += quotechar + re.sub(r"("+quotechar+")","\\\1",element) + quotechar
							else:
								rangee += currtable[row,col]
							
							sortie.write(rangee.encode("utf-8") )
							#delimiter.join([ quotechar+re.sub(r"("+quotechar+")","\\\1",currtable[row,col])+quotechar if len(quotechar) > 1 else currtable[row,col]  ]).encode("utf-8") 
						sortie.write("\n")
				
			
			else:
				QMessageBox.warning(self, "Erreur","Format de fichier non pris en charge.")
			
		else:
			pass
				
		
	
	def openfile(self, filename):
			if filename:
				if filename.endswith(".xlsx"):
					subtab= QtGui.QTabWidget()
					wb = opx.load_workbook(filename, guess_types=False)
			
					for sheet in wb:
						
						self.tabtable[filename][sheet.title] = Table(sheet)
						subtab.addTab(self.tabtable[filename][sheet.title],sheet.title)
										
					self.tabs.addTab(subtab,os.path.basename(filename))
					self.tabs.setTabToolTip (self.tabindex, QString(filename))
					self.nameindex[self.tabindex]=filename
					self.tabindex += 1
					self.tabs.setCurrentWidget(subtab)
					# self.show()
				
				elif filename.endswith(".csv"):
					delim,qc=self.csvaskbox()
					with open(filename) as openfile:
						z=csv.reader(openfile,delimiter=delim,quotechar=qc)
						self.tabtable[filename][os.path.basename(filename)]=Table()
						for i,x in enumerate(z):
							for j,y in enumerate(x):
								self.tabtable[filename][os.path.basename(filename)][i,j]=y
					
					#subtab.addTab(self.tabtable[filename],os.path.basename(filename))
					self.tabs.addTab(self.tabtable[filename][os.path.basename(filename)],os.path.basename(filename))
					self.tabs.setTabToolTip (self.tabindex, QString(filename))
					self.nameindex[self.tabindex]=filename
					self.tabindex += 1
					self.tabs.setCurrentWidget(self.tabtable[filename][os.path.basename(filename)])
						
				
				else:
					QMessageBox.warning(self, "Erreur","Format de fichier non pris en charge.")
		
	def csvaskbox(self):
		delimiter,quotechar="\t","\""
		return delimiter,quotechar
	
	
	def lemmasearch(self):
		if not self.ltok:
			self.ltok=Lemmtok(os.path.dirname(os.path.realpath(__file__))+"/lefff-3.4.mlex/lefff-3.4.mlex")
		
		
		raise NotImplementedError
	
	def classify(self):
		if not self.ltok:
			self.ltok=Lemmtok(os.path.dirname(os.path.realpath(__file__))+"/lefff-3.4.mlex/lefff-3.4.mlex")
		
		currtable=self.tabs.currentWidget().currentWidget()
		i=0
		corpus=dict()
		
		for item in currtable.selectedItems():
			i += 1
			corpus[i]=unicode(item.text())
		
		texts=self.ltok.tokenize(corpus)
		
		NUMTOPICS,NUMPASS,SEUILPROBA,SEUILMOT,MINIMUM=self.ldaaskbox()
		
		dictionary = corpora.Dictionary(texts)
		dictionary.filter_extremes(no_below=MINIMUM,no_above=SEUILMOT)
		dictionary.compactify()
		bow = [dictionary.doc2bow(text) for text in texts]
		corpus_tfidf =  models.TfidfModel(bow)[bow]
		lda=models.ldamodel.LdaModel(corpus=corpus_tfidf, id2word=dictionary, num_topics=NUMTOPICS,update_every=0, chunksize=4000, passes=NUMPASS, alpha='auto', eta='auto', minimum_probability=SEUILPROBA)
			#QMessageBox.about(self, "Info",item.text())

	def ldaaskbox(self):
		NUMTOPICS=20
		NUMPASS=15
		SEUILPROBA =0.3
		SEUILMOT=0.95
		MINIMUM=2
		return NUMTOPICS,NUMPASS,SEUILPROBA,SEUILMOT,MINIMUM
				
if __name__ == '__main__':
	
	logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
	app = QtGui.QApplication(sys.argv)
	ex = Main()
	sys.exit(app.exec_())
