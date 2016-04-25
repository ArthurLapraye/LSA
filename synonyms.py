#!/usr/bin/python -i
#-*- encoding: utf-8 -*-
#Copyright Arthur Lapraye 2016

from lxml import etree


wolf = etree.parse("../wolf-1.0b4 (1).xml")

print(len(wolf.findall("SYNSET")))