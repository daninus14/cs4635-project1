import xml.etree.ElementTree as ET
# debugging
import pdb


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
			return "<Rule: " + self.a_fig.shape + " - create-delete >"
		changes = ""
		for attribute in vars(self).keys():
			if vars(self)[attribute] != 0 and attribute != 'a_fig' and attribute != "b_fig":
				changes += " " + attribute + ","
		changes = changes if changes != "" else " No Change"
		ruleRepr = "<Rule: " + self.a_fig.shape + " - " + self.b_fig.shape + ":" + changes + ">"
		return ruleRepr

	def get_change_value(self):
		if self.createdelete != 0:
			return self.createdelete
		# pdb.set_trace()
		val = self.shape + self.size + self.rotation_to_largest_vertical_line + self.vertical_location
		val += self.horizontal_location + self.vertical_reflection + self.horizontal_reflection
		return val

	def get_difference_with_rule(self, otherRule):
		""" 
			Also add case for having rules be applied to similar objects.

			So for any two rules a,b with objects a_{0}, a_{1}, etc, we have that
			the rules difference is also (adds) the value difference between a_{0} and b_{0}
			This fact reinforces the importance of proper ordering of figure in frame A to figure in frame B
		"""
		return self.get_difference_with_rule_modified(otherRule)

		if self.createdelete != 0:
			return abs(self.createdelete - otherRule.get_change_value())
		total = 0
		total += abs(self.shape - otherRule.shape)
		# print "self.size: " + str(self.size)
		# print "otherRule.size: " + str(otherRule.size)
		total += abs(self.size - otherRule.size)
		total += abs(self.vertical_reflection - otherRule.vertical_reflection)
		total += abs(self.horizontal_reflection - otherRule.horizontal_reflection)
		# print "total: " + str(total)
		total += abs(self.vertical_location - otherRule.vertical_location)
		total += abs(self.horizontal_location - otherRule.horizontal_location)
		total += abs(self.rotation_to_largest_vertical_line - otherRule.rotation_to_largest_vertical_line)
		# print "total: " + str(total)
		# adding a weight of 2 to accentuate differences between how the rule works is more important than 
		# the differences between the figures the rules are applied to
		total *=2
		# Now, the difference between the objects the rules are applied to
		# pdb.set_trace()
		# if not otherRule or not otherRule.b_fig:
		# 	pdb.set_trace()
		# print "total: " + str(total)
		# total += self.a_fig.get_rule_to_match(otherRule.a_fig).get_change_value()
		# print "total: " + str(total)
		# print "self.a_fig.get_rule_to_match(otherRule.a_fig).get_change_value()): " + str(self.a_fig.get_rule_to_match(otherRule.a_fig).get_change_value())
		if not otherRule.b_fig:
			total += abs(otherRule.createdelete + self.get_change_value() - self.a_fig.get_rule_to_match(otherRule.a_fig).get_change_value()) 
			# Note that here the plus is on purpose since the figures must be very different!
		else: 
			# print "abs(self.b_fig.get_rule_to_match(otherRule.b_fig).get_change_value() - self.a_fig.get_rule_to_match(otherRule.a_fig).get_change_value()): " + str(abs(self.b_fig.get_rule_to_match(otherRule.b_fig).get_change_value() - self.a_fig.get_rule_to_match(otherRule.a_fig).get_change_value()))
			total += abs(self.b_fig.get_rule_to_match(otherRule.b_fig).get_change_value() - self.a_fig.get_rule_to_match(otherRule.a_fig).get_change_value())
		return total
		

	def get_difference_with_rule_modified(self, other_rule):
		""" 
			Add docstring here!
		"""
		total = 0
		# This compares the figures in self to the figures in other_rule
		for [curr_self_fig, curr_other_fig] in [[self.a_fig, other_rule.a_fig], [self.b_fig, other_rule.b_fig]]:
				if curr_self_fig != None and curr_other_fig != None:
					total += curr_self_fig.get_difference_to_figure(curr_other_fig)
				elif not (curr_self_fig == None and curr_other_fig == None):
					total += 10

		# this compares the transformation of the self rule to the other_rule
		# difference = 0
		if set(vars(self).keys()) == set(vars(other_rule).keys()):
			for skey in vars(self).keys():
				total += 0 if vars(self)[skey] == vars(other_rule)[skey] else 2
		else:
			print "\n\n\tnot currently handling rules with different attributes"
			print "\n\n"
		return total