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

stoplist=set(["de","la","le","les","un","des","du","à","cela","ça","est","alors","au","aussi","autre","avant","avec","avoir","bon","car","ce","cela","ces","ceux","chaque","ci","comme",
"comment","dans","des","du","dedans","dehors","depuis","donc","dos","début","elle","elles","en","encore","essai","est","et","eu","fait","faites","fois","font","hors","ici","il","ils",
"je","la","le","les","leur","là","ma","maintenant","mais","mes","mine","moins","mon","mot","même","ni","nommés","notre","nous","ou","où","par","parce","pas","peut",
"peu","plupart","pour","pourquoi","quand","que","quel","quelle","quelles","quels","qui","sa","sans","ses","seulement","si","sien","son","sont","soyez","sur","ta","tandis",
"tellement","tels","tes","ton","tous","tout","trop","très","tu","vont","votre","vous","vu","ça","étaient","état","étions","été","être"])

corpus=dict()



for row in wb['A1']:
	#text.insert(t.END, u" | ".join([ unicode(cell.value)  for cell in row])+"\n")
	if row[2].value:
		corpus[row[1].value]=unicode(row[2].value)
	
texts=[ [word for word in corpus[x].lower().split("' .;:\t") ] for x in corpus ]	

print texts 

bigram = models.Phrases(texts)

raw_input()

print bigram

if False:

	dictionary = corpora.Dictionary(texts)
	#print(dictionary)
	corpus = [dictionary.doc2bow(text) for text in texts]
	#print(corpus)

	tfidf = models.TfidfModel(corpus)
	corpus_tfidf = tfidf[corpus]

	lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=20)
	corpus_lsi = lsi[corpus_tfidf]
	pprint(lsi.show_topics(20))

	#for doc in corpus_lsi:
	#	print doc

	index = similarities.MatrixSimilarity(lsi[corpus])

	#print corpus_lsi[0]

	#text.pack( side = t.LEFT, fill = t.BOTH, expand=1 )
	#scroll2.config( command = text.xview )
	#scrollbar.config( command = text.yview )
	#text.pack()
	#root.mainloop()
