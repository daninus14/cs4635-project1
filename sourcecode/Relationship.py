import xml.etree.ElementTree as ET


class Relationship(object):
	""" docstring for Relationship
		for each element e_{i} in a frame F, we have that e_{i} will have fields of relationships with every other
		elemtn in Elements(F), so that relationships_{e_{i}} = {e_{j} | e_{j} \in Elements(F) and e_{j} \neq e_{i}}

	"""
	def __init__(self, gfigure1, gfigure2, glocation1vs2):
		super(Relationship, self).__init__()
		self.figure1 = gfigure1
		self.figure2 = gfigure2
		self.location1vs2 = glocation1vs2

	@classmethod
	def deSerializeXML(cls, xmlObject):

		return cls(figure1, figure2, location1vs2)
		