
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
		
#Arthur Lapraye - copyright 2016