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

if __name__=="__main__":
	"""
		output : corpus collocs
		
		à intégrer avec le système de recherche
		
	"""