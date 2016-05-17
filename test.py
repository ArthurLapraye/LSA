#!/usr/bin/python -i
#-*- encoding: utf-8 -*-
#Copyright Arthur Lapraye 2016
#TODO : coller une licence compatible avec tout ça (à faire à la fin)

import openpyxl as xl #Licence MIT / Expat
# import Tkinter as t

import numpy as np #Licence BSD
import scipy.stats as stats #Licence BSD
import matplotlib.pyplot as plt #Licence matplotlib basée sur la PSF http://matplotlib.org/users/license.html
import matplotlib as mpl 
from gensim import corpora, models, similarities,matutils #Licence LGPL (check version)
from sklearn.manifold import MDS  #BSD license
from sklearn.cluster import KMeans as km, AgglomerativeClustering as AC, SpectralClustering as SC

#Librairie standard
#Licence PSF - (Python Software Foundation )
import sys
import logging
import csv
import re
from unidecode import unidecode
import os  # for os.path.basename
from pprint import pprint
from collections import defaultdict #Idem

from collocs import collocs,col1

#module local
from synonyms import synonymes

#Variables globales
stoplist=set([u"","","",
u"a","a",
u"as","as",
u"ai","ai", 
u"au","au", 
u"aux","aux", 
u"avec","avec", 
u"avoir","avoir",
u"c","c", 
u"c'est","c'est",
u"ça","ça", 
u"ca","ca", 
u"ces","ces",
u"ce","ce", 
u"cela","cela", 
u"cet","cet",
u"ci","ci",
u"cette","cette",
u"comme","comme",
u"comment","comment",
u"cln","cln",u"clr","clr",u"cla","cla",u"cld","cld",
u"d","d","d",
u"d'","d'",
u"dans","dans",
u"de","de",
u"des","des",
u"du","du",
u"en","en",
u"est","est",
u"et","et",
u"faire","faire",
u"fait","fait",
u"il","il",
u"j","j",
u"je","je",u"j","j",
u"l","l",
"lui",
u"la","la",
u"là","là",
u"le","le",
u"les","les",
u"lf","lf",
u"m","m",
u"mon","mon",
u"me","me",
u"ma","ma",
u"mais","mais",
u"moi","moi",
u"n","n",
u"ne","ne",
u"on","on",
u"ont","ont",
u"ou","ou",
u"où","où",
u"parce","parce",
u"plus","plus",
u"pas","pas",
u"pour","pour",
u"par","par",
u"qu","qu",
u"que","que",
u"qui","qui",
u"quot","quot",
u"r","r",
u"sur","sur",
u"s","s",
u"sa","sa",
u"se","se",u"sep","sep",
u"si","si",
u"son","son",
u"suis","suis",
u"très","très",
u"un","un",
u"une","une",
u"y","y",
u"à","à",
u"ça","ça", 
u"été","été",
u"être",
u"vous"])

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
NUMTOPICS=int(sys.argv[1])
NUMPASS=int(sys.argv[2])
SEUILPROBA =0.3
SEUILMOT=0.75
MINIMUM=2
np.random.seed(42)
FICHIER="../241013efs_all.csv"

lemmatiseur=defaultdict(set)
l2=defaultdict(set)

with open("../lefff-3.4.mlex/lefff-3.4.mlex") as lexique:
	lefff=csv.reader(lexique,delimiter="\t",quotechar=None)
	for x in lefff:
		if x[0] not in stoplist and x[2] not in stoplist:
			lemmatiseur[x[0].decode("utf-8")].add(x[2].decode("utf-8"))
	
for u in lemmatiseur:
	if unidecode(u) not in lemmatiseur:
		l2[unidecode(u)].update(lemmatiseur[u])
		
lemmatiseur.update(l2)

logging.info("Lemmatiseur fini de charger !")

syno=synonymes()

logging.info("Dictionnaire de synonymes chargés")

# print "\""+ u"\",\"".join(sorted(list(stoplist))) + "\""
print u"Nombre de groupes :\t",NUMTOPICS,"\nPasses :\t",NUMPASS,"\nSeuil :\t",SEUILPROBA,"\nSeuil mot:\t",SEUILMOT


def loadfile(filename):
	_,ext=filename.split(".")
	
	corpus=dict()
	i=0
	
	if ext == "csv":
		with open(filename) as openfile:
			z=csv.reader(openfile,delimiter=";", quotechar="\"")
			col=int(raw_input("Donnez la colonne à analyser."))
			for x in z:
				if x[col]:
					corpus[i]=x[col].decode("utf-8")
					i += 1

	
	elif ext == "xlsx":
		wb = xl.load_workbook(filename, guess_types=True)
		feuille=raw_input("Donner le nom de la feuille")
		col=int(raw_input("Donnez la colonne à analyser."))
		for row in wb[feuille]:
			if row[col].value:
				uuid=row[1].value
				corpus[i]=unicode(row[col].value)
				i += 1

	else:
		logging.critical("Type de fichier non reconnu")
		sys.exit(-1)
	
	return corpus

		
