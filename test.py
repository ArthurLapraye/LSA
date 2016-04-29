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



logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

#root = t.Tk()
#text = t.Text(root)
#scrollbar = t.Scrollbar(root)
#scrollbar.pack( side = t.RIGHT, fill=t.Y )
#scroll2 = t.Scrollbar(root,orient=t.HORIZONTAL)
#scroll2.pack( side = t.BOTTOM, fill=t.X )

#text = t.Listbox(root, yscrollcommand = scrollbar.set, xscrollcommand=scroll2.set )


#Variables globales

NUMTOPICS=int(sys.argv[1])
NUMPASS=int(sys.argv[2])
SEUILPROBA =0.15

np.random.seed(42)
 #Idiosyncrasie du LEFFF, à corriger pour éviter collision avec acronymes
stoplist=set([u"",
u"a",
"as",
u"ai", 
u"au", 
u"aux", 
u"avec", 
u"avoir",
u"c", 
u"c'est",
u"ça", 
u"ca", 
u"ces",
u"ce", 
u"cela", 
u"cet",
u"ci",
u"cette",
u"comme",
u"comment",
u"cln",u"clr",u"cla",u"cld",
u"d",
u"d'",
u"dans",
u"de",
u"des",
u"du",
u"en",
u"est",
u"et",
u"faire",
u"fait",
u"il",
u"j",
u"je",u"j",
u"l",
"lui",
u"la",
u"là",
u"le",
u"les",
u"lf",
u"m",
u"mon",
u"me",
u"ma",
u"mais",
u"moi",
u"n",
u"ne",
u"on",
u"ont",
u"ou",
u"où",
u"parce",
u"plus",
u"pas",
u"pour",
u"par",
u"qu",
u"que",
u"qui",
u"quot",
u"r",
u"sur",
u"s",
u"sa",
u"se",u"sep",
u"si",
u"son",
u"suis",
u"un",
u"une",
u"y",
u"à",
u"ça", 
u"été",
u"être"
u"vous"])

lemmatiseur=defaultdict(set)
l2=defaultdict(set)

with open("../lefff-3.4.mlex/lefff-3.4.mlex") as lexique:
	lefff=csv.reader(lexique,delimiter="\t",quotechar=None)
	for x in lefff:
		if x[0] not in stoplist:
			lemmatiseur[x[0].decode("utf-8")].add(x[2].decode("utf-8"))
	
for u in lemmatiseur:
	if unidecode(u) not in lemmatiseur:
		l2[unidecode(u)].update(lemmatiseur[u])
		
lemmatiseur.update(l2)
			


# print "\""+ u"\",\"".join(sorted(list(stoplist))) + "\""
print u"Nombre de groupes :",NUMTOPICS,"Passes :",NUMPASS,"Seuil :",SEUILPROBA
print


corpus=dict()
i=0

# wb = xl.load_workbook("../QO10 - Copie.xlsx", guess_types=True)
# for row in wb['A1']:
	# if row[2].value:
		# uuid=row[1].value
		# corpus[i]=unicode(row[2].value)
		# i += 1


		
with open("../241013efs_all.csv") as openfile:
	z=csv.reader(openfile,delimiter=";", quotechar="\"")
	for x in z:
		if x[58]:
			corpus[i]=x[58].decode("utf-8")
			i += 1

			
			
def tokenize(corpus):
	
	total,lemma=0.0,0.0
	tok=re.compile(u"[ &*,;:.'^?!\/)(-><]+",flags=re.UNICODE)
	texts=list()
	identifiant=dict()
		
	for x in corpus:
		elem=[]
		for word in tok.split(corpus[x].lower()):
			if word in stoplist:
				#print word.encode("utf-8")
				pass
			else:
				total += 1.0
				if word in lemmatiseur:
					if lemmatiseur[word] not in stoplist:
						elem += lemmatiseur[word]
						if len(lemmatiseur[word]) > 1:
							print >> sys.stderr, "Warning : more than 1 lemma",word.encode("utf-8")
						lemma += 1
				else:
					elem.append(word)
		
		texts.append(elem)
	
	print "Tokens :",total
	print "Lemmatisés",lemma
	return texts

	
