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
import unidecode
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

NUMTOPICS=int(sys.argv[1])
NUMPASS=int(sys.argv[2])
COLLS=eval(sys.argv[3])
SEUILPROBA =0.5


np.random.seed(42)

stoplist=set([u"d",u"c",u"l",u"ou",u"suis",u"je",u"",u"ce",u"cet",u"cette",u"n",u"et",u"de",u"du",u"le",u"la",u"les",u"un",u"une",u"d'",u"des",u"que",u"c'est",u"est",u"faire",
u"pour",u"cela",u"ça",u"ca",u"a",u"à",u"aux",u"été",u"on","si",u"en",u"ont",u"sa",u"son",u"plus",u"qu",u"l","il",u"j",u"y",u"se",u"qui",u"comme",u"comment",'avec',u"fait",u"été"])
# print "\""+ u"\",\"".join(sorted(list(stoplist))) + "\""
print u"Nombre de groupes :",NUMTOPICS,"Passes :",NUMPASS,"Collocations :",COLLS,"Seuil :",SEUILPROBA
print

tok=re.compile(u"[ &*,;:.'^?!\/)(-><]+",flags=re.UNICODE)


# wb = xl.load_workbook("../QO10 - Copie.xlsx", guess_types=True)
# for row in wb['A1']:
	# text.insert(t.END, u" | ".join([ unicode(cell.value)  for cell in row])+"\n")
	# if row[2].value:
		# corpus[row[1].value]=unicode(row[2].value)
	
# texts=[ [word for word in corpus[x].lower().split()  ] for x in corpus ]	


corpus=dict()
with open("../241013efs_all.csv") as openfile:
	z=csv.reader(openfile,delimiter=";", quotechar="\"")
	t=0
	for i,x in enumerate(z):
		# if x[-54]:
			#print i,x[58]
		corpus[i]=x[58]
		t += 1
			# sys.exit(0)


def tokenize(corpus,bigrams=False):
		
	i=0
	texts=list()
	identifiant=dict()

	for x in corpus:
		identifiant[i]=x
		elem=[]
		prev="DEB"
		for word in tok.split(corpus[x].lower()):
			#print word.encode("utf-8")
			if word not in stoplist and word != "à":
				elem.append(word)
				
				if bigrams:
					elem.append(prev+"_-_"+word)
					prev=word
		
		if bigrams:
			elem.append(prev+"_-_END")	
		
		texts.append(elem)
		i += 1
	
	return texts

	
def collocs(texts):
	prev=texts
	bigram = models.Phrases(texts)
	texts=map(lambda x : bigram[x],texts)
	
	# if not texts:
		# raise NoTextError

	if prev == texts:
		return texts
	else:
		return collocs(texts)

#texts=collocs(texts)

if COLLS:
	texts = collocs(tokenize(corpus))
else:
	texts= tokenize(corpus,bigrams=False) #

# print texts
# print len([x for x in texts if len(x) > 0])

if True:
	dictionary = corpora.Dictionary(texts)
	bow = [dictionary.doc2bow(text) for text in texts]

	tfidf = models.TfidfModel(bow)
	corpus_tfidf = tfidf[bow]
	

	lda=models.ldamodel.LdaModel(corpus=corpus_tfidf, id2word=dictionary, num_topics=NUMTOPICS,update_every=0, chunksize=5000, passes=NUMPASS)
	#lda.show_topics(30))
	groups=defaultdict(list)
	
	data = lda[bow]

	
	t=dict()
	c=dict()
	
	for i in corpus:
		for topic,confid in lda[bow[i]]:
			t[topic]=t.get(topic,[]) + [(i,confid)]
			c[i] = t.get(i, []) + [(topic,confid)]
	
	for topic in t:
		print "\n------------------------------",topic,"-----------------------------------"
		print "\tMots les plus probables : ",",".join([ dictionary[x].encode("utf-8") for x,y in lda.get_topic_terms(topic) ]),"\n"
		# print unicode(lda.print_topic(topic))
		print "Code\tRang\tN°\tProba\tVerbatim"
		for j,(i,confid) in enumerate(sorted( ((i,confid) for (i,confid) in t[topic] if confid > SEUILPROBA), key=lambda x : x[1], reverse=True) ):	
			print str(topic)+"\t"+str(j)+"\t"+str(i)+"\t"+str(confid)+"\t"+corpus[i]
			
		# raw_input("\n>")

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
	
	
	# lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=10 )
	# corpus_lsi = lsi[corpus_tfidf]
	
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
