#!/usr/bin/python -i
#-*- encoding: utf-8 -*-
#Copyright Arthur Lapraye 2016

import sys
import re
from collections import defaultdict
from lxml import etree

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

syns=defaultdict(set)

for id in dic:
	for mot in dic[id]:
		syns[mot].update(dic[id])

		
# input = "gul baba"
# while input <> "\n":
	# input = raw_input("Mot:>")
	# print syns[input.decode("utf-8")]
	
print len(syns)