import xml.etree.ElementTree as ET
# debugging
import pdb 
from Rule import *
from log import *

class Figure(object):
	""" docstring for Figure

		We consider something to be normal if largest portion is on top of half 
			way point of the longest vertical line. Otherwise it is reflected.

		We consider something to be normal if largest portion is on the right of 
			longest vertical line. Otherwise it is reflected.
		vertical_reflection: False if largest portion on the right of longest vertical line, True otherwise
		horizontal_reflection: False if largest portion on the right of longest horizontal line, True otherwise

		rotation_to_largest_vertical_line is in degrees (360 = 0 = 2*pi)

	"""
	def __init__(self, given_data):
		super(Figure, self).__init__()
		self.data = given_data

	def __str__(self):
		if "shape" in self.data.keys() and "size" in self.data.keys():
			figureStr = "Figure " + self.data["shape"] + " of size " + self.data["size"]
		else:
			figureStr = "shape __str__ definition needed!"
			# should use some functional programming here! look it up in the documentation!
			# idea is to take each field and give its name (key) and value
		return figureStr

	@classmethod
	def deSerializeXML(cls, xmlObject):
		""" TO DO: Add an index attribute!"""
		propertiesXML = xmlObject.getchildren()
		data = {}
		for propertyXML in propertiesXML:
			if propertyXML.tag not in data.keys():
				data[propertyXML.tag] = propertyXML.text
			else:
				print "property: " + str(propertyXML.tag) + " with value: " + str(propertyXML.text) + " already added!"

		return cls(data)

	def get_rule_to_match(self, other_figure):
		""" Include also a section for relationships for this rule and how they change, assign a weight of 2 for relationships,
			so that a circle going outside of another circle is valued at 2, and the two circles together is also valued at 2 
			(1 for each one of the circles moving) 

			Although, a circle moving outside another circle would really have value 3, 2 for the relationship change, and 1 for 
			the change in actual location
		"""
		if other_figure == None: 
			print "Figure.py:get_rule_to_match:53 This should never be called! "
			return self.get_rule_create_delete()

		rule_data = self.get_rule_difference_value(other_figure)
		# rule_data = self.get_rule_difference_value(other_figure, rule_data)

		return Rule(self,other_figure,rule_data)

	def get_rule_difference_value(self, other_figure):

		if other_figure == None: 
			print "ERROR FIGURE.PY LINE 75"
			return 10
		rule_data = {}
		if set(self.data.keys()) == set(other_figure.data.keys()):
			for skey in self.data.keys():
				rule_data[skey] = 0 if self.data[skey] == other_figure.data[skey] else 1
		else:
			print "\n\n\tnot currently handling figures with different attributes"
			print "\n\n"
		return rule_data


	def get_rule_create_delete(self):
		rule_data = {}
		for property_key in self.data.keys():
			rule_data[property_key] = 0
		return Rule(self,None,rule_data,10)

	def get_difference_to_figure(self, other_figure):
		if other_figure == None: return 10
		difference = 0
		if set(self.data.keys()) == set(other_figure.data.keys()):
			for skey in self.data.keys():
				difference += 0 if self.data[skey] == other_figure.data[skey] else 1
		else:
			print "\n\n\tnot currently handling figures with different attributes"
			print "\n\n"
		return difference

