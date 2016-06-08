#!/usr/bin/python -i
#-*- encoding: utf-8 -*-
#Copyright Arthur Lapraye 2016
#TODO : coller une licence compatible avec tout ça (à faire à la fin)

import openpyxl as xl #Licence MIT / Expat

import numpy as np #Licence BSD
import scipy.stats as stats #Licence BSD
from gensim import corpora, models, similarities,matutils #Licence LGPL (check version)

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


#module local
from collocs import collocs,col1
from synonyms import synonymes
from lemmtok import Lemmtok

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def loadfile(filename):
	name, ext=os.path.splitext(filename)
	
	corpus=dict()
	i=0
	
	if ext == ".csv":
		with open(filename) as openfile:
			z=csv.reader(openfile,delimiter=";", quotechar="\"")
			col=int(raw_input("Donnez la colonne à analyser."))
			for x in z:
				if x[col]:
					corpus[i]=x[col].decode("utf-8")
					i += 1

	
	elif ext == ".xlsx":
		wb = xl.load_workbook(filename, guess_types=False)
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

if __name__ == "__main__":
	NUMTOPICS=int(sys.argv[2])
	NUMPASS=int(sys.argv[3])
	SEUILPROBA =0.3
	SEUILMOT=0.95
	MINIMUM=2
	np.random.seed(42)
	FICHIER=sys.argv[1]

	print u"Nombre de groupes :\t",NUMTOPICS,"\nPasses :\t",NUMPASS,"\nSeuil :\t",SEUILPROBA,"\nSeuil mot:\t",SEUILMOT
	lemmtok=Lemmtok(os.path.dirname(os.path.realpath(__file__))+"/"+"../lefff-3.4.mlex/lefff-3.4.mlex")
		
	corpus=loadfile(FICHIER)
	logging.info("Corpus chargé")
	texts= lemmtok.toklemize(corpus)	
	logging.info("Tokenisation effectuée")


	dictionary = corpora.Dictionary(texts)
	dictionary.filter_extremes(no_below=MINIMUM,no_above=SEUILMOT)
	dictionary.compactify()
	bow = [dictionary.doc2bow(text) for text in texts]
	corpus_tfidf =  models.TfidfModel(bow)[bow]
	

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
	
