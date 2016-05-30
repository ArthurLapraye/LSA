# -*- coding: utf-8 -*-
#
#Ce programme nécessite PyQt4. 
#Pour l'installer sous Linux : sudo apt-get install PyQt4-dev-tools
#Arthur Lapraye - 2014 

import operator
import codecs
import os
import os.path
from PyQt4 import *
from PyQt4 import QtCore, QtGui, QtWebKit
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from dic import *

#self.text_edit_evt.connect(self.textEdit.append)

try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	_fromUtf8 = lambda s: s


class helpwindow(object):
	def init(self):
		self.MainWindow = QMainWindow()
		self.MainWindow.setObjectName(_fromUtf8("Help"))
		
		self.help = QtWebKit.QWebView()
		#self.help.setReadOnly(True)
		
		self.help.setUrl(QtCore.QUrl("./aide/aide.html"))
		
		self.buttonfermer = QPushButton()
		self.buttonfermer.setText("Fermer l'aide")
		self.buttonfermer.clicked.connect(self.MainWindow.hide)
		
		self.bardoutaide = QToolBar()
		self.bardoutaide.addWidget(self.buttonfermer)
		
		self.layoutMain = QHBoxLayout()
		self.layoutMain.addWidget(self.help)
		
		self.centralWidget = QWidget(self.MainWindow)
		
		self.centralWidget.setLayout(self.layoutMain)
		
		self.MainWindow.setCentralWidget(self.centralWidget)
		self.MainWindow.setWindowTitle(QtGui.QApplication.translate("Navilangue",
			"Aide - Navilangue - Arthur Lapraye 2014", None, QtGui.QApplication.UnicodeUTF8))
		
		QtCore.QMetaObject.connectSlotsByName(self.MainWindow)
		self.MainWindow.addToolBar(Qt.BottomToolBarArea, self.bardoutaide)
		
		self.Desktop = QApplication.desktop()
		Width=self.Desktop.width()
		Height=self.Desktop.height()
		Wposition = (Width/2) - 400#(self.MainWindow.width()/2 )
		Hposition = (Height/2) - 300#(self.MainWindow.height()/2)


