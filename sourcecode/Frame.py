import xml.etree.ElementTree as ET
from Figure import *
from Rule import *

class Frame:

	def __init__(self, gindex, gfigures):
		self.figures = gfigures
		self.index = gindex

	def __str__(self):
		return "Frame: " + str(self.index)

	def __repr__(self):
		return "<Frame: " + str(self.index) + ">"

	@classmethod
	def deSerializeXML(cls, xmlObject):
		attributes = xmlObject.attrib
		index = None
		for k in attributes.keys():
			if k == 'index' and (k[0] == '(' or k[0].isdigit()):
				index = eval(attributes[k])
			elif k == 'index':
				index = attributes[k]
			else:
				print "attr: " + str(k) + " with value: " + str(attributes[k]) + " is not recognized"
		figuresXML = xmlObject.getchildren()
		figures = []
		for figureXML in figuresXML:
			figures.append(Figure.deSerializeXML(figureXML))
		return cls(index, figures)