# with open("") 
			
def tokenize(corpus):
	
	total,lemma=0.0,0.0
	tok=re.compile(u"[0-9#*+\[\]_\" &*,;:.'^?!\/)(><-]+",flags=re.UNICODE)
	texts=list()
	
	lexicon=defaultdict(float)
		
	for x in corpus:
		elem=[]
		for word in tok.split(corpus[x].lower()):
			if word not in stoplist:
				total += 1.0
				if word in lemmatiseur:
					if lemmatiseur[word] not in stoplist:
						elem += lemmatiseur[word]
						lemma += 1
						for x in lemmatiseur[word]:
							lexicon[x] += 1
				else:
					elem.append(word)
					lexicon[word] += 1
		
		texts.append(elem)
		
	return texts


corpus=loadfile(FICHIER)
logging.info("Corpus chargé")

logging.info("Tokenisation")

texts= tokenize(corpus)

if True:
	dictionary = corpora.Dictionary(texts)
	
	once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq == 1]
	dictionary.filter_tokens(once_ids)
	dictionary.filter_extremes(no_below=MINIMUM,no_above=SEUILMOT)
	dictionary.compactify()
	
	bow = [dictionary.doc2bow(text) for text in texts]

	tfidf = models.TfidfModel(bow)
	corpus_tfidf = tfidf[bow]
	

	lda=models.ldamodel.LdaModel(corpus=corpus_tfidf, id2word=dictionary, num_topics=NUMTOPICS,update_every=0, chunksize=4000, passes=NUMPASS, alpha='auto', eta='auto', minimum_probability=SEUILPROBA)
	# lda.show_topics(30))
	# groups=defaultdict(list)
	
	# lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=	NUMTOPICS )
	# corpus_lsi = lsi[corpus_tfidf]	
	

	
	t=dict()
	c=defaultdict(list)
	# reliquat=0
	for i in corpus:
		for topic,confid in lda[corpus_tfidf[i]]:
			t[topic]=t.get(topic,[]) + [(i,confid)]
			c[i].append( (topic,confid) )
	
	print "Reliquat\t"+str(len(corpus)-len(c))
	print "Classés:\t"+str(len(c))
	print
	print "Code\tMots clefs\t"
	
	for n,topic in enumerate(sorted(t,key=lambda topic : len([x for x,y in t[topic] ]), reverse=True)):
		print str(topic)+"\t"+",".join([ dictionary[x].encode("utf-8") for x,y in lda.get_topic_terms(topic) ])+"\t"+"=NB.SI(C"+str(11+NUMTOPICS)+":H1048576;"+str(topic)+")"+"\t"+"=C"+str(9+n)+"/($B$6+$B$5)\t"
		# print "\n+",n,"------------------------------",topic,"-----------------------------------"
		# print "\tMots les plus probables : ",",".join([ dictionary[x].encode("utf-8") for x,y in lda.get_topic_terms(topic) ]),"\n"
		# print "Code\tRang\tN°\tProba\tVerbatim"
		# stop=True
		# for j,(i,confid) in enumerate(sorted(t[topic],key=lambda (x,y) : y, reverse=True)):
			
			# if confid > SEUILPROBA and stop:
				# print str(topic)+"\t"+str(j)+"\t"+str(i)+"\t"+str(confid)+"\t"+corpus[i].encode("utf-8") #,sorted(c[i],key=lambda (x,y) : y, reverse=True)
				# seen.add(i)
			# elif i not in seen:
				# reliquat += 1
				# seen.add(i)
	print
	print "numero\tverbatim\tcode\tcode\tcode\tcode\tcode\tcode"
	for element in corpus:
		print str(element)+"\t"+corpus[element].encode("utf-8")+"\t"+"\t".join([str(x) for x,y in c[element]])
	


"""Idées : 
Correcteur d'orthographe online (?) basé sur une distance de levenshtein, pour remplacer l'absence de lemmatiseur.
=> Peut-etre rajouter les mots proches présents dans le corpus (e,g sauvé sera rajouter à ce qui contient sauver etc... sans doute une mauvaise idée mais à tester)
 
Changer le système de seuil si c'est des probas pour permettre l'attribution automatique de plusieurs codes

Système de re-classification : dégager les sujets dans un 1er temps puis les utiliser pour reclasser le reste. 

Créer un système pour permettre d'identifier les synonymes du corpus +> FAIT (et ça marche pas)

Pré-traitement semi-manuel (?) sur les entités nommées : parfois pertinent de remplacer tout nom de localité par VILLE pour meilleurs regroupements statistiques
"""

#TODO : Utiliser différents autres corpus de taille variable + créer une interface de chargement moins merdique. Graphique ? 
