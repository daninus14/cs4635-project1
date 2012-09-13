import xml.etree.ElementTree as ET
# debugging
import pdb

class Figure(object):
	""" docstring for Figure

		We consider something to be normal if largest portion is on top of half 
			way point of the longest vertical line. Otherwise it is reflected.

		We consider something to be normal if largest portion is on the right of 
			longest vertical line. Otherwise it is reflected.

		rotation_to_largest_vertical_line is in degrees (360 = 0 = 2*pi)

		Also include an inside of, an outside off (with possibilities for above, below, center / left, right, center)

		Consider the possibility of simply adding some list of arguments which basically weigh equally and are the same as 
		the others, then, the system would be very very flexible
	"""
	def __init__(self, gshape, gsize, grotation, gvloc, ghloc, gvref, ghref):
		super(Figure, self).__init__()
		self.shape = gshape
		self.size = gsize
		self.rotation_to_largest_vertical_line = grotation
		self.vertical_location = gvloc 
		self.horizontal_location = ghloc 
		self.vertical_reflection = gvref 
		self.horizontal_reflection = ghref 

	def __str__(self):
		figureStr = "Figure " + self.shape + " of size " + self.size
		return figureStr

	@classmethod
	def deSerializeXML(cls, xmlObject):
		""" TO DO: Add an index attribute!"""
		propertiesXML = xmlObject.getchildren()
		shape = "NA"
		size = "NA"
		rot = "NA"
		vloc = "NA"
		hloc = "NA"
		vref = "NA"
		href = "NA"
		for propertyXML in propertiesXML:
			if propertyXML.tag == "shape":
				shape = propertyXML.text
			elif propertyXML.tag == "size": # actually, make a dictionary with values from very small, small, medium, large, very larg
				size = propertyXML.text
			elif propertyXML.tag == "rotation_to_largest_vertical_line": # do this based on each 45 degree rotation. so there are 360/8
				rot = propertyXML.text
			elif propertyXML.tag == "vertical_location":
				vloc = propertyXML.text
			elif propertyXML.tag == "horizontal_location":
				hloc = propertyXML.text
			elif propertyXML.tag == "vertical_reflection":
				vref = propertyXML.text
			elif propertyXML.tag == "horizontal_reflection":
				href = propertyXML.text
			else:
				print "property: " + str(propertyXML.tag) + " with value: " + str(propertyXML.text) + " not recognized"

		return cls(shape, size, rot, vloc, hloc, vref, href)

	def get_rule_to_match(self, otherFigure):
		""" Include also a section for relationships for this rule and how they change, assign a weight of 2 for relationships,
			so that a circle going outside of another circle is valued at 2, and the two circles together is also valued at 2 
			(1 for each one of the circles moving) 

			Although, a circle moving outside another circle would really have value 3, 2 for the relationship change, and 1 for 
			the change in actual location
		"""
		vref = 0 
		shape = 0
		size = 0
		rotation = 0
		vloc = 0
		hloc = 0
		vref = 0
		href = 0
		if otherFigure.shape != self.shape:
			shape = 5
		if otherFigure.size != self.size:
			# Eventually have some sort of scale dependency where the value is not actually one, 
			# but rather self.size - otherFigure.size
			shape = 1 
		if otherFigure.rotation_to_largest_vertical_line != self.rotation_to_largest_vertical_line:
			rotation = 1
		if otherFigure.vertical_location != self.vertical_location:
			vloc = 1
		if otherFigure.horizontal_location != self.horizontal_location:
			hloc = 1
		if self.vertical_reflection != otherFigure.vertical_reflection:
			vref = 1
		if self.horizontal_reflection != otherFigure.horizontal_reflection:
			href = 1

		return Rule(self,otherFigure,shape,size,rotation,vloc,hloc,vref,href)

		# print "need to come up with a way to find rule to match!"

	def get_rule_create_delete(self):
		return Rule(self,None,0,0,0,0,0,0,0,10)


class Rule(object):
	"""docstring for Rule"""
	def __init__(self, ga_fig, gb_fig, gshape, gsize, grotation, gvloc, ghloc, gvref, ghref, gcreatedelete=0):
		super(Rule, self).__init__()
		self.shape = gshape
		self.size = gsize
		self.rotation_to_largest_vertical_line = grotation
		self.vertical_location = gvloc 
		self.horizontal_location = ghloc 
		self.vertical_reflection = gvref 
		self.horizontal_reflection = ghref
		self.a_fig = ga_fig
		self.b_fig = gb_fig
		self.createdelete = gcreatedelete

	def __str__(self):
		if self.createdelete != 0:
			return "Rule create-delete of " + self.a_fig.shape 
		ruleStr = "Rule from " + self.a_fig.shape + " to " + self.b_fig.shape
		return ruleStr

	def __repr__(self):
		if self.createdelete != 0:
			return "<Rule: " + self.a_fig.shape + " <-> create-delete >"
		ruleRepr = "<Rule: " + self.a_fig.shape + " -> " + self.b_fig.shape + ">"
		return ruleRepr

	def get_change_value(self):
		if self.createdelete != 0:
			return self.createdelete
		# pdb.set_trace()
		val = self.shape + self.size + self.rotation_to_largest_vertical_line + self.vertical_location
		val += self.horizontal_location + self.vertical_reflection + self.horizontal_reflection
		return val

	def get_difference_with_rule(self, otherRule):
		if self.createdelete != 0:
			return abs(self.createdelete - otherRule.get_change_value())
		total = 0
		total += abs(self.shape - otherRule.shape)
		total += abs(self.size - otherRule.size)
		total += abs(self.vertical_reflection - otherRule.vertical_reflection)
		total += abs(self.horizontal_reflection - otherRule.horizontal_reflection)
		total += abs(self.vertical_location - otherRule.vertical_location)
		total += abs(self.horizontal_location - otherRule.horizontal_location)
		total += abs(self.rotation_to_largest_vertical_line - otherRule.rotation_to_largest_vertical_line)
		return total
		