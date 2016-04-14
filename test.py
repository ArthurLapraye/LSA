#!/usr/bin/python -i
#-*- encoding: utf-8 -*-

import openpyxl as xl
# import Tkinter as t
from gensim import corpora, models, similarities,matutils
from pprint import pprint
from collections import defaultdict
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

import logging

import unidecode

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import re

wb = xl.load_workbook("../QO10 - Copie.xlsx", guess_types=True)


np.random.seed(42)

#root = t.Tk()
#text = t.Text(root)
#scrollbar = t.Scrollbar(root)
#scrollbar.pack( side = t.RIGHT, fill=t.Y )
#scroll2 = t.Scrollbar(root,orient=t.HORIZONTAL)
#scroll2.pack( side = t.BOTTOM, fill=t.X )


#text = t.Listbox(root, yscrollcommand = scrollbar.set, xscrollcommand=scroll2.set )


#Largely adapted from Gensim documentation
#https://radimrehurek.com/gensim/tut2.html
#

stoplist=set([u"je",u"",u"ce",u"cet",u"cette",u"n",u"et",u"de",u"du",u"le",u"la",u"les",u"un",u"une",u"d'",u"des",u"que",u"c'est",u"est",u"faire",
u"pour",u"cela",u"ça",u"ca",u"a",u"à",u"en",u"ont",u"sa",u"son",u"plus",u"qu",u"l","il",u"j",u"y",u"se",u"qui",u"comme",u"comment"])
#print "\""+ "\",\"".join(sorted(list(stoplist))) + "\""

corpus=dict()

tok=re.compile(u"[ ,;:.'^?!/)(-]+",flags=re.UNICODE)


for row in wb['A1']:
	#text.insert(t.END, u" | ".join([ unicode(cell.value)  for cell in row])+"\n")
	if row[2].value:
		corpus[row[1].value]=unicode(row[2].value)
	
# texts=[ [word for word in corpus[x].lower().split()  ] for x in corpus ]	

identifiant=dict()

texts=list()

i=0


for x in corpus:
	identifiant[i]=x
	elem=[]
	# prev="DEB"
	for word in tok.split(corpus[x].lower()):
		#print word.encode("utf-8")
		if word not in stoplist:
			elem.append(word)
			# prev=word
		
	# elem.append(word)	
	
	texts.append(elem)
	i += 1

#print texts 

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

texts=collocs(texts)

# print texts

if True:
	dictionary = corpora.Dictionary(texts)
	bow = [dictionary.doc2bow(text) for text in texts]

	tfidf = models.TfidfModel(bow)
	corpus_tfidf = tfidf[bow]
	
	# print corpus_tfidf
	
	# zek=models.ldamodel.LdaModel(corpus=corpus_tfidf, id2word=dictionary, num_topics=5) #update_every=5, chunksize=200, passes=5)
	# pprint(zek.show_topics(5))
	# groups=defaultdict(list)
	
	# lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=10 )
	# corpus_lsi = lsi[corpus_tfidf]
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
	
	# t=dict()
	
	# for i in identifiant:
		# for topic,confid in sorted(lsi[bow[i]],key=lambda x : x[1], reverse=True)[:3]:
			# t[topic]=t.get(topic,[]) + [(corpus[identifiant[i]].encode("utf-8"),confid)]
	
	# for topic in t:
		# for pair in t[topic]:
			# print topic,pair
			
		# raw_input()

	# for similarities in index[:3]:
		# print similarities

#dictionary = corpora.Dictionary(line.lower().split() for line in open('corpus.txt','rb'))
	once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq == 1]
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


