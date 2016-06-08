#!/usr/bin/python
#-*- encoding: utf-8 -*-
#Arthur Lapraye - copyright 2016
# This file is part of X-TAL.

# X-TAL is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# X-TAL is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with X-TAL.  If not, see <http://www.gnu.org/licenses/>. 

import csv
import logging
import re
from unidecode import unidecode


class Lemmtok(object):
	def __init__(self,LEFFFPATH):
	
		self.stoplist=set([u"","","",u"a","a",u"as","as",u"ai","ai",u"au","au",u"aux","aux",u"avec","avec",u"avoir","avoir",u"c","c",u"c'est","c'est",u"ça","ça",u"ca","ca",u"ces","ces",u"ce","ce",u"cela","cela",u"cet","cet",u"ci","ci",u"cette","cette",u"comme","comme",u"comment","comment",u"cln","cln",u"clr","clr",u"cla","cla",u"cld","cld",u"d","d","d",u"d'","d'",u"dans","dans",u"de","de",u"des","des",u"du","du",u"en","en",u"est","est",u"et","et",u"faire","faire",u"fait","fait",u"il","il",u"j","j",u"je","je",u"j","j",u"l","l","lui",u"la","la",u"là","là",u"le","le",u"les","les",u"lf","lf",u"m","m",u"mon","mon",u"me","me",u"ma","ma",u"mais","mais",u"moi","moi",u"n","n",u"ne","ne",u"on","on",u"ont","ont",u"ou","ou",u"où","où",u"parce","parce",u"plus","plus",u"pas","pas",u"pour","pour",u"par","par",u"qu","qu",u"que","que",u"qui","qui",u"quot","quot",u"r","r",u"sur","sur",u"s","s",u"sa","sa",u"se","se",u"sep","sep",u"si","si",u"son","son",u"suis","suis",u"très","très",u"un","un",u"une","une",u"y","y",u"à","à",u"ça","ça",u"été","été",u"être",u"vous"])
		
		self.lemmatiseur=dict()
		self.formes=dict()
		self.l2=dict()
		self.cats=set()

		with open(LEFFFPATH) as lexique:
			
			for x in csv.reader(lexique,delimiter="\t",quotechar=None):
				if True:
					forme=x[0].decode("utf-8")
					cat= x[1].decode("utf-8")
					lemme=x[2].decode("utf-8").upper()+"."+cat
					self.cats.add(cat)
					if forme in self.lemmatiseur:
						self.lemmatiseur[forme].add(lemme)
					else:
						self.lemmatiseur[forme]={lemme}
					if lemme in self.formes:
							self.formes[lemme].add(forme)
					else:
						self.formes[lemme]={forme}
			
		for u in self.lemmatiseur:
			sansaccent=unidecode(u)
			if sansaccent not in self.lemmatiseur:
				if sansaccent not in self.l2:
					self.l2[sansaccent]=self.lemmatiseur[u]
				else:
					self.l2[sansaccent].update(self.lemmatiseur[u])
				
		self.lemmatiseur.update(self.l2)

		logging.info("Le lemmatiseur fini de charger !")
	
		
	def toklemize_corpus(self,corpus,case_sensitive=False):
		texts=list()
		
		for x in corpus:
			elem=self.toklemize(corpus[x],case_sensitive)
			texts.append(elem)
			
		return texts
	
	def toklemize(self,chaine,case_sensitive=False,prune_stopwords=True):
		tok=re.compile(u"[#*+\[\]_\" &*,;:.'^?!\/)(><-]+",flags=re.UNICODE)
		elem=[]
		chaine=re.sub("[0-9]+"," \1 ",chaine,0)
		if not case_sensitive:
			chaine=chaine.lower()
		
		if prune_stopwords:
			stoplist=self.stoplist
		else:
			stoplist=[]
		
		for word in tok.split(chaine):
				if word not in stoplist:
					if word in self.lemmatiseur:
						if self.lemmatiseur[word] not in stoplist:
							elem += self.lemmatiseur[word]
					else:
						elem.append(word)
						#lexicon[word] += 1
		return elem
	
	def tokenize(self,string):
		tok=re.compile(u"[#*+\[\]_\" &*,;:.'^?!\/)(><-]+",flags=re.UNICODE)
		return tok.split(string.lower() )

	def index(corpus):
		raise NotImplementedError

if __name__=="__main__":
	import sys
	LEFFFPATH=sys.argv[1]
	lt=Lemmtok(LEFFFPATH)
	print lt.cats
	while 1:
		try:
			entr=raw_input(">>>").decode("utf-8")
			out=lt.lemmatiseur[entr]
			print out
		except KeyError:
			print "Erreur : mot inconnu"
		except EOFError:
			print
			break
