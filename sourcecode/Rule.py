import xml.etree.ElementTree as ET
# debugging
import pdb


class Rule(object):
	"""docstring for Rule"""
	def __init__(self, ga_fig, gb_fig, given_data, gcreatedelete=0):
		super(Rule, self).__init__()
		self.data = given_data
		self.a_fig = ga_fig
		self.b_fig = gb_fig
		self.createdelete = gcreatedelete

	def __str__(self):
		if self.createdelete != 0: # "createdelete" in self.data.keys() and self.data["createdelete"] != 0:
			return "Rule create-delete of " + self.a_fig.shape 
		elif "shape" in self.a_fig.data.keys() and "shape" in self.b_fig.data.keys():
			ruleStr = "Rule from " + self.a_fig.data["shape"] + " to " + self.b_fig.data["shape"]
		else:
			# Do some functional programming magic here to consider every possible field...
			ruleStr = "rule too large for a single line!"
		return ruleStr

	# def __repr__(self):
	# 	if self.createdelete != 0:
	# 		return "<Rule: " + self.a_fig.shape + " - create-delete >"
	# 	changes = ""
	# 	for attribute in vars(self).keys():
	# 		if vars(self)[attribute] != 0 and attribute != 'a_fig' and attribute != "b_fig":
	# 			changes += " " + attribute + ","
	# 	changes = changes if changes != "" else " No Change"
	# 	ruleRepr = "<Rule: " + self.a_fig.shape + " - " + self.b_fig.shape + ":" + changes + ">"
	# 	return ruleRepr

	def get_change_value(self):
		if self.createdelete != 0:
			return self.createdelete
		# pdb.set_trace()
		total_value = 0
		for curr_key in self.data.keys(): total_value += self.data[curr_key] 
		return total_value

	def get_difference_with_rule(self, other_rule):
		""" 
			Also add case for having rules be applied to similar objects.

			So for any two rules a,b with objects a_{0}, a_{1}, etc, we have that
			the rules difference is also (adds) the value difference between a_{0} and b_{0}
			This fact reinforces the importance of proper ordering of figure in frame A to figure in frame B
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
		if set(self.data.keys()) == set(other_rule.data.keys()):
			for skey in self.data.keys():
				total += 0 if self.data[skey] == other_rule.data[skey] else 2
		# else:
			# print "\n\n\tnot currently handling rules with different attributes"
			# print "self.data.keys(): " + str(self.data.keys())
			# print "other_rule.data.keys(): " + str(other_rule.data.keys())
			# print "\n\n"
		return total