# def distdl(a,b):
	# d=defaultdict(float)
	# cost=0
	
	# for i in xrange(-1,len(a)):
		# d[i, 0] = i
	# for j in xrange(-1,len(b)):
		# d[(0, j)] = j
	
	# for i in range(0,len(a)):
		# for j in range(0,len(b)):
			# if a[i] == b[j]:
				# cost = 0
			# else:
				# cost = 1
			# d[i, j]= min(d[i-1, j] + 1,d[i, j-1] + 1,d[i-1, j-1] + cost)
			
			# if i > 1 and j > 1 and a[i] == b[j-1] and a[i-1] == b[j]:
				# d[i, j] = min(d[i, j],d[i-2, j-2] + cost)
			
	# return d[len(a)-1, len(b)-1]
	
texts= tokenize(corpus) #

# print texts
# print len(texts)
# print len([x for x in texts if len(x) > 0])

# lexicon=defaultdict(float)
# for t in texts:
	# for w in t:
		# lexicon[w] += 1

# for elem in sorted(stoplist):
	# print elem.encode("utf-8")

# for w in sorted(lexicon,key=lambda x : lexicon[x], reverse=True):
	# print w,lexicon[w]
	
# dist=dict()
	
# for keys in lexicon:
	# for clefs in lexicon:
		# if clefs != keys:
			# dist[clefs,keys]=distdl(clefs,keys)

if True:
	dictionary = corpora.Dictionary(texts)
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

	
	# seen=set()
	for n,topic in enumerate(sorted(t,key=lambda topic : len([x for x,y in t[topic] ]), reverse=True)[:10]):
		print str(n)+"\t"+str(topic)+"\t"+",".join([ dictionary[x].encode("utf-8") for x,y in lda.get_topic_terms(topic) ])+"\t"+"=NB.SI(C17:H1048576;"+str(topic)+")"+"\t"
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
	
	
	
	
	
	print "Reliquat",len(corpus)-len(c)
	print "Classés: ",len(c)
	
	
	# data = lda[bow]
			# kmodel=km(n_clusters=10,n_init=100)
	# kmodel = SC(n_clusters=10,n_neighbors=20)
	# print len(dictionary)
	# densetf = matutils.corpus2dense(corpus_tfidf,num_terms=len(dictionary))
	# kmodel.fit(densetf)
	
	# clusters = kmodel.labels_.tolist()

	#for i,elem in enumerate(clusters):
		# print elem,unicode(corpus[identifiant[i]]).encode("utf-8")
	
	# raw_input()
	
	# for i,elem in enumerate(kmodel.predict(densetf)):
		# print unicode(corpus[identifiant[i]]).encode("UTF-8"),unicode(elem)
	

	
	# kmodel=km(n_clusters=5)
	# print len(dictionary)
	# kmodel.fit(corpus_lsi)
	
	# for i,elem in enumerate(kmodel.predict(corpus_lsi)):
		# print unicode(corpus[identifiant[i]]).encode("UTF-8"),unicode(elem)
	
	
	# column_labels = range(0,len(dictionary))
	# row_labels = dictionary.keys()
	# data = corpus_tfidf
	
	#From 

	
	# convert two components as we're plotting points in a two-dimensional plane
	# "precomputed" because we provide a distance matrix
	# we will also specify `random_state` so the plot is reproducible.
	
	# MDS()

	# mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)

	# pos = mds.fit_transform(dist)  # shape (n_components, n_samples)

	# xs, ys = pos[:, 0], pos[:, 1]
		
	
	
	# print data
	# fig, ax = plt.subplots()
	# heatmap = ax.pcolor(data, cmap=plt.cm.Blues)

	# put the major ticks at the middle of each cell
	# ax.set_xticks(np.arange(data.shape[0])+0.5, minor=False)
	# ax.set_yticks(np.arange(data.shape[1])+0.5, minor=False)

	# want a more natural, table-like display
	# ax.invert_yaxis()
	# ax.xaxis.tick_top()

	# ax.set_xticklabels(row_labels, minor=False)
	# ax.set_yticklabels(column_labels, minor=False)
	# plt.show()
	
	# print corpus_tfidf
	

	# sims = index[data]
	# sims = sorted(enumerate(sims), key=lambda item: -item[1])
	# print sims
		
		
	# data = np.transpose(matutils.corpus2dense(data, num_terms=100 ))
	
	# plt.matshow(data)
	# plt.show()
	
	
	# pprint(lsi.show_topics(10))

	#for doc in corpus_lsi:
	#	print doc

	# print "toto"
	# index = similarities.MatrixSimilarity(lsi[bow])
	
	# for elt in enumerate(index):
		# print corpus[identifiant[i]],elt
	
	

	#print corpus_lsi

	#text.pack( side = t.LEFT, fill = t.BOTH, expand=1 )
	#scroll2.config( command = text.xview )
	#scrollbar.config( command = text.yview )
	#text.pack()
	#root.mainloop()
	
	# for i,toto in enumerate(bow):
		# print corpus[identifiant[i]].encode("utf-8"),toto,[ dictionary[x] for x,y in toto]
	
	#for x in sorted(dictionary,key= lambda x : len(dictionary[x]), reverse=False) :
	#	print x, dictionary[x].encode("utf-8")
	# for similarities in index[:3]:
		# print similarities

#dictionary = corpora.Dictionary(line.lower().split() for line in open('corpus.txt','rb'))
	# once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq == 1]
	#dictionary.filter_tokens(once_ids)
	#dictionary.filter_extremes(no_above=5,keep_n=100000)
	#dictionary.compactify()
	
	# From http://blog.cigrainger.com/2014/07/lda-number.html

	# class MyCorpus(object):
		# def __iter__(self):
			# for line in open('corpus.txt','r'):
				# yield dictionary.doc2bow(line.lower().split())

	# my_corpus = MyCorpus()

	# l = np.array([sum(cnt for _, cnt in doc) for doc in bow])
	
	# def sym_kl(p,q):
		# return np.sum([stats.entropy(p,q),stats.entropy(q,p)])
 
	# def arun(corpus,dictionary,min_topics=1,max_topics=10,step=1):
		# kl = []
		# for i in range(min_topics,max_topics,step):
			# lda = models.ldamodel.LdaModel(corpus=corpus,id2word=dictionary,num_topics=i)
			# m1 = lda.expElogbeta
			# U,cm1,V = np.linalg.svd(m1)
			# Document-topic matrix
			# lda_topics = lda[bow]
			# m2 = matutils.corpus2dense(lda_topics, lda.num_topics).transpose()
			# cm2 = l.dot(m2)
			# cm2 = cm2 + 0.0001
			# cm2norm = np.linalg.norm(l)
			# cm2 = cm2/cm2norm
			# kl.append(sym_kl(cm1,cm2))
		# return kl
		
	# kl = arun(bow,dictionary,max_topics=100)

	# Plot kl divergence against number of topics
	# plt.plot(kl)
	# plt.ylabel('Symmetric KL Divergence')
	# plt.xlabel('Number of Topics')
	# plt.savefig('kldiv.png', bbox_inches='tight')

"""Idées : 
Correcteur d'orthographe online (?) basé sur une distance de levenshtein, pour remplacer l'absence de lemmatiseur.
=> Peut-etre rajouter les mots proches présents dans le corpus (e,g sauvé sera rajouter à ce qui contient sauver etc... sans doute une mauvaise idée mais à tester)
 
Changer le système de seuil si c'est des probas pour permettre l'attribution automatique de plusieurs codes

Système de re-classification : dégager les sujets dans un 1er temps puis les utiliser pour reclasser le reste. 

Créer un système pour permettre d'identifier les synonymes du corpus

Pré-traitement semi-manuel (?) sur les entités nommées : parfois pertinent de remplacer tout nom de localité par VILLE pour meilleurs regroupements statistiques
"""
#TODO : Examiner le reliquat ; Trier les sujets par nb d'éléments
#TODO : Utiliser différents autres corpus de taille variable + créer une interface de chargement moins merdique. Graphique ?