class Ui_MainWindow(object):
	def setupUi(self):
		
		self.codec0 = QtCore.QTextCodec.codecForName("UTF-16");
		self.Desktop = QApplication.desktop()
		Width=self.Desktop.width()
		Height=self.Desktop.height()
		print Width, Height
		
		QtWebKit.QWebSettings.setIconDatabasePath("./")
		self.MainWindow = QtGui.QMainWindow()
		self.MainWindow.setObjectName(_fromUtf8("Navilangue"))
		
		self.centralWidget = QWidget(self.MainWindow)
		self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
		
		self.topWidget = QWidget(self.MainWindow)
		self.topWidget.setObjectName(_fromUtf8("topWidget"))
		
		self.pushButton = QtGui.QPushButton()
		#self.pushButton.setGeometry(QtCore.QRect(0, 10, 94, 27))
		self.pushButton.setObjectName(_fromUtf8("pushButton"))
		self.pushButton.setText(QtGui.QApplication.translate("Navilangue", "Go !", None, QtGui.QApplication.UnicodeUTF8))
		self.pushButton.clicked.connect(self.handleButton)
		self.pushButton.setToolTip("Lancer la navigation.")
		
		self.button2 = QPushButton()
		self.button2.setText("Voir la source")
		self.button2.clicked.connect(self.button2handle)
		self.button2.setToolTip("Afficher la source de la page web.")
		
		leftarr = QPixmap("./leftarrow.png")
		leftarrow = QIcon(leftarr)
		
		rightarr = QPixmap("arrowright.png")
		rightarrow = QIcon(rightarr)
		
		floppy = QPixmap("floppy.png")
		floppydisk = QIcon(floppy)
		
		iconsize = QSize(13,13)
		
		self.forward = QPushButton()
		self.forward.setIcon(rightarrow)
		self.forward.setIconSize(iconsize)
		self.forward.clicked.connect(self.goforward)
		self.forward.setEnabled(False)
		self.forward.setToolTip(u"Avancer à la page suivante.")
		
		
		self.back = QPushButton()
		self.back.setIcon(leftarrow)
		self.back.setIconSize(iconsize)
		self.back.clicked.connect(self.goback)
		self.back.setEnabled(False)
		self.back.setToolTip(u"Revenir à la page précédente.")
		
		self.save = QPushButton()
		self.save.setIcon(floppydisk)
		self.save.setIconSize(iconsize)
		self.save.clicked.connect(self.savepage)
		self.save.setToolTip(u"Sauver la vue actuelle.")
		
		self.buttonHTML = QPushButton()
		self.buttonHTML.setText("Voir la page")
		self.buttonHTML.clicked.connect(self.BHTML)
		self.buttonHTML.setToolTip("Afficher la page comme une page web")
		
		self.buttonPlain = QPushButton()
		self.buttonPlain.setText("Voir le texte brut")
		self.buttonPlain.clicked.connect(self.BPLAIN)
		self.buttonPlain.setToolTip("Afficher le texte brut de la page.")
		
		self.buttonLang = QPushButton()
		self.buttonLang.setText("Langue ?")
		self.buttonLang.clicked.connect(self.Lang)
		self.buttonLang.setToolTip(u"Détecter la langue du document")
		
		self.buttonAdd = QPushButton()
		self.buttonAdd.setText("Ajouter une langue ou enrichir un corpus existant.")
		self.buttonAdd.clicked.connect(self.ajout)
		self.buttonAdd.setToolTip(u"Permet de rajouter le texte de la page courante à un corpus existante" +
						u" ou d'en faire un nouveau corpus pour une nouvelle langue.")
		
		self.buttonStats = QPushButton()
		self.buttonStats.setText("Montrer les distances.")
		self.buttonStats.clicked.connect(self.showtrigs)
		self.buttonStats.setToolTip(u"Afficher les distances pour chaque langue, et les trigrammes fréquents.")
		
		self.buttonaide = QPushButton()
		self.buttonaide.setText("Aide.")
		self.buttonaide.clicked.connect(self.aide)
		self.buttonaide.setToolTip("Besoin d'aide ?")
		
		self.buttondico = QPushButton()
		self.buttondico.setText("Dictionnaire")
		self.buttondico.clicked.connect(self.dictio)
		self.buttondico.setToolTip(u"Afficher les mots du documents par nombre d'occurrences décroissantes.")
		
		self.buttonLang.setEnabled(False)
		self.buttondico.setEnabled(False)
		self.buttonStats.setEnabled(False)
		self.save.setEnabled(False)
		
		self.urlbar = QLineEdit()
		#self.urlbar.setGeometry(QtCore.QRect(100, 10, 701, 27))
		self.urlbar.setAutoFillBackground(True)
		self.urlbar.setObjectName(_fromUtf8("urlbar"))
		self.urlbar.returnPressed.connect(self.handleButton)
		self.urlbar.setToolTip("Barre d'adresse. Entrez une URI ou un mot-clef de recherche.")
		
		self.webView = QtWebKit.QWebView(self.centralWidget)
		#self.webView.setGeometry(QtCore.QRect(0, 40, 800, 600))
		self.webView.setObjectName(_fromUtf8("webView"))
		self.webView.loadFinished.connect(self.sourceit)
		self.webView.urlChanged.connect(lambda u: self.urlbar.setText(u.toString()))
		
		self.message="3|2|23(_)|2 : |o4(_+3 |\|0|\| (/-/4|?(_+33..."
		
		self.source = QTextEdit()
		self.source.setReadOnly(True)
	
		self.plain = QTextEdit()
		self.plain.setReadOnly(True)
		
		self.stats = QTextEdit()
		self.stats.setReadOnly(True)
		
		self.dico = QTextBrowser()
		self.dico.setReadOnly(True)
		self.dico.anchorClicked.connect(self.handleurl)
		
		self.layoutHorizontal = QHBoxLayout()
		self.layoutHorizontal.addWidget(self.back)
		self.layoutHorizontal.addWidget(self.forward)
		self.layoutHorizontal.addWidget(self.urlbar)
		self.layoutHorizontal.addWidget(self.pushButton)
		
		
		self.layoutMain = QHBoxLayout()
		self.layoutMain.addWidget(self.webView)
		
		
		self.current = self.webView
		
		self.topWidget.setLayout(self.layoutHorizontal)
		
		self.progressbar = QtGui.QProgressBar()
		self.progressbar.setMinimum(0)
		self.progressbar.setMaximum(100)
		
		self.centralWidget.setLayout(self.layoutMain)
		self.status = QStatusBar()
		self.status.addPermanentWidget(self.buttonaide)
		self.status.addPermanentWidget(self.save)
		self.status.addWidget(self.progressbar)
		
		self.menuwidge = QToolBar()
		self.menuwidge.addWidget(self.buttonHTML)
		self.menuwidge.addWidget(self.button2)
		self.menuwidge.addWidget(self.buttonPlain)
		self.menuwidge.addWidget(self.buttonLang)
		self.menuwidge.addWidget(self.buttonStats)
		self.menuwidge.addWidget(self.buttondico)
		
		self.bardoutil = QToolBar()
		self.bardoutil.addWidget(self.buttonAdd)
		
		self.uptrigs = QPushButton()
		self.uptrigs.setText(u"Régénérer les trigrammes.")
		self.uptrigs.clicked.connect(self.regtrigs)
		self.uptrigs.setToolTip(u"Régénérer le dictionnaire de fréquence de trigrammes employé par le logiciel.")
		
		self.bartrigs = QToolBar()
		self.bartrigs.addWidget(self.uptrigs)
		
		self.MainWindow.setMenuWidget(self.topWidget)
		self.MainWindow.setCentralWidget(self.centralWidget)
		self.MainWindow.addToolBar(Qt.TopToolBarArea,self.menuwidge)
		self.MainWindow.addToolBar(Qt.BottomToolBarArea, self.bardoutil)
		self.bardoutil.hide()
		self.MainWindow.addToolBar(Qt.BottomToolBarArea, self.bartrigs)
		self.bartrigs.hide()
		self.MainWindow.setStatusBar(self.status)
		self.MainWindow.setWindowTitle(QtGui.QApplication.translate("Navilangue", "Navilangue - Arthur Lapraye 2014", None, QtGui.QApplication.UnicodeUTF8))
		self.MainWindow.setWindowIcon(self.webView.icon())
		
		QtCore.QMetaObject.connectSlotsByName(self.MainWindow)
		
		self.helpwindow = helpwindow()
		
		with open("qtstyle.css") as stylesheetfile:
			self.MainWindow.setStyleSheet(stylesheetfile.read())
		
		
		Wposition = (Width/2) - 400#(self.MainWindow.width()/2 )
		Hposition = (Height/2) - 300#(self.MainWindow.height()/2)
		self.MainWindow.move(Wposition,Hposition)
	
	def currentwidget(self,makecurrent):
		self.current.setParent(None)
		self.current = makecurrent
		if makecurrent != self.plain:
			self.bardoutil.hide()
		
		if makecurrent != self.stats:
			self.bartrigs.hide()
		
		self.layoutMain.addWidget(self.current)
		
	def print_progress(self, percent):
	
		palette = QtGui.QPalette(self.progressbar.palette())
		palette.setColor(QtGui.QPalette.Highlight,
		QtGui.QColor(QtCore.Qt.red))

		self.progressbar.setPalette(palette)
		
		self.buttonLang.setEnabled(False)
		self.buttondico.setEnabled(False)
		self.buttonStats.setEnabled(False)
		self.buttonAdd.setEnabled(False)
		self.save.setEnabled(False)
		
		#self.progressbar.setStyleSheet(DEFAULT_STYLE)
		self.progressbar.setFormat("Chargement: " + str(percent) + " %")
		self.progressbar.setValue(percent)
		self.source.setPlainText(QApplication.translate("Navilangue",
								unicode(self.webView.page().mainFrame().toHtml()).encode('utf-8'),
								None,
								QApplication.UnicodeUTF8))
		self.plain.setPlainText(QApplication.translate("Navilangue", unicode(self.webView.page().mainFrame().toPlainText()).encode('utf-8'),
								None, QApplication.UnicodeUTF8))
		#print "Chargement : " + str(percent) + " %"
		
	def handleButton(self):
		z=self.urlbar.text()
		self.handleurl(z)
	
	def button2handle(self):
		self.currentwidget(self.source)
	
	def handleurl(self, url):
		codec0 = QtCore.QTextCodec.codecForName("UTF-16");
		url = unicode(codec0.fromUnicode(url), 'UTF-16')
		print url, u" requise"
		self.urlbar.setText(url)
		if re.match(r'https?://',url):
			self.webView.setUrl(QtCore.QUrl( _fromUtf8(url)))
			self.webView.loadProgress.connect(self.print_progress)
		elif url.startswith("file://"):
			self.webView.setUrl(QtCore.QUrl(_fromUtf8(url[7:])))
			self.webView.loadProgress.connect(self.print_progress)
		else:
			self.handleurl(u"http://www.google.fr/search?q=\""+url+"\"")
	
	def BHTML(self):
		self.currentwidget(self.webView)
	
	def BPLAIN(self):
		self.bardoutil.show()
		self.currentwidget(self.plain)
	
	def Lang(self):
		z= identifier(self.message)
		QMessageBox.about(self.MainWindow,"Langue du document",QApplication.translate("Navilangue", z, None, QApplication.UnicodeUTF8))
	
	def showtrigs(self):
		self.bartrigs.show()
		self.currentwidget(self.stats)
	
	def ajout(self):
		codec0 = QtCore.QTextCodec.codecForName("UTF-16");
		fd = QFileDialog()
		fd.setOption(fd.DontConfirmOverwrite, True)
		self.filename= fd.getSaveFileName(None,
						caption=QtCore.QString(u"Ajouter le corpus courant à un fichier"),
						directory=QtCore.QString('./langues'),
						filter=QtCore.QString('Fichiers Textes (*.txt);; Tous les fichiers (*)'),
						selectedFilter=QtCore.QString('*.*'))
		if self.filename != u'':
			with open(unicode(self.filename), "a") as myfile:
				myfile.write(self.message.encode("UTF-8"))
			updatedic(unicode(codec0.fromUnicode(self.filename), 'UTF-16'))
		
			QMessageBox.about(self.MainWindow,"Langue du document",
				QApplication.translate("Navilangue", "Le fichier" + self.filename + 
				" a bien été mis à jour, ainsi que les trigrammes correspondants", None, QApplication.UnicodeUTF8))
		#print self.message[-4:]
	
	
	def regtrigs(self):
		languesfiles= []
		corpusf = {}
		trigsf = {}
		try:
			makedic()
			QMessageBox.about(self.MainWindow,"Langue du document",
			QApplication.translate("Navilangue", "Trigrammes régénérés.", None, QApplication.UnicodeUTF8))
		except IOError as e:
			p="Erreur {0} :: {1}".format(e.errno, e.strerror)
			QMessageBox.about(self.MainWindow,"Langue du document",
			QApplication.translate("Navilangue", p, None, QApplication.UnicodeUTF8))
		
		
	def savepage(self):
		files_types = "HTML (*.html *.html);;txt (*.txt);; Tous les fichiers (*)"
		nomdefichier =  QFileDialog.getSaveFileName(None,
						caption=QtCore.QString("Enregistrer"),
						directory=QtCore.QString('./'),
						filter=files_types,
						selectedFilter=QtCore.QString('*.html'))
		if self.current == self.webView:
			registering = unicode(self.codec0.fromUnicode(self.webView.page().mainFrame().toHtml()), 'utf-16')
		elif self.current == self.dico:
			registering = unicode(self.codec0.fromUnicode(self.dico.toHtml()), 'utf-16')
		else:
			registering = unicode(self.codec0.fromUnicode(self.current.toPlainText()), 'utf-16')
		
		with open(unicode(nomdefichier), "w") as myfile:
			myfile.write(registering.encode('utf-8'))
			print nomdefichier, "enregistré."
			QMessageBox.about(self.MainWindow,"Langue du document",
				QApplication.translate("Navilangue", 
						"Fichier "+ nomdefichier+ " enregistré.", 
						None, QApplication.UnicodeUTF8))
		
	
	def dictio(self):
		self.currentwidget(self.dico)
		
	def aide(self):
		print "Vous voulez de l'aide ?"
		self.helpwindow.init()
		self.helpwindow.MainWindow.show()
	
	def goforward(self):
		self.webView.forward()
	
	def goback(self):
		self.webView.back()
	
	def sourceit(self):
		self.buttonLang.setEnabled(True)
		self.buttondico.setEnabled(True)
		self.buttonStats.setEnabled(True)
		self.save.setEnabled(True)
		
		if  self.webView.page().history().canGoBack():
			self.back.setEnabled(True)
		else:
			self.back.setEnabled(False)
		
		if self.webView.page().history().canGoForward():
			self.forward.setEnabled(True)
		else:
			self.forward.setEnabled(False)
		
		#self.progressbar.setStyleSheet(COMPLETED_STYLE)
		
		palette = QtGui.QPalette(self.progressbar.palette())
		palette.setColor(QtGui.QPalette.Highlight,
		QtGui.QColor(QtCore.Qt.blue))

		self.progressbar.setPalette(palette)
		
		self.progressbar.setFormat(u"Chargement terminé")
		
		codec0 = QtCore.QTextCodec.codecForName("UTF-16");
		tmp= self.webView.page().mainFrame().toPlainText()
		self.message= unicode(codec0.fromUnicode(tmp), 'UTF-16')
		monurl = unicode(codec0.fromUnicode(self.urlbar.text()), 'UTF-16')
		
		print "Self.message unicode : " + str(isinstance(self.message, unicode))
		
		self.source.setPlainText(QApplication.translate("Navilangue",
								unicode(self.webView.page().mainFrame().toHtml()).encode('utf-8'),
								None,
								QApplication.UnicodeUTF8))
								
		self.plain.setPlainText(QApplication.translate("Navilangue", self.message,
								None, QApplication.UnicodeUTF8))
		
		self.buttonAdd.setEnabled(True)
								
		self.MainWindow.setWindowTitle(QtGui.QApplication.translate("Navilangue",
										unicode(self.webView.title()).encode('utf-8')+" | Navilangue - Arthur Lapraye 2014",
										None, QtGui.QApplication.UnicodeUTF8))
		self.MainWindow.setWindowIcon(self.webView.icon())
		
		self.dico.setText(dico(self.message,monurl))
		
		trig = trigram(self.message)
		dists =dist(self.message)
		
		statmsg =  u'<html><head><title>Statistiques du Navilangue pour' + monurl + u'</title></head><body>'
		statmsg	+= u'<h1>Statistiques pour '+ monurl +'</h1>'
		statmsg += u'<h2>Distances en termes de fréquences de trigrammes</h2>\n\n'
		statmsg += '\n<table><tr><th>Rang</th><th>Langue</th><th>Distance</th></tr>'
		#print "Hello Statmsg unicode ? " + str(isinstance(statmsg, unicode))
		#print "URLbar unicode ? " + str(isinstance(monurl, unicode))
		p=0
		for z in sorted(dists, key=dists.get, reverse=False):
			p+=1
			statmsg = statmsg + u'\n<tr><td>' + str(p) + u' </td><td>' + z + u'</td> <td>' + str(dists[z]) + "</td></tr>"
		
		statmsg = statmsg + u'</table>\n\n<h2 id="Trig">Trigrammes les plus fréquents dans ce texte</h2>\n'
		
		statmsg += u'<table><tr><th>Fréquence</th><th>Trigramme</th></tr>\n'
		
		p = 0
		
		for x in sorted(trig, key=trig.get, reverse=True):
			if p < 100:
				statmsg =  statmsg + u'\n<tr><td>' + str(trig[x]) + u'</td> <td>' + x + '</td></tr>'
				p += 1
		
		statmsg += u'</table></body></html>'
		
		#print "Full Statmsg unicode ?" + str(isinstance(statmsg, unicode))
		self.stats.setHtml(statmsg) #QApplication.translate("Navilangue",statmsg, None, QApplication.UnicodeUTF8))
		print monurl, u"chargée"
		




