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

import sys
import re
from collections import defaultdict,MutableMapping
from lxml import etree

class synonymes(MutableMapping):
	def __init__(self,*args, **kwargs):
		dic=defaultdict(set)
		wolf = etree.parse("../wolf-1.0b4 (1).xml")
		
		for x in wolf.findall("SYNSET"):
			for id in x.findall("ID"):
				for z in x.findall("SYNONYM"):
					for y in z.findall("LITERAL"):
						if y.text:
							if y.text != "_EMPTY_":
								# print y.text.encode("utf-8")
								dic[id.text].add(re.sub("[ 	]+","_",y.text))
		

		
		self.syns=defaultdict(set)
		for id in dic:
			for mot in dic[id]:
				self.syns[mot].update(dic[id])
					
		# input = "gul baba"
		# while input <> "\n":
			# input = raw_input("Mot:>")
			# print syns[input.decode("utf-8")]
			
		# print len(self.syns)
		
	def __getitem__(self, key):
		return self.syns[key]

	def __setitem__(self, key, value):
		self.syns[key] = value

	def __delitem__(self, key):
		del self.syns[key]

	def __iter__(self):
		return iter(self.syns)

	def __len__(self):
		return len(self.syns)

	def __keytransform__(self, key):
		return key

if __name__ == "__main__":
	toto=synonyms()
	input = True
	while input <> "\n":
		input=raw_input("Mot:>")
		print toto[input.decode("utf-8")]


		
		