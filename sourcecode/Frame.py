import xml.etree.ElementTree as ET
from sourcecode.Figure import *
from sourcecode.Rule import *

class Frame:

	def __init__(self, gindex, gfigures):
		self.figures = gfigures
		self.index = gindex

	@classmethod
	def deSerializeXML(cls, xmlObject):
		attributes = xmlObject.attrib
		index = None
		for k in attributes.keys():
			if k == 'index':
				index = attributes[k]
			else:
				print "attr: " + str(k) + " with value: " + str(attributes[k]) + " is not recognized"
		figuresXML = xmlObject.getchildren()
		figures = []
		for figureXML in figuresXML:
			figures.append(Figure.deSerializeXML(figureXML))
		return cls(index, figures)