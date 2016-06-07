#!/usr/bin/python
#-*- encoding: utf-8 -*-

import openpyxl as opx
import gensim
import sys
import os
import csv
import logging
import functools
import traceback
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
	def __init__(self,sheet=None,dimensions=None):
		
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
		elif dimensions:
			row_count,column_count=dimensions
			super(Table,self).__init__(row_count,column_count)
		else:
			super(Table,self).__init__()
		
	def __getitem__(self,pair):
		x,y=pair
		item=self.item(x, y)
		#print item
		z = unicode(item.text()) if item else ""
		
		return z
	
	def __setitem__(self,pair,value):
		x,y=pair
		
		item=self.item(x, y)
		
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
		"""
		Fonction d'initialisation de la fenêtre, met en place tout les éléments interactifs du programme. 
		"""
		self.new=0
		super(Main, self).__init__()
		
		self.setContextMenuPolicy(Qt.ActionsContextMenu)
		
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
		saveAction.setStatusTip(_fromUtf8(u"Sauvegarde le fichier courant"))
		saveAction.triggered.connect(lambda : self.savefile(self.getfilename(flag=2) ) )
		
		#Actions du menu recherche
		
		lemmaSearch = QtGui.QAction(QtGui.QIcon('searchMenu.png'),'&Recherche par lemmes',self)
		lemmaSearch.setShortcut('Ctrl+Maj+L')
		lemmaSearch.setStatusTip(_fromUtf8(u"Rechercher les différentes formes d'un mot dans le corpus"))
		lemmaSearch.triggered.connect(self.lemmasearch)
		
		#Actions du menu classifier
		classAction = QtGui.QAction(QtGui.QIcon('defaults.png'),'&Classification LDA',self)
		classAction.setShortcut('Ctrl+Maj+T')
		classAction.setStatusTip(_fromUtf8(u"Classifier automatiquement les éléments sélectionnés"))
		classAction.triggered.connect(self.classify)
		
		codAction = QtGui.QAction(QtGui.QIcon('defaults.png'),_fromUtf8('&Coder la sélection'),self)
		codAction.setShortcut('Ctrl+B')
		codAction.setStatusTip( _fromUtf8(u"Attribuer un code aux éléments sélectionnés.") )
		codAction.triggered.connect(self.codelems)
		
		newAction = QtGui.QAction(QtGui.QIcon('defaults.png'),_fromUtf8('&Extraire les éléments'),self)
		newAction.setShortcut("Ctrl+N")
		newAction.setStatusTip(_fromUtf8("Créer une nouvelle feuille à partir de la sélection."))
		newAction.triggered.connect(self.newpage)
		
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
		classMenu.addAction(codAction)
		
		map(self.addAction, [newAction,loadAction,saveAction,exitAction,lemmaSearch,classAction,codAction])
		
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
	def graphicalerrors(func):
		@functools.wraps(func)
		def wrapper(self,*args,**kwargs):
			try:
				op=func(self,*args,**kwargs)
			except Exception as e:
				# e.__doc__
				# e.message
				logging.error(traceback.format_exc())
				QMessageBox.warning(self, _fromUtf8("Erreur"),_fromUtf8(e.__doc__+"\n"+e.message))
				raise e
			
			return op
		
		return wrapper
	
	@graphicalerrors
	def getcurrenttab(self):
		currenttab=self.tabs.currentWidget()
		currtable=currenttab.currentWidget() if isinstance(currenttab,QTabWidget) else currenttab
		return currtable
		
	
	@graphicalerrors
	def getfilename(self,flag=None):
		"""
			Fonction pour obtenir le nom d'un fichier, 
			Soit à ouvrir - flag=1 
			Soit à enregistrer - flag=2 
			La fonction ouvre le dialogue par défaut du système d'exploitation.
		"""
		files_types = "XLSX (*.xlsx);;CSV (*.csv);;Tous les fichiers (*)"
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
	
	@graphicalerrors
	def savefile(self,filename):
		"""
		Fonction de sauvegarde des fichiers : sauvegarde soit au format XLSX, auquel cas tout les onglets sont sauvegardés comme des feuilles
		Soit au format CSV auquel cas seul l'onglet courant est sauvegardé
		"""
		if filename:
			if filename.endswith(".xlsx"):
				name=self.nameindex[self.tabs.currentIndex()]
				
				fichier=opx.Workbook(write_only=True,guess_types=True)
				
				for elem in self.tabtable[name]:
					sheet=fichier.create_sheet()
					#print elem
					sheet.title = elem
					table = self.tabtable[name][elem]
					#print name,elem
					for row in xrange(0,table.rowCount()):
						sheet.append([ table[row,col] for col in xrange(0,table.columnCount()) ])
						#for col in table.columnCount():
				
				
				fichier.save(filename)
				
				# 
				# for index in xrange(0,currwidg.count()):
					# z=currwidg.widget(index)
					# name=currwidg.tabtext()
			elif filename.endswith(".csv"):
				ok,delimiter,quotechar=self.csvaskbox()
				if ok:
					currtable=self.getcurrenttab()
					with open(filename,"w") as sortie:
						
						for row in xrange(0,currtable.rowCount()):
							for col in xrange(0,currtable.columnCount()):
								rangee=""
								element= currtable[row,col]
								
								if col > 0:
										rangee += delimiter
								if quotechar:
									rangee += quotechar + re.sub(r"("+quotechar+")","\\\1",element) + quotechar
								else:
									rangee += element
								
								sortie.write(rangee.encode("utf-8") )
								#delimiter.join([ quotechar+re.sub(r"("+quotechar+")","\\\1",currtable[row,col])+quotechar if len(quotechar) > 1 else currtable[row,col]  ]).encode("utf-8") 
							sortie.write("\n")
				
			
			else:
				QMessageBox.warning(self, "Erreur","Format de fichier non pris en charge.")
			
		else:
			pass
	
	@graphicalerrors
	def openfile(self, filename):
		"""
			Fonction d'ouverture des fichiers.
			Ouvre les fichiers XLSX avec le module openpyxl
			Ou les fichiers CSV avec le module csv. 
			Crée un onglet pour chaque fichier ouvert, et un sub-onglet pour chaque feuille des fichiers XLSX.
		"""
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
				ok,delim,qc=self.csvaskbox()
					
				if ok:
					self.tabtable[filename][os.path.basename(filename)]=Table()
					csvtable=self.tabtable[filename][os.path.basename(filename)]
					self.tabs.addTab(csvtable,os.path.basename(filename))
					self.tabs.setTabToolTip (self.tabindex, QString(filename))
					self.nameindex[self.tabindex]=filename
					self.tabindex += 1
					self.tabs.setCurrentWidget(csvtable)
					
					with open(filename) as openfile:
						z=csv.reader(openfile,delimiter=delim,quotechar=qc)
					
						
						for i,x in enumerate(z):
							if i >= csvtable.rowCount():
									rowPosition = csvtable.rowCount()
									csvtable.insertRow(rowPosition)
							for j,y in enumerate(x):
								if j >= csvtable.columnCount():
									columnPosition = csvtable.columnCount()
									csvtable.insertColumn(columnPosition)
								csvtable[i,j]=y.decode("utf-8")
							
					#subtab.addTab(self.tabtable[filename],os.path.basename(filename))
					
						
				
			else:
				QMessageBox.warning(self, "Erreur","Format de fichier non pris en charge.")
	
	@graphicalerrors	
	def csvaskbox(self):
		"""
		Fonction pour demander à l'utilisateur via un QDialog les paramètres du fichier CSV à prendre en entrée. 
		Les séparateurs possibles sont la tabulation, la virgule, et le point-virgule. Les caractère de citation sont les guillemets doubles, simple.
		Ces paramètres sont transmis tels quels au module csv.
		
		"""
		
		#Dictionnaire de variable
		#Utilisé parce que les events .connect doivent être liés à des fonctions, parce qu'on ne peut pas faire d'assignation dans un lambda
		#Et parce que les fonctions internes ne peuvent pas modifier les variables de la fonction qui les enveloppe
		#Sauf en python 3 avec le mot-clef nonlocal.
		dc={'delimiter':",",
		'quotechar':"\""}
		
		box = QDialog()
		
		def chosen():
			box.accept()
		
		def die():
			box.reject()
		
		def quotecharchanged(index):
			dc['quotechar'] = ['"',"'",None][index]
		
		def delimiterchanged(index):
			dc['delimiter'] = ["\t", ",", ";"][index]
		
		
		layout = QVBoxLayout()
		lt = QHBoxLayout()
		ht = QHBoxLayout()
		
		delimiterchoice = QtGui.QComboBox(box)
		delimiterchoice.addItems(["Tabulation","Virgule ,","Point-Virgule ;"])
		delimiterchoice.currentIndexChanged.connect(delimiterchanged)
		
		quotecharchoice = QtGui.QComboBox(box)
		quotecharchoice.addItems(["Guillemets doubles \" ","Guillemets simples ' ","Aucun"])
		quotecharchoice.currentIndexChanged.connect(quotecharchanged)
		
		
		okbutton = QPushButton("ok",box)
		okbutton.clicked.connect(chosen)
		
		cancelbutton = QPushButton("Annuler",box)
		cancelbutton.clicked.connect(die)
		
		ht.addWidget(okbutton)
		ht.addWidget(cancelbutton)
		
		lt.addWidget(delimiterchoice)
		lt.addWidget(quotecharchoice)
		layout.addLayout(lt)
		layout.addLayout(ht)
		# b1.move(50,50)
		
		box.setLayout(layout)
		box.setWindowTitle(_fromUtf8(u"Paramètres du fichier CSV"))
		box.setGeometry(150,150,300,200)
		box.setWindowModality(Qt.ApplicationModal)
		if box.exec_():
			return True,dc['delimiter'],dc['quotechar']
		else:
			return False, dc['delimiter'],dc['quotechar']
	
	@graphicalerrors
	def lemmasearch(self,*args):
		if not self.ltok:
			self.ltok=Lemmtok(os.path.dirname(os.path.realpath(__file__))+"/lefff-3.4.mlex/lefff-3.4.mlex")
		
		
		raise NotImplementedError
	
	@graphicalerrors
	def classify(self,*args):
		
		try:
			currtable=self.tabs.currentWidget().currentWidget()
		except AttributeError:
			raise Exception("Erreur : vous devez ouvrir un fichier pour faire de la classification...")
		
		if not self.ltok:
			self.ltok=Lemmtok(os.path.dirname(os.path.realpath(__file__))+"/lefff-3.4.mlex/lefff-3.4.mlex")
		
		
		i=0
		corpus=dict()
		
		for item in currtable.selectedItems():
			i += 1
			corpus[i]=unicode(item.text())
		
		if i == 0:
			raise Exception('Le corpus sélectionné est vide. Opération impossible.')
		
		texts=self.ltok.tokenize(corpus)
		
		NUMTOPICS,NUMPASS,SEUILPROBA,SEUILMOT,MINIMUM=self.ldaaskbox()
		
		dictionary = corpora.Dictionary(texts)
		dictionary.filter_extremes(no_below=MINIMUM,no_above=SEUILMOT)
		dictionary.compactify()
		bow = [dictionary.doc2bow(text) for text in texts]
		corpus_tfidf =  models.TfidfModel(bow)[bow]
		lda=models.ldamodel.LdaModel(corpus=corpus_tfidf, id2word=dictionary, num_topics=NUMTOPICS,update_every=0, chunksize=4000, passes=NUMPASS, alpha='auto', eta='auto', minimum_probability=SEUILPROBA)
		
			#QMessageBox.about(self, "Info",item.text())
	
	@graphicalerrors
	def ldaaskbox(self):
		params={'topics':20,
		'passes':15,
		'seuilmin':0.3,
		'maxpres':0.95,
		'minpres':2}
				
		
		return params['topics'],params['passes'],params['seuilmin'],params['maxpres'],params['minpres']
	
	@graphicalerrors
	def codelems(self,*args):
		
		code=1
		
		currtable=self.getcurrenttab()
		
		columnPosition = currtable.columnCount()
		currtable.insertColumn(columnPosition)
		for item in currtable.selectedItems():
			currtable[item.row(),columnPosition] = str(code)
			
	
	@graphicalerrors
	def newpage(self,*args):
		
		currtable=self.getcurrenttab()
		selection=currtable.selectedItems()
		minrow=min([i.row() for i in selection])
		maxrow=max([i.row() for i in selection])
		mincol=min([i.column() for i in selection])
		maxcol=max([i.column() for i in selection])
		selectname="xtal_"+str(self.new)
		
		self.new += 1
		
		
		self.tabtable[selectname][selectname]=Table(dimensions=(maxrow-minrow+1,1+maxcol-mincol))
		newtable=self.tabtable[selectname][selectname]
		self.tabs.addTab(newtable,selectname)
		self.tabs.setTabToolTip (self.tabindex, selectname)
		self.nameindex[self.tabindex]=selectname
		self.tabindex += 1
		self.tabs.setCurrentWidget(newtable)
		for i in selection:
			newtable[i.row()-minrow, i.column() - mincol] = i.text()
		
				
if __name__ == '__main__':
	
	logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
	app = QtGui.QApplication(sys.argv)
	ex = Main()
	sys.exit(app.exec_())
