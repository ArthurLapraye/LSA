#!/usr/bin/python -i
#-*- encoding: utf-8 -*-

import openpyxl as xl
# import Tkinter as t
from gensim import corpora, models, similarities
from pprint import pprint

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

stoplist=["de","la","le","les","un","des","du","à"]

corpus=dict()



for row in wb['A1']:
	#text.insert(t.END, u" | ".join([ unicode(cell.value)  for cell in row])+"\n")
	if row[2].value:
		corpus[row[1].value]=row[2].value
	
texts=[ [word for word in unicode(corpus[x]).lower().split() if word not in stoplist] for x in corpus ]	

dictionary = corpora.Dictionary(texts)
#print(dictionary)
corpus = [dictionary.doc2bow(text) for text in texts]
#print(corpus)

tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]

lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=30)
corpus_lsi = lsi[corpus_tfidf]
pprint(lsi.show_topics(10))

#for doc in corpus_lsi:
#	print doc

index = similarities.MatrixSimilarity(lsi[corpus])

print corpus_lsi[0]

#text.pack( side = t.LEFT, fill = t.BOTH, expand=1 )
#scroll2.config( command = text.xview )
#scrollbar.config( command = text.yview )
#text.pack()
#root.mainloop()
