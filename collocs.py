#!/usr/bin/python
#-*- encoding: utf-8 -*-
#Copyright Arthur Lapraye 2016
from gensim import models

#Fonction qui répète la fonction "models.phrases" de Gensim jusqu'au point fixe.
#S'est révélée inutile à l'usage. 

def collocs(texts):
	prev=texts
	bigram = models.Phrases(texts)
	texts=map(lambda x : bigram[x],texts)
	
	if prev == texts:
		return texts
	else:
		return collocs(texts)



def col1(texts):
	prev=texts
	bigram = models.Phrases(texts)
	texts=map(lambda x : bigram[x],texts)
	
	return texts
	

		
#Arthur Lapraye - copyright 2016