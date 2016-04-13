#!/usr/bin/python -i
#-*- encoding: utf-8 -*-

import openpyxl as xl
# import Tkinter as t
from gensim import corpora, models, similarities
from pprint import pprint

import re

wb = xl.load_workbook("../QO10 - Copie.xlsx", guess_types=True)


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

stoplist=set(["","et","de","du","le","la","les","un","une","d'","des","que","c'est","est","faire","pour","cela","ça","ca","a","à","en","ont","sa","son"])
print "\""+ "\",\"".join(sorted(list(stoplist))) + "\""

corpus=dict()

tok=re.compile(u"[ ,;:']+")


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
	for word in tok.split(corpus[x].lower()):
		#print word.encode("utf-8")
		if word not in stoplist:
			elem.append(word)
	
	texts.append(elem)
	i += 1

#print texts 

bigram = models.Phrases(texts)

btexts=map(lambda x : bigram[x],texts)

trigram=models.Phrases(btexts)

#raw_input()

texts = map(lambda x : trigram[x],btexts)

if True:

	dictionary = corpora.Dictionary(texts)
	#print(dictionary)
	bow = [dictionary.doc2bow(text) for text in texts]
	#print(corpus)

	tfidf = models.TfidfModel(bow)
	corpus_tfidf = tfidf[bow]

	lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=10)
	corpus_lsi = lsi[corpus_tfidf]
	pprint(lsi.show_topics(10))

	#for doc in corpus_lsi:
	#	print doc

	index = similarities.MatrixSimilarity(lsi[bow])

	#print corpus_lsi[0]

	#text.pack( side = t.LEFT, fill = t.BOTH, expand=1 )
	#scroll2.config( command = text.xview )
	#scrollbar.config( command = text.yview )
	#text.pack()
	#root.mainloop()
	
	for i,toto in enumerate(corpus):
		print corpus[identifiant[i]],toto
