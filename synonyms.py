#!/usr/bin/python -i
#-*- encoding: utf-8 -*-
#Copyright Arthur Lapraye 2016

from lxml import etree
import sys


wolf = etree.parse("../wolf-1.0b4 (1).xml")

for x in wolf.findall("SYNSET"):
	for id in x.findall("ID"):
		print id.text
	print
	for z in x.findall("SYNONYM"):
		for y in z.findall("LITERAL"):
			if y.text:
				if y.text != "_EMPTY_":
					print y.text.encode("utf-8")
			else:
				print >> sys.stderr, "Attention : valeur none pour",x,y
		
		print
		
